#!/usr/bin/env python3
"""Leakage and selection audit for second_try.

This step reads the current artifacts and writes a conservative audit. It is
intentionally claim-oriented: a completed audit can still invalidate a claim.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import time
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text).casefold()
    return re.sub(r"\s+", " ", text).strip()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


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


def find_line(path: Path, pattern: str) -> str:
    compiled = re.compile(pattern)
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            if compiled.search(line):
                return f"{path}:{lineno}"
    return f"{path}:NOT_FOUND"


def split_integrity_checks(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], dict[str, int]]:
    audit_rows: list[dict[str, str]] = []
    key_counts = Counter((row["iso"], row["verse_id"]) for row in rows)
    duplicate_keys = sum(1 for count in key_counts.values() if count > 1)
    splits_by_key: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in rows:
        splits_by_key[(row["iso"], row["verse_id"])].add(row["split"])
    split_overlap = sum(1 for splits in splits_by_key.values() if len(splits) > 1)

    dev_bad = sum(1 for row in rows if row["split"] == "dev" and row["book"] != "MAR")
    test_bad = sum(1 for row in rows if row["split"] == "test" and row["book"] != "JOH")
    train_bad = sum(1 for row in rows if row["split"] == "train" and row["book"] in {"MAR", "JOH"})

    def add(check_id: str, evidence: str, observed: int, expected: str, status: str, impact: str) -> None:
        audit_rows.append(
            {
                "check_id": check_id,
                "category": "split_integrity",
                "evidence": evidence,
                "observed": str(observed),
                "expected": expected,
                "status": status,
                "impact": impact,
            }
        )

    add("SPLIT_DUPLICATE_ISO_VERSE", "target10_bible_verses.tsv", duplicate_keys, "0", "PASS" if duplicate_keys == 0 else "FAIL", "duplicate source rows can leak examples")
    add("SPLIT_VERSE_ASSIGNED_TO_MULTIPLE_SPLITS", "target10_bible_verses.tsv", split_overlap, "0", "PASS" if split_overlap == 0 else "FAIL", "same verse in train/dev/test invalidates held-out split")
    add("SPLIT_DEV_BOOK_ONLY_MARK", "target10_bible_verses.tsv", dev_bad, "0", "PASS" if dev_bad == 0 else "FAIL", "dev must remain Mark only")
    add("SPLIT_TEST_BOOK_ONLY_JOHN", "target10_bible_verses.tsv", test_bad, "0", "PASS" if test_bad == 0 else "FAIL", "test must remain John only")
    add("SPLIT_TRAIN_EXCLUDES_MARK_JOHN", "target10_bible_verses.tsv", train_bad, "0", "PASS" if train_bad == 0 else "FAIL", "train must exclude dev/test books")
    return audit_rows, {
        "duplicate_keys": duplicate_keys,
        "split_overlap": split_overlap,
        "dev_bad": dev_bad,
        "test_bad": test_bad,
        "train_bad": train_bad,
    }


def text_duplicate_checks(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], dict[str, int]]:
    audit_rows: list[dict[str, str]] = []
    duplicate_pairs = {"train_dev": 0, "train_test": 0, "dev_test": 0}
    examples: dict[str, str] = {}
    by_iso_text: dict[tuple[str, str], set[str]] = defaultdict(set)
    by_iso_text_rows: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = (row["iso"], normalize_text(row["text"]))
        by_iso_text[key].add(row["split"])
        by_iso_text_rows[key].append(row)

    for key, splits in by_iso_text.items():
        for pair_name, pair in {
            "train_dev": {"train", "dev"},
            "train_test": {"train", "test"},
            "dev_test": {"dev", "test"},
        }.items():
            if pair.issubset(splits):
                duplicate_pairs[pair_name] += 1
                if pair_name not in examples:
                    row_bits = [f"{r['iso']}:{r['split']}:{r['verse_id']}" for r in by_iso_text_rows[key][:4]]
                    examples[pair_name] = ",".join(row_bits)

    for pair_name, observed in duplicate_pairs.items():
        audit_rows.append(
            {
                "check_id": f"TEXT_DUPLICATE_{pair_name.upper()}",
                "category": "text_duplicate",
                "evidence": examples.get(pair_name, "NO_EXAMPLE"),
                "observed": str(observed),
                "expected": "0 preferred",
                "status": "PASS" if observed == 0 else "WARN_DISCLOSED",
                "impact": "exact normalized text duplicates across splits can inflate text memorization but are not verse-id oracle leakage",
            }
        )
    return audit_rows, duplicate_pairs


def selection_checks(root: Path) -> tuple[list[dict[str, str]], list[dict[str, str]], list[str]]:
    audit_rows: list[dict[str, str]] = []
    invalidated: list[dict[str, str]] = []
    trace_lines: list[str] = []
    step07 = root / "07_translation_benchmark"
    branch = root / "branches" / "branch_001_translation_retrieval_gap"
    step09 = root / "09_top_tier_validation"

    run_step07 = step07 / "run_step07.py"
    step07_loop_line = find_line(run_step07, r"for src_iso in target_isos")
    step07_best_line = find_line(run_step07, r"if best_metrics is None or metrics\[\"chrf\"\] > best_metrics\[\"chrf\"\]")
    step07_test_line = find_line(run_step07, r"split\": \"John/test\"")
    step07_selection_evidence = f"{step07_loop_line}; {step07_best_line}; {step07_test_line}"
    audit_rows.append(
        {
            "check_id": "SEL_STEP07_TARGET_PAIR_SELECTED_ON_TEST",
            "category": "selection",
            "evidence": step07_selection_evidence,
            "observed": "target pair chosen by maximum chrF over John/test pairs",
            "expected": "dev-only pair selection before test",
            "status": "FAIL_INVALIDATES_TRANSLATION_SELECTION",
            "impact": "Step 07 original target pair cannot be used as an unbiased test result",
        }
    )
    invalidated.append(
        {
            "run_id": "step07_translation_20260610_231227",
            "artifact": str(step07 / "score_table.tsv"),
            "invalidated_claim": "unbiased target pair selection for original adapted translation row",
            "reason": "target pair was selected by John/test chrF across target language pairs",
            "status_after_audit": "EXPLORATORY_ONLY",
            "return_to": "07_translation_benchmark",
        }
    )

    branch_scores = read_tsv(branch / "score_table.tsv")
    test_rows = [row for row in branch_scores if row.get("split") == "test"]
    prior_test_rows = [row for row in test_rows if row.get("run_id") != "branch001_sentence_embedding_20260610_234706"]
    audit_rows.append(
        {
            "check_id": "SEL_BRANCH_TEST_FEEDBACK_BEFORE_FINAL",
            "category": "selection",
            "evidence": str(branch / "score_table.tsv"),
            "observed": str(len(prior_test_rows)),
            "expected": "0 prior test attempts before final model-family decision",
            "status": "FAIL_INVALIDATES_BRANCH_SUCCESS",
            "impact": "branch family/model search saw held-out John test feedback before final LaBSE success",
        }
    )
    invalidated.append(
        {
            "run_id": "branch001_sentence_embedding_20260610_234706",
            "artifact": str(branch / "score_table.tsv"),
            "invalidated_claim": "final Branch 001 success as single held-out test decision",
            "reason": f"{len(prior_test_rows)} prior branch test rows were measured before the final LaBSE row",
            "status_after_audit": "EXPLORATORY_SUPERSEDED",
            "return_to": "07_translation_benchmark",
        }
    )

    step07_scores = read_tsv(step07 / "score_table.tsv")
    branch_row = next((row for row in step07_scores if row.get("run_id") == "branch001_sentence_embedding_20260610_234706"), None)
    mixed_method = branch_row is not None and "model=sentence-transformers/LaBSE" in branch_row.get("notes", "") and "Spanish.xml->English.xml John" in branch_row.get("high_resource_dataset", "")
    audit_rows.append(
        {
            "check_id": "SEL_BRANCH_MIXED_METHOD_REFERENCE",
            "category": "selection",
            "evidence": str(step07 / "score_table.tsv"),
            "observed": "LaBSE target row compared to XLM-R high-resource reference" if mixed_method else "not_detected",
            "expected": "same method for high-resource and target ratio",
            "status": "FAIL_INVALIDATES_BRANCH_SUCCESS" if mixed_method else "PASS",
            "impact": "mixed-method ratio cannot support top-tier translation threshold",
        }
    )
    if mixed_method:
        invalidated.append(
            {
                "run_id": "branch001_sentence_embedding_20260610_234706",
                "artifact": str(step07 / "score_table.tsv"),
                "invalidated_claim": "translation reaches 80 percent of high-resource reference",
                "reason": "target branch used LaBSE+CSLS while high-resource reference used XLM-R retrieval",
                "status_after_audit": "EXPLORATORY_SUPERSEDED_BY_STEP09",
                "return_to": "09_top_tier_validation / 07_translation_benchmark",
            }
        )

    step09_scores = read_tsv(step09 / "score_table.tsv")
    step09_methods = {row["method_id"]: row for row in step09_scores}
    step09_fail = step09_methods.get("selected_adapted_xlmr_cosine", {}).get("status") == "FAIL"
    audit_rows.append(
        {
            "check_id": "SEL_STEP09_METHOD_MATCHED_AUDIT",
            "category": "selection",
            "evidence": str(step09 / "score_table.tsv"),
            "observed": "method-matched rows present; selected adapted ratio=" + step09_methods.get("selected_adapted_xlmr_cosine", {}).get("method_matched_ratio", "MISSING"),
            "expected": "same method for high-resource and target; dev-selected target pair",
            "status": "PASS_NEGATIVE_RESULT" if step09_fail else "PASS",
            "impact": "Step 09 is the current authority for top-tier translation claims",
        }
    )
    if step09_fail:
        invalidated.append(
            {
                "run_id": step09_methods.get("selected_adapted_xlmr_cosine", {}).get("run_id", "step09"),
                "artifact": str(step09 / "score_table.tsv"),
                "invalidated_claim": "selected adapted XLM-R reaches 80 percent translation reference",
                "reason": "method-matched ratio is below threshold",
                "status_after_audit": "UNSUPPORTED_FOR_MAIN_MODEL",
                "return_to": "05_mlm_adaptation / 07_translation_benchmark",
            }
        )

    trace_lines.append("# Step 10 Selection Trace")
    trace_lines.append("")
    trace_lines.append("## Step 07 Original")
    trace_lines.append("")
    trace_lines.append("- Target pair selection loops over target language pairs on John/test and keeps the maximum chrF row.")
    trace_lines.append(f"- Evidence: `{step07_selection_evidence}`")
    trace_lines.append("- Decision: exploratory only; not an unbiased held-out target-pair result.")
    trace_lines.append("")
    trace_lines.append("## Branch 001")
    trace_lines.append("")
    trace_lines.append(f"- Branch score table contains `{len(test_rows)}` test rows and `{len(prior_test_rows)}` prior test rows before the final LaBSE row.")
    for row in test_rows:
        trace_lines.append(f"- `{row['run_id']}` / `{row['setup']}` / test chrF `{row['chrf']}` / ratio `{row['ratio_to_high_resource']}` / status `{row['status']}`")
    trace_lines.append("- Decision: Branch 001 remains exploratory because final model-family choice followed earlier test feedback and the Step 07 high-resource comparison was mixed-method.")
    trace_lines.append("")
    trace_lines.append("## Step 09")
    trace_lines.append("")
    for method_id, row in step09_methods.items():
        trace_lines.append(f"- `{method_id}`: high test chrF `{row['high_resource_test_chrf']}`, target test chrF `{row['target_test_chrf']}`, ratio `{row['method_matched_ratio']}`, status `{row['status']}`")
    trace_lines.append("- Decision: translation success claim remains blocked until a fresh held-out method-matched main-model run passes.")
    return audit_rows, invalidated, trace_lines


def main() -> None:
    started = time.time()
    root = Path("docs/exp/second_try").resolve()
    step_dir = root / "10_leakage_selection_audit"
    run_id = "step10_leakage_selection_" + datetime.now().strftime("%Y%m%d_%H%M%S")

    target_rows = read_tsv(root / "01_data_and_splits" / "target10_bible_verses.tsv")
    audit_rows: list[dict[str, str]] = []
    split_rows, split_summary = split_integrity_checks(target_rows)
    text_rows, text_summary = text_duplicate_checks(target_rows)
    selection_rows, invalidated_rows, trace_lines = selection_checks(root)
    audit_rows.extend(split_rows)
    audit_rows.extend(text_rows)
    audit_rows.extend(selection_rows)

    fail_count = sum(1 for row in audit_rows if row["status"].startswith("FAIL"))
    warn_count = sum(1 for row in audit_rows if row["status"].startswith("WARN"))
    pass_count = sum(1 for row in audit_rows if row["status"].startswith("PASS"))
    artifact_gate = "PASS" if audit_rows and invalidated_rows else "FAIL"
    claim_gate = "FAIL" if fail_count else "PASS"

    for row in audit_rows:
        row["run_id"] = run_id

    score_rows = [
        {
            "run_id": run_id,
            "claim": "split_integrity_for_target10",
            "evidence": "target10_bible_verses.tsv",
            "observed": json.dumps(split_summary, sort_keys=True),
            "decision": "SUPPORTED" if all(v == 0 for v in split_summary.values()) else "UNSUPPORTED",
            "status": "PASS" if all(v == 0 for v in split_summary.values()) else "FAIL",
            "notes": "book-level train/dev/test split integrity",
        },
        {
            "run_id": run_id,
            "claim": "no_exact_text_duplicate_risk",
            "evidence": "target10_bible_verses.tsv",
            "observed": json.dumps(text_summary, sort_keys=True),
            "decision": "DISCLOSED_RISK" if any(v > 0 for v in text_summary.values()) else "SUPPORTED",
            "status": "WARN_DISCLOSED" if any(v > 0 for v in text_summary.values()) else "PASS",
            "notes": "exact normalized duplicates across splits are reported separately from verse-id leakage",
        },
        {
            "run_id": run_id,
            "claim": "step07_translation_success_is_unbiased",
            "evidence": "07_translation_benchmark/run_step07.py",
            "observed": "target pair selected on John/test",
            "decision": "UNSUPPORTED",
            "status": "FAIL_INVALIDATES_CLAIM",
            "notes": "Step07 original target-pair row is exploratory only",
        },
        {
            "run_id": run_id,
            "claim": "branch001_translation_success_is_top_tier_safe",
            "evidence": "branches/branch_001_translation_retrieval_gap/score_table.tsv; 09_top_tier_validation/score_table.tsv",
            "observed": "prior branch test feedback plus mixed-method reference; Step09 ratio below threshold",
            "decision": "UNSUPPORTED",
            "status": "FAIL_INVALIDATES_CLAIM",
            "notes": "Branch001 is exploratory and superseded by Step09",
        },
    ]

    leakage_path = step_dir / "leakage_audit.tsv"
    score_path = step_dir / "score_table.tsv"
    invalidated_path = step_dir / "invalidated_runs.tsv"
    trace_path = step_dir / "selection_trace.md"
    results_path = step_dir / "results.md"
    file_results_path = step_dir / "file_results.tsv"

    audit_fields = ["run_id", "check_id", "category", "evidence", "observed", "expected", "status", "impact"]
    write_tsv(leakage_path, audit_rows, audit_fields)
    write_tsv(
        score_path,
        score_rows,
        ["run_id", "claim", "evidence", "observed", "decision", "status", "notes"],
    )
    write_tsv(
        invalidated_path,
        invalidated_rows,
        ["run_id", "artifact", "invalidated_claim", "reason", "status_after_audit", "return_to"],
    )
    trace_path.write_text("\n".join(trace_lines) + "\n", encoding="utf-8")

    results_path.write_text(
        f"""# Step 10 Results: Leakage And Selection Audit

Status: COMPLETED

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Artifact gate status: {artifact_gate}

Claim gate status: {claim_gate}

## Summary

Step 10 completed the P0 leakage and selection audit requested by Step 09 follow-up `F06`. The target10 book split itself passes the structural split checks. However, the translation success claim remains invalidated because Step 07 selected the original target pair on John/test, Branch 001 used repeated test feedback before the final LaBSE row, and the Branch 001 pass used a mixed-method high-resource comparison.

## Counts

| Item | Count |
| --- | ---: |
| audit checks | {len(audit_rows)} |
| pass-like checks | {pass_count} |
| warnings | {warn_count} |
| fail/invalidating checks | {fail_count} |
| invalidated run rows | {len(invalidated_rows)} |

## Main Findings

- Split integrity: `PASS`; no duplicated `(iso, verse_id)`, no verse assigned to multiple splits, and Mark/John split rules hold.
- Exact normalized text duplicate risk: `{"WARN_DISCLOSED" if any(v > 0 for v in text_summary.values()) else "PASS"}`; see `leakage_audit.tsv`.
- Step 07 original target selection: `FAIL_INVALIDATES_TRANSLATION_SELECTION`.
- Branch 001 top-tier success: `FAIL_INVALIDATES_BRANCH_SUCCESS`.
- Step 09 method-matched audit remains the current authority: selected adapted ratio below threshold.

## Failure Return

Failed gate: selection_protocol_for_translation_claim

Observed evidence: Step 07 target-pair selection used John/test; Branch 001 saw prior test feedback and used a mixed-method high-resource comparison.

Return-to step: `07_translation_benchmark` plus fresh held-out evaluation; if stronger main-model evidence is required, also return to `05_mlm_adaptation`.

Required fix: freeze method/model/pair/scoring on dev only, use method-matched high-resource and target scoring, and evaluate once on a fresh held-out set before making a top-tier translation claim.
""",
        encoding="utf-8",
    )

    file_rows = [
        file_result("score_table", score_path, "claim-level audit summary", "PASS_NEGATIVE_RESULT"),
        file_result("leakage_audit", leakage_path, "per-check leakage and selection audit", "PASS_NEGATIVE_RESULT"),
        file_result("selection_trace", trace_path, "chronological selection trace", "PASS_NEGATIVE_RESULT"),
        file_result("invalidated_runs", invalidated_path, "claims invalidated by audit", "PASS_NEGATIVE_RESULT"),
        file_result("results", results_path, "step result summary", "PASS_NEGATIVE_RESULT"),
    ]
    write_tsv(file_results_path, file_rows, ["file_role", "path", "rows_or_lines", "bytes", "md5", "status", "notes"])

    print(f"run_id={run_id}")
    print(f"artifact_gate_status={artifact_gate}")
    print(f"claim_gate_status={claim_gate}")
    print(f"fail_count={fail_count}")
    print(f"warn_count={warn_count}")
    print(f"runtime_minutes={(time.time() - started) / 60.0:.3f}")


if __name__ == "__main__":
    main()
