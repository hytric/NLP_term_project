#!/usr/bin/env python3
"""Probe whether non-fvt Step14 initializations repair v2 MLM failure."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
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

from transformers import AutoModelForMaskedLM, XLMRobertaTokenizer, logging as transformers_logging


STEP15_PATH = Path(__file__).resolve().parents[1] / "15_v2_mlm_control" / "run_step15.py"
STEP18_PATH = Path(__file__).resolve().parents[1] / "18_v2_added_token_repair" / "run_step18.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


step15 = load_module("step15_utils", STEP15_PATH)
step18 = load_module("step18_utils", STEP18_PATH)


SCORE_FIELDS = ["run_id", "gate_id", "criterion", "observed", "required", "status", "return_to", "notes"]
SUMMARY_FIELDS = [
    "run_id",
    "init_method",
    "seed",
    "source_checkpoint",
    "train_steps",
    "actual_train_steps",
    "target_train_tokens",
    "batch_size",
    "max_length",
    "learning_rate",
    "train_rows_available",
    "train_examples_seen",
    "train_tokens_seen",
    "token_budget_status",
    "zero_step_dev_loss",
    "final_dev_loss",
    "dev_loss_delta",
    "relative_loss_delta_pct",
    "mean_train_loss",
    "runtime_minutes",
    "tokens_per_sec",
    "checkpoint_path",
    "status",
    "notes",
]
CURVE_FIELDS = [
    "run_id",
    "init_method",
    "seed",
    "stage",
    "step",
    "train_examples_seen",
    "train_tokens_seen",
    "eval_rows",
    "eval_masked_tokens",
    "dev_loss",
    "pseudo_ppl",
    "train_loss_mean_since_eval",
    "learning_rate",
    "status",
    "notes",
]
CATEGORY_FIELDS = [
    "run_id",
    "init_method",
    "probe_role",
    "seed",
    "checkpoint_path",
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
    "init_method",
    "completed",
    "raw_mean_final_loss",
    "raw_delta_vs_fvt_mean",
    "raw_ratio_vs_original_mean",
    "added_improved_vs_fvt",
    "base_nonworse_vs_fvt",
    "all_nonworse_vs_fvt",
    "mean_added_delta_vs_fvt",
    "mean_base_delta_vs_fvt",
    "mean_all_delta_vs_fvt",
    "status",
    "notes",
]


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    step18.write_tsv(path, rows, fieldnames)


def read_tsv(path: Path) -> list[dict[str, str]]:
    return step18.read_tsv(path)


def checkpoint_map_from_step14(path: Path) -> dict[str, Path]:
    out = {}
    for row in read_tsv(path):
        if row["status"] == "PASS":
            out[row["init_method"]] = Path(row["checkpoint_path"])
    return out


def fvt_baseline_rows(path: Path) -> tuple[list[dict[str, str]], list[dict[str, str]], float, float]:
    rows = read_tsv(path)
    adapted = [row for row in rows if row["model_family"] == "adapted_extended"]
    original = [row for row in rows if row["model_family"] == "original_control"]
    if len(adapted) < 3 or len(original) < 3:
        raise RuntimeError("Step15 summary must contain adapted and original rows")
    adapted_mean = statistics.mean(float(row["final_dev_loss"]) for row in adapted)
    original_mean = statistics.mean(float(row["final_dev_loss"]) for row in original)
    return adapted, original, adapted_mean, original_mean


def category_rows_for_checkpoint(run_id: str, init_method: str, probe_role: str, seed: int, checkpoint: Path, dev_texts: list[str], base_vocab_size: int, device: torch.device, args: argparse.Namespace) -> list[dict[str, str]]:
    tokenizer = XLMRobertaTokenizer.from_pretrained(str(checkpoint), local_files_only=True)
    model = AutoModelForMaskedLM.from_pretrained(str(checkpoint), local_files_only=True)
    model.to(device)
    raw_rows = step18.evaluate_categories(model, tokenizer, dev_texts, device, args, base_vocab_size, seed, run_id, str(checkpoint), "final")
    model.to("cpu")
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    rows = []
    for row in raw_rows:
        rows.append(
            {
                "run_id": run_id,
                "init_method": init_method,
                "probe_role": probe_role,
                "seed": str(seed),
                "checkpoint_path": row["checkpoint_path"],
                "category": row["category"],
                "non_special_tokens": row["non_special_tokens"],
                "masked_tokens": row["masked_tokens"],
                "mean_loss": row["mean_loss"],
                "loss_share_pct": row["loss_share_pct"],
                "token_share_pct": row["token_share_pct"],
                "status": row["status"],
            }
        )
    return rows


def category_value(rows: list[dict[str, str]], init_method: str, seed: str, category: str) -> float:
    for row in rows:
        if row["init_method"] == init_method and row["seed"] == seed and row["category"] == category:
            return float(row["mean_loss"])
    raise KeyError((init_method, seed, category))


def mean(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def summarize_method(run_id: str, method: str, method_rows: list[dict[str, str]], category_rows: list[dict[str, str]], seeds: list[int], fvt_raw_mean: float, original_raw_mean: float) -> dict[str, str]:
    raw_mean = statistics.mean(float(row["final_dev_loss"]) for row in method_rows)
    added_deltas = []
    base_deltas = []
    all_deltas = []
    for seed in seeds:
        seed_s = str(seed)
        added_deltas.append(category_value(category_rows, method, seed_s, "added") - category_value(category_rows, "fvt", seed_s, "added"))
        base_deltas.append(category_value(category_rows, method, seed_s, "base") - category_value(category_rows, "fvt", seed_s, "base"))
        all_deltas.append(category_value(category_rows, method, seed_s, "all") - category_value(category_rows, "fvt", seed_s, "all"))
    added_improved = sum(1 for value in added_deltas if value < 0.0)
    base_nonworse = sum(1 for value in base_deltas if value <= 0.0)
    all_nonworse = sum(1 for value in all_deltas if value <= 0.0)
    status = "PASS" if raw_mean <= fvt_raw_mean and added_improved == len(seeds) and base_nonworse == len(seeds) and all_nonworse == len(seeds) else "FAIL"
    return {
        "run_id": run_id,
        "init_method": method,
        "completed": f"{len(method_rows)}/{len(seeds)}",
        "raw_mean_final_loss": f"{raw_mean:.6f}",
        "raw_delta_vs_fvt_mean": f"{raw_mean - fvt_raw_mean:.6f}",
        "raw_ratio_vs_original_mean": f"{raw_mean / original_raw_mean:.6f}",
        "added_improved_vs_fvt": f"{added_improved}/{len(seeds)}",
        "base_nonworse_vs_fvt": f"{base_nonworse}/{len(seeds)}",
        "all_nonworse_vs_fvt": f"{all_nonworse}/{len(seeds)}",
        "mean_added_delta_vs_fvt": f"{mean(added_deltas):.6f}",
        "mean_base_delta_vs_fvt": f"{mean(base_deltas):.6f}",
        "mean_all_delta_vs_fvt": f"{mean(all_deltas):.6f}",
        "status": status,
        "notes": "passes only if raw mean and every category seed gate beat fvt",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--checkpoint-root", default="/home/axt/mnt2/jongha/second_try/checkpoints/21_v2_alt_init_mlm_probe")
    parser.add_argument("--step14-scores", default="docs/exp/second_try/14_v2_embedding_init/v2_embedding_init_scores.tsv")
    parser.add_argument("--step15-summary", default="docs/exp/second_try/15_v2_mlm_control/seed_summary.tsv")
    parser.add_argument("--train-text", default="/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_tokenizer_mlm_train.txt")
    parser.add_argument("--dev-text", default="/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_mlm_dev_mark.txt")
    parser.add_argument("--base-model", default="xlm-roberta-base")
    parser.add_argument("--init-methods", default="mean,align")
    parser.add_argument("--seeds", default="13,17,23")
    parser.add_argument("--train-limit", type=int, default=0)
    parser.add_argument("--dev-limit", type=int, default=0)
    parser.add_argument("--train-steps", type=int, default=1800)
    parser.add_argument("--target-train-tokens", type=int, default=500000)
    parser.add_argument("--token-budget-tolerance", type=float, default=1.02)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--eval-batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--learning-rate", type=float, default=5e-5)
    parser.add_argument("--eval-every", type=int, default=800)
    parser.add_argument("--eval-mask-prob", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=21021)
    args = parser.parse_args()

    transformers_logging.set_verbosity_error()
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    torch.backends.cuda.matmul.allow_tf32 = True
    start = time.time()
    run_id = "step21_v2_alt_init_probe_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    step_dir = Path(args.step_dir).resolve()
    checkpoint_root = Path(args.checkpoint_root).resolve()
    checkpoint_root.mkdir(parents=True, exist_ok=True)
    config_root = step_dir / "training_configs"
    config_root.mkdir(parents=True, exist_ok=True)

    methods = [item.strip() for item in args.init_methods.split(",") if item.strip()]
    seeds = [int(item.strip()) for item in args.seeds.split(",") if item.strip()]
    if len(seeds) < 3:
        raise ValueError("Step21 requires at least three seeds")
    step14_map = checkpoint_map_from_step14(Path(args.step14_scores))
    for method in methods:
        if method not in step14_map:
            raise RuntimeError(f"missing Step14 checkpoint for init method {method}")
    fvt_rows, original_rows, fvt_raw_mean, original_raw_mean = fvt_baseline_rows(Path(args.step15_summary))
    fvt_by_seed = {row["seed"]: Path(row["checkpoint_path"]) for row in fvt_rows}
    train_texts = step15.read_lines(Path(args.train_text), args.train_limit)
    dev_texts = step15.read_lines(Path(args.dev_text), args.dev_limit)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    base_vocab_size = len(XLMRobertaTokenizer.from_pretrained(args.base_model, local_files_only=True))

    common_config = {
        "run_id": run_id,
        "methods": methods,
        "seeds": seeds,
        "train_text": str(Path(args.train_text).resolve()),
        "dev_text": str(Path(args.dev_text).resolve()),
        "train_rows_loaded": len(train_texts),
        "dev_rows_loaded": len(dev_texts),
        "target_train_tokens": args.target_train_tokens,
        "selection_data": "MAR_dev_only",
        "final_access": "NO_ACT_FINAL_ACCESS",
    }
    (config_root / "common_config.json").write_text(json.dumps(common_config, ensure_ascii=False, indent=2), encoding="utf-8")

    summary_rows: list[dict[str, str]] = []
    curve_rows: list[dict[str, str]] = []
    checkpoint_dirs: list[Path] = []
    for method in methods:
        method_checkpoint_root = checkpoint_root / method
        method_config_dir = config_root / method
        method_config_dir.mkdir(parents=True, exist_ok=True)
        for seed in seeds:
            print(f"training init_method={method} seed={seed}", flush=True)
            summary, curves, checkpoint_dir = step15.train_one(
                "adapted_extended",
                seed,
                run_id,
                train_texts,
                dev_texts,
                device,
                args,
                step14_map[method],
                method_checkpoint_root,
                method_config_dir,
            )
            summary = {
                "run_id": run_id,
                "init_method": method,
                "seed": summary["seed"],
                "source_checkpoint": summary["source_checkpoint"],
                "train_steps": summary["train_steps"],
                "actual_train_steps": summary["actual_train_steps"],
                "target_train_tokens": summary["target_train_tokens"],
                "batch_size": summary["batch_size"],
                "max_length": summary["max_length"],
                "learning_rate": summary["learning_rate"],
                "train_rows_available": summary["train_rows_available"],
                "train_examples_seen": summary["train_examples_seen"],
                "train_tokens_seen": summary["train_tokens_seen"],
                "token_budget_status": summary["token_budget_status"],
                "zero_step_dev_loss": summary["zero_step_dev_loss"],
                "final_dev_loss": summary["final_dev_loss"],
                "dev_loss_delta": summary["dev_loss_delta"],
                "relative_loss_delta_pct": summary["relative_loss_delta_pct"],
                "mean_train_loss": summary["mean_train_loss"],
                "runtime_minutes": summary["runtime_minutes"],
                "tokens_per_sec": summary["tokens_per_sec"],
                "checkpoint_path": summary["checkpoint_path"],
                "status": summary["status"],
                "notes": summary["notes"],
            }
            summary_rows.append(summary)
            for curve in curves:
                curve_rows.append(
                    {
                        "run_id": run_id,
                        "init_method": method,
                        "seed": curve["seed"],
                        "stage": curve["stage"],
                        "step": curve["step"],
                        "train_examples_seen": curve["train_examples_seen"],
                        "train_tokens_seen": curve["train_tokens_seen"],
                        "eval_rows": curve["eval_rows"],
                        "eval_masked_tokens": curve["eval_masked_tokens"],
                        "dev_loss": curve["dev_loss"],
                        "pseudo_ppl": curve["pseudo_ppl"],
                        "train_loss_mean_since_eval": curve["train_loss_mean_since_eval"],
                        "learning_rate": curve["learning_rate"],
                        "status": curve["status"],
                        "notes": curve["notes"],
                    }
                )
            checkpoint_dirs.append(checkpoint_dir)

    category_rows: list[dict[str, str]] = []
    for seed in seeds:
        category_rows.extend(category_rows_for_checkpoint(run_id, "fvt", "baseline_step15", seed, fvt_by_seed[str(seed)], dev_texts, base_vocab_size, device, args))
    for row in summary_rows:
        category_rows.extend(category_rows_for_checkpoint(run_id, row["init_method"], "alt_init_step21", int(row["seed"]), Path(row["checkpoint_path"]), dev_texts, base_vocab_size, device, args))

    variant_rows = []
    for method in methods:
        variant_rows.append(summarize_method(run_id, method, [row for row in summary_rows if row["init_method"] == method], category_rows, seeds, fvt_raw_mean, original_raw_mean))
    passing_methods = [row for row in variant_rows if row["status"] == "PASS"]
    completed = len(summary_rows)
    required = len(methods) * len(seeds)
    token_counts = [int(row["train_tokens_seen"]) for row in summary_rows]
    min_tokens = min(token_counts) if token_counts else 0
    max_tokens = max(token_counts) if token_counts else 0
    token_ratio = max_tokens / max(1, min_tokens)
    token_budget_matched = all(row["token_budget_status"] == "PASS" for row in summary_rows) and token_ratio <= args.token_budget_tolerance
    artifact_gate = completed == required and token_budget_matched
    probe_gate = artifact_gate and bool(passing_methods)
    best_method = sorted(variant_rows, key=lambda row: (row["status"] != "PASS", float(row["raw_mean_final_loss"])))[0]
    best_seed_row = sorted([row for row in summary_rows if row["init_method"] == best_method["init_method"]], key=lambda row: float(row["final_dev_loss"]))[0]

    score_rows = [
        {
            "run_id": run_id,
            "gate_id": "G01_required_runs",
            "criterion": "all alternative init/seed runs complete",
            "observed": f"{completed}/{required}",
            "required": f"{required}/{required}",
            "status": "PASS" if completed == required else "FAIL",
            "return_to": "21_v2_alt_init_mlm_probe",
            "notes": f"methods={','.join(methods)}",
        },
        {
            "run_id": run_id,
            "gate_id": "G02_no_final_access",
            "criterion": "ACT final data not read",
            "observed": "NO_ACT_FINAL_ACCESS",
            "required": "NO_ACT_FINAL_ACCESS",
            "status": "PASS",
            "return_to": "12_v2_split_protocol",
            "notes": "Step14 scores, Step15 summary, train text, and Mark/dev text only",
        },
        {
            "run_id": run_id,
            "gate_id": "G03_token_budget_match",
            "criterion": "alternative init runs use matched train token budget",
            "observed": f"min_tokens={min_tokens}; max_tokens={max_tokens}; token_ratio={token_ratio:.6f}; target={args.target_train_tokens}",
            "required": f"token_ratio<={args.token_budget_tolerance:.6f}",
            "status": "PASS" if token_budget_matched else "FAIL",
            "return_to": "21_v2_alt_init_mlm_probe",
            "notes": "same target token budget as Step15",
        },
        {
            "run_id": run_id,
            "gate_id": "G04_any_alt_init_beats_fvt",
            "criterion": "at least one alternative init beats fvt on raw mean and category seed gates",
            "observed": f"passing_methods={len(passing_methods)}/{len(methods)}",
            "required": ">=1",
            "status": "PASS" if passing_methods else "FAIL",
            "return_to": "14_v2_embedding_init",
            "notes": "; ".join(f"{row['init_method']}: raw_delta={row['raw_delta_vs_fvt_mean']}, added={row['added_improved_vs_fvt']}, base={row['base_nonworse_vs_fvt']}, all={row['all_nonworse_vs_fvt']}" for row in variant_rows),
        },
        {
            "run_id": run_id,
            "gate_id": "G05_original_control_context",
            "criterion": "best alternative raw mean remains compared to original-control context",
            "observed": f"best={best_method['init_method']}; raw_ratio_vs_original={best_method['raw_ratio_vs_original_mean']}",
            "required": "recorded",
            "status": "PASS",
            "return_to": "15_v2_mlm_control",
            "notes": "diagnostic because tokenizer vocabularies differ",
        },
        {
            "run_id": run_id,
            "gate_id": "G06_checkpoint_selection",
            "criterion": "best alternative init checkpoint selected on Mark/dev only",
            "observed": f"method={best_method['init_method']}; checkpoint={best_seed_row['checkpoint_path']}",
            "required": "one method and one checkpoint",
            "status": "PASS",
            "return_to": "21_v2_alt_init_mlm_probe",
            "notes": f"probe_gate={'PASS' if probe_gate else 'FAIL'}",
        },
    ]

    score_path = step_dir / "score_table.tsv"
    summary_path = step_dir / "init_probe_summary.tsv"
    curves_path = step_dir / "init_probe_learning_curves.tsv"
    category_path = step_dir / "init_probe_category_loss.tsv"
    variants_path = step_dir / "init_probe_variant_summary.tsv"
    selection_path = step_dir / "checkpoint_selection.md"
    access_path = step_dir / "v2_no_final_access_audit.tsv"
    results_path = step_dir / "results.md"
    file_results_path = step_dir / "file_results.tsv"

    write_tsv(score_path, score_rows, SCORE_FIELDS)
    write_tsv(summary_path, summary_rows, SUMMARY_FIELDS)
    write_tsv(curves_path, curve_rows, CURVE_FIELDS)
    write_tsv(category_path, category_rows, CATEGORY_FIELDS)
    write_tsv(variants_path, variant_rows, VARIANT_FIELDS)
    selection_path.write_text(
        f"""# Step 21 Checkpoint Selection

Run id: `{run_id}`

Selection data: `MAR` dev only.

Final data access: `NO_ACT_FINAL_ACCESS`.

Selected alternative init method: `{best_method['init_method']}`

Selected checkpoint: `{best_seed_row['checkpoint_path']}`

| Metric | Value |
| --- | --- |
| probe gate | `{'PASS' if probe_gate else 'FAIL'}` |
| passing methods | `{len(passing_methods)}/{len(methods)}` |
| fvt raw mean final loss | `{fvt_raw_mean:.6f}` |
| original-control raw mean final loss | `{original_raw_mean:.6f}` |
| selected raw mean final loss | `{best_method['raw_mean_final_loss']}` |
| selected raw delta vs fvt | `{best_method['raw_delta_vs_fvt_mean']}` |
| selected added improved vs fvt | `{best_method['added_improved_vs_fvt']}` |
| selected base nonworse vs fvt | `{best_method['base_nonworse_vs_fvt']}` |
| selected all nonworse vs fvt | `{best_method['all_nonworse_vs_fvt']}` |
""",
        encoding="utf-8",
    )
    access_rows = [
        {
            "run_id": run_id,
            "input_role": "step14_scores",
            "path": str(Path(args.step14_scores).resolve()),
            "allowed_split": "selected_on_MAR_dev",
            "rows_or_files": str(step18.count_rows(Path(args.step14_scores))),
            "md5": step18.md5_file(Path(args.step14_scores)),
            "final_access": "NO",
            "status": "PASS",
        },
        {
            "run_id": run_id,
            "input_role": "step15_summary",
            "path": str(Path(args.step15_summary).resolve()),
            "allowed_split": "checkpoint_metadata",
            "rows_or_files": str(step18.count_rows(Path(args.step15_summary))),
            "md5": step18.md5_file(Path(args.step15_summary)),
            "final_access": "NO",
            "status": "PASS",
        },
        {
            "run_id": run_id,
            "input_role": "train_text",
            "path": str(Path(args.train_text).resolve()),
            "allowed_split": "train",
            "rows_or_files": str(step18.count_rows(Path(args.train_text))),
            "md5": step18.md5_file(Path(args.train_text)),
            "final_access": "NO",
            "status": "PASS",
        },
        {
            "run_id": run_id,
            "input_role": "dev_text",
            "path": str(Path(args.dev_text).resolve()),
            "allowed_split": "MAR_dev",
            "rows_or_files": str(step18.count_rows(Path(args.dev_text))),
            "md5": step18.md5_file(Path(args.dev_text)),
            "final_access": "NO",
            "status": "PASS",
        },
    ]
    write_tsv(access_path, access_rows, ["run_id", "input_role", "path", "allowed_split", "rows_or_files", "md5", "final_access", "status"])
    results_path.write_text(
        f"""# Step 21 Results: V2 Alternative-Initialization MLM Probe

Status: COMPLETED

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Artifact gate status: {'PASS' if artifact_gate else 'FAIL'}

Probe gate status: {'PASS' if probe_gate else 'FAIL'}

## Summary

Step 21 trains alternative Step14 initialization checkpoints with the same 500k-token MLM budget as Step15 and compares them against the Step15 `fvt` adapted baseline. It uses train text and Mark/dev only. ACT final was not read.

| Metric | Value |
| --- | ---: |
| methods | {','.join(methods)} |
| completed runs | {completed}/{required} |
| passing methods | {len(passing_methods)}/{len(methods)} |
| fvt raw mean final loss | {fvt_raw_mean:.6f} |
| original-control raw mean final loss | {original_raw_mean:.6f} |
| best method | {best_method['init_method']} |
| best raw mean final loss | {best_method['raw_mean_final_loss']} |
| best raw delta vs fvt | {best_method['raw_delta_vs_fvt_mean']} |
| best raw ratio vs original | {best_method['raw_ratio_vs_original_mean']} |

## Interpretation

If probe gate passes, rerun Step15/16 style control and normalized metric audits with that initialization before downstream or translation final readout. If probe gate fails, alternative initialization did not resolve the model-dependent failure.

## Failure Return

Failed gate: {'NOT_APPLICABLE' if probe_gate else 'alternative_init_probe_gate'}

Observed evidence: {'NOT_APPLICABLE' if probe_gate else f"passing_methods={len(passing_methods)}/{len(methods)}; best={best_method['init_method']}; raw_delta_vs_fvt={best_method['raw_delta_vs_fvt_mean']}"}

Return-to step: {'NOT_APPLICABLE' if probe_gate else '14_v2_embedding_init or tokenizer/objective redesign'}

Required fix: {'NOT_APPLICABLE' if probe_gate else 'revisit tokenizer/objective or downgrade model-dependent claim'}

Runtime minutes: {(time.time() - start) / 60.0:.3f}
""",
        encoding="utf-8",
    )
    file_rows = [
        step18.file_result("score_table", score_path, "probe gate table"),
        step18.file_result("init_probe_summary", summary_path, "per-method per-seed MLM summary"),
        step18.file_result("init_probe_learning_curves", curves_path, "zero/final Mark-dev curves"),
        step18.file_result("init_probe_category_loss", category_path, "category loss comparison with fvt baseline"),
        step18.file_result("init_probe_variant_summary", variants_path, "per-method aggregate gates"),
        step18.file_result("checkpoint_selection", selection_path, "selected alternative init checkpoint"),
        step18.file_result("no_final_access_audit", access_path, "input access audit"),
        step18.file_result("results", results_path, "step result summary"),
    ]
    for checkpoint_dir in checkpoint_dirs:
        file_rows.append(step18.file_result(f"checkpoint_{checkpoint_dir.parent.name}_{checkpoint_dir.name}", checkpoint_dir, "alternative-init adapted checkpoint"))
    write_tsv(file_results_path, file_rows, ["file_role", "path", "rows_or_files", "bytes", "md5", "status", "notes"])

    print(f"run_id={run_id}")
    print(f"artifact_gate_status={'PASS' if artifact_gate else 'FAIL'}")
    print(f"probe_gate_status={'PASS' if probe_gate else 'FAIL'}")
    print(f"passing_methods={len(passing_methods)}/{len(methods)}")
    print(f"best_method={best_method['init_method']}")
    print(f"selected_checkpoint={best_seed_row['checkpoint_path']}")


if __name__ == "__main__":
    main()
