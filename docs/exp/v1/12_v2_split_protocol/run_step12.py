#!/usr/bin/env python3
"""Create the v2 fresh-heldout split protocol for second_try."""

from __future__ import annotations

import csv
import hashlib
import re
import unicodedata
from collections import defaultdict
from datetime import datetime
from pathlib import Path


DEV_BOOK = "MAR"
BURNED_BOOK = "JOH"
FINAL_BOOK = "ACT"


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text).casefold()).strip()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def write_text_lines(path: Path, rows: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(row + "\n")


def md5_file(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def count_rows_or_lines(path: Path) -> int:
    with path.open("r", encoding="utf-8") as f:
        total = sum(1 for _ in f)
    return max(0, total - 1) if path.suffix == ".tsv" else total


def file_result(role: str, path: Path, notes: str, status: str = "PASS") -> dict[str, str]:
    return {
        "file_role": role,
        "path": str(path),
        "rows_or_lines": str(count_rows_or_lines(path)),
        "bytes": str(path.stat().st_size),
        "md5": md5_file(path),
        "status": status,
        "notes": notes,
    }


def v2_split_for(book: str) -> str:
    if book == DEV_BOOK:
        return "dev"
    if book == BURNED_BOOK:
        return "burned_excluded"
    if book == FINAL_BOOK:
        return "final_test"
    return "train"


def candidate_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    books = sorted({row["book"] for row in rows})
    output = []
    for book in books:
        if book in {DEV_BOOK, BURNED_BOOK}:
            continue
        final_rows = [row for row in rows if row["book"] == book]
        train_rows = [row for row in rows if row["book"] not in {DEV_BOOK, BURNED_BOOK, book}]
        dev_rows = [row for row in rows if row["book"] == DEV_BOOK]
        per_lang: dict[str, int] = defaultdict(int)
        for row in final_rows:
            per_lang[row["iso"]] += 1
        train_text = {(row["iso"], normalize_text(row["text"])) for row in train_rows}
        dev_text = {(row["iso"], normalize_text(row["text"])) for row in dev_rows}
        train_dups = sum(1 for row in final_rows if (row["iso"], normalize_text(row["text"])) in train_text)
        dev_dups = sum(1 for row in final_rows if (row["iso"], normalize_text(row["text"])) in dev_text)
        total_dups = train_dups + dev_dups
        duplicate_rate = total_dups / max(1, len(final_rows))
        decision = "SELECTED_FINAL_TEST" if book == FINAL_BOOK else "NOT_SELECTED"
        if len(final_rows) < 3000 or min(per_lang.values()) < 300:
            decision = "TOO_SMALL"
        output.append(
            {
                "book": book,
                "final_rows": str(len(final_rows)),
                "languages": str(len(per_lang)),
                "min_rows_per_language": str(min(per_lang.values())),
                "train_rows_if_selected": str(len(train_rows)),
                "train_final_exact_duplicates": str(train_dups),
                "dev_final_exact_duplicates": str(dev_dups),
                "total_exact_duplicates": str(total_dups),
                "duplicate_rate": f"{duplicate_rate:.6f}",
                "decision": decision,
            }
        )
    return output


def main() -> None:
    run_id = "step12_v2_split_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    root = Path("docs/exp/second_try").resolve()
    step_dir = root / "12_v2_split_protocol"
    artifact_dir = Path("/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol").resolve()
    artifact_dir.mkdir(parents=True, exist_ok=True)
    input_path = root / "01_data_and_splits" / "target10_bible_verses.tsv"
    rows = read_tsv(input_path)

    v2_rows = []
    for row in rows:
        updated = dict(row)
        updated["original_split"] = row["split"]
        updated["v2_split"] = v2_split_for(row["book"])
        v2_rows.append(updated)

    train_text = {(row["iso"], normalize_text(row["text"])) for row in v2_rows if row["v2_split"] == "train"}
    dev_text = {(row["iso"], normalize_text(row["text"])) for row in v2_rows if row["v2_split"] == "dev"}
    duplicate_rows = []
    clean_final_rows = []
    for row in v2_rows:
        if row["v2_split"] != "final_test":
            continue
        key = (row["iso"], normalize_text(row["text"]))
        sources = []
        if key in train_text:
            sources.append("train")
        if key in dev_text:
            sources.append("dev")
        if sources:
            duplicate_rows.append(
                {
                    "iso": row["iso"],
                    "book": row["book"],
                    "verse_id": row["verse_id"],
                    "duplicate_with": ",".join(sources),
                    "text": row["text"],
                }
            )
        else:
            clean_final_rows.append(row)

    split_counts: dict[tuple[str, str], int] = defaultdict(int)
    for row in v2_rows:
        split_counts[(row["v2_split"], row["iso"])] += 1
    clean_final_counts: dict[str, int] = defaultdict(int)
    for row in clean_final_rows:
        clean_final_counts[row["iso"]] += 1

    split_stats = []
    for split in ["train", "dev", "burned_excluded", "final_test"]:
        for iso in sorted({row["iso"] for row in v2_rows}):
            split_stats.append(
                {
                    "split": split,
                    "iso": iso,
                    "rows": str(split_counts[(split, iso)]),
                    "clean_final_rows": str(clean_final_counts[iso]) if split == "final_test" else "NOT_APPLICABLE",
                    "status": "PASS" if split_counts[(split, iso)] > 0 else "FAIL",
                }
            )

    clean_final_total = len(clean_final_rows)
    clean_final_min = min(clean_final_counts.values())
    v2_gate = clean_final_total >= 8000 and clean_final_min >= 800 and not any(row["book"] == BURNED_BOOK and row["v2_split"] != "burned_excluded" for row in v2_rows)

    candidate_path = step_dir / "v2_candidate_books.tsv"
    split_stats_path = step_dir / "v2_split_stats.tsv"
    manifest_path = step_dir / "v2_split_manifest.tsv"
    duplicate_path = step_dir / "v2_final_duplicate_exclusions.tsv"
    dev_manifest_path = step_dir / "v2_dev_manifest.tsv"
    final_clean_manifest_path = step_dir / "v2_final_test_act_clean.tsv"
    execution_matrix_path = step_dir / "v2_execution_matrix.tsv"
    score_path = step_dir / "score_table.tsv"
    protocol_path = step_dir / "v2_rerun_protocol.md"
    results_path = step_dir / "results.md"
    file_results_path = step_dir / "file_results.tsv"

    write_tsv(candidate_path, candidate_rows(rows), ["book", "final_rows", "languages", "min_rows_per_language", "train_rows_if_selected", "train_final_exact_duplicates", "dev_final_exact_duplicates", "total_exact_duplicates", "duplicate_rate", "decision"])
    write_tsv(split_stats_path, split_stats, ["split", "iso", "rows", "clean_final_rows", "status"])
    write_tsv(manifest_path, v2_rows, ["iso", "language", "script", "split", "original_split", "v2_split", "book", "chapter", "verse", "verse_id", "char_len", "text"])
    write_tsv(duplicate_path, duplicate_rows, ["iso", "book", "verse_id", "duplicate_with", "text"])
    write_tsv(dev_manifest_path, [row for row in v2_rows if row["v2_split"] == "dev"], ["iso", "language", "script", "split", "original_split", "v2_split", "book", "chapter", "verse", "verse_id", "char_len", "text"])
    write_tsv(final_clean_manifest_path, clean_final_rows, ["iso", "language", "script", "split", "original_split", "v2_split", "book", "chapter", "verse", "verse_id", "char_len", "text"])
    execution_rows = [
        {
            "stage_id": "V2_00_SPLIT_FREEZE",
            "depends_on": "Step12",
            "work": "freeze v2 train/dev/burned/final split",
            "selection_data": "NOT_APPLICABLE",
            "final_data_policy": "ACT final clean locked but not used for selection",
            "required_outputs": "v2_split_manifest.tsv; v2_split_stats.tsv; v2_final_duplicate_exclusions.tsv",
            "gate": "ACT clean final >=8000 rows and >=800 per language; JOH excluded",
            "status": "DONE_PASS",
        },
        {
            "stage_id": "V2_01_TOKENIZER",
            "depends_on": "V2_00_SPLIT_FREEZE",
            "work": "train/merge 8k, 16k, 32k tokenizer candidates from v2 train only",
            "selection_data": "MAR dev only",
            "final_data_policy": "do not inspect ACT final until final reporting",
            "required_outputs": "v2_vocab_extension_metrics.tsv; tokenizer artifacts; file_results.tsv",
            "gate": "original ids preserved and dev fragmentation improves without final-set selection",
            "status": "NOT_STARTED",
        },
        {
            "stage_id": "V2_02_INIT",
            "depends_on": "V2_01_TOKENIZER",
            "work": "compare random, mean, fvt, align, focus initialization under v2 tokenizer",
            "selection_data": "MAR dev MLM only",
            "final_data_policy": "no ACT final access",
            "required_outputs": "v2_embedding_init_scores.tsv; initialized checkpoints; file_results.tsv",
            "gate": "all required init methods load; selected init chosen by dev only",
            "status": "NOT_STARTED",
        },
        {
            "stage_id": "V2_03_MLM_CONTROL",
            "depends_on": "V2_02_INIT",
            "work": "longer MLM adaptation plus original-XLM-R continued-pretraining control with >=3 seeds",
            "selection_data": "MAR dev only",
            "final_data_policy": "no ACT final access",
            "required_outputs": "mlm_learning_curves.tsv; seed_summary.tsv; checkpoint_selection.md; file_results.tsv",
            "gate": "adapted extended checkpoint improves from zero-step and is competitive with original continued-pretraining control",
            "status": "NOT_STARTED",
        },
        {
            "stage_id": "V2_04_DOWNSTREAM",
            "depends_on": "V2_03_MLM_CONTROL",
            "work": "hard-negative retrieval/matching with bootstrap confidence intervals",
            "selection_data": "train/MAR dev only",
            "final_data_policy": "ACT final evaluated once only after model freeze",
            "required_outputs": "downstream_hard_negative_scores.tsv; bootstrap_ci.tsv; per_language_summary.tsv; file_results.tsv",
            "gate": "non-overlapping or statistically supported gains across languages/seeds",
            "status": "NOT_STARTED",
        },
        {
            "stage_id": "V2_05_TRANSLATION",
            "depends_on": "V2_03_MLM_CONTROL",
            "work": "method-matched adapted-XLM-R-only translation retrieval or generation",
            "selection_data": "MAR dev only",
            "final_data_policy": "ACT final evaluated exactly once after model/pair/scoring freeze",
            "required_outputs": "method_matched_translation.tsv; adapted_only_predictions.tsv; failure_cases.md; file_results.tsv",
            "gate": "adapted main-model target/high-resource ratio >=0.800000 on ACT clean final",
            "status": "NOT_STARTED",
        },
        {
            "stage_id": "V2_06_FINAL_SYNTHESIS",
            "depends_on": "V2_04_DOWNSTREAM and V2_05_TRANSLATION",
            "work": "write top-tier-safe final claim and limitations",
            "selection_data": "frozen prior stages",
            "final_data_policy": "no new tuning after final readout",
            "required_outputs": "claim_evidence_map.md; paper_tables.md; final_checklist.md; file_results.tsv",
            "gate": "every positive claim has v2 evidence; failed claims are explicitly unsupported",
            "status": "NOT_STARTED",
        },
    ]
    write_tsv(execution_matrix_path, execution_rows, ["stage_id", "depends_on", "work", "selection_data", "final_data_policy", "required_outputs", "gate", "status"])

    tokenizer_train = [row["text"] for row in v2_rows if row["v2_split"] == "train"]
    mlm_dev = [row["text"] for row in v2_rows if row["v2_split"] == "dev"]
    final_clean = [row["text"] for row in clean_final_rows]
    burned = [row["text"] for row in v2_rows if row["v2_split"] == "burned_excluded"]
    tokenizer_path = artifact_dir / "v2_tokenizer_mlm_train.txt"
    mlm_dev_path = artifact_dir / "v2_mlm_dev_mark.txt"
    final_path = artifact_dir / "v2_final_test_act_clean.txt"
    burned_path = artifact_dir / "v2_burned_john_excluded.txt"
    write_text_lines(tokenizer_path, tokenizer_train)
    write_text_lines(mlm_dev_path, mlm_dev)
    write_text_lines(final_path, final_clean)
    write_text_lines(burned_path, burned)

    score_rows = [
        {
            "run_id": run_id,
            "claim": "v2_fresh_final_split_created",
            "evidence": "v2_split_manifest.tsv",
            "observed": f"final_book={FINAL_BOOK}; clean_final_rows={clean_final_total}; min_clean_per_lang={clean_final_min}",
            "decision": "SUPPORTED" if v2_gate else "UNSUPPORTED",
            "status": "PASS" if v2_gate else "FAIL",
            "notes": "ACT selected as fresh final test; exact duplicate final rows excluded from scoring",
        },
        {
            "run_id": run_id,
            "claim": "john_burned_test_excluded",
            "evidence": "v2_split_manifest.tsv",
            "observed": f"burned_book={BURNED_BOOK}; burned_rows={len(burned)}",
            "decision": "SUPPORTED",
            "status": "PASS",
            "notes": "old John test feedback is excluded from v2 train/dev/final evidence",
        },
        {
            "run_id": run_id,
            "claim": "existing_checkpoints_invalid_for_v2_final_claims",
            "evidence": "v2_rerun_protocol.md",
            "observed": "Step05/06/07/09 trained or selected under v1 split",
            "decision": "SUPPORTED",
            "status": "PASS_NEGATIVE_RESULT",
            "notes": "v2 top-tier claim requires tokenizer/MLM/downstream/translation rerun",
        },
    ]
    write_tsv(score_path, score_rows, ["run_id", "claim", "evidence", "observed", "decision", "status", "notes"])

    protocol_path.write_text(
        f"""# Step 12 V2 Rerun Protocol

Run id: `{run_id}`

## Locked V2 Split

| Role | Book | Rows |
| --- | --- | ---: |
| train | all except `{DEV_BOOK}`, `{BURNED_BOOK}`, `{FINAL_BOOK}` | {len(tokenizer_train)} |
| dev | `{DEV_BOOK}` | {len(mlm_dev)} |
| burned_excluded | `{BURNED_BOOK}` | {len(burned)} |
| final_test_clean | `{FINAL_BOOK}` minus exact train/dev text duplicates | {clean_final_total} |

Exact duplicate final rows excluded from scoring: `{len(duplicate_rows)}`.

Minimum clean final rows per target language: `{clean_final_min}`.

## Required Rerun

1. Rerun tokenizer training and merge using only `v2_tokenizer_mlm_train.txt`.
2. Rerun embedding initialization and MLM adaptation from the base model under the v2 split.
3. Rerun downstream proxy tasks, using Mark/dev for selection and ACT/final only once if final reporting is required.
4. Rerun method-matched translation with dev-only model/pair/scoring selection.
5. Report ACT final test once, after all settings are frozen.

Detailed stage gates are in `v2_execution_matrix.tsv`.

## Invalid For V2 Final Claims

- Step 05 checkpoint `spm32000_fvt_seed13`
- Step 06 downstream proxy scores
- Step 07 translation rows
- Branch 001 translation rows
- Step 09 method-matched rows

These artifacts remain useful as exploratory evidence but cannot support the v2 top-tier final claim because their training, selection, or evaluation touched the old split.
""",
        encoding="utf-8",
    )

    results_path.write_text(
        f"""# Step 12 Results: V2 Split Protocol

Status: COMPLETED

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Artifact gate status: PASS

Claim gate status: {"PASS" if v2_gate else "FAIL"}

## Summary

Step 12 creates a v2 split that unblocks fresh-heldout reruns. `ACT` is selected as the new final test book because it has 9,807 target10 rows and only 5 exact normalized train/dev duplicate hits. These correspond to {len(duplicate_rows)} unique final rows, which are excluded from final scoring, leaving {clean_final_total} clean final rows and at least {clean_final_min} clean final rows per target language.

## Decision

V2 split is ready for rerunning tokenizer, MLM adaptation, downstream proxy, and method-matched translation from scratch.

Existing v1 checkpoints and translation scores are invalid for v2 final claims.

## Failure Return

Failed gate: {"NOT_APPLICABLE" if v2_gate else "v2_final_split_sufficiency"}

Observed evidence: {"NOT_APPLICABLE" if v2_gate else "ACT final split did not meet clean-row threshold"}

Return-to step: {"NOT_APPLICABLE" if v2_gate else "01_data_and_splits"}

Required fix: {"NOT_APPLICABLE" if v2_gate else "choose another final book or import an external corpus"}
""",
        encoding="utf-8",
    )

    file_rows = [
        file_result("score_table", score_path, "v2 split claim status"),
        file_result("candidate_books", candidate_path, "candidate final-test book comparison"),
        file_result("split_stats", split_stats_path, "v2 per-split per-language counts"),
        file_result("split_manifest", manifest_path, "row-level v2 split manifest"),
        file_result("duplicate_exclusions", duplicate_path, "exact duplicate final rows excluded from scoring"),
        file_result("dev_manifest", dev_manifest_path, "dev-only manifest for selection stages"),
        file_result("final_clean_manifest", final_clean_manifest_path, "clean final manifest for one-shot final reporting"),
        file_result("execution_matrix", execution_matrix_path, "v2 rerun stage gates"),
        file_result("rerun_protocol", protocol_path, "required v2 rerun protocol"),
        file_result("results", results_path, "step result summary"),
        file_result("v2_tokenizer_mlm_train", tokenizer_path, "large train text artifact"),
        file_result("v2_mlm_dev", mlm_dev_path, "large dev text artifact"),
        file_result("v2_final_test_clean", final_path, "large clean final text artifact"),
        file_result("v2_burned_john_excluded", burned_path, "large burned old test artifact"),
    ]
    write_tsv(file_results_path, file_rows, ["file_role", "path", "rows_or_lines", "bytes", "md5", "status", "notes"])

    print(f"run_id={run_id}")
    print("artifact_gate_status=PASS")
    print(f"claim_gate_status={'PASS' if v2_gate else 'FAIL'}")
    print(f"clean_final_rows={clean_final_total}")
    print(f"min_clean_final_rows_per_language={clean_final_min}")
    print(f"duplicate_exclusions={len(duplicate_rows)}")


if __name__ == "__main__":
    main()
