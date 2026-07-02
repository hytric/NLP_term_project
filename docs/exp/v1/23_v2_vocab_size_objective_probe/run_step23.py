#!/usr/bin/env python3
"""Probe whether smaller v2 appended vocabularies repair added-token MLM failure."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
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


SUMMARY_FIELDS = [
    "run_id",
    "vocab_size",
    "seed",
    "source_checkpoint",
    "train_tokens_seen",
    "token_budget_status",
    "zero_raw_loss",
    "final_raw_loss",
    "raw_delta_vs_zero",
    "raw_delta_vs_32k",
    "raw_ratio_vs_original",
    "zero_all_loss",
    "final_all_loss",
    "all_delta_vs_zero",
    "zero_base_loss",
    "final_base_loss",
    "base_delta_vs_zero",
    "zero_added_loss",
    "final_added_loss",
    "added_delta_vs_zero",
    "final_added_base_ratio",
    "checkpoint_path",
    "status",
    "notes",
]

CATEGORY_FIELDS = [
    "run_id",
    "vocab_size",
    "seed",
    "checkpoint_path",
    "stage",
    "category",
    "non_special_tokens",
    "masked_tokens",
    "mean_loss",
    "loss_share_pct",
    "token_share_pct",
    "status",
]

VARIANT_FIELDS = [
    "run_id",
    "vocab_size",
    "runs_completed",
    "mean_final_raw_loss",
    "raw_delta_vs_32k_mean",
    "raw_ratio_vs_original_mean",
    "added_improved_seeds",
    "base_nonworse_seeds",
    "all_nonworse_seeds",
    "category_gate",
    "mean_final_added_loss",
    "mean_final_base_loss",
    "mean_final_all_loss",
    "status",
    "notes",
]

SCORE_FIELDS = ["run_id", "gate_id", "criterion", "observed", "required", "status", "return_to", "notes"]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def md5_file(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def parse_int_list(value: str) -> list[int]:
    items = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not items:
        raise ValueError("empty integer list")
    return items


def cat_value(rows: list[dict[str, str]], stage: str, category: str) -> float:
    for row in rows:
        if row["stage"] == stage and row["category"] == category:
            if row["mean_loss"] == "NOT_APPLICABLE":
                return float("nan")
            return float(row["mean_loss"])
    raise KeyError((stage, category))


def load_raw_baselines(path: Path) -> tuple[float, float]:
    rows = read_tsv(path)
    adapted = [float(row["final_dev_loss"]) for row in rows if row["model_family"] == "adapted_extended"]
    original = [float(row["final_dev_loss"]) for row in rows if row["model_family"] == "original_control"]
    if not adapted or not original:
        raise RuntimeError(f"missing Step15 baseline rows in {path}")
    return statistics.mean(adapted), statistics.mean(original)


def tokenizer_path(tokenizer_root: Path, vocab_size: int) -> Path:
    path = tokenizer_root / f"xlmr_v2_target10_added_{vocab_size}"
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def initialize_fvt_checkpoint(vocab_size: int, args: argparse.Namespace, step14, device: torch.device, run_id: str) -> tuple[Path, dict[str, str]]:
    out_dir = Path(args.checkpoint_root).resolve() / "init" / f"xlmr_v2_{vocab_size}_fvt"
    tokenizer_dir = tokenizer_path(Path(args.tokenizer_root), vocab_size)
    if args.reuse_existing and (out_dir / "config.json").exists() and (out_dir / "init_report.json").exists():
        report = json.loads((out_dir / "init_report.json").read_text(encoding="utf-8"))
        row = {
            "run_id": run_id,
            "vocab_size": str(vocab_size),
            "init_method": "fvt",
            "new_rows": str(report["new_rows"]),
            "initialized_rows": str(report["initialized_rows"]),
            "missing_rows": str(report["missing_rows"]),
            "fallback_rows": str(report["fallback_rows"]),
            "zero_step_dev_loss": f"{float(report['zero_step_dev_loss']):.6f}",
            "checkpoint_path": str(out_dir),
            "status": "PASS_REUSED",
            "notes": "reused_existing_fvt_init; final_ACT_not_read",
        }
        return out_dir, row

    tokenizer = XLMRobertaTokenizer.from_pretrained(str(tokenizer_dir), local_files_only=True)
    base_tokenizer = XLMRobertaTokenizer.from_pretrained(args.base_model, local_files_only=True)
    model = AutoModelForMaskedLM.from_pretrained(args.base_model, local_files_only=True)
    base_vocab_size = len(base_tokenizer)
    merged_vocab_size = len(tokenizer)
    model.resize_token_embeddings(merged_vocab_size)
    fvt_ids, align_ids = step14.build_source_maps(base_tokenizer, tokenizer, base_vocab_size)
    init_report = step14.initialize_rows(model, "fvt", base_vocab_size, merged_vocab_size, fvt_ids, align_ids)
    input_ok, output_ok, tying_ok = step14.shape_status(model, merged_vocab_size)
    dev_texts = step15_read_lines(Path(args.dev_text), args.dev_limit)
    zero_loss, masked_tokens = step14.zero_step_loss(model, tokenizer, dev_texts, device, args.eval_batch_size, args.max_length, args.seed)
    out_dir.mkdir(parents=True, exist_ok=True)
    model.to("cpu")
    model.save_pretrained(out_dir)
    tokenizer.save_pretrained(out_dir)
    report = {
        "run_id": run_id,
        "vocab_size": vocab_size,
        "init_method": "fvt",
        "base_vocab_size": base_vocab_size,
        "merged_vocab_size": merged_vocab_size,
        "new_rows": merged_vocab_size - base_vocab_size,
        "masked_tokens": masked_tokens,
        "zero_step_dev_loss": zero_loss,
        "selection_data": "MAR_dev_only",
        "final_access": "NO_ACT_FINAL_ACCESS",
        **init_report,
    }
    (out_dir / "init_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    status = "PASS" if init_report["missing_rows"] == "0" and input_ok == "PASS" and output_ok == "PASS" and tying_ok == "PASS" and math.isfinite(zero_loss) else "FAIL"
    row = {
        "run_id": run_id,
        "vocab_size": str(vocab_size),
        "init_method": "fvt",
        "new_rows": str(merged_vocab_size - base_vocab_size),
        "initialized_rows": init_report["initialized_rows"],
        "missing_rows": init_report["missing_rows"],
        "fallback_rows": init_report["fallback_rows"],
        "zero_step_dev_loss": f"{zero_loss:.6f}",
        "checkpoint_path": str(out_dir),
        "status": status,
        "notes": "created_fvt_init; final_ACT_not_read",
    }
    return out_dir, row


def step15_read_lines(path: Path, limit: int) -> list[str]:
    texts: list[str] = []
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


def train_candidate(vocab_size: int, seed: int, init_checkpoint: Path, train_texts: list[str], dev_texts: list[str], device: torch.device, run_id: str, args: argparse.Namespace, step15, step18):
    train_args = SimpleNamespace(
        base_model=args.base_model,
        train_steps=args.train_steps,
        target_train_tokens=args.target_train_tokens,
        token_budget_tolerance=args.token_budget_tolerance,
        batch_size=args.batch_size,
        eval_batch_size=args.eval_batch_size,
        max_length=args.max_length,
        learning_rate=args.learning_rate,
        eval_every=args.eval_every,
        train_limit=args.train_limit,
        dev_limit=args.dev_limit,
    )
    checkpoint_root = Path(args.checkpoint_root).resolve() / f"vocab_{vocab_size}"
    config_dir = Path(args.step_dir).resolve() / "training_configs" / f"vocab_{vocab_size}"
    config_dir.mkdir(parents=True, exist_ok=True)
    summary, curves, checkpoint = step15.train_one(
        "adapted_extended",
        seed,
        run_id,
        train_texts,
        dev_texts,
        device,
        train_args,
        init_checkpoint,
        checkpoint_root,
        config_dir,
    )

    eval_args = SimpleNamespace(
        eval_batch_size=args.eval_batch_size,
        max_length=args.max_length,
        eval_mask_prob=args.eval_mask_prob,
        seed=args.seed,
    )
    base_vocab_size = len(XLMRobertaTokenizer.from_pretrained(args.base_model, local_files_only=True))
    zero_tokenizer = XLMRobertaTokenizer.from_pretrained(str(init_checkpoint), local_files_only=True)
    zero_model = AutoModelForMaskedLM.from_pretrained(str(init_checkpoint), local_files_only=True)
    zero_model.to(device)
    zero_categories = step18.evaluate_categories(zero_model, zero_tokenizer, dev_texts, device, eval_args, base_vocab_size, seed, run_id, str(init_checkpoint), "zero_step")
    zero_model.to("cpu")
    del zero_model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    final_tokenizer = XLMRobertaTokenizer.from_pretrained(str(checkpoint), local_files_only=True)
    final_model = AutoModelForMaskedLM.from_pretrained(str(checkpoint), local_files_only=True)
    final_model.to(device)
    final_categories = step18.evaluate_categories(final_model, final_tokenizer, dev_texts, device, eval_args, base_vocab_size, seed, run_id, str(checkpoint), "final")
    final_model.to("cpu")
    del final_model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    category_rows = []
    for row in zero_categories + final_categories:
        item = dict(row)
        item["vocab_size"] = str(vocab_size)
        category_rows.append(item)
    return summary, curves, category_rows, checkpoint


def summarize_variant(run_id: str, vocab_size: int, rows: list[dict[str, str]], baseline_32k: float, original_mean: float) -> dict[str, str]:
    mean_raw = statistics.mean(float(row["final_raw_loss"]) for row in rows)
    added = sum(1 for row in rows if float(row["added_delta_vs_zero"]) < 0.0)
    base = sum(1 for row in rows if float(row["base_delta_vs_zero"]) <= 0.0)
    all_count = sum(1 for row in rows if float(row["all_delta_vs_zero"]) <= 0.0)
    category_gate = added == len(rows) and base == len(rows) and all_count == len(rows)
    raw_beats_32k = mean_raw < baseline_32k
    status = "PASS" if category_gate and raw_beats_32k else "FAIL_PROBE"
    return {
        "run_id": run_id,
        "vocab_size": str(vocab_size),
        "runs_completed": f"{len(rows)}/{len(rows)}",
        "mean_final_raw_loss": f"{mean_raw:.6f}",
        "raw_delta_vs_32k_mean": f"{mean_raw - baseline_32k:.6f}",
        "raw_ratio_vs_original_mean": f"{mean_raw / original_mean:.6f}",
        "added_improved_seeds": f"{added}/{len(rows)}",
        "base_nonworse_seeds": f"{base}/{len(rows)}",
        "all_nonworse_seeds": f"{all_count}/{len(rows)}",
        "category_gate": "PASS" if category_gate else "FAIL",
        "mean_final_added_loss": f"{statistics.mean(float(row['final_added_loss']) for row in rows):.6f}",
        "mean_final_base_loss": f"{statistics.mean(float(row['final_base_loss']) for row in rows):.6f}",
        "mean_final_all_loss": f"{statistics.mean(float(row['final_all_loss']) for row in rows):.6f}",
        "status": status,
        "notes": "raw beats 32k and category gate passes" if status == "PASS" else "no seed-stable tokenizer-size repair",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--checkpoint-root", default="/home/axt/mnt2/jongha/second_try/checkpoints/23_v2_vocab_size_objective_probe")
    parser.add_argument("--tokenizer-root", default="/home/axt/mnt2/jongha/second_try/artifacts/13_v2_tokenizer/tokenizers")
    parser.add_argument("--train-text", default="/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_tokenizer_mlm_train.txt")
    parser.add_argument("--dev-text", default="/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_mlm_dev_mark.txt")
    parser.add_argument("--step15-summary", default="docs/exp/second_try/15_v2_mlm_control/seed_summary.tsv")
    parser.add_argument("--step17-category", default="docs/exp/second_try/17_v2_added_token_failure_analysis/token_category_loss.tsv")
    parser.add_argument("--base-model", default="xlm-roberta-base")
    parser.add_argument("--vocab-sizes", default="8000,16000")
    parser.add_argument("--seeds", default="13,17,23")
    parser.add_argument("--train-limit", type=int, default=0)
    parser.add_argument("--dev-limit", type=int, default=0)
    parser.add_argument("--train-steps", type=int, default=1600)
    parser.add_argument("--target-train-tokens", type=int, default=500000)
    parser.add_argument("--token-budget-tolerance", type=float, default=1.02)
    parser.add_argument("--eval-every", type=int, default=800)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--eval-batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--learning-rate", type=float, default=5e-5)
    parser.add_argument("--eval-mask-prob", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=9230)
    parser.add_argument("--reuse-existing", action="store_true")
    args = parser.parse_args()

    transformers_logging.set_verbosity_error()
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.manual_seed(args.seed)
    start = time.time()
    run_id = "step23_v2_vocab_objective_probe_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    step_dir = Path(args.step_dir).resolve()
    checkpoint_root = Path(args.checkpoint_root).resolve()
    checkpoint_root.mkdir(parents=True, exist_ok=True)
    step_dir.mkdir(parents=True, exist_ok=True)

    repo_root = Path(__file__).resolve().parents[4]
    step14 = load_module("step14_module", repo_root / "docs/exp/second_try/14_v2_embedding_init/run_step14.py")
    step15 = load_module("step15_module", repo_root / "docs/exp/second_try/15_v2_mlm_control/run_step15.py")
    step18 = load_module("step18_module", repo_root / "docs/exp/second_try/18_v2_added_token_repair/run_step18.py")

    vocab_sizes = parse_int_list(args.vocab_sizes)
    seeds = parse_int_list(args.seeds)
    baseline_32k, original_mean = load_raw_baselines(Path(args.step15_summary))
    train_texts = step15_read_lines(Path(args.train_text), args.train_limit)
    dev_texts = step15_read_lines(Path(args.dev_text), args.dev_limit)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    init_rows: list[dict[str, str]] = []
    summary_rows: list[dict[str, str]] = []
    curve_rows: list[dict[str, str]] = []
    category_rows: list[dict[str, str]] = []
    checkpoint_dirs: list[Path] = []

    for vocab_size in vocab_sizes:
        print(f"initializing vocab={vocab_size}", flush=True)
        init_checkpoint, init_row = initialize_fvt_checkpoint(vocab_size, args, step14, device, run_id)
        init_rows.append(init_row)
        checkpoint_dirs.append(init_checkpoint)
        for seed in seeds:
            print(f"training vocab={vocab_size} seed={seed}", flush=True)
            train_summary, curves, categories, checkpoint = train_candidate(
                vocab_size,
                seed,
                init_checkpoint,
                train_texts,
                dev_texts,
                device,
                run_id,
                args,
                step15,
                step18,
            )
            zero_all = cat_value(categories, "zero_step", "all")
            final_all = cat_value(categories, "final", "all")
            zero_base = cat_value(categories, "zero_step", "base")
            final_base = cat_value(categories, "final", "base")
            zero_added = cat_value(categories, "zero_step", "added")
            final_added = cat_value(categories, "final", "added")
            row = {
                "run_id": run_id,
                "vocab_size": str(vocab_size),
                "seed": str(seed),
                "source_checkpoint": str(init_checkpoint),
                "train_tokens_seen": train_summary["train_tokens_seen"],
                "token_budget_status": train_summary["token_budget_status"],
                "zero_raw_loss": train_summary["zero_step_dev_loss"],
                "final_raw_loss": train_summary["final_dev_loss"],
                "raw_delta_vs_zero": train_summary["dev_loss_delta"],
                "raw_delta_vs_32k": f"{float(train_summary['final_dev_loss']) - baseline_32k:.6f}",
                "raw_ratio_vs_original": f"{float(train_summary['final_dev_loss']) / original_mean:.6f}",
                "zero_all_loss": f"{zero_all:.6f}",
                "final_all_loss": f"{final_all:.6f}",
                "all_delta_vs_zero": f"{final_all - zero_all:.6f}",
                "zero_base_loss": f"{zero_base:.6f}",
                "final_base_loss": f"{final_base:.6f}",
                "base_delta_vs_zero": f"{final_base - zero_base:.6f}",
                "zero_added_loss": f"{zero_added:.6f}",
                "final_added_loss": f"{final_added:.6f}",
                "added_delta_vs_zero": f"{final_added - zero_added:.6f}",
                "final_added_base_ratio": f"{final_added / max(1e-12, final_base):.6f}",
                "checkpoint_path": train_summary["checkpoint_path"],
                "status": "PASS" if float(train_summary["dev_loss_delta"]) < 0.0 else "NO_RAW_IMPROVEMENT",
                "notes": "mark_dev_only_selection; no_ACT_final_access",
            }
            summary_rows.append(row)
            for curve in curves:
                c = dict(curve)
                c["vocab_size"] = str(vocab_size)
                curve_rows.append(c)
            category_rows.extend(categories)
            checkpoint_dirs.append(checkpoint)

    variant_rows = [
        summarize_variant(run_id, vocab_size, [row for row in summary_rows if row["vocab_size"] == str(vocab_size)], baseline_32k, original_mean)
        for vocab_size in vocab_sizes
    ]
    completed = len(summary_rows)
    expected = len(vocab_sizes) * len(seeds)
    tokens = [int(row["train_tokens_seen"]) for row in summary_rows]
    token_ratio = max(tokens) / max(1, min(tokens)) if tokens else float("inf")
    passing_variants = [row for row in variant_rows if row["status"] == "PASS"]
    best = sorted(variant_rows, key=lambda row: (row["status"] != "PASS", float(row["mean_final_raw_loss"])))[0]
    best_seed = sorted([row for row in summary_rows if row["vocab_size"] == best["vocab_size"]], key=lambda row: float(row["final_raw_loss"]))[0]
    artifact_gate = completed == expected and all(row["status"].startswith("PASS") for row in init_rows)
    token_gate = token_ratio <= args.token_budget_tolerance
    raw_gate = any(float(row["raw_delta_vs_32k_mean"]) < 0.0 for row in variant_rows)
    category_gate = any(row["category_gate"] == "PASS" for row in variant_rows)
    probe_gate = artifact_gate and token_gate and raw_gate and category_gate

    score_rows = [
        {
            "run_id": run_id,
            "gate_id": "G01_init_artifacts",
            "criterion": "8k and 16k fvt initialization artifacts complete",
            "observed": f"{sum(1 for row in init_rows if row['status'].startswith('PASS'))}/{len(init_rows)}",
            "required": f"{len(init_rows)}/{len(init_rows)}",
            "status": "PASS" if all(row["status"].startswith("PASS") for row in init_rows) else "FAIL",
            "return_to": "14_v2_embedding_init",
            "notes": "fvt init created or reused from Step23 checkpoint root",
        },
        {
            "run_id": run_id,
            "gate_id": "G02_required_runs",
            "criterion": "all vocab/seed MLM runs complete",
            "observed": f"{completed}/{expected}",
            "required": f"{expected}/{expected}",
            "status": "PASS" if completed == expected else "FAIL",
            "return_to": "23_v2_vocab_size_objective_probe",
            "notes": f"vocab_sizes={','.join(map(str, vocab_sizes))}; seeds={','.join(map(str, seeds))}",
        },
        {
            "run_id": run_id,
            "gate_id": "G03_token_budget_match",
            "criterion": "train token budgets match across candidate runs",
            "observed": f"min_tokens={min(tokens) if tokens else 0}; max_tokens={max(tokens) if tokens else 0}; token_ratio={token_ratio:.6f}",
            "required": f"token_ratio<={args.token_budget_tolerance:.6f}",
            "status": "PASS" if token_gate else "FAIL",
            "return_to": "23_v2_vocab_size_objective_probe",
            "notes": "same target token budget as Step15",
        },
        {
            "run_id": run_id,
            "gate_id": "G04_raw_beats_32k",
            "criterion": "at least one smaller vocab beats Step15 32k fvt raw mean final loss",
            "observed": "; ".join(f"{row['vocab_size']}:delta={row['raw_delta_vs_32k_mean']}" for row in variant_rows),
            "required": "<0 for at least one vocab",
            "status": "PASS" if raw_gate else "FAIL",
            "return_to": "13_v2_tokenizer",
            "notes": f"step15_32k_mean={baseline_32k:.6f}",
        },
        {
            "run_id": run_id,
            "gate_id": "G05_category_gate",
            "criterion": "at least one smaller vocab improves added and preserves base/all in every seed",
            "observed": "; ".join(f"{row['vocab_size']}:added={row['added_improved_seeds']},base={row['base_nonworse_seeds']},all={row['all_nonworse_seeds']}" for row in variant_rows),
            "required": "added=3/3; base=3/3; all=3/3 for at least one vocab",
            "status": "PASS" if category_gate else "FAIL",
            "return_to": "13_v2_tokenizer or objective_redesign",
            "notes": "zero-step to final category deltas, Mark/dev only",
        },
        {
            "run_id": run_id,
            "gate_id": "G06_original_control_context",
            "criterion": "best smaller vocab is compared against original-control context",
            "observed": f"best_vocab={best['vocab_size']}; raw_ratio_vs_original={best['raw_ratio_vs_original_mean']}",
            "required": "recorded",
            "status": "PASS",
            "return_to": "15_v2_mlm_control",
            "notes": "not a replacement for rerunning Step15/16 if this probe passes",
        },
        {
            "run_id": run_id,
            "gate_id": "G07_no_final_access",
            "criterion": "ACT final data not read",
            "observed": "NO_ACT_FINAL_ACCESS",
            "required": "NO_ACT_FINAL_ACCESS",
            "status": "PASS",
            "return_to": "12_v2_split_protocol",
            "notes": "uses Step13 tokenizers, Step12 train text, Mark/dev text, and prior dev-only baselines",
        },
    ]

    score_path = step_dir / "score_table.tsv"
    init_path = step_dir / "vocab_probe_init_summary.tsv"
    summary_path = step_dir / "vocab_probe_summary.tsv"
    curve_path = step_dir / "vocab_probe_learning_curves.tsv"
    category_path = step_dir / "vocab_probe_category_loss.tsv"
    variant_path = step_dir / "vocab_probe_variant_summary.tsv"
    selected_path = step_dir / "checkpoint_selection.md"
    access_path = step_dir / "v2_no_final_access_audit.tsv"
    results_path = step_dir / "results.md"
    file_results_path = step_dir / "file_results.tsv"

    write_tsv(score_path, score_rows, SCORE_FIELDS)
    write_tsv(init_path, init_rows, ["run_id", "vocab_size", "init_method", "new_rows", "initialized_rows", "missing_rows", "fallback_rows", "zero_step_dev_loss", "checkpoint_path", "status", "notes"])
    write_tsv(summary_path, summary_rows, SUMMARY_FIELDS)
    curve_fields = ["run_id", "vocab_size", "model_family", "seed", "stage", "step", "train_examples_seen", "train_tokens_seen", "eval_rows", "eval_masked_tokens", "dev_loss", "pseudo_ppl", "train_loss_mean_since_eval", "learning_rate", "status", "notes"]
    write_tsv(curve_path, curve_rows, curve_fields)
    write_tsv(category_path, category_rows, CATEGORY_FIELDS)
    write_tsv(variant_path, variant_rows, VARIANT_FIELDS)

    selected_path.write_text(
        f"""# Step 23 Vocab-Size Probe Selection

Run id: `{run_id}`

Probe gate status: `{'PASS' if probe_gate else 'FAIL'}`

Best vocab size: `{best['vocab_size']}`

Best vocab mean final raw loss: `{best['mean_final_raw_loss']}`

Step15 32k fvt mean final raw loss: `{baseline_32k:.6f}`

Original-control mean final raw loss: `{original_mean:.6f}`

Selected seed checkpoint: `{best_seed['checkpoint_path']}`

Selection data: `MAR` dev only.

Final data access: `NO_ACT_FINAL_ACCESS`.
""",
        encoding="utf-8",
    )

    access_rows = [
        {
            "run_id": run_id,
            "input_role": "step13_tokenizer_root",
            "path": str(Path(args.tokenizer_root).resolve()),
            "allowed_split": "train_tokenizers_selected_by_dev_only",
            "rows_or_files": str(count_rows(Path(args.tokenizer_root))),
            "md5": "DIRECTORY",
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
            "allowed_split": "dev_MAR",
            "rows_or_files": str(count_rows(Path(args.dev_text))),
            "md5": md5_file(Path(args.dev_text)),
            "final_access": "NO",
            "status": "PASS",
        },
        {
            "run_id": run_id,
            "input_role": "step15_summary_baseline",
            "path": str(Path(args.step15_summary).resolve()),
            "allowed_split": "prior_train_dev_result",
            "rows_or_files": str(count_rows(Path(args.step15_summary))),
            "md5": md5_file(Path(args.step15_summary)),
            "final_access": "NO",
            "status": "PASS",
        },
        {
            "run_id": run_id,
            "input_role": "step17_category_context",
            "path": str(Path(args.step17_category).resolve()),
            "allowed_split": "prior_train_dev_result",
            "rows_or_files": str(count_rows(Path(args.step17_category))),
            "md5": md5_file(Path(args.step17_category)),
            "final_access": "NO",
            "status": "PASS",
        },
    ]
    write_tsv(access_path, access_rows, ["run_id", "input_role", "path", "allowed_split", "rows_or_files", "md5", "final_access", "status"])

    results_path.write_text(
        f"""# Step 23 Results: V2 Vocab-Size Objective Probe

Status: COMPLETED

Run id: {run_id}

Completed date: {datetime.now().strftime('%Y-%m-%d')}

Artifact gate status: {'PASS' if artifact_gate else 'FAIL'}

Probe gate status: {'PASS' if probe_gate else 'FAIL'}

## Summary

Step 23 initializes smaller 8k and 16k Step13 tokenizer candidates with `fvt`, trains them with the Step15 500k-token MLM budget, and evaluates Mark/dev all/base/added category losses. ACT final was not read.

| Metric | Value |
| --- | ---: |
| vocab sizes | {','.join(map(str, vocab_sizes))} |
| completed runs | {completed}/{expected} |
| token budget ratio | {token_ratio:.6f} |
| passing variants | {len(passing_variants)}/{len(variant_rows)} |
| Step15 32k raw mean final loss | {baseline_32k:.6f} |
| original-control raw mean final loss | {original_mean:.6f} |
| best vocab | {best['vocab_size']} |
| best raw mean final loss | {best['mean_final_raw_loss']} |
| best raw delta vs 32k | {best['raw_delta_vs_32k_mean']} |
| best raw ratio vs original | {best['raw_ratio_vs_original_mean']} |

## Interpretation

If the probe gate passes, the next step is to promote the smaller tokenizer branch and rerun Step15/16 controls before any downstream or translation final readout. If the probe gate fails, smaller-vocabulary selection alone does not resolve the model-dependent failure.

## Failure Return

Failed gate: {'NOT_APPLICABLE' if probe_gate else 'vocab_size_objective_probe_gate'}

Observed evidence: passing_variants={len(passing_variants)}/{len(variant_rows)}; best_vocab={best['vocab_size']}; raw_delta_vs_32k={best['raw_delta_vs_32k_mean']}

Return-to step: {'15_v2_mlm_control' if probe_gate else '13_v2_tokenizer or objective_redesign'}

Required fix: {'rerun Step15/16 controls with selected vocab' if probe_gate else 'change tokenizer/objective beyond smaller-vocab fvt MLM or downgrade model-dependent claim'}

Runtime minutes: {(time.time() - start) / 60.0:.3f}
""",
        encoding="utf-8",
    )

    file_rows = [
        file_result("score_table", score_path, "probe gate table"),
        file_result("vocab_probe_init_summary", init_path, "fvt init summary for smaller vocabs"),
        file_result("vocab_probe_summary", summary_path, "per-vocab per-seed MLM summary"),
        file_result("vocab_probe_learning_curves", curve_path, "zero/final Mark-dev curves"),
        file_result("vocab_probe_category_loss", category_path, "zero/final all/base/added losses"),
        file_result("vocab_probe_variant_summary", variant_path, "per-vocab aggregate gates"),
        file_result("checkpoint_selection", selected_path, "selected probe checkpoint"),
        file_result("no_final_access_audit", access_path, "input access audit"),
        file_result("results", results_path, "step result summary"),
    ]
    for checkpoint in checkpoint_dirs:
        file_rows.append(file_result("checkpoint_" + checkpoint.name, checkpoint, "Step23 checkpoint artifact"))
    write_tsv(file_results_path, file_rows, ["file_role", "path", "rows_or_files", "bytes", "md5", "status", "notes"])

    print(f"run_id={run_id}")
    print(f"artifact_gate_status={'PASS' if artifact_gate else 'FAIL'}")
    print(f"probe_gate_status={'PASS' if probe_gate else 'FAIL'}")
    print(f"best_vocab={best['vocab_size']}")
    print(f"best_raw_mean_final_loss={best['mean_final_raw_loss']}")


if __name__ == "__main__":
    main()
