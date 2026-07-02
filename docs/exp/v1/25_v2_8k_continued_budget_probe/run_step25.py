#!/usr/bin/env python3
"""Continue the Step24 8k/control checkpoints to probe a larger MLM budget."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import statistics
import time
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

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

from transformers import AutoModelForMaskedLM, XLMRobertaTokenizer, logging as transformers_logging


SCORE_FIELDS = ["run_id", "gate_id", "criterion", "observed", "required", "status", "return_to", "notes"]
SUMMARY_FIELDS = [
    "run_id",
    "model_family",
    "seed",
    "source_checkpoint",
    "source_train_tokens",
    "continued_train_tokens",
    "total_train_tokens",
    "token_budget_status",
    "source_recorded_loss",
    "source_eval_loss",
    "continued_final_loss",
    "loss_delta_vs_source_eval",
    "batch_size",
    "max_length",
    "learning_rate",
    "actual_train_steps",
    "runtime_minutes",
    "tokens_per_sec",
    "checkpoint_path",
    "status",
    "notes",
]
CURVE_FIELDS = [
    "run_id",
    "model_family",
    "seed",
    "stage",
    "step",
    "continued_train_tokens",
    "total_train_tokens",
    "dev_loss",
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


def read_lines(path: Path, limit: int) -> list[str]:
    texts = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            text = line.rstrip("\n")
            if text.strip():
                texts.append(text)
            if limit > 0 and len(texts) >= limit:
                break
    if not texts:
        raise RuntimeError(f"no texts loaded from {path}")
    return texts


def load_sources(path: Path) -> list[dict[str, str]]:
    rows = read_tsv(path)
    usable = []
    for row in rows:
        if row["model_family"] not in {"adapted_8k", "original_control"}:
            continue
        checkpoint = Path(row["checkpoint_path"])
        if not checkpoint.exists():
            raise FileNotFoundError(checkpoint)
        usable.append(row)
    if len(usable) != 6:
        raise RuntimeError(f"expected six Step24 source rows, found {len(usable)}")
    return usable


def mean(rows: list[dict[str, str]], family: str, column: str) -> float:
    return statistics.mean(float(row[column]) for row in rows if row["model_family"] == family)


def std(rows: list[dict[str, str]], family: str, column: str) -> float:
    vals = [float(row[column]) for row in rows if row["model_family"] == family]
    return statistics.pstdev(vals) if len(vals) > 1 else 0.0


def continue_one(
    row: dict[str, str],
    run_id: str,
    train_texts: list[str],
    dev_texts: list[str],
    device: torch.device,
    args: argparse.Namespace,
    step15,
    checkpoint_root: Path,
) -> tuple[dict[str, str], list[dict[str, str]], Path]:
    seed = int(row["seed"])
    torch.manual_seed(seed)
    source = Path(row["checkpoint_path"])
    family = row["model_family"]
    tokenizer = XLMRobertaTokenizer.from_pretrained(str(source), local_files_only=True)
    model = AutoModelForMaskedLM.from_pretrained(str(source), local_files_only=True)
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate)
    start_time = time.time()
    source_tokens = int(row["train_tokens_seen"])
    source_recorded_loss = float(row["final_dev_loss"])
    source_eval_loss, _ = step15.evaluate(model, tokenizer, dev_texts, device, args.eval_batch_size, args.max_length, args.seed + seed * 100000)
    curves = [
        {
            "run_id": run_id,
            "model_family": family,
            "seed": str(seed),
            "stage": "source_eval",
            "step": "0",
            "continued_train_tokens": "0",
            "total_train_tokens": str(source_tokens),
            "dev_loss": f"{source_eval_loss:.6f}",
            "status": "PASS",
            "notes": "source checkpoint re-evaluated on Mark/dev",
        }
    ]
    model.train()
    order = step15.make_training_order(len(train_texts), args.train_steps * args.batch_size, seed + args.order_seed_offset)
    continued_tokens = 0
    actual_steps = 0
    final_loss = source_eval_loss
    last_eval_step = 0
    for step in range(1, args.train_steps + 1):
        indices = order[(step - 1) * args.batch_size : step * args.batch_size]
        batch_texts = [train_texts[index] for index in indices]
        batch, _, token_count = step15.make_masked_batch(tokenizer, batch_texts, device, args.max_length, (seed + args.order_seed_offset) * 100000 + step)
        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)
        continued_tokens += token_count
        actual_steps = step
        if step % args.eval_every == 0:
            final_loss, _ = step15.evaluate(model, tokenizer, dev_texts, device, args.eval_batch_size, args.max_length, args.seed + seed * 100000 + step * 1000)
            curves.append(
                {
                    "run_id": run_id,
                    "model_family": family,
                    "seed": str(seed),
                    "stage": "dev_eval",
                    "step": str(step),
                    "continued_train_tokens": str(continued_tokens),
                    "total_train_tokens": str(source_tokens + continued_tokens),
                    "dev_loss": f"{final_loss:.6f}",
                    "status": "PASS",
                    "notes": "scheduled Mark/dev eval",
                }
            )
            last_eval_step = step
            model.train()
        if continued_tokens >= args.additional_train_tokens:
            break
    if actual_steps > 0 and last_eval_step != actual_steps:
        final_loss, _ = step15.evaluate(model, tokenizer, dev_texts, device, args.eval_batch_size, args.max_length, args.seed + seed * 100000 + actual_steps * 1000)
        curves.append(
            {
                "run_id": run_id,
                "model_family": family,
                "seed": str(seed),
                "stage": "final_eval",
                "step": str(actual_steps),
                "continued_train_tokens": str(continued_tokens),
                "total_train_tokens": str(source_tokens + continued_tokens),
                "dev_loss": f"{final_loss:.6f}",
                "status": "PASS",
                "notes": "final Mark/dev eval after continuation budget",
            }
        )
    out_dir = checkpoint_root / f"{family}_continued_seed{seed}"
    out_dir.mkdir(parents=True, exist_ok=True)
    model.to("cpu")
    model.save_pretrained(out_dir)
    tokenizer.save_pretrained(out_dir)
    report = {
        "run_id": run_id,
        "model_family": family,
        "seed": seed,
        "source_checkpoint": str(source),
        "source_train_tokens": source_tokens,
        "continued_train_tokens": continued_tokens,
        "total_train_tokens": source_tokens + continued_tokens,
        "source_eval_loss": source_eval_loss,
        "continued_final_loss": final_loss,
        "selection_data": "MAR_dev_only",
        "final_access": "NO_ACT_FINAL_ACCESS",
        "fresh_optimizer_state": True,
    }
    (out_dir / "continued_budget_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    runtime = time.time() - start_time
    status = "PASS" if final_loss < source_eval_loss else "NO_IMPROVEMENT"
    if family == "original_control":
        status = "CONTROL_COMPLETE"
    summary = {
        "run_id": run_id,
        "model_family": family,
        "seed": str(seed),
        "source_checkpoint": str(source),
        "source_train_tokens": str(source_tokens),
        "continued_train_tokens": str(continued_tokens),
        "total_train_tokens": str(source_tokens + continued_tokens),
        "token_budget_status": "PASS" if continued_tokens >= args.additional_train_tokens else "FAIL",
        "source_recorded_loss": f"{source_recorded_loss:.6f}",
        "source_eval_loss": f"{source_eval_loss:.6f}",
        "continued_final_loss": f"{final_loss:.6f}",
        "loss_delta_vs_source_eval": f"{final_loss - source_eval_loss:.6f}",
        "batch_size": str(args.batch_size),
        "max_length": str(args.max_length),
        "learning_rate": f"{args.learning_rate:.8f}",
        "actual_train_steps": str(actual_steps),
        "runtime_minutes": f"{runtime / 60.0:.3f}",
        "tokens_per_sec": f"{continued_tokens / max(1e-6, runtime):.3f}",
        "checkpoint_path": str(out_dir),
        "status": status,
        "notes": "fresh_optimizer_continuation; mark_dev_only; no_ACT_final_access",
    }
    return summary, curves, out_dir


def evaluate_normalized(summary_rows: list[dict[str, str]], dev_texts: list[str], device: torch.device, args: argparse.Namespace, step16, run_id: str) -> list[dict[str, str]]:
    metric_rows: list[dict[str, str]] = []
    eval_args = SimpleNamespace(batch_size=args.eval_batch_size, max_length=args.max_length, seed=args.seed)
    for row in summary_rows:
        family = "adapted_extended" if row["model_family"] == "adapted_8k" else "original_control"
        eval_row = {"model_family": family, "seed": row["seed"], "checkpoint_path": row["checkpoint_path"]}
        print(f"normalizing family={row['model_family']} seed={row['seed']}", flush=True)
        metric = step16.evaluate_checkpoint(eval_row, dev_texts, device, eval_args, run_id)
        if metric["model_family"] == "adapted_extended":
            metric["model_family"] = "adapted_8k"
        metric_rows.append(metric)
    return metric_rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--checkpoint-root", default="/home/axt/mnt2/jongha/second_try/checkpoints/25_v2_8k_continued_budget_probe")
    parser.add_argument("--step24-raw-summary", default="docs/exp/second_try/24_v2_8k_mlm_control/raw_control_summary.tsv")
    parser.add_argument("--train-text", default="/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_tokenizer_mlm_train.txt")
    parser.add_argument("--dev-text", default="/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_mlm_dev_mark.txt")
    parser.add_argument("--train-limit", type=int, default=0)
    parser.add_argument("--dev-limit", type=int, default=0)
    parser.add_argument("--train-steps", type=int, default=1600)
    parser.add_argument("--additional-train-tokens", type=int, default=500000)
    parser.add_argument("--token-budget-tolerance", type=float, default=1.02)
    parser.add_argument("--competitive-margin", type=float, default=1.10)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--eval-batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--learning-rate", type=float, default=5e-5)
    parser.add_argument("--eval-every", type=int, default=800)
    parser.add_argument("--seed", type=int, default=5252)
    parser.add_argument("--order-seed-offset", type=int, default=500003)
    args = parser.parse_args()

    transformers_logging.set_verbosity_error()
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    torch.backends.cuda.matmul.allow_tf32 = True
    start = time.time()
    run_id = "step25_v2_8k_continued_budget_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    step_dir = Path(args.step_dir).resolve()
    checkpoint_root = Path(args.checkpoint_root).resolve()
    step_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_root.mkdir(parents=True, exist_ok=True)
    repo_root = Path(__file__).resolve().parents[4]
    step15 = load_module("step15_module", repo_root / "docs/exp/second_try/15_v2_mlm_control/run_step15.py")
    step16 = load_module("step16_module", repo_root / "docs/exp/second_try/16_v2_mlm_metric_fairness/run_step16.py")

    sources = load_sources(Path(args.step24_raw_summary))
    train_texts = read_lines(Path(args.train_text), args.train_limit)
    dev_texts = read_lines(Path(args.dev_text), args.dev_limit)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    summary_rows: list[dict[str, str]] = []
    curve_rows: list[dict[str, str]] = []
    checkpoint_dirs: list[Path] = []
    for row in sources:
        print(f"continuing family={row['model_family']} seed={row['seed']}", flush=True)
        summary, curves, checkpoint = continue_one(row, run_id, train_texts, dev_texts, device, args, step15, checkpoint_root)
        summary_rows.append(summary)
        curve_rows.extend(curves)
        checkpoint_dirs.append(checkpoint)

    metric_rows = evaluate_normalized(summary_rows, dev_texts, device, args, step16, run_id)
    completed = len(summary_rows)
    total_tokens = [int(row["total_train_tokens"]) for row in summary_rows]
    continued_tokens = [int(row["continued_train_tokens"]) for row in summary_rows]
    token_ratio = max(total_tokens) / max(1, min(total_tokens))
    continued_ratio = max(continued_tokens) / max(1, min(continued_tokens))
    adapted_improved = sum(1 for row in summary_rows if row["model_family"] == "adapted_8k" and float(row["loss_delta_vs_source_eval"]) < 0.0)
    adapted_mean = mean(summary_rows, "adapted_8k", "continued_final_loss")
    adapted_std = std(summary_rows, "adapted_8k", "continued_final_loss")
    original_mean = mean(summary_rows, "original_control", "continued_final_loss")
    original_std = std(summary_rows, "original_control", "continued_final_loss")
    raw_ratio = adapted_mean / original_mean
    adapted_word = mean(metric_rows, "adapted_8k", "estimated_nll_per_word")
    adapted_word_std = std(metric_rows, "adapted_8k", "estimated_nll_per_word")
    original_word = mean(metric_rows, "original_control", "estimated_nll_per_word")
    original_word_std = std(metric_rows, "original_control", "estimated_nll_per_word")
    adapted_char = mean(metric_rows, "adapted_8k", "estimated_nll_per_char")
    adapted_char_std = std(metric_rows, "adapted_8k", "estimated_nll_per_char")
    original_char = mean(metric_rows, "original_control", "estimated_nll_per_char")
    original_char_std = std(metric_rows, "original_control", "estimated_nll_per_char")
    word_ratio = adapted_word / original_word
    char_ratio = adapted_char / original_char
    artifact_gate = completed == 6 and len(metric_rows) == 6
    token_gate = token_ratio <= args.token_budget_tolerance and continued_ratio <= args.token_budget_tolerance
    claim_gate = artifact_gate and token_gate and word_ratio <= args.competitive_margin and char_ratio <= args.competitive_margin
    best_adapted = sorted([row for row in summary_rows if row["model_family"] == "adapted_8k"], key=lambda row: float(row["continued_final_loss"]))[0]

    score_rows = [
        {
            "run_id": run_id,
            "gate_id": "G01_required_runs",
            "criterion": "all 8k adapted and original-control continuation runs complete",
            "observed": f"summary_rows={completed}/6; normalized_rows={len(metric_rows)}/6",
            "required": "6/6 and 6/6",
            "status": "PASS" if artifact_gate else "FAIL",
            "return_to": "25_v2_8k_continued_budget_probe",
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
            "notes": "Step24 sources, train text, and Mark/dev text only",
        },
        {
            "run_id": run_id,
            "gate_id": "G03_token_budget_match",
            "criterion": "total and continued token budgets match across families/seeds",
            "observed": f"total_ratio={token_ratio:.6f}; continued_ratio={continued_ratio:.6f}; min_total={min(total_tokens)}; max_total={max(total_tokens)}",
            "required": f"ratios<={args.token_budget_tolerance:.6f}",
            "status": "PASS" if token_gate else "FAIL",
            "return_to": "25_v2_8k_continued_budget_probe",
            "notes": "approximately 1M total train tokens per run",
        },
        {
            "run_id": run_id,
            "gate_id": "G04_adapted_continues_improving",
            "criterion": "8k adapted branch improves over its 500k source checkpoint in every seed",
            "observed": f"{adapted_improved}/3",
            "required": "3/3",
            "status": "PASS" if adapted_improved == 3 else "FAIL",
            "return_to": "25_v2_8k_continued_budget_probe",
            "notes": "source checkpoint re-evaluated before continuation",
        },
        {
            "run_id": run_id,
            "gate_id": "G05_raw_control_context",
            "criterion": "raw 1M-ish 8k/original ratio recorded",
            "observed": f"ratio={raw_ratio:.6f}; adapted_mean={adapted_mean:.6f}; original_mean={original_mean:.6f}",
            "required": "recorded",
            "status": "PASS",
            "return_to": "NOT_APPLICABLE",
            "notes": "raw token losses are diagnostic across tokenizers",
        },
        {
            "run_id": run_id,
            "gate_id": "G06_word_normalized_competitive",
            "criterion": "continued 8k estimated NLL per word is within original-control margin",
            "observed": f"ratio={word_ratio:.6f}; adapted_mean={adapted_word:.6f}; original_mean={original_word:.6f}",
            "required": f"ratio<={args.competitive_margin:.6f}",
            "status": "PASS" if word_ratio <= args.competitive_margin else "FAIL",
            "return_to": "objective_or_data_redesign",
            "notes": "Step16-style normalized diagnostic",
        },
        {
            "run_id": run_id,
            "gate_id": "G07_char_normalized_competitive",
            "criterion": "continued 8k estimated NLL per character is within original-control margin",
            "observed": f"ratio={char_ratio:.6f}; adapted_mean={adapted_char:.6f}; original_mean={original_char:.6f}",
            "required": f"ratio<={args.competitive_margin:.6f}",
            "status": "PASS" if char_ratio <= args.competitive_margin else "FAIL",
            "return_to": "objective_or_data_redesign",
            "notes": "Step16-style normalized diagnostic",
        },
        {
            "run_id": run_id,
            "gate_id": "G08_checkpoint_selection",
            "criterion": "best continued 8k checkpoint selected on Mark/dev only",
            "observed": best_adapted["checkpoint_path"],
            "required": "one selected checkpoint",
            "status": "PASS",
            "return_to": "25_v2_8k_continued_budget_probe",
            "notes": f"seed={best_adapted['seed']}; continued_final_loss={best_adapted['continued_final_loss']}",
        },
    ]

    score_path = step_dir / "score_table.tsv"
    summary_path = step_dir / "continued_budget_summary.tsv"
    curve_path = step_dir / "continued_budget_curves.tsv"
    metrics_path = step_dir / "normalized_mlm_scores.tsv"
    selected_path = step_dir / "checkpoint_selection.md"
    access_path = step_dir / "v2_no_final_access_audit.tsv"
    results_path = step_dir / "results.md"
    file_results_path = step_dir / "file_results.tsv"

    write_tsv(score_path, score_rows, SCORE_FIELDS)
    write_tsv(summary_path, summary_rows, SUMMARY_FIELDS)
    write_tsv(curve_path, curve_rows, CURVE_FIELDS)
    write_tsv(metrics_path, metric_rows, METRIC_FIELDS)
    selected_path.write_text(
        f"""# Step 25 Continued-Budget Selection

Run id: `{run_id}`

Probe gate status: `{'PASS' if claim_gate else 'FAIL'}`

Selected continued 8k checkpoint: `{best_adapted['checkpoint_path']}`

Selected seed: `{best_adapted['seed']}`

8k continued mean loss: `{adapted_mean:.6f}`

Original-control continued mean loss: `{original_mean:.6f}`

Raw ratio: `{raw_ratio:.6f}`

Word-normalized ratio: `{word_ratio:.6f}`

Char-normalized ratio: `{char_ratio:.6f}`

Selection data: `MAR` dev only.

Final data access: `NO_ACT_FINAL_ACCESS`.
""",
        encoding="utf-8",
    )
    access_rows = [
        {
            "run_id": run_id,
            "input_role": "step24_raw_summary",
            "path": str(Path(args.step24_raw_summary).resolve()),
            "allowed_split": "prior_train_dev_result",
            "rows_or_files": str(count_rows(Path(args.step24_raw_summary))),
            "md5": md5_file(Path(args.step24_raw_summary)),
            "final_access": "NO",
            "status": "PASS",
        },
        {
            "run_id": run_id,
            "input_role": "train_text",
            "path": str(Path(args.train_text).resolve()),
            "allowed_split": "train",
            "rows_or_files": str(count_rows(Path(args.train_text))),
            "md5": md5_file(Path(args.train_text)),
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
        f"""# Step 25 Results: V2 8k Continued-Budget Probe

Status: COMPLETED

Run id: {run_id}

Completed date: {datetime.now().strftime('%Y-%m-%d')}

Artifact gate status: {'PASS' if artifact_gate and token_gate else 'FAIL'}

Probe gate status: {'PASS' if claim_gate else 'FAIL'}

## Summary

Step 25 continues the Step24 8k adapted and original-control checkpoints for an additional 500k train tokens, producing approximately 1M total train tokens per run. This is a fresh-optimizer continuation probe, not a final from-scratch 1M-token control. It uses train text and Mark/dev only. ACT final was not read.

| Metric | 8k Adapted Mean | Original Mean | Ratio |
| --- | ---: | ---: | ---: |
| continued final dev loss | {adapted_mean:.6f} +/- {adapted_std:.6f} | {original_mean:.6f} +/- {original_std:.6f} | {raw_ratio:.6f} |
| estimated NLL per word | {adapted_word:.6f} +/- {adapted_word_std:.6f} | {original_word:.6f} +/- {original_word_std:.6f} | {word_ratio:.6f} |
| estimated NLL per char | {adapted_char:.6f} +/- {adapted_char_std:.6f} | {original_char:.6f} +/- {original_char_std:.6f} | {char_ratio:.6f} |

## Interpretation

If the probe gate passes, open a formal from-scratch 1M-token control rerun before downstream or translation final readout. If it fails, longer 8k MLM alone does not rescue the model-dependent claim.

## Failure Return

Failed gate: {'NOT_APPLICABLE' if claim_gate else 'continued_budget_competitive_gate'}

Observed evidence: {'NOT_APPLICABLE' if claim_gate else f'word_ratio={word_ratio:.6f}, char_ratio={char_ratio:.6f}'}

Return-to step: {'formal_1M_control_rerun' if claim_gate else 'objective_or_data_redesign'}

Required fix: {'rerun from scratch with matched 1M budget' if claim_gate else 'redesign objective/data or downgrade model-dependent claim'}

Runtime minutes: {(time.time() - start) / 60.0:.3f}
""",
        encoding="utf-8",
    )

    file_rows = [
        file_result("score_table", score_path, "continued-budget gate table"),
        file_result("continued_budget_summary", summary_path, "per-family per-seed continuation summary"),
        file_result("continued_budget_curves", curve_path, "source/final continuation curves"),
        file_result("normalized_mlm_scores", metrics_path, "normalized Mark-dev MLM diagnostics"),
        file_result("checkpoint_selection", selected_path, "best continued 8k checkpoint"),
        file_result("no_final_access_audit", access_path, "input access audit"),
        file_result("results", results_path, "step result summary"),
    ]
    for checkpoint in checkpoint_dirs:
        file_rows.append(file_result("checkpoint_" + checkpoint.name, checkpoint, "continued-budget checkpoint"))
    write_tsv(file_results_path, file_rows, ["file_role", "path", "rows_or_files", "bytes", "md5", "status", "notes"])

    print(f"run_id={run_id}")
    print(f"artifact_gate_status={'PASS' if artifact_gate and token_gate else 'FAIL'}")
    print(f"probe_gate_status={'PASS' if claim_gate else 'FAIL'}")
    print(f"raw_ratio={raw_ratio:.6f}")
    print(f"word_ratio={word_ratio:.6f}")
    print(f"char_ratio={char_ratio:.6f}")


if __name__ == "__main__":
    main()
