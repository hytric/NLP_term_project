#!/usr/bin/env python3
"""Fresh held-out feasibility audit for second_try."""

from __future__ import annotations

import csv
import hashlib
from collections import defaultdict
from datetime import datetime
from pathlib import Path


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


def file_result(role: str, path: Path, notes: str, status: str) -> dict[str, str]:
    return {
        "file_role": role,
        "path": str(path),
        "rows_or_lines": str(count_rows_or_lines(path)),
        "bytes": str(path.stat().st_size),
        "md5": md5_file(path),
        "status": status,
        "notes": notes,
    }


def main() -> None:
    root = Path("docs/exp/second_try").resolve()
    step_dir = root / "11_fresh_holdout_feasibility"
    run_id = "step11_fresh_holdout_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    target_path = root / "01_data_and_splits" / "target10_bible_verses.tsv"
    rows = read_tsv(target_path)

    books_by_split: dict[str, set[str]] = defaultdict(set)
    rows_by_split: dict[str, int] = defaultdict(int)
    for row in rows:
        books_by_split[row["split"]].add(row["book"])
        rows_by_split[row["split"]] += 1

    train_books = books_by_split["train"]
    dev_books = books_by_split["dev"]
    test_books = books_by_split["test"]
    all_books = set().union(*books_by_split.values())
    untouched_books = all_books - train_books - dev_books - test_books

    second_try_artifacts = Path("/home/axt/mnt2/jongha/second_try/artifacts")
    non_current_parallel = []
    if second_try_artifacts.exists():
        for path in second_try_artifacts.rglob("*"):
            if not path.is_file():
                continue
            lowered = path.name.lower()
            if any(key in lowered for key in ["parallel", "translation", "heldout", "fresh"]):
                non_current_parallel.append(str(path))

    repo_processed = Path("/home/axt/mnt2/jongha/Glot500-py39-eval/data/processed")
    legacy_candidates = []
    if repo_processed.exists():
        for path in repo_processed.rglob("*"):
            if not path.is_file():
                continue
            parts = "/".join(path.parts).lower()
            if any(key in parts for key in ["nmt_", "parallel", "aligned", "flores", "tatoeba"]):
                legacy_candidates.append(str(path))
                if len(legacy_candidates) >= 20:
                    break

    availability_rows = [
        {
            "source_id": "current_train_books",
            "path": str(target_path),
            "candidate_type": "bible_books",
            "rows": str(rows_by_split["train"]),
            "books": ",".join(sorted(train_books)),
            "prior_use": "tokenizer_training_and_mlm_adaptation",
            "decision": "REQUIRES_RERUN",
            "reason": "train books are not fresh for top-tier final translation evaluation",
        },
        {
            "source_id": "current_dev_mark",
            "path": str(target_path),
            "candidate_type": "bible_books",
            "rows": str(rows_by_split["dev"]),
            "books": ",".join(sorted(dev_books)),
            "prior_use": "dev_selection",
            "decision": "REQUIRES_RERUN",
            "reason": "Mark is already used for dev selection",
        },
        {
            "source_id": "current_test_john",
            "path": str(target_path),
            "candidate_type": "bible_books",
            "rows": str(rows_by_split["test"]),
            "books": ",".join(sorted(test_books)),
            "prior_use": "Step07_Branch001_Step09_test_feedback",
            "decision": "REQUIRES_RERUN",
            "reason": "John test is burned by repeated branch feedback and Step09 evaluation",
        },
        {
            "source_id": "untouched_current_books",
            "path": str(target_path),
            "candidate_type": "bible_books",
            "rows": "0",
            "books": ",".join(sorted(untouched_books)) if untouched_books else "NONE",
            "prior_use": "none",
            "decision": "NOT_FOUND",
            "reason": "current split assigns every available target10 book to train/dev/test",
        },
        {
            "source_id": "second_try_external_parallel",
            "path": "/home/axt/mnt2/jongha/second_try/artifacts",
            "candidate_type": "external_or_noncurrent_parallel",
            "rows": str(len(non_current_parallel)),
            "books": "NOT_APPLICABLE",
            "prior_use": "second_try_artifact_search",
            "decision": "NOT_FOUND" if not non_current_parallel else "REVIEW_REQUIRED",
            "reason": "no ready fresh external parallel evaluation corpus under second_try artifacts" if not non_current_parallel else "candidate files need provenance audit before use",
        },
        {
            "source_id": "legacy_processed_parallel",
            "path": str(repo_processed),
            "candidate_type": "legacy_processed_data",
            "rows": str(len(legacy_candidates)),
            "books": "NOT_APPLICABLE",
            "prior_use": "outside_second_try_evidence_scope",
            "decision": "OUT_OF_SCOPE",
            "reason": "legacy processed files exist but cannot be used as second_try evidence without reimport/provenance and new split",
        },
    ]

    usable_now = [row for row in availability_rows if row["decision"] == "USABLE_NOW"]
    current_fresh_available = bool(usable_now)
    claim_gate = "PASS" if current_fresh_available else "FAIL"

    score_rows = [
        {
            "run_id": run_id,
            "claim": "fresh_heldout_available_in_current_second_try",
            "evidence": "data_availability.tsv",
            "observed": "USABLE_NOW candidates=" + str(len(usable_now)),
            "decision": "SUPPORTED" if current_fresh_available else "UNSUPPORTED",
            "status": "PASS" if current_fresh_available else "FAIL_BLOCKS_F02_F03",
            "notes": "top-tier translation rerun needs a fresh held-out set not touched by adaptation, dev selection, or prior test feedback",
        },
        {
            "run_id": run_id,
            "claim": "legacy_processed_data_can_be_used_directly",
            "evidence": str(repo_processed),
            "observed": "legacy candidate files=" + str(len(legacy_candidates)),
            "decision": "UNSUPPORTED",
            "status": "FAIL_OUT_OF_SCOPE",
            "notes": "user constrained second_try evidence; legacy files require reimport/provenance before use",
        },
    ]

    protocol_lines = [
        "# Step 11 Fresh-Heldout Protocol",
        "",
        "## Decision",
        "",
        "No current second_try artifact provides a fresh held-out translation test set.",
        "",
        "## Why",
        "",
        f"- Train books are already used by tokenizer training and MLM adaptation: `{','.join(sorted(train_books))}`.",
        f"- Dev books are already used for selection: `{','.join(sorted(dev_books))}`.",
        f"- Test books are already burned by Step07/Branch001/Step09 feedback: `{','.join(sorted(test_books))}`.",
        "- No untouched target10 book remains in the current split.",
        "- Legacy processed translation files exist outside the second_try evidence boundary and need reimport/provenance before use.",
        "",
        "## Required Protocol For F02/F03",
        "",
        "1. Return to `01_data_and_splits` and reserve a new final held-out book before tokenizer training and MLM adaptation, or add a new external parallel corpus under second_try with provenance.",
        "2. Rerun tokenizer/MLM adaptation if the held-out book changes the training corpus.",
        "3. Select method/model/pair/scoring on dev only.",
        "4. Evaluate exactly once on the fresh final held-out set.",
        "5. Report method-matched high-resource and target ratios in one score table.",
    ]

    availability_path = step_dir / "data_availability.tsv"
    score_path = step_dir / "score_table.tsv"
    protocol_path = step_dir / "fresh_holdout_protocol.md"
    results_path = step_dir / "results.md"
    file_results_path = step_dir / "file_results.tsv"

    write_tsv(
        availability_path,
        availability_rows,
        ["source_id", "path", "candidate_type", "rows", "books", "prior_use", "decision", "reason"],
    )
    write_tsv(score_path, score_rows, ["run_id", "claim", "evidence", "observed", "decision", "status", "notes"])
    protocol_path.write_text("\n".join(protocol_lines) + "\n", encoding="utf-8")
    results_path.write_text(
        f"""# Step 11 Results: Fresh-Heldout Feasibility

Status: COMPLETED

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Artifact gate status: PASS

Claim gate status: {claim_gate}

## Summary

Step 11 checked whether P0 follow-ups `F02` and `F03` can be run as top-tier fresh-heldout translation experiments using the current second_try artifacts. They cannot. Every current target10 Bible book is already assigned to train/dev/test, the train books were used for tokenizer/MLM adaptation, Mark was used for selection, and John was burned by repeated test feedback and Step09.

## Decision

Current fresh held-out available: `{current_fresh_available}`.

Legacy processed data may contain translation files, but it is outside the second_try evidence boundary and must be reimported with provenance before use.

## Failure Return

Failed gate: fresh_heldout_available_for_F02_F03

Observed evidence: no `USABLE_NOW` candidate in `data_availability.tsv`.

Return-to step: `01_data_and_splits`

Required fix: reserve a new final held-out book before retraining, or import a new external parallel corpus under second_try with provenance and locked dev/test selection rules.
""",
        encoding="utf-8",
    )

    file_rows = [
        file_result("score_table", score_path, "fresh-heldout claim status", "PASS_NEGATIVE_RESULT"),
        file_result("data_availability", availability_path, "candidate data source audit", "PASS_NEGATIVE_RESULT"),
        file_result("fresh_holdout_protocol", protocol_path, "required protocol for F02/F03", "PASS_NEGATIVE_RESULT"),
        file_result("results", results_path, "step result summary", "PASS_NEGATIVE_RESULT"),
    ]
    write_tsv(file_results_path, file_rows, ["file_role", "path", "rows_or_lines", "bytes", "md5", "status", "notes"])

    print(f"run_id={run_id}")
    print("artifact_gate_status=PASS")
    print(f"claim_gate_status={claim_gate}")
    print(f"usable_now={len(usable_now)}")
    print(f"legacy_candidates={len(legacy_candidates)}")


if __name__ == "__main__":
    main()
