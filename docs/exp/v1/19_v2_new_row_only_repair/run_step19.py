#!/usr/bin/env python3
"""Train a new-row-only repair on top of Step15 adapted checkpoints."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import os
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


STEP18_PATH = Path(__file__).resolve().parents[1] / "18_v2_added_token_repair" / "run_step18.py"
spec = importlib.util.spec_from_file_location("step18_utils", STEP18_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load Step18 utilities from {STEP18_PATH}")
step18 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(step18)


SCORE_FIELDS = ["run_id", "gate_id", "criterion", "observed", "required", "status", "return_to", "notes"]
SUMMARY_FIELDS = [
    "run_id",
    "seed",
    "source_checkpoint",
    "train_steps_limit",
    "actual_train_steps",
    "target_train_tokens",
    "train_tokens_seen",
    "batch_size",
    "learning_rate",
    "weight_decay",
    "base_mask_prob",
    "added_mask_prob",
    "base_loss_weight",
    "added_loss_weight",
    "source_all_loss",
    "final_all_loss",
    "all_loss_delta_vs_source",
    "step17_baseline_all_loss",
    "all_loss_delta_vs_step17",
    "source_base_loss",
    "final_base_loss",
    "base_loss_delta_vs_source",
    "step17_baseline_base_loss",
    "base_loss_delta_vs_step17",
    "source_added_loss",
    "final_added_loss",
    "added_loss_delta_vs_source",
    "step17_baseline_added_loss",
    "added_loss_delta_vs_step17",
    "final_added_base_ratio",
    "checkpoint_path",
    "status",
    "notes",
]
CATEGORY_FIELDS = [
    "run_id",
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
CURVE_FIELDS = [
    "run_id",
    "seed",
    "stage",
    "step",
    "train_tokens_seen",
    "all_loss",
    "base_loss",
    "added_loss",
    "added_base_ratio",
    "status",
    "notes",
]
TRAINABLE_FIELDS = [
    "run_id",
    "seed",
    "source_checkpoint",
    "checkpoint_path",
    "total_parameter_count",
    "requires_grad_parameter_count",
    "effective_trainable_scalar_count",
    "requires_grad_parameter_names",
    "base_vocab_size",
    "vocab_size",
    "new_rows",
    "embedding_trainable",
    "lm_head_bias_trainable",
    "base_embedding_sample_max_abs_delta",
    "added_embedding_mean_abs_delta",
    "base_bias_sample_max_abs_delta",
    "added_bias_mean_abs_delta",
    "base_rows_preserved",
    "added_rows_changed",
    "status",
    "notes",
]


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    step18.write_tsv(path, rows, fieldnames)


def read_tsv(path: Path) -> list[dict[str, str]]:
    return step18.read_tsv(path)


def adapted_sources(path: Path) -> dict[str, Path]:
    out: dict[str, Path] = {}
    for row in read_tsv(path):
        if row["model_family"] == "adapted_extended":
            checkpoint = Path(row["checkpoint_path"])
            if not checkpoint.exists():
                raise RuntimeError(f"missing Step15 checkpoint: {checkpoint}")
            out[row["seed"]] = checkpoint
    if len(out) < 3:
        raise RuntimeError(f"expected at least three adapted Step15 checkpoints, found {len(out)}")
    return out


def configure_new_row_only(model, base_vocab_size: int):
    for param in model.parameters():
        param.requires_grad_(False)
    embedding = model.get_input_embeddings().weight
    embedding.requires_grad_(True)

    def zero_base_embedding_grad(grad: torch.Tensor) -> torch.Tensor:
        grad = grad.clone()
        grad[:base_vocab_size].zero_()
        return grad

    embedding.register_hook(zero_base_embedding_grad)
    bias = getattr(model.lm_head, "bias", None)
    if bias is not None:
        bias.requires_grad_(True)

        def zero_base_bias_grad(grad: torch.Tensor) -> torch.Tensor:
            grad = grad.clone()
            grad[:base_vocab_size].zero_()
            return grad

        bias.register_hook(zero_base_bias_grad)
    return embedding, bias


def parameter_audit_before(model, base_vocab_size: int, vocab_size: int) -> dict[str, str]:
    total = sum(param.numel() for param in model.parameters())
    grad_params = [(name, param) for name, param in model.named_parameters() if param.requires_grad]
    requires_grad_count = sum(param.numel() for _, param in grad_params)
    hidden_size = model.get_input_embeddings().weight.shape[1]
    effective = (vocab_size - base_vocab_size) * hidden_size
    bias = getattr(model.lm_head, "bias", None)
    if bias is not None and bias.requires_grad:
        effective += vocab_size - base_vocab_size
    return {
        "total_parameter_count": str(total),
        "requires_grad_parameter_count": str(requires_grad_count),
        "effective_trainable_scalar_count": str(effective),
        "requires_grad_parameter_names": ",".join(name for name, _ in grad_params),
        "embedding_trainable": "YES" if model.get_input_embeddings().weight.requires_grad else "NO",
        "lm_head_bias_trainable": "YES" if bias is not None and bias.requires_grad else "NO",
    }


def sample_base_indices(base_vocab_size: int) -> torch.Tensor:
    stride = max(1, base_vocab_size // 512)
    indices = list(range(0, base_vocab_size, stride))
    indices.extend([0, 1, 2, 3, base_vocab_size - 1])
    indices = sorted({idx for idx in indices if 0 <= idx < base_vocab_size})
    return torch.tensor(indices, dtype=torch.long)


def snapshot_rows(model, base_vocab_size: int):
    embedding = model.get_input_embeddings().weight.detach().cpu()
    base_idx = sample_base_indices(base_vocab_size)
    base_embedding = embedding[base_idx].clone()
    added_embedding = embedding[base_vocab_size:].clone()
    bias = getattr(model.lm_head, "bias", None)
    if bias is None:
        base_bias = None
        added_bias = None
    else:
        bias_cpu = bias.detach().cpu()
        base_bias = bias_cpu[base_idx].clone()
        added_bias = bias_cpu[base_vocab_size:].clone()
    return base_idx, base_embedding, added_embedding, base_bias, added_bias


def row_delta_audit(model, base_vocab_size: int, before) -> dict[str, str]:
    base_idx, base_embedding, added_embedding, base_bias, added_bias = before
    embedding = model.get_input_embeddings().weight.detach().cpu()
    base_delta = (embedding[base_idx] - base_embedding).abs().max().item()
    added_delta = (embedding[base_vocab_size:] - added_embedding).abs().mean().item()
    bias = getattr(model.lm_head, "bias", None)
    if bias is None or base_bias is None or added_bias is None:
        base_bias_delta = "NOT_APPLICABLE"
        added_bias_delta = "NOT_APPLICABLE"
    else:
        bias_cpu = bias.detach().cpu()
        base_bias_delta = f"{(bias_cpu[base_idx] - base_bias).abs().max().item():.12f}"
        added_bias_delta = f"{(bias_cpu[base_vocab_size:] - added_bias).abs().mean().item():.12f}"
    base_ok = base_delta <= 1e-10 and (base_bias_delta == "NOT_APPLICABLE" or float(base_bias_delta) <= 1e-10)
    added_changed = added_delta > 0.0 or (added_bias_delta != "NOT_APPLICABLE" and float(added_bias_delta) > 0.0)
    return {
        "base_embedding_sample_max_abs_delta": f"{base_delta:.12f}",
        "added_embedding_mean_abs_delta": f"{added_delta:.12f}",
        "base_bias_sample_max_abs_delta": base_bias_delta,
        "added_bias_mean_abs_delta": added_bias_delta,
        "base_rows_preserved": "PASS" if base_ok else "FAIL",
        "added_rows_changed": "PASS" if added_changed else "FAIL",
        "status": "PASS" if base_ok and added_changed else "FAIL",
    }


def cat_value(rows: list[dict[str, str]], stage: str, category: str) -> float:
    return step18.cat_value(rows, stage, category)


def train_seed(seed: int, run_id: str, source_checkpoint: Path, train_texts: list[str], dev_texts: list[str], step17_baseline: dict[str, dict[str, float]], base_vocab_size: int, device: torch.device, args: argparse.Namespace, checkpoint_root: Path):
    torch.manual_seed(seed)
    tokenizer = XLMRobertaTokenizer.from_pretrained(str(source_checkpoint), local_files_only=True)
    model = AutoModelForMaskedLM.from_pretrained(str(source_checkpoint), local_files_only=True)
    model.to(device)
    vocab_size = len(tokenizer)
    embedding, bias = configure_new_row_only(model, base_vocab_size)
    before_snapshot = snapshot_rows(model, base_vocab_size)
    param_audit = parameter_audit_before(model, base_vocab_size, vocab_size)
    optimizer = torch.optim.AdamW([param for param in model.parameters() if param.requires_grad], lr=args.learning_rate, weight_decay=args.weight_decay)
    checkpoint_path = checkpoint_root / f"new_row_only_seed{seed}"

    source_rows = step18.evaluate_categories(model, tokenizer, dev_texts, device, args, base_vocab_size, seed, run_id, str(source_checkpoint), "source")
    curve_rows = [
        {
            "run_id": run_id,
            "seed": str(seed),
            "stage": "source",
            "step": "0",
            "train_tokens_seen": "0",
            "all_loss": f"{cat_value(source_rows, 'source', 'all'):.6f}",
            "base_loss": f"{cat_value(source_rows, 'source', 'base'):.6f}",
            "added_loss": f"{cat_value(source_rows, 'source', 'added'):.6f}",
            "added_base_ratio": f"{cat_value(source_rows, 'source', 'added') / max(1e-12, cat_value(source_rows, 'source', 'base')):.6f}",
            "status": "PASS",
            "notes": "source Step15 adapted checkpoint; standard eval mask",
        }
    ]

    order = step18.make_order(len(train_texts), args.train_steps * args.batch_size, seed)
    train_tokens = 0
    actual_steps = 0
    start_time = time.time()
    model.train()
    for step in range(1, args.train_steps + 1):
        batch_indices = order[(step - 1) * args.batch_size : step * args.batch_size]
        batch_texts = [train_texts[idx] for idx in batch_indices]
        batch, token_count = step18.make_train_batch(
            tokenizer,
            batch_texts,
            device,
            args.max_length,
            seed * 100000 + step,
            base_vocab_size,
            args.base_mask_prob,
            args.added_mask_prob,
        )
        outputs = model(**batch)
        loss = step18.weighted_mlm_loss(outputs.logits, batch["labels"], base_vocab_size, args.base_loss_weight, args.added_loss_weight)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)
        train_tokens += token_count
        actual_steps = step
        if train_tokens >= args.target_train_tokens:
            break

    final_rows = step18.evaluate_categories(model, tokenizer, dev_texts, device, args, base_vocab_size, seed, run_id, str(checkpoint_path), "final")
    model.to("cpu")
    delta_audit = row_delta_audit(model, base_vocab_size, before_snapshot)
    checkpoint_path.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(checkpoint_path)
    tokenizer.save_pretrained(checkpoint_path)
    report = {
        "run_id": run_id,
        "seed": seed,
        "objective": "new_row_only_added_token_repair",
        "source_checkpoint": str(source_checkpoint),
        "actual_train_steps": actual_steps,
        "target_train_tokens": args.target_train_tokens,
        "train_tokens_seen": train_tokens,
        "base_mask_prob": args.base_mask_prob,
        "added_mask_prob": args.added_mask_prob,
        "base_loss_weight": args.base_loss_weight,
        "added_loss_weight": args.added_loss_weight,
        "weight_decay": args.weight_decay,
        "selection_data": "MAR_dev_only",
        "final_access": "NO_ACT_FINAL_ACCESS",
    }
    (checkpoint_path / "new_row_only_repair_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    runtime = time.time() - start_time

    source_all = cat_value(source_rows, "source", "all")
    source_base = cat_value(source_rows, "source", "base")
    source_added = cat_value(source_rows, "source", "added")
    final_all = cat_value(final_rows, "final", "all")
    final_base = cat_value(final_rows, "final", "base")
    final_added = cat_value(final_rows, "final", "added")
    baseline_all = step17_baseline[str(seed)]["all"]
    baseline_base = step17_baseline[str(seed)]["base"]
    baseline_added = step17_baseline[str(seed)]["added"]
    status = "PASS" if final_added < source_added and final_all <= source_all and final_base <= source_base and delta_audit["status"] == "PASS" else "NO_REPAIR"
    curve_rows.append(
        {
            "run_id": run_id,
            "seed": str(seed),
            "stage": "final",
            "step": str(actual_steps),
            "train_tokens_seen": str(train_tokens),
            "all_loss": f"{final_all:.6f}",
            "base_loss": f"{final_base:.6f}",
            "added_loss": f"{final_added:.6f}",
            "added_base_ratio": f"{final_added / max(1e-12, final_base):.6f}",
            "status": "PASS",
            "notes": "new-row-only final; standard eval mask",
        }
    )
    summary = {
        "run_id": run_id,
        "seed": str(seed),
        "source_checkpoint": str(source_checkpoint),
        "train_steps_limit": str(args.train_steps),
        "actual_train_steps": str(actual_steps),
        "target_train_tokens": str(args.target_train_tokens),
        "train_tokens_seen": str(train_tokens),
        "batch_size": str(args.batch_size),
        "learning_rate": f"{args.learning_rate:.8f}",
        "weight_decay": f"{args.weight_decay:.8f}",
        "base_mask_prob": f"{args.base_mask_prob:.6f}",
        "added_mask_prob": f"{args.added_mask_prob:.6f}",
        "base_loss_weight": f"{args.base_loss_weight:.6f}",
        "added_loss_weight": f"{args.added_loss_weight:.6f}",
        "source_all_loss": f"{source_all:.6f}",
        "final_all_loss": f"{final_all:.6f}",
        "all_loss_delta_vs_source": f"{final_all - source_all:.6f}",
        "step17_baseline_all_loss": f"{baseline_all:.6f}",
        "all_loss_delta_vs_step17": f"{final_all - baseline_all:.6f}",
        "source_base_loss": f"{source_base:.6f}",
        "final_base_loss": f"{final_base:.6f}",
        "base_loss_delta_vs_source": f"{final_base - source_base:.6f}",
        "step17_baseline_base_loss": f"{baseline_base:.6f}",
        "base_loss_delta_vs_step17": f"{final_base - baseline_base:.6f}",
        "source_added_loss": f"{source_added:.6f}",
        "final_added_loss": f"{final_added:.6f}",
        "added_loss_delta_vs_source": f"{final_added - source_added:.6f}",
        "step17_baseline_added_loss": f"{baseline_added:.6f}",
        "added_loss_delta_vs_step17": f"{final_added - baseline_added:.6f}",
        "final_added_base_ratio": f"{final_added / max(1e-12, final_base):.6f}",
        "checkpoint_path": str(checkpoint_path),
        "status": status,
        "notes": f"runtime_minutes={runtime / 60.0:.3f}; no_ACT_final_access",
    }
    trainable = {
        "run_id": run_id,
        "seed": str(seed),
        "source_checkpoint": str(source_checkpoint),
        "checkpoint_path": str(checkpoint_path),
        **param_audit,
        "base_vocab_size": str(base_vocab_size),
        "vocab_size": str(vocab_size),
        "new_rows": str(vocab_size - base_vocab_size),
        **delta_audit,
        "notes": "embedding/output matrix is tied; gradient hook zeros rows below base_vocab_size",
    }
    return summary, source_rows + final_rows, curve_rows, trainable, checkpoint_path


def mean(rows: list[dict[str, str]], column: str) -> float:
    return sum(float(row[column]) for row in rows) / max(1, len(rows))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--checkpoint-root", default="/home/axt/mnt2/jongha/second_try/checkpoints/19_v2_new_row_only_repair")
    parser.add_argument("--step15-summary", default="docs/exp/second_try/15_v2_mlm_control/seed_summary.tsv")
    parser.add_argument("--train-text", default="/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_tokenizer_mlm_train.txt")
    parser.add_argument("--dev-manifest", default="docs/exp/second_try/12_v2_split_protocol/v2_dev_manifest.tsv")
    parser.add_argument("--baseline-category", default="docs/exp/second_try/17_v2_added_token_failure_analysis/token_category_loss.tsv")
    parser.add_argument("--base-model", default="xlm-roberta-base")
    parser.add_argument("--seeds", default="13,17,23")
    parser.add_argument("--train-limit", type=int, default=0)
    parser.add_argument("--dev-limit", type=int, default=0)
    parser.add_argument("--train-steps", type=int, default=1800)
    parser.add_argument("--target-train-tokens", type=int, default=500000)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--eval-batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--learning-rate", type=float, default=5e-5)
    parser.add_argument("--weight-decay", type=float, default=0.0)
    parser.add_argument("--base-mask-prob", type=float, default=0.15)
    parser.add_argument("--added-mask-prob", type=float, default=0.30)
    parser.add_argument("--eval-mask-prob", type=float, default=0.15)
    parser.add_argument("--base-loss-weight", type=float, default=1.0)
    parser.add_argument("--added-loss-weight", type=float, default=3.0)
    parser.add_argument("--seed", type=int, default=10190)
    args = parser.parse_args()

    transformers_logging.set_verbosity_error()
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    start = time.time()
    run_id = "step19_v2_new_row_only_repair_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    step_dir = Path(args.step_dir).resolve()
    checkpoint_root = Path(args.checkpoint_root).resolve()
    checkpoint_root.mkdir(parents=True, exist_ok=True)
    sources = adapted_sources(Path(args.step15_summary))
    train_texts = step18.read_train_lines(Path(args.train_text), args.train_limit)
    dev_texts = step18.read_dev_texts(Path(args.dev_manifest), args.dev_limit)
    baseline = step18.load_baseline_category(Path(args.baseline_category))
    base_vocab_size = len(XLMRobertaTokenizer.from_pretrained(args.base_model, local_files_only=True))
    seeds = [int(seed.strip()) for seed in args.seeds.split(",") if seed.strip()]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    summary_rows: list[dict[str, str]] = []
    category_rows: list[dict[str, str]] = []
    curve_rows: list[dict[str, str]] = []
    trainable_rows: list[dict[str, str]] = []
    checkpoint_dirs: list[Path] = []
    for seed in seeds:
        print(f"training new-row-only repair seed={seed}", flush=True)
        summary, categories, curves, trainable, checkpoint_path = train_seed(
            seed,
            run_id,
            sources[str(seed)],
            train_texts,
            dev_texts,
            baseline,
            base_vocab_size,
            device,
            args,
            checkpoint_root,
        )
        summary_rows.append(summary)
        category_rows.extend(categories)
        curve_rows.extend(curves)
        trainable_rows.append(trainable)
        checkpoint_dirs.append(checkpoint_path)

    completed = len(summary_rows)
    added_improved_source = sum(1 for row in summary_rows if float(row["added_loss_delta_vs_source"]) < 0.0)
    base_nonworse_source = sum(1 for row in summary_rows if float(row["base_loss_delta_vs_source"]) <= 0.0)
    all_nonworse_source = sum(1 for row in summary_rows if float(row["all_loss_delta_vs_source"]) <= 0.0)
    trainable_pass = sum(1 for row in trainable_rows if row["status"] == "PASS")
    repaired = sum(1 for row in summary_rows if row["status"] == "PASS")
    artifact_gate = completed == len(seeds)
    repair_gate = artifact_gate and trainable_pass == len(seeds) and added_improved_source == len(seeds) and base_nonworse_source == len(seeds) and all_nonworse_source == len(seeds)
    best = sorted(summary_rows, key=lambda row: float(row["final_added_loss"]))[0]

    score_rows = [
        {
            "run_id": run_id,
            "gate_id": "G01_required_repair_runs",
            "criterion": "all new-row-only repair seeds complete",
            "observed": f"{completed}/{len(seeds)}",
            "required": f"{len(seeds)}/{len(seeds)}",
            "status": "PASS" if artifact_gate else "FAIL",
            "return_to": "19_v2_new_row_only_repair",
            "notes": "adapted Step15 checkpoint repaired per seed",
        },
        {
            "run_id": run_id,
            "gate_id": "G02_no_final_access",
            "criterion": "ACT final data not read",
            "observed": "NO_ACT_FINAL_ACCESS",
            "required": "NO_ACT_FINAL_ACCESS",
            "status": "PASS",
            "return_to": "12_v2_split_protocol",
            "notes": "train text, Mark/dev manifest, Step15 metadata, and Step17 baseline only",
        },
        {
            "run_id": run_id,
            "gate_id": "G03_trainable_audit",
            "criterion": "only appended rows effectively update",
            "observed": f"{trainable_pass}/{len(seeds)}",
            "required": f"{len(seeds)}/{len(seeds)}",
            "status": "PASS" if trainable_pass == len(seeds) else "FAIL",
            "return_to": "19_v2_new_row_only_repair",
            "notes": "base row sample delta must be zero and added rows must change",
        },
        {
            "run_id": run_id,
            "gate_id": "G04_added_loss_improves",
            "criterion": "added-token dev loss improves versus source Step15 checkpoint in every seed",
            "observed": f"{added_improved_source}/{len(seeds)}",
            "required": f"{len(seeds)}/{len(seeds)}",
            "status": "PASS" if added_improved_source == len(seeds) else "FAIL",
            "return_to": "19_v2_new_row_only_repair",
            "notes": f"mean_delta={mean(summary_rows, 'added_loss_delta_vs_source'):.6f}",
        },
        {
            "run_id": run_id,
            "gate_id": "G05_base_loss_nonworse",
            "criterion": "base-token dev loss does not worsen versus source Step15 checkpoint in every seed",
            "observed": f"{base_nonworse_source}/{len(seeds)}",
            "required": f"{len(seeds)}/{len(seeds)}",
            "status": "PASS" if base_nonworse_source == len(seeds) else "FAIL",
            "return_to": "19_v2_new_row_only_repair",
            "notes": f"mean_delta={mean(summary_rows, 'base_loss_delta_vs_source'):.6f}",
        },
        {
            "run_id": run_id,
            "gate_id": "G06_all_loss_nonworse",
            "criterion": "all-token dev loss does not worsen versus source Step15 checkpoint in every seed",
            "observed": f"{all_nonworse_source}/{len(seeds)}",
            "required": f"{len(seeds)}/{len(seeds)}",
            "status": "PASS" if all_nonworse_source == len(seeds) else "FAIL",
            "return_to": "19_v2_new_row_only_repair",
            "notes": f"mean_delta={mean(summary_rows, 'all_loss_delta_vs_source'):.6f}",
        },
        {
            "run_id": run_id,
            "gate_id": "G07_repair_checkpoint_selection",
            "criterion": "best repaired checkpoint selected by lowest added-token dev loss",
            "observed": best["checkpoint_path"],
            "required": "one checkpoint path",
            "status": "PASS",
            "return_to": "19_v2_new_row_only_repair",
            "notes": f"seed={best['seed']}; final_added_loss={best['final_added_loss']}",
        },
    ]

    score_path = step_dir / "score_table.tsv"
    summary_path = step_dir / "new_row_repair_summary.tsv"
    category_path = step_dir / "new_row_category_loss.tsv"
    curves_path = step_dir / "new_row_learning_curves.tsv"
    trainable_path = step_dir / "trainable_parameters.tsv"
    selection_path = step_dir / "checkpoint_selection.md"
    access_path = step_dir / "v2_no_final_access_audit.tsv"
    results_path = step_dir / "results.md"
    file_results_path = step_dir / "file_results.tsv"

    write_tsv(score_path, score_rows, SCORE_FIELDS)
    write_tsv(summary_path, summary_rows, SUMMARY_FIELDS)
    write_tsv(category_path, category_rows, CATEGORY_FIELDS)
    write_tsv(curves_path, curve_rows, CURVE_FIELDS)
    write_tsv(trainable_path, trainable_rows, TRAINABLE_FIELDS)
    selection_path.write_text(
        f"""# Step 19 Checkpoint Selection

Run id: `{run_id}`

Selection data: `MAR` dev only.

Final data access: `NO_ACT_FINAL_ACCESS`.

Selected repaired checkpoint: `{best['checkpoint_path']}`

| Metric | Value |
| --- | --- |
| selected seed | `{best['seed']}` |
| source all loss | `{best['source_all_loss']}` |
| final all loss | `{best['final_all_loss']}` |
| all loss delta vs source | `{best['all_loss_delta_vs_source']}` |
| source added loss | `{best['source_added_loss']}` |
| final added loss | `{best['final_added_loss']}` |
| added loss delta vs source | `{best['added_loss_delta_vs_source']}` |
| final added/base ratio | `{best['final_added_base_ratio']}` |
| repair gate | `{'PASS' if repair_gate else 'FAIL'}` |
""",
        encoding="utf-8",
    )
    access_rows = [
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
            "input_role": "dev_manifest",
            "path": str(Path(args.dev_manifest).resolve()),
            "allowed_split": "MAR_dev",
            "rows_or_files": str(step18.count_rows(Path(args.dev_manifest))),
            "md5": step18.md5_file(Path(args.dev_manifest)),
            "final_access": "NO",
            "status": "PASS",
        },
        {
            "run_id": run_id,
            "input_role": "baseline_category",
            "path": str(Path(args.baseline_category).resolve()),
            "allowed_split": "diagnostic_metadata",
            "rows_or_files": str(step18.count_rows(Path(args.baseline_category))),
            "md5": step18.md5_file(Path(args.baseline_category)),
            "final_access": "NO",
            "status": "PASS",
        },
    ]
    write_tsv(access_path, access_rows, ["run_id", "input_role", "path", "allowed_split", "rows_or_files", "md5", "final_access", "status"])

    results_path.write_text(
        f"""# Step 19 Results: V2 New-Row-Only Added-Token Repair

Status: COMPLETED

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Artifact gate status: {'PASS' if artifact_gate else 'FAIL'}

Repair gate status: {'PASS' if repair_gate else 'FAIL'}

## Summary

Step 19 starts from each Step15 adapted checkpoint, freezes model behavior, and trains only appended vocabulary rows plus appended LM-head bias rows. Evaluation uses Mark/dev only. ACT final was not read.

| Metric | Value |
| --- | ---: |
| completed seeds | {completed}/{len(seeds)} |
| trainable audit pass seeds | {trainable_pass}/{len(seeds)} |
| added-token improved seeds | {added_improved_source}/{len(seeds)} |
| base-token nonworse seeds | {base_nonworse_source}/{len(seeds)} |
| all-token nonworse seeds | {all_nonworse_source}/{len(seeds)} |
| repaired seeds | {repaired}/{len(seeds)} |
| mean added loss delta vs source | {mean(summary_rows, 'added_loss_delta_vs_source'):.6f} |
| mean base loss delta vs source | {mean(summary_rows, 'base_loss_delta_vs_source'):.6f} |
| mean all loss delta vs source | {mean(summary_rows, 'all_loss_delta_vs_source'):.6f} |
| selected seed | {best['seed']} |
| selected checkpoint | {best['checkpoint_path']} |

## Interpretation

If repair gate passes, rerun Step15/Step16 style original-control comparisons with this repaired checkpoint family before any downstream or translation final readout. If repair gate fails, keep the result as a failed repair and try a staged or lower-learning-rate variant.

## Failure Return

Failed gate: {'NOT_APPLICABLE' if repair_gate else 'new_row_only_repair_gate'}

Observed evidence: {'NOT_APPLICABLE' if repair_gate else f"trainable_pass={trainable_pass}/{len(seeds)}, added_improved={added_improved_source}/{len(seeds)}, base_nonworse={base_nonworse_source}/{len(seeds)}, all_nonworse={all_nonworse_source}/{len(seeds)}"}

Return-to step: {'NOT_APPLICABLE' if repair_gate else '15_v2_mlm_control or 19_v2_new_row_only_repair'}

Required fix: {'NOT_APPLICABLE' if repair_gate else 'try lower learning rate, staged new-row training, or changed added-token objective'}

Runtime minutes: {(time.time() - start) / 60.0:.3f}
""",
        encoding="utf-8",
    )
    file_rows = [
        step18.file_result("score_table", score_path, "repair gate table"),
        step18.file_result("new_row_repair_summary", summary_path, "per-seed new-row repair summary"),
        step18.file_result("new_row_category_loss", category_path, "source/final category losses"),
        step18.file_result("new_row_learning_curves", curves_path, "source/final category curves"),
        step18.file_result("trainable_parameters", trainable_path, "trainable parameter and row-delta audit"),
        step18.file_result("checkpoint_selection", selection_path, "selected new-row repair checkpoint"),
        step18.file_result("no_final_access_audit", access_path, "input access audit"),
        step18.file_result("results", results_path, "step result summary"),
    ]
    for checkpoint_dir in checkpoint_dirs:
        file_rows.append(step18.file_result(f"checkpoint_{checkpoint_dir.name}", checkpoint_dir, "new-row-only repaired checkpoint"))
    write_tsv(file_results_path, file_rows, ["file_role", "path", "rows_or_files", "bytes", "md5", "status", "notes"])

    print(f"run_id={run_id}")
    print(f"artifact_gate_status={'PASS' if artifact_gate else 'FAIL'}")
    print(f"repair_gate_status={'PASS' if repair_gate else 'FAIL'}")
    print(f"trainable_pass={trainable_pass}/{len(seeds)}")
    print(f"added_improved_source={added_improved_source}/{len(seeds)}")
    print(f"base_nonworse_source={base_nonworse_source}/{len(seeds)}")
    print(f"all_nonworse_source={all_nonworse_source}/{len(seeds)}")
    print(f"selected_checkpoint={best['checkpoint_path']}")


if __name__ == "__main__":
    main()
