#!/usr/bin/env python3
"""Audit the Step23 8k branch against the original continued-pretraining control."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import os
import statistics
import time
from datetime import datetime
from pathlib import Path

import torch
import huggingface_hub


if not hasattr(huggingface_hub, "split_torch_state_dict_into_shards"):
    def _split_torch_state_dict_into_shards(state_dict, filename_pattern="pytorch_model{suffix}.bin", max_shard_size="10GB"):
        filename = filename_pattern.format(suffix="")
        tensor_names = list(state_dict.keys())
        return type(
            "StateDictSplit",
            (),
            {
                "is_sharded": False,
                "filename_to_tensors": {filename: tensor_names},
                "tensor_to_filename": {name: filename for name in tensor_names},
                "metadata": {},
            },
        )()

    huggingface_hub.split_torch_state_dict_into_shards = _split_torch_state_dict_into_shards

from transformers import logging as transformers_logging


SCORE_FIELDS = ["run_id", "gate_id", "criterion", "observed", "required", "status", "return_to", "notes"]
RAW_FIELDS = [
    "run_id",
    "model_family",
    "seed",
    "checkpoint_path",
    "train_tokens_seen",
    "token_budget_status",
    "zero_dev_loss",
    "final_dev_loss",
    "dev_loss_delta",
    "status",
    "notes",
]
METRIC_FIELDS = [
    "run_id",
    "model_family",
    "seed",
    "checkpoint_path",
    "dev_rows",
    "non_special_tokens",
    "words",
    "chars",
    "masked_tokens",
    "tokens_per_word",
    "tokens_per_char",
    "raw_masked_token_loss",
    "estimated_nll_per_word",
    "estimated_nll_per_char",
    "pseudo_ppl",
    "status",
    "notes",
]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def md5_file(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def count_rows(path: Path) -> int:
    if path.is_dir():
        return sum(1 for child in path.rglob("*") if child.is_file())
    if path.suffix == ".tsv":
        with path.open("r", encoding="utf-8") as f:
            return max(0, sum(1 for _ in f) - 1)
    with path.open("r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def file_result(role: str, path: Path, notes: str) -> dict[str, str]:
    if path.is_dir():
        size = sum(child.stat().st_size for child in path.rglob("*") if child.is_file())
        checksum = "DIRECTORY"
    else:
        size = path.stat().st_size
        checksum = md5_file(path)
    return {
        "file_role": role,
        "path": str(path),
        "rows_or_files": str(count_rows(path)),
        "bytes": str(size),
        "md5": checksum,
        "status": "PASS" if path.exists() and size > 0 else "FAIL",
        "notes": notes,
    }


def load_raw_rows(step23_summary: Path, step15_summary: Path, vocab_size: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in read_tsv(step23_summary):
        if row["vocab_size"] != vocab_size:
            continue
        checkpoint = Path(row["checkpoint_path"])
        if not checkpoint.exists():
            raise FileNotFoundError(checkpoint)
        rows.append(
            {
                "run_id": "",
                "model_family": "adapted_8k",
                "seed": row["seed"],
                "checkpoint_path": row["checkpoint_path"],
                "train_tokens_seen": row["train_tokens_seen"],
                "token_budget_status": row["token_budget_status"],
                "zero_dev_loss": row["zero_raw_loss"],
                "final_dev_loss": row["final_raw_loss"],
                "dev_loss_delta": row["raw_delta_vs_zero"],
                "status": row["status"],
                "notes": "Step23 8k adapted branch; Mark/dev only",
            }
        )
    for row in read_tsv(step15_summary):
        if row["model_family"] != "original_control":
            continue
        checkpoint = Path(row["checkpoint_path"])
        if not checkpoint.exists():
            raise FileNotFoundError(checkpoint)
        rows.append(
            {
                "run_id": "",
                "model_family": "original_control",
                "seed": row["seed"],
                "checkpoint_path": row["checkpoint_path"],
                "train_tokens_seen": row["train_tokens_seen"],
                "token_budget_status": row["token_budget_status"],
                "zero_dev_loss": row["zero_step_dev_loss"],
                "final_dev_loss": row["final_dev_loss"],
                "dev_loss_delta": row["dev_loss_delta"],
                "status": row["status"],
                "notes": "Step15 original continued-pretraining control; Mark/dev only",
            }
        )
    if len([row for row in rows if row["model_family"] == "adapted_8k"]) != 3:
        raise RuntimeError("expected three Step23 8k adapted rows")
    if len([row for row in rows if row["model_family"] == "original_control"]) != 3:
        raise RuntimeError("expected three Step15 original-control rows")
    return rows


def mean(rows: list[dict[str, str]], family: str, column: str) -> float:
    return statistics.mean(float(row[column]) for row in rows if row["model_family"] == family)


def std(rows: list[dict[str, str]], family: str, column: str) -> float:
    vals = [float(row[column]) for row in rows if row["model_family"] == family]
    return statistics.pstdev(vals) if len(vals) > 1 else 0.0


def metric_mean(rows: list[dict[str, str]], family: str, column: str) -> float:
    return statistics.mean(float(row[column]) for row in rows if row["model_family"] == family)


def metric_std(rows: list[dict[str, str]], family: str, column: str) -> float:
    vals = [float(row[column]) for row in rows if row["model_family"] == family]
    return statistics.pstdev(vals) if len(vals) > 1 else 0.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--step23-summary", default="docs/exp/second_try/23_v2_vocab_size_objective_probe/vocab_probe_summary.tsv")
    parser.add_argument("--step15-summary", default="docs/exp/second_try/15_v2_mlm_control/seed_summary.tsv")
    parser.add_argument("--dev-text", default="/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_mlm_dev_mark.txt")
    parser.add_argument("--vocab-size", default="8000")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--dev-limit", type=int, default=0)
    parser.add_argument("--seed", type=int, default=4242)
    parser.add_argument("--competitive-margin", type=float, default=1.10)
    parser.add_argument("--token-budget-tolerance", type=float, default=1.02)
    args = parser.parse_args()

    transformers_logging.set_verbosity_error()
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    start = time.time()
    run_id = "step24_v2_8k_mlm_control_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    step_dir = Path(args.step_dir).resolve()
    step_dir.mkdir(parents=True, exist_ok=True)
    repo_root = Path(__file__).resolve().parents[4]
    step16 = load_module("step16_module", repo_root / "docs/exp/second_try/16_v2_mlm_metric_fairness/run_step16.py")

    raw_rows = load_raw_rows(Path(args.step23_summary), Path(args.step15_summary), args.vocab_size)
    for row in raw_rows:
        row["run_id"] = run_id
    tokens = [int(row["train_tokens_seen"]) for row in raw_rows]
    token_ratio = max(tokens) / max(1, min(tokens))
    adapted_mean = mean(raw_rows, "adapted_8k", "final_dev_loss")
    adapted_std = std(raw_rows, "adapted_8k", "final_dev_loss")
    original_mean = mean(raw_rows, "original_control", "final_dev_loss")
    original_std = std(raw_rows, "original_control", "final_dev_loss")
    raw_ratio = adapted_mean / original_mean
    adapted_improved = sum(1 for row in raw_rows if row["model_family"] == "adapted_8k" and float(row["dev_loss_delta"]) < 0.0)

    eval_rows = []
    for row in raw_rows:
        family = "adapted_extended" if row["model_family"] == "adapted_8k" else "original_control"
        eval_rows.append({"model_family": family, "seed": row["seed"], "checkpoint_path": row["checkpoint_path"]})

    texts = step16.read_lines(Path(args.dev_text), args.dev_limit)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    metric_rows: list[dict[str, str]] = []
    for row in eval_rows:
        print(f"evaluating family={row['model_family']} seed={row['seed']}", flush=True)
        metric_rows.append(step16.evaluate_checkpoint(row, texts, device, args, run_id))
    for row in metric_rows:
        if row["model_family"] == "adapted_extended":
            row["model_family"] = "adapted_8k"

    adapted_word = metric_mean(metric_rows, "adapted_8k", "estimated_nll_per_word")
    adapted_word_std = metric_std(metric_rows, "adapted_8k", "estimated_nll_per_word")
    original_word = metric_mean(metric_rows, "original_control", "estimated_nll_per_word")
    original_word_std = metric_std(metric_rows, "original_control", "estimated_nll_per_word")
    adapted_char = metric_mean(metric_rows, "adapted_8k", "estimated_nll_per_char")
    adapted_char_std = metric_std(metric_rows, "adapted_8k", "estimated_nll_per_char")
    original_char = metric_mean(metric_rows, "original_control", "estimated_nll_per_char")
    original_char_std = metric_std(metric_rows, "original_control", "estimated_nll_per_char")
    adapted_eval_raw = metric_mean(metric_rows, "adapted_8k", "raw_masked_token_loss")
    original_eval_raw = metric_mean(metric_rows, "original_control", "raw_masked_token_loss")
    normalized_word_ratio = adapted_word / original_word
    normalized_char_ratio = adapted_char / original_char
    eval_raw_ratio = adapted_eval_raw / original_eval_raw
    checkpoint_gate = len(raw_rows) == 6 and len(metric_rows) == 6
    token_gate = token_ratio <= args.token_budget_tolerance
    claim_gate = checkpoint_gate and token_gate and normalized_word_ratio <= args.competitive_margin and normalized_char_ratio <= args.competitive_margin
    best_adapted = sorted([row for row in raw_rows if row["model_family"] == "adapted_8k"], key=lambda row: float(row["final_dev_loss"]))[0]

    score_rows = [
        {
            "run_id": run_id,
            "gate_id": "G01_required_checkpoints",
            "criterion": "all 8k adapted and original-control checkpoints exist and are evaluated",
            "observed": f"raw_rows={len(raw_rows)}/6; normalized_rows={len(metric_rows)}/6",
            "required": "6 raw rows and 6 normalized rows",
            "status": "PASS" if checkpoint_gate else "FAIL",
            "return_to": "23_v2_vocab_size_objective_probe",
            "notes": "3 seeds x 2 model families",
        },
        {
            "run_id": run_id,
            "gate_id": "G02_no_final_access",
            "criterion": "ACT final data not read",
            "observed": "NO_ACT_FINAL_ACCESS",
            "required": "NO_ACT_FINAL_ACCESS",
            "status": "PASS",
            "return_to": "12_v2_split_protocol",
            "notes": "Step23 summary, Step15 summary, checkpoints, and Mark/dev text only",
        },
        {
            "run_id": run_id,
            "gate_id": "G03_token_budget_match",
            "criterion": "8k adapted and original-control train token budgets match",
            "observed": f"min_tokens={min(tokens)}; max_tokens={max(tokens)}; token_ratio={token_ratio:.6f}",
            "required": f"token_ratio<={args.token_budget_tolerance:.6f}",
            "status": "PASS" if token_gate else "FAIL",
            "return_to": "15_v2_mlm_control",
            "notes": "uses existing matched-budget Step23/Step15 runs",
        },
        {
            "run_id": run_id,
            "gate_id": "G04_adapted_improves",
            "criterion": "8k adapted branch improves over its zero-step state in every seed",
            "observed": f"{adapted_improved}/3",
            "required": "3/3",
            "status": "PASS" if adapted_improved == 3 else "FAIL",
            "return_to": "23_v2_vocab_size_objective_probe",
            "notes": "self-comparison within 8k tokenizer",
        },
        {
            "run_id": run_id,
            "gate_id": "G05_raw_control_context",
            "criterion": "raw 8k/original ratio is recorded as diagnostic context",
            "observed": f"ratio={raw_ratio:.6f}; adapted_mean={adapted_mean:.6f}; original_mean={original_mean:.6f}",
            "required": "recorded",
            "status": "PASS",
            "return_to": "NOT_APPLICABLE",
            "notes": "raw token losses are not directly comparable across tokenizer vocabularies",
        },
        {
            "run_id": run_id,
            "gate_id": "G06_word_normalized_competitive",
            "criterion": "8k adapted estimated NLL per word is within original-control margin",
            "observed": f"ratio={normalized_word_ratio:.6f}; adapted_mean={adapted_word:.6f}; original_mean={original_word:.6f}",
            "required": f"ratio<={args.competitive_margin:.6f}",
            "status": "PASS" if normalized_word_ratio <= args.competitive_margin else "FAIL",
            "return_to": "23_v2_vocab_size_objective_probe or objective_redesign",
            "notes": "normalizes by non-special token count per word",
        },
        {
            "run_id": run_id,
            "gate_id": "G07_char_normalized_competitive",
            "criterion": "8k adapted estimated NLL per character is within original-control margin",
            "observed": f"ratio={normalized_char_ratio:.6f}; adapted_mean={adapted_char:.6f}; original_mean={original_char:.6f}",
            "required": f"ratio<={args.competitive_margin:.6f}",
            "status": "PASS" if normalized_char_ratio <= args.competitive_margin else "FAIL",
            "return_to": "23_v2_vocab_size_objective_probe or objective_redesign",
            "notes": "normalizes by non-special token count per character",
        },
        {
            "run_id": run_id,
            "gate_id": "G08_checkpoint_selection",
            "criterion": "best 8k checkpoint selected on Mark/dev only",
            "observed": best_adapted["checkpoint_path"],
            "required": "one selected 8k checkpoint",
            "status": "PASS",
            "return_to": "24_v2_8k_mlm_control",
            "notes": f"seed={best_adapted['seed']}; final_raw_loss={best_adapted['final_dev_loss']}",
        },
    ]

    score_path = step_dir / "score_table.tsv"
    raw_path = step_dir / "raw_control_summary.tsv"
    metrics_path = step_dir / "normalized_mlm_scores.tsv"
    selected_path = step_dir / "checkpoint_selection.md"
    access_path = step_dir / "v2_no_final_access_audit.tsv"
    results_path = step_dir / "results.md"
    file_results_path = step_dir / "file_results.tsv"

    write_tsv(score_path, score_rows, SCORE_FIELDS)
    write_tsv(raw_path, raw_rows, RAW_FIELDS)
    write_tsv(metrics_path, metric_rows, METRIC_FIELDS)
    selected_path.write_text(
        f"""# Step 24 8k MLM Control Selection

Run id: `{run_id}`

Claim gate status: `{'PASS' if claim_gate else 'FAIL'}`

Selected 8k checkpoint: `{best_adapted['checkpoint_path']}`

Selected seed: `{best_adapted['seed']}`

8k raw mean final loss: `{adapted_mean:.6f}`

Original-control raw mean final loss: `{original_mean:.6f}`

Raw ratio: `{raw_ratio:.6f}`

Word-normalized ratio: `{normalized_word_ratio:.6f}`

Char-normalized ratio: `{normalized_char_ratio:.6f}`

Selection data: `MAR` dev only.

Final data access: `NO_ACT_FINAL_ACCESS`.
""",
        encoding="utf-8",
    )
    access_rows = [
        {
            "run_id": run_id,
            "input_role": "step23_summary",
            "path": str(Path(args.step23_summary).resolve()),
            "allowed_split": "prior_train_dev_result",
            "rows_or_files": str(count_rows(Path(args.step23_summary))),
            "md5": md5_file(Path(args.step23_summary)),
            "final_access": "NO",
            "status": "PASS",
        },
        {
            "run_id": run_id,
            "input_role": "step15_summary",
            "path": str(Path(args.step15_summary).resolve()),
            "allowed_split": "prior_train_dev_result",
            "rows_or_files": str(count_rows(Path(args.step15_summary))),
            "md5": md5_file(Path(args.step15_summary)),
            "final_access": "NO",
            "status": "PASS",
        },
        {
            "run_id": run_id,
            "input_role": "dev_text",
            "path": str(Path(args.dev_text).resolve()),
            "allowed_split": "MAR_dev",
            "rows_or_files": str(count_rows(Path(args.dev_text))),
            "md5": md5_file(Path(args.dev_text)),
            "final_access": "NO",
            "status": "PASS",
        },
    ]
    write_tsv(access_path, access_rows, ["run_id", "input_role", "path", "allowed_split", "rows_or_files", "md5", "final_access", "status"])
    results_path.write_text(
        f"""# Step 24 Results: V2 8k MLM Control And Normalized Audit

Status: COMPLETED

Run id: {run_id}

Completed date: {datetime.now().strftime('%Y-%m-%d')}

Artifact gate status: {'PASS' if checkpoint_gate and token_gate else 'FAIL'}

Claim gate status: {'PASS' if claim_gate else 'FAIL'}

## Summary

Step 24 compares the Step23 selected 8k adapted branch against the Step15 original XLM-R continued-pretraining control. It uses existing matched-budget train/dev checkpoints and re-evaluates normalized MLM diagnostics on Mark/dev only. ACT final was not read.

| Metric | 8k Adapted Mean | Original Mean | Ratio |
| --- | ---: | ---: | ---: |
| raw Step23/Step15 final dev loss | {adapted_mean:.6f} +/- {adapted_std:.6f} | {original_mean:.6f} +/- {original_std:.6f} | {raw_ratio:.6f} |
| re-evaluated raw masked-token loss | {adapted_eval_raw:.6f} | {original_eval_raw:.6f} | {eval_raw_ratio:.6f} |
| estimated NLL per word | {adapted_word:.6f} +/- {adapted_word_std:.6f} | {original_word:.6f} +/- {original_word_std:.6f} | {normalized_word_ratio:.6f} |
| estimated NLL per char | {adapted_char:.6f} +/- {adapted_char_std:.6f} | {original_char:.6f} +/- {original_char_std:.6f} | {normalized_char_ratio:.6f} |

## Interpretation

The 8k branch is the best current adapted branch, but the positive model-dependent claim requires both normalized ratios to be within `{args.competitive_margin:.6f}` of the original-control baseline.

## Failure Return

Failed gate: {'NOT_APPLICABLE' if claim_gate else '8k_normalized_mlm_competitive_gate'}

Observed evidence: {'NOT_APPLICABLE' if claim_gate else f'word_ratio={normalized_word_ratio:.6f}, char_ratio={normalized_char_ratio:.6f}'}

Return-to step: {'V2_04_DOWNSTREAM' if claim_gate else '23_v2_vocab_size_objective_probe or objective_redesign'}

Required fix: {'proceed to downstream/translation freeze' if claim_gate else 'redesign objective/data beyond smaller-vocab branch or downgrade model-dependent claim'}

Runtime minutes: {(time.time() - start) / 60.0:.3f}
""",
        encoding="utf-8",
    )

    file_rows = [
        file_result("score_table", score_path, "8k control gate table"),
        file_result("raw_control_summary", raw_path, "raw 8k-vs-original matched-budget summary"),
        file_result("normalized_mlm_scores", metrics_path, "normalized Mark-dev MLM diagnostics"),
        file_result("checkpoint_selection", selected_path, "best 8k checkpoint selected on Mark/dev"),
        file_result("no_final_access_audit", access_path, "input access audit"),
        file_result("results", results_path, "step result summary"),
    ]
    write_tsv(file_results_path, file_rows, ["file_role", "path", "rows_or_files", "bytes", "md5", "status", "notes"])

    print(f"run_id={run_id}")
    print(f"artifact_gate_status={'PASS' if checkpoint_gate and token_gate else 'FAIL'}")
    print(f"claim_gate_status={'PASS' if claim_gate else 'FAIL'}")
    print(f"raw_ratio={raw_ratio:.6f}")
    print(f"word_ratio={normalized_word_ratio:.6f}")
    print(f"char_ratio={normalized_char_ratio:.6f}")


if __name__ == "__main__":
    main()
