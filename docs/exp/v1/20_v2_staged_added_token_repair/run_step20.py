#!/usr/bin/env python3
"""Run a staged added-token repair grid after Step19 failed."""

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
STEP19_PATH = Path(__file__).resolve().parents[1] / "19_v2_new_row_only_repair" / "run_step19.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


step18 = load_module("step18_utils", STEP18_PATH)
step19 = load_module("step19_utils", STEP19_PATH)


SCORE_FIELDS = ["run_id", "gate_id", "criterion", "observed", "required", "status", "return_to", "notes"]
SUMMARY_FIELDS = [
    "run_id",
    "variant_id",
    "mode",
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
    "source_base_loss",
    "final_base_loss",
    "base_loss_delta_vs_source",
    "source_added_loss",
    "final_added_loss",
    "added_loss_delta_vs_source",
    "final_added_base_ratio",
    "checkpoint_path",
    "status",
    "notes",
]
CATEGORY_FIELDS = [
    "run_id",
    "variant_id",
    "mode",
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
    "variant_id",
    "mode",
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
    "variant_id",
    "mode",
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
VARIANT_FIELDS = [
    "run_id",
    "variant_id",
    "mode",
    "learning_rate",
    "completed",
    "trainable_pass",
    "added_improved",
    "base_nonworse",
    "all_nonworse",
    "mean_added_delta",
    "mean_base_delta",
    "mean_all_delta",
    "status",
    "notes",
]


class Variant:
    def __init__(self, variant_id: str, mode: str, learning_rate: float):
        self.variant_id = variant_id
        self.mode = mode
        self.learning_rate = learning_rate


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    step18.write_tsv(path, rows, fieldnames)


def read_tsv(path: Path) -> list[dict[str, str]]:
    return step18.read_tsv(path)


def parse_variants(raw: str) -> list[Variant]:
    variants: list[Variant] = []
    for item in raw.split(","):
        if not item.strip():
            continue
        parts = item.split(":")
        if len(parts) != 3:
            raise ValueError(f"variant must be id:mode:lr, got {item}")
        variant_id, mode, lr = parts
        if mode not in {"bias_only", "new_row_only"}:
            raise ValueError(f"unknown mode: {mode}")
        variants.append(Variant(variant_id=variant_id, mode=mode, learning_rate=float(lr)))
    if not variants:
        raise ValueError("no variants configured")
    return variants


def configure_trainable(model, base_vocab_size: int, mode: str):
    for param in model.parameters():
        param.requires_grad_(False)
    embedding = model.get_input_embeddings().weight
    bias = getattr(model.lm_head, "bias", None)
    if mode == "new_row_only":
        embedding.requires_grad_(True)

        def zero_base_embedding_grad(grad: torch.Tensor) -> torch.Tensor:
            grad = grad.clone()
            grad[:base_vocab_size].zero_()
            return grad

        embedding.register_hook(zero_base_embedding_grad)
    if bias is not None:
        bias.requires_grad_(True)

        def zero_base_bias_grad(grad: torch.Tensor) -> torch.Tensor:
            grad = grad.clone()
            grad[:base_vocab_size].zero_()
            return grad

        bias.register_hook(zero_base_bias_grad)
    return embedding, bias


def parameter_audit_before(model, base_vocab_size: int, vocab_size: int, mode: str) -> dict[str, str]:
    total = sum(param.numel() for param in model.parameters())
    grad_params = [(name, param) for name, param in model.named_parameters() if param.requires_grad]
    requires_grad_count = sum(param.numel() for _, param in grad_params)
    hidden_size = model.get_input_embeddings().weight.shape[1]
    effective = 0
    if mode == "new_row_only":
        effective += (vocab_size - base_vocab_size) * hidden_size
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


def make_added_train_batch(tokenizer, texts: list[str], device: torch.device, max_length: int, seed: int, base_vocab_size: int, base_prob: float, added_prob: float):
    encoded = tokenizer(texts, padding=True, truncation=True, max_length=max_length, return_tensors="pt")
    input_ids = encoded["input_ids"]
    attention_mask = encoded["attention_mask"]
    labels = input_ids.clone()
    special_mask = step18.special_mask_for(tokenizer, labels, attention_mask)
    added_positions = labels.ge(base_vocab_size) & (~special_mask)
    generator = torch.Generator()
    generator.manual_seed(seed)
    probability = torch.full(labels.shape, base_prob)
    probability[added_positions] = added_prob
    probability.masked_fill_(special_mask, 0.0)
    masked = torch.bernoulli(probability, generator=generator).bool()
    if masked.sum().item() == 0:
        added_available = added_positions.nonzero(as_tuple=False)
        if len(added_available) > 0:
            masked[added_available[0, 0], added_available[0, 1]] = True
        else:
            available = (special_mask == 0).nonzero(as_tuple=False)
            if len(available) > 0:
                masked[available[0, 0], available[0, 1]] = True
    labels[~masked] = -100
    input_ids = input_ids.clone()
    input_ids[masked] = tokenizer.mask_token_id
    token_count = int((~special_mask).sum().item())
    return {
        "input_ids": input_ids.to(device),
        "attention_mask": attention_mask.to(device),
        "labels": labels.to(device),
    }, token_count


def stable_variant_offset(variant_id: str) -> int:
    total = 0
    for idx, char in enumerate(variant_id):
        total += (idx + 1) * ord(char)
    return total


def cat_value(rows: list[dict[str, str]], stage: str, category: str) -> float:
    return step18.cat_value(rows, stage, category)


def add_variant_fields(rows: list[dict[str, str]], variant: Variant) -> list[dict[str, str]]:
    out = []
    for row in rows:
        new = {"variant_id": variant.variant_id, "mode": variant.mode}
        new.update(row)
        ordered = {
            "run_id": new["run_id"],
            "variant_id": new["variant_id"],
            "mode": new["mode"],
            "seed": new["seed"],
            "checkpoint_path": new["checkpoint_path"],
            "stage": new["stage"],
            "category": new["category"],
            "non_special_tokens": new["non_special_tokens"],
            "masked_tokens": new["masked_tokens"],
            "mean_loss": new["mean_loss"],
            "loss_share_pct": new["loss_share_pct"],
            "token_share_pct": new["token_share_pct"],
            "status": new["status"],
        }
        out.append(ordered)
    return out


def train_variant_seed(variant: Variant, seed: int, run_id: str, source_checkpoint: Path, train_texts: list[str], dev_texts: list[str], base_vocab_size: int, device: torch.device, args: argparse.Namespace, checkpoint_root: Path):
    torch.manual_seed(seed)
    tokenizer = XLMRobertaTokenizer.from_pretrained(str(source_checkpoint), local_files_only=True)
    model = AutoModelForMaskedLM.from_pretrained(str(source_checkpoint), local_files_only=True)
    model.to(device)
    vocab_size = len(tokenizer)
    configure_trainable(model, base_vocab_size, variant.mode)
    before_snapshot = step19.snapshot_rows(model, base_vocab_size)
    param_audit = parameter_audit_before(model, base_vocab_size, vocab_size, variant.mode)
    optimizer = torch.optim.AdamW([param for param in model.parameters() if param.requires_grad], lr=variant.learning_rate, weight_decay=args.weight_decay)
    checkpoint_path = checkpoint_root / variant.variant_id / f"{variant.variant_id}_seed{seed}"

    source_rows_raw = step18.evaluate_categories(model, tokenizer, dev_texts, device, args, base_vocab_size, seed, run_id, str(source_checkpoint), "source")
    source_rows = add_variant_fields(source_rows_raw, variant)
    curve_rows = [
        {
            "run_id": run_id,
            "variant_id": variant.variant_id,
            "mode": variant.mode,
            "seed": str(seed),
            "stage": "source",
            "step": "0",
            "train_tokens_seen": "0",
            "all_loss": f"{cat_value(source_rows_raw, 'source', 'all'):.6f}",
            "base_loss": f"{cat_value(source_rows_raw, 'source', 'base'):.6f}",
            "added_loss": f"{cat_value(source_rows_raw, 'source', 'added'):.6f}",
            "added_base_ratio": f"{cat_value(source_rows_raw, 'source', 'added') / max(1e-12, cat_value(source_rows_raw, 'source', 'base')):.6f}",
            "status": "PASS",
            "notes": "source Step15 adapted checkpoint; standard eval mask",
        }
    ]

    variant_offset = stable_variant_offset(variant.variant_id)
    order = step18.make_order(len(train_texts), args.train_steps * args.batch_size, seed + variant_offset % 10000)
    train_tokens = 0
    actual_steps = 0
    start_time = time.time()
    model.train()
    for step in range(1, args.train_steps + 1):
        batch_indices = order[(step - 1) * args.batch_size : step * args.batch_size]
        batch_texts = [train_texts[idx] for idx in batch_indices]
        batch, token_count = make_added_train_batch(
            tokenizer,
            batch_texts,
            device,
            args.max_length,
            seed * 100000 + step + variant_offset % 100000,
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

    final_rows_raw = step18.evaluate_categories(model, tokenizer, dev_texts, device, args, base_vocab_size, seed, run_id, str(checkpoint_path), "final")
    final_rows = add_variant_fields(final_rows_raw, variant)
    model.to("cpu")
    delta_audit = step19.row_delta_audit(model, base_vocab_size, before_snapshot)
    checkpoint_path.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(checkpoint_path)
    tokenizer.save_pretrained(checkpoint_path)
    report = {
        "run_id": run_id,
        "variant_id": variant.variant_id,
        "mode": variant.mode,
        "seed": seed,
        "objective": "added_only_staged_repair_grid",
        "source_checkpoint": str(source_checkpoint),
        "actual_train_steps": actual_steps,
        "target_train_tokens": args.target_train_tokens,
        "train_tokens_seen": train_tokens,
        "learning_rate": variant.learning_rate,
        "base_mask_prob": args.base_mask_prob,
        "added_mask_prob": args.added_mask_prob,
        "base_loss_weight": args.base_loss_weight,
        "added_loss_weight": args.added_loss_weight,
        "selection_data": "MAR_dev_only",
        "final_access": "NO_ACT_FINAL_ACCESS",
    }
    (checkpoint_path / "staged_added_repair_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    runtime = time.time() - start_time

    source_all = cat_value(source_rows_raw, "source", "all")
    source_base = cat_value(source_rows_raw, "source", "base")
    source_added = cat_value(source_rows_raw, "source", "added")
    final_all = cat_value(final_rows_raw, "final", "all")
    final_base = cat_value(final_rows_raw, "final", "base")
    final_added = cat_value(final_rows_raw, "final", "added")
    status = "PASS" if final_added < source_added and final_all <= source_all and final_base <= source_base and delta_audit["status"] == "PASS" else "NO_REPAIR"
    curve_rows.append(
        {
            "run_id": run_id,
            "variant_id": variant.variant_id,
            "mode": variant.mode,
            "seed": str(seed),
            "stage": "final",
            "step": str(actual_steps),
            "train_tokens_seen": str(train_tokens),
            "all_loss": f"{final_all:.6f}",
            "base_loss": f"{final_base:.6f}",
            "added_loss": f"{final_added:.6f}",
            "added_base_ratio": f"{final_added / max(1e-12, final_base):.6f}",
            "status": "PASS",
            "notes": "staged repair final; standard eval mask",
        }
    )
    summary = {
        "run_id": run_id,
        "variant_id": variant.variant_id,
        "mode": variant.mode,
        "seed": str(seed),
        "source_checkpoint": str(source_checkpoint),
        "train_steps_limit": str(args.train_steps),
        "actual_train_steps": str(actual_steps),
        "target_train_tokens": str(args.target_train_tokens),
        "train_tokens_seen": str(train_tokens),
        "batch_size": str(args.batch_size),
        "learning_rate": f"{variant.learning_rate:.8f}",
        "weight_decay": f"{args.weight_decay:.8f}",
        "base_mask_prob": f"{args.base_mask_prob:.6f}",
        "added_mask_prob": f"{args.added_mask_prob:.6f}",
        "base_loss_weight": f"{args.base_loss_weight:.6f}",
        "added_loss_weight": f"{args.added_loss_weight:.6f}",
        "source_all_loss": f"{source_all:.6f}",
        "final_all_loss": f"{final_all:.6f}",
        "all_loss_delta_vs_source": f"{final_all - source_all:.6f}",
        "source_base_loss": f"{source_base:.6f}",
        "final_base_loss": f"{final_base:.6f}",
        "base_loss_delta_vs_source": f"{final_base - source_base:.6f}",
        "source_added_loss": f"{source_added:.6f}",
        "final_added_loss": f"{final_added:.6f}",
        "added_loss_delta_vs_source": f"{final_added - source_added:.6f}",
        "final_added_base_ratio": f"{final_added / max(1e-12, final_base):.6f}",
        "checkpoint_path": str(checkpoint_path),
        "status": status,
        "notes": f"runtime_minutes={runtime / 60.0:.3f}; no_ACT_final_access",
    }
    trainable = {
        "run_id": run_id,
        "variant_id": variant.variant_id,
        "mode": variant.mode,
        "seed": str(seed),
        "source_checkpoint": str(source_checkpoint),
        "checkpoint_path": str(checkpoint_path),
        **param_audit,
        "base_vocab_size": str(base_vocab_size),
        "vocab_size": str(vocab_size),
        "new_rows": str(vocab_size - base_vocab_size),
        **delta_audit,
        "notes": f"mode={variant.mode}; gradient hook zeros rows below base_vocab_size",
    }
    return summary, source_rows + final_rows, curve_rows, trainable, checkpoint_path


def mean(rows: list[dict[str, str]], column: str) -> float:
    return sum(float(row[column]) for row in rows) / max(1, len(rows))


def summarize_variant(run_id: str, variant: Variant, rows: list[dict[str, str]], trainable_rows: list[dict[str, str]], expected: int) -> dict[str, str]:
    completed = len(rows)
    trainable_pass = sum(1 for row in trainable_rows if row["variant_id"] == variant.variant_id and row["status"] == "PASS")
    added = sum(1 for row in rows if float(row["added_loss_delta_vs_source"]) < 0.0)
    base = sum(1 for row in rows if float(row["base_loss_delta_vs_source"]) <= 0.0)
    all_ = sum(1 for row in rows if float(row["all_loss_delta_vs_source"]) <= 0.0)
    status = "PASS" if completed == expected and trainable_pass == expected and added == expected and base == expected and all_ == expected else "FAIL"
    return {
        "run_id": run_id,
        "variant_id": variant.variant_id,
        "mode": variant.mode,
        "learning_rate": f"{variant.learning_rate:.8f}",
        "completed": f"{completed}/{expected}",
        "trainable_pass": f"{trainable_pass}/{expected}",
        "added_improved": f"{added}/{expected}",
        "base_nonworse": f"{base}/{expected}",
        "all_nonworse": f"{all_}/{expected}",
        "mean_added_delta": f"{mean(rows, 'added_loss_delta_vs_source'):.6f}",
        "mean_base_delta": f"{mean(rows, 'base_loss_delta_vs_source'):.6f}",
        "mean_all_delta": f"{mean(rows, 'all_loss_delta_vs_source'):.6f}",
        "status": status,
        "notes": "variant passes only if every seed passes every repair gate",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--checkpoint-root", default="/home/axt/mnt2/jongha/second_try/checkpoints/20_v2_staged_added_token_repair")
    parser.add_argument("--step15-summary", default="docs/exp/second_try/15_v2_mlm_control/seed_summary.tsv")
    parser.add_argument("--train-text", default="/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_tokenizer_mlm_train.txt")
    parser.add_argument("--dev-manifest", default="docs/exp/second_try/12_v2_split_protocol/v2_dev_manifest.tsv")
    parser.add_argument("--baseline-category", default="docs/exp/second_try/17_v2_added_token_failure_analysis/token_category_loss.tsv")
    parser.add_argument("--base-model", default="xlm-roberta-base")
    parser.add_argument("--variants", default="bias_only_added_lr1e-3:bias_only:0.001,bias_only_added_lr1e-4:bias_only:0.0001,new_row_added_lr1e-5:new_row_only:0.00001")
    parser.add_argument("--seeds", default="13,17,23")
    parser.add_argument("--train-limit", type=int, default=0)
    parser.add_argument("--dev-limit", type=int, default=0)
    parser.add_argument("--train-steps", type=int, default=1800)
    parser.add_argument("--target-train-tokens", type=int, default=500000)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--eval-batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--weight-decay", type=float, default=0.0)
    parser.add_argument("--base-mask-prob", type=float, default=0.0)
    parser.add_argument("--added-mask-prob", type=float, default=0.30)
    parser.add_argument("--eval-mask-prob", type=float, default=0.15)
    parser.add_argument("--base-loss-weight", type=float, default=1.0)
    parser.add_argument("--added-loss-weight", type=float, default=3.0)
    parser.add_argument("--seed", type=int, default=12020)
    args = parser.parse_args()

    transformers_logging.set_verbosity_error()
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    start = time.time()
    run_id = "step20_v2_staged_added_repair_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    step_dir = Path(args.step_dir).resolve()
    checkpoint_root = Path(args.checkpoint_root).resolve()
    checkpoint_root.mkdir(parents=True, exist_ok=True)
    variants = parse_variants(args.variants)
    seeds = [int(seed.strip()) for seed in args.seeds.split(",") if seed.strip()]
    sources = step19.adapted_sources(Path(args.step15_summary))
    train_texts = step18.read_train_lines(Path(args.train_text), args.train_limit)
    dev_texts = step18.read_dev_texts(Path(args.dev_manifest), args.dev_limit)
    base_vocab_size = len(XLMRobertaTokenizer.from_pretrained(args.base_model, local_files_only=True))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    summary_rows: list[dict[str, str]] = []
    category_rows: list[dict[str, str]] = []
    curve_rows: list[dict[str, str]] = []
    trainable_rows: list[dict[str, str]] = []
    checkpoint_dirs: list[Path] = []
    for variant in variants:
        for seed in seeds:
            print(f"training staged repair variant={variant.variant_id} seed={seed}", flush=True)
            summary, categories, curves, trainable, checkpoint_path = train_variant_seed(
                variant,
                seed,
                run_id,
                sources[str(seed)],
                train_texts,
                dev_texts,
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

    expected_runs = len(variants) * len(seeds)
    completed = len(summary_rows)
    variant_rows = []
    for variant in variants:
        rows = [row for row in summary_rows if row["variant_id"] == variant.variant_id]
        variant_rows.append(summarize_variant(run_id, variant, rows, trainable_rows, len(seeds)))
    passing_variants = [row for row in variant_rows if row["status"] == "PASS"]
    artifact_gate = completed == expected_runs
    repair_gate = artifact_gate and bool(passing_variants)
    best_variant = sorted(variant_rows, key=lambda row: (row["status"] != "PASS", float(row["mean_added_delta"])))[0]
    best_seed_row = sorted([row for row in summary_rows if row["variant_id"] == best_variant["variant_id"]], key=lambda row: float(row["final_added_loss"]))[0]
    max_trainable_fail = sum(1 for row in trainable_rows if row["status"] != "PASS")

    score_rows = [
        {
            "run_id": run_id,
            "gate_id": "G01_required_variant_runs",
            "criterion": "all configured variant/seed runs complete",
            "observed": f"{completed}/{expected_runs}",
            "required": f"{expected_runs}/{expected_runs}",
            "status": "PASS" if artifact_gate else "FAIL",
            "return_to": "20_v2_staged_added_token_repair",
            "notes": f"variants={','.join(v.variant_id for v in variants)}",
        },
        {
            "run_id": run_id,
            "gate_id": "G02_no_final_access",
            "criterion": "ACT final data not read",
            "observed": "NO_ACT_FINAL_ACCESS",
            "required": "NO_ACT_FINAL_ACCESS",
            "status": "PASS",
            "return_to": "12_v2_split_protocol",
            "notes": "train text, Mark/dev manifest, Step15 metadata, and Step17 metadata only",
        },
        {
            "run_id": run_id,
            "gate_id": "G03_trainable_audit",
            "criterion": "all variant trainable audits pass",
            "observed": f"failures={max_trainable_fail}",
            "required": "failures=0",
            "status": "PASS" if max_trainable_fail == 0 else "FAIL",
            "return_to": "20_v2_staged_added_token_repair",
            "notes": "base row sample delta must be zero; intended rows must change",
        },
        {
            "run_id": run_id,
            "gate_id": "G04_any_variant_repairs",
            "criterion": "at least one variant improves added loss without base/all degradation in every seed",
            "observed": f"passing_variants={len(passing_variants)}/{len(variants)}",
            "required": ">=1",
            "status": "PASS" if passing_variants else "FAIL",
            "return_to": "20_v2_staged_added_token_repair",
            "notes": "; ".join(f"{row['variant_id']}: added={row['added_improved']}, base={row['base_nonworse']}, all={row['all_nonworse']}" for row in variant_rows),
        },
        {
            "run_id": run_id,
            "gate_id": "G05_variant_selection",
            "criterion": "best variant and checkpoint selected on Mark/dev only",
            "observed": f"variant={best_variant['variant_id']}; checkpoint={best_seed_row['checkpoint_path']}",
            "required": "one variant and one checkpoint",
            "status": "PASS",
            "return_to": "20_v2_staged_added_token_repair",
            "notes": f"repair_gate={'PASS' if repair_gate else 'FAIL'}; final_added_loss={best_seed_row['final_added_loss']}",
        },
    ]

    score_path = step_dir / "score_table.tsv"
    summary_path = step_dir / "staged_repair_summary.tsv"
    category_path = step_dir / "staged_category_loss.tsv"
    curves_path = step_dir / "staged_learning_curves.tsv"
    trainable_path = step_dir / "trainable_parameters.tsv"
    variants_path = step_dir / "variant_summary.tsv"
    selection_path = step_dir / "variant_selection.md"
    access_path = step_dir / "v2_no_final_access_audit.tsv"
    results_path = step_dir / "results.md"
    file_results_path = step_dir / "file_results.tsv"

    write_tsv(score_path, score_rows, SCORE_FIELDS)
    write_tsv(summary_path, summary_rows, SUMMARY_FIELDS)
    write_tsv(category_path, category_rows, CATEGORY_FIELDS)
    write_tsv(curves_path, curve_rows, CURVE_FIELDS)
    write_tsv(trainable_path, trainable_rows, TRAINABLE_FIELDS)
    write_tsv(variants_path, variant_rows, VARIANT_FIELDS)
    selection_path.write_text(
        f"""# Step 20 Variant Selection

Run id: `{run_id}`

Selection data: `MAR` dev only.

Final data access: `NO_ACT_FINAL_ACCESS`.

Selected variant: `{best_variant['variant_id']}`

Selected checkpoint: `{best_seed_row['checkpoint_path']}`

| Metric | Value |
| --- | --- |
| repair gate | `{'PASS' if repair_gate else 'FAIL'}` |
| passing variants | `{len(passing_variants)}/{len(variants)}` |
| selected mode | `{best_variant['mode']}` |
| selected learning rate | `{best_variant['learning_rate']}` |
| selected mean added delta | `{best_variant['mean_added_delta']}` |
| selected mean base delta | `{best_variant['mean_base_delta']}` |
| selected mean all delta | `{best_variant['mean_all_delta']}` |
| selected seed | `{best_seed_row['seed']}` |
| selected final added loss | `{best_seed_row['final_added_loss']}` |
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
    ]
    write_tsv(access_path, access_rows, ["run_id", "input_role", "path", "allowed_split", "rows_or_files", "md5", "final_access", "status"])

    results_path.write_text(
        f"""# Step 20 Results: V2 Staged Added-Token Repair Grid

Status: COMPLETED

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Artifact gate status: {'PASS' if artifact_gate else 'FAIL'}

Repair gate status: {'PASS' if repair_gate else 'FAIL'}

## Summary

Step 20 tests added-token-only repair variants from the Step15 adapted checkpoints. It uses train text and Mark/dev only. ACT final was not read.

| Metric | Value |
| --- | ---: |
| configured variants | {len(variants)} |
| completed variant/seed runs | {completed}/{expected_runs} |
| passing variants | {len(passing_variants)}/{len(variants)} |
| trainable audit failures | {max_trainable_fail} |
| selected variant | {best_variant['variant_id']} |
| selected mean added delta | {best_variant['mean_added_delta']} |
| selected mean base delta | {best_variant['mean_base_delta']} |
| selected mean all delta | {best_variant['mean_all_delta']} |

## Interpretation

If repair gate passes, rerun Step15/Step16 style original-control comparisons with the selected variant family before downstream or translation final readout. If repair gate fails, added-token repair remains unresolved and model-dependent positive claims remain blocked.

## Failure Return

Failed gate: {'NOT_APPLICABLE' if repair_gate else 'staged_added_token_repair_gate'}

Observed evidence: {'NOT_APPLICABLE' if repair_gate else f"passing_variants={len(passing_variants)}/{len(variants)}; selected_mean_added_delta={best_variant['mean_added_delta']}"}

Return-to step: {'NOT_APPLICABLE' if repair_gate else '14_v2_embedding_init or 15_v2_mlm_control'}

Required fix: {'NOT_APPLICABLE' if repair_gate else 'revisit initialization, token objective, or explicitly downgrade model-dependent claim'}

Runtime minutes: {(time.time() - start) / 60.0:.3f}
""",
        encoding="utf-8",
    )
    file_rows = [
        step18.file_result("score_table", score_path, "repair gate table"),
        step18.file_result("staged_repair_summary", summary_path, "per-variant per-seed repair summary"),
        step18.file_result("staged_category_loss", category_path, "source/final category losses"),
        step18.file_result("staged_learning_curves", curves_path, "source/final category curves"),
        step18.file_result("trainable_parameters", trainable_path, "trainable parameter and row-delta audit"),
        step18.file_result("variant_summary", variants_path, "per-variant aggregate gates"),
        step18.file_result("variant_selection", selection_path, "selected repair variant/checkpoint"),
        step18.file_result("no_final_access_audit", access_path, "input access audit"),
        step18.file_result("results", results_path, "step result summary"),
    ]
    for checkpoint_dir in checkpoint_dirs:
        file_rows.append(step18.file_result(f"checkpoint_{checkpoint_dir.parent.name}_{checkpoint_dir.name}", checkpoint_dir, "staged repair checkpoint"))
    write_tsv(file_results_path, file_rows, ["file_role", "path", "rows_or_files", "bytes", "md5", "status", "notes"])

    print(f"run_id={run_id}")
    print(f"artifact_gate_status={'PASS' if artifact_gate else 'FAIL'}")
    print(f"repair_gate_status={'PASS' if repair_gate else 'FAIL'}")
    print(f"passing_variants={len(passing_variants)}/{len(variants)}")
    print(f"selected_variant={best_variant['variant_id']}")
    print(f"selected_checkpoint={best_seed_row['checkpoint_path']}")


if __name__ == "__main__":
    main()
