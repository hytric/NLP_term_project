#!/usr/bin/env python3
"""Run v2 MLM adaptation with an original XLM-R continued-pretraining control."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
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


FAMILIES = ("adapted_extended", "original_control")
SCORE_FIELDS = ["run_id", "gate_id", "criterion", "observed", "required", "status", "return_to", "notes"]
SUMMARY_FIELDS = [
    "run_id",
    "model_family",
    "seed",
    "source_checkpoint",
    "tokenizer_source",
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
    "checkpoint_saved",
    "status",
    "notes",
]
CURVE_FIELDS = [
    "run_id",
    "model_family",
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


def md5_file(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
    if path.suffix in {".md", ".json", ".txt"}:
        with path.open("r", encoding="utf-8") as f:
            return sum(1 for _ in f)
    return 1


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
    seeds = [int(item.strip()) for item in value.split(",") if item.strip()]
    if len(seeds) < 3:
        raise ValueError("Step 15 requires at least three seeds")
    return seeds


def read_lines(path: Path, limit: int) -> list[str]:
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


def load_selected_init(path: Path) -> tuple[str, Path]:
    method = "NOT_FOUND"
    checkpoint = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Selected init method:"):
            method = line.split("`", 2)[1]
        if line.startswith("Checkpoint path:"):
            checkpoint = Path(line.split("`", 2)[1])
    if checkpoint is None:
        raise RuntimeError("selected Step 14 checkpoint path not found")
    return method, checkpoint


def make_training_order(num_texts: int, total_examples: int, seed: int) -> list[int]:
    order: list[int] = []
    epoch = 0
    while len(order) < total_examples:
        generator = torch.Generator()
        generator.manual_seed(seed + epoch * 7919)
        order.extend(torch.randperm(num_texts, generator=generator).tolist())
        epoch += 1
    return order[:total_examples]


def mean_float(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def pseudo_ppl(loss: float) -> float:
    return math.exp(min(loss, 20.0))


def make_masked_batch(tokenizer, texts: list[str], device: torch.device, max_length: int, seed: int) -> tuple[dict[str, torch.Tensor], int, int]:
    encoded = tokenizer(texts, padding=True, truncation=True, max_length=max_length, return_tensors="pt")
    input_ids = encoded["input_ids"]
    attention_mask = encoded["attention_mask"]
    labels = input_ids.clone()
    generator = torch.Generator()
    generator.manual_seed(seed)
    probability = torch.full(labels.shape, 0.15)
    special_mask = torch.zeros_like(labels, dtype=torch.bool)
    for special_id in tokenizer.all_special_ids:
        special_mask |= labels.eq(special_id)
    special_mask |= attention_mask.eq(0)
    probability.masked_fill_(special_mask, 0.0)
    masked = torch.bernoulli(probability, generator=generator).bool()
    if masked.sum().item() == 0:
        available = (special_mask == 0).nonzero(as_tuple=False)
        if len(available) > 0:
            masked[available[0, 0], available[0, 1]] = True
    labels[~masked] = -100
    input_ids[masked] = tokenizer.mask_token_id
    batch = {
        "input_ids": input_ids.to(device),
        "attention_mask": attention_mask.to(device),
        "labels": labels.to(device),
    }
    return batch, int(masked.sum().item()), int(attention_mask.sum().item())


def evaluate(model, tokenizer, texts: list[str], device: torch.device, batch_size: int, max_length: int, seed: int) -> tuple[float, int]:
    model.eval()
    weighted_loss = 0.0
    total_masked = 0
    with torch.no_grad():
        for start in range(0, len(texts), batch_size):
            batch_texts = texts[start : start + batch_size]
            batch, masked_count, _ = make_masked_batch(tokenizer, batch_texts, device, max_length, seed + start)
            outputs = model(**batch)
            weighted_loss += float(outputs.loss.item()) * masked_count
            total_masked += masked_count
    return weighted_loss / max(1, total_masked), total_masked


def load_family(family: str, args: argparse.Namespace, adapted_checkpoint: Path):
    if family == "adapted_extended":
        source = adapted_checkpoint
        tokenizer = XLMRobertaTokenizer.from_pretrained(str(source), local_files_only=True)
        model = AutoModelForMaskedLM.from_pretrained(str(source), local_files_only=True)
        return model, tokenizer, str(source), str(source)
    if family == "original_control":
        tokenizer = XLMRobertaTokenizer.from_pretrained(args.base_model, local_files_only=True)
        model = AutoModelForMaskedLM.from_pretrained(args.base_model, local_files_only=True)
        return model, tokenizer, args.base_model, args.base_model
    raise ValueError(f"unknown family: {family}")


def write_run_config(config_dir: Path, run_id: str, family: str, seed: int, source: str, tokenizer_source: str, args: argparse.Namespace) -> None:
    payload = {
        "run_id": run_id,
        "model_family": family,
        "seed": seed,
        "source_checkpoint": source,
        "tokenizer_source": tokenizer_source,
        "train_steps": args.train_steps,
        "target_train_tokens": args.target_train_tokens,
        "token_budget_tolerance": args.token_budget_tolerance,
        "batch_size": args.batch_size,
        "eval_batch_size": args.eval_batch_size,
        "max_length": args.max_length,
        "learning_rate": args.learning_rate,
        "eval_every": args.eval_every,
        "train_limit": args.train_limit,
        "dev_limit": args.dev_limit,
        "selection_data": "MAR_dev_only",
        "final_access": "NO_ACT_FINAL_ACCESS",
    }
    (config_dir / f"{family}_seed{seed}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def train_one(
    family: str,
    seed: int,
    run_id: str,
    train_texts: list[str],
    dev_texts: list[str],
    device: torch.device,
    args: argparse.Namespace,
    adapted_checkpoint: Path,
    checkpoint_root: Path,
    config_dir: Path,
) -> tuple[dict[str, str], list[dict[str, str]], Path]:
    torch.manual_seed(seed)
    model, tokenizer, source, tokenizer_source = load_family(family, args, adapted_checkpoint)
    write_run_config(config_dir, run_id, family, seed, source, tokenizer_source, args)
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate)
    curves: list[dict[str, str]] = []
    start_time = time.time()
    train_examples_seen = 0
    train_tokens_seen = 0
    losses_all: list[float] = []
    losses_since_eval: list[float] = []

    zero_loss, zero_masked = evaluate(model, tokenizer, dev_texts, device, args.eval_batch_size, args.max_length, seed + 100000)
    curves.append(
        {
            "run_id": run_id,
            "model_family": family,
            "seed": str(seed),
            "stage": "zero_step",
            "step": "0",
            "train_examples_seen": "0",
            "train_tokens_seen": "0",
            "eval_rows": str(len(dev_texts)),
            "eval_masked_tokens": str(zero_masked),
            "dev_loss": f"{zero_loss:.6f}",
            "pseudo_ppl": f"{pseudo_ppl(zero_loss):.6f}",
            "train_loss_mean_since_eval": "NOT_APPLICABLE",
            "learning_rate": f"{args.learning_rate:.8f}",
            "status": "PASS",
            "notes": "zero_step_mark_dev_only",
        }
    )

    model.train()
    order = make_training_order(len(train_texts), args.train_steps * args.batch_size, seed)
    final_loss = zero_loss
    final_masked = zero_masked
    final_step = 0
    last_eval_step = 0
    for step in range(1, args.train_steps + 1):
        indices = order[(step - 1) * args.batch_size : step * args.batch_size]
        batch_texts = [train_texts[index] for index in indices]
        batch, _, token_count = make_masked_batch(tokenizer, batch_texts, device, args.max_length, seed * 100000 + step)
        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)
        train_loss = float(loss.item())
        losses_all.append(train_loss)
        losses_since_eval.append(train_loss)
        train_examples_seen += len(batch_texts)
        train_tokens_seen += token_count
        final_step = step

        if step % args.eval_every == 0 or step == args.train_steps:
            final_loss, final_masked = evaluate(model, tokenizer, dev_texts, device, args.eval_batch_size, args.max_length, seed + 100000 + step * 1000)
            last_eval_step = step
            curves.append(
                {
                    "run_id": run_id,
                    "model_family": family,
                    "seed": str(seed),
                    "stage": "dev_eval",
                    "step": str(step),
                    "train_examples_seen": str(train_examples_seen),
                    "train_tokens_seen": str(train_tokens_seen),
                    "eval_rows": str(len(dev_texts)),
                    "eval_masked_tokens": str(final_masked),
                    "dev_loss": f"{final_loss:.6f}",
                    "pseudo_ppl": f"{pseudo_ppl(final_loss):.6f}",
                    "train_loss_mean_since_eval": f"{mean_float(losses_since_eval):.6f}",
                    "learning_rate": f"{args.learning_rate:.8f}",
                    "status": "PASS",
                    "notes": "scheduled_mark_dev_eval",
                }
            )
            losses_since_eval = []
            model.train()
        if args.target_train_tokens > 0 and train_tokens_seen >= args.target_train_tokens:
            break

    if final_step > 0 and last_eval_step != final_step:
        final_loss, final_masked = evaluate(model, tokenizer, dev_texts, device, args.eval_batch_size, args.max_length, seed + 100000 + final_step * 1000)
        curves.append(
            {
                "run_id": run_id,
                "model_family": family,
                "seed": str(seed),
                "stage": "final_token_budget_eval",
                "step": str(final_step),
                "train_examples_seen": str(train_examples_seen),
                "train_tokens_seen": str(train_tokens_seen),
                "eval_rows": str(len(dev_texts)),
                "eval_masked_tokens": str(final_masked),
                "dev_loss": f"{final_loss:.6f}",
                "pseudo_ppl": f"{pseudo_ppl(final_loss):.6f}",
                "train_loss_mean_since_eval": f"{mean_float(losses_since_eval):.6f}",
                "learning_rate": f"{args.learning_rate:.8f}",
                "status": "PASS",
                "notes": "final_mark_dev_eval_after_token_budget",
            }
        )

    runtime = time.time() - start_time
    out_dir = checkpoint_root / f"{family}_seed{seed}"
    out_dir.mkdir(parents=True, exist_ok=True)
    model.to("cpu")
    model.save_pretrained(out_dir)
    tokenizer.save_pretrained(out_dir)
    report = {
        "run_id": run_id,
        "model_family": family,
        "seed": seed,
        "source_checkpoint": source,
        "tokenizer_source": tokenizer_source,
        "train_steps": args.train_steps,
        "target_train_tokens": args.target_train_tokens,
        "actual_train_steps": final_step,
        "train_examples_seen": train_examples_seen,
        "train_tokens_seen": train_tokens_seen,
        "zero_step_dev_loss": zero_loss,
        "final_dev_loss": final_loss,
        "dev_loss_delta": final_loss - zero_loss,
        "selection_data": "MAR_dev_only",
        "final_access": "NO_ACT_FINAL_ACCESS",
    }
    (out_dir / "v2_mlm_control_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    del model

    delta = final_loss - zero_loss
    status = "PASS" if family == "adapted_extended" and delta < 0 else "CONTROL_COMPLETE"
    if family == "adapted_extended" and delta >= 0:
        status = "NO_IMPROVEMENT"
    summary = {
        "run_id": run_id,
        "model_family": family,
        "seed": str(seed),
        "source_checkpoint": source,
        "tokenizer_source": tokenizer_source,
        "train_steps": str(args.train_steps),
        "actual_train_steps": str(final_step),
        "target_train_tokens": str(args.target_train_tokens),
        "batch_size": str(args.batch_size),
        "max_length": str(args.max_length),
        "learning_rate": f"{args.learning_rate:.8f}",
        "train_rows_available": str(len(train_texts)),
        "train_examples_seen": str(train_examples_seen),
        "train_tokens_seen": str(train_tokens_seen),
        "token_budget_status": "PASS" if args.target_train_tokens <= 0 or train_tokens_seen >= args.target_train_tokens else "FAIL",
        "zero_step_dev_loss": f"{zero_loss:.6f}",
        "final_dev_loss": f"{final_loss:.6f}",
        "dev_loss_delta": f"{delta:.6f}",
        "relative_loss_delta_pct": f"{(delta / zero_loss) * 100.0:.6f}",
        "mean_train_loss": f"{mean_float(losses_all):.6f}",
        "runtime_minutes": f"{runtime / 60.0:.3f}",
        "tokens_per_sec": f"{train_tokens_seen / max(1e-6, runtime):.3f}",
        "checkpoint_path": str(out_dir),
        "checkpoint_saved": "yes",
        "status": status,
        "notes": f"actual_steps={final_step}; mark_dev_only_selection; no_ACT_final_access",
    }
    return summary, curves, out_dir


def aggregate(rows: list[dict[str, str]], family: str, column: str) -> tuple[float, float]:
    values = [float(row[column]) for row in rows if row["model_family"] == family]
    mean = statistics.mean(values)
    std = statistics.pstdev(values) if len(values) > 1 else 0.0
    return mean, std


def update_matrix(path: Path, claim_gate: bool) -> None:
    if not path.exists():
        return
    with path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
        fieldnames = rows[0].keys() if rows else []
    for row in rows:
        if row.get("stage_id") == "V2_03_MLM_CONTROL":
            row["status"] = "DONE_PASS" if claim_gate else "DONE_FAIL_CLAIM"
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def update_followups(path: Path, artifact_gate: bool, claim_gate: bool, adapted_all_improved: bool, competitive: bool) -> None:
    if not path.exists():
        return
    with path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
        fieldnames = rows[0].keys() if rows else []
    if claim_gate:
        status = "DONE_PASS"
    elif artifact_gate and adapted_all_improved and not competitive:
        status = "DONE_FAIL_NOT_COMPETITIVE"
    elif artifact_gate:
        status = "DONE_FAIL"
    else:
        status = "RUN_INCOMPLETE"
    for row in rows:
        if row.get("followup_id") == "F01_longer_mlm_control":
            row["status"] = status
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def build_step(args: argparse.Namespace) -> None:
    transformers_logging.set_verbosity_error()
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    torch.backends.cuda.matmul.allow_tf32 = True
    start = time.time()
    run_id = "step15_v2_mlm_control_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    seeds = parse_int_list(args.seeds)
    step_dir = Path(args.step_dir).resolve()
    checkpoint_root = Path(args.checkpoint_root).resolve()
    config_dir = step_dir / "training_configs"
    checkpoint_root.mkdir(parents=True, exist_ok=True)
    config_dir.mkdir(parents=True, exist_ok=True)

    selected_method, adapted_checkpoint = load_selected_init(Path(args.selected_init))
    train_texts = read_lines(Path(args.train_text), args.train_limit)
    dev_texts = read_lines(Path(args.dev_text), args.dev_limit)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    common_config = {
        "run_id": run_id,
        "families": list(FAMILIES),
        "seeds": seeds,
        "selected_init_method": selected_method,
        "selected_init_checkpoint": str(adapted_checkpoint),
        "train_text": str(Path(args.train_text).resolve()),
        "dev_text": str(Path(args.dev_text).resolve()),
        "train_rows_loaded": len(train_texts),
        "dev_rows_loaded": len(dev_texts),
        "train_steps": args.train_steps,
        "target_train_tokens": args.target_train_tokens,
        "batch_size": args.batch_size,
        "eval_batch_size": args.eval_batch_size,
        "max_length": args.max_length,
        "learning_rate": args.learning_rate,
        "eval_every": args.eval_every,
        "competitive_margin": args.competitive_margin,
        "token_budget_tolerance": args.token_budget_tolerance,
        "device": str(device),
        "selection_data": "MAR_dev_only",
        "final_access": "NO_ACT_FINAL_ACCESS",
    }
    (config_dir / "common_config.json").write_text(json.dumps(common_config, ensure_ascii=False, indent=2), encoding="utf-8")

    summary_rows: list[dict[str, str]] = []
    curve_rows: list[dict[str, str]] = []
    checkpoint_dirs: list[Path] = []
    for seed in seeds:
        for family in FAMILIES:
            print(f"running family={family} seed={seed}", flush=True)
            summary, curves, checkpoint_dir = train_one(
                family,
                seed,
                run_id,
                train_texts,
                dev_texts,
                device,
                args,
                adapted_checkpoint,
                checkpoint_root,
                config_dir,
            )
            summary_rows.append(summary)
            curve_rows.extend(curves)
            checkpoint_dirs.append(checkpoint_dir)

    required_runs = len(FAMILIES) * len(seeds)
    completed_runs = len(summary_rows)
    adapted_rows = [row for row in summary_rows if row["model_family"] == "adapted_extended"]
    original_rows = [row for row in summary_rows if row["model_family"] == "original_control"]
    adapted_improved = sum(1 for row in adapted_rows if row["status"] == "PASS")
    original_complete = sum(1 for row in original_rows if row["status"] == "CONTROL_COMPLETE")
    adapted_mean, adapted_std = aggregate(summary_rows, "adapted_extended", "final_dev_loss")
    original_mean, original_std = aggregate(summary_rows, "original_control", "final_dev_loss")
    ratio = adapted_mean / original_mean if original_mean > 0 else float("inf")
    competitive = ratio <= args.competitive_margin
    adapted_all_improved = adapted_improved == len(seeds)
    token_counts = [int(row["train_tokens_seen"]) for row in summary_rows]
    min_tokens = min(token_counts) if token_counts else 0
    max_tokens = max(token_counts) if token_counts else 0
    token_ratio = max_tokens / max(1, min_tokens)
    token_budget_all = all(row["token_budget_status"] == "PASS" for row in summary_rows)
    token_budget_matched = args.target_train_tokens <= 0 or (token_budget_all and token_ratio <= args.token_budget_tolerance)
    artifact_gate = completed_runs == required_runs and original_complete == len(seeds) and token_budget_matched
    claim_gate = artifact_gate and adapted_all_improved and competitive

    selected_adapted = sorted(adapted_rows, key=lambda row: float(row["final_dev_loss"]))[0]
    selected_original = sorted(original_rows, key=lambda row: float(row["final_dev_loss"]))[0]

    score_rows = [
        {
            "run_id": run_id,
            "gate_id": "G01_required_runs",
            "criterion": "all model-family/seed runs complete",
            "observed": f"{completed_runs}/{required_runs}",
            "required": f"{required_runs}/{required_runs}",
            "status": "PASS" if completed_runs == required_runs else "FAIL",
            "return_to": "15_v2_mlm_control",
            "notes": "2 families x >=3 seeds",
        },
        {
            "run_id": run_id,
            "gate_id": "G02_seed_count",
            "criterion": "at least three seeds per family",
            "observed": f"{len(seeds)}",
            "required": ">=3",
            "status": "PASS" if len(seeds) >= 3 else "FAIL",
            "return_to": "15_v2_mlm_control",
            "notes": ",".join(str(seed) for seed in seeds),
        },
        {
            "run_id": run_id,
            "gate_id": "G03_no_final_access",
            "criterion": "ACT final data not read",
            "observed": "NO_ACT_FINAL_ACCESS",
            "required": "NO_ACT_FINAL_ACCESS",
            "status": "PASS",
            "return_to": "12_v2_split_protocol",
            "notes": "train txt and Mark/dev txt only",
        },
        {
            "run_id": run_id,
            "gate_id": "G04_adapted_improves",
            "criterion": "adapted checkpoint improves over zero-step in every seed",
            "observed": f"{adapted_improved}/{len(seeds)}",
            "required": f"{len(seeds)}/{len(seeds)}",
            "status": "PASS" if adapted_all_improved else "FAIL",
            "return_to": "14_v2_embedding_init",
            "notes": "self-comparison within adapted tokenizer",
        },
        {
            "run_id": run_id,
            "gate_id": "G05_original_control_complete",
            "criterion": "original XLM-R continued-pretraining control completes every seed",
            "observed": f"{original_complete}/{len(seeds)}",
            "required": f"{len(seeds)}/{len(seeds)}",
            "status": "PASS" if original_complete == len(seeds) else "FAIL",
            "return_to": "15_v2_mlm_control",
            "notes": "control checkpoints saved",
        },
        {
            "run_id": run_id,
            "gate_id": "G06_competitive_control",
            "criterion": "adapted mean final dev loss is within configured control margin",
            "observed": f"ratio={ratio:.6f}; adapted_mean={adapted_mean:.6f}; original_mean={original_mean:.6f}",
            "required": f"ratio<={args.competitive_margin:.6f}",
            "status": "PASS" if competitive else "FAIL",
            "return_to": "15_v2_mlm_control",
            "notes": "diagnostic because tokenizer vocabularies differ",
        },
        {
            "run_id": run_id,
            "gate_id": "G07_token_budget_match",
            "criterion": "all family/seed runs use matched train token budget",
            "observed": f"min_tokens={min_tokens}; max_tokens={max_tokens}; token_ratio={token_ratio:.6f}; target={args.target_train_tokens}",
            "required": f"token_ratio<={args.token_budget_tolerance:.6f}" if args.target_train_tokens > 0 else "fixed-step run; diagnostic only",
            "status": "PASS" if token_budget_matched else "FAIL",
            "return_to": "15_v2_mlm_control",
            "notes": "token-matched control prevents original tokenizer from seeing more train tokens",
        },
        {
            "run_id": run_id,
            "gate_id": "G08_checkpoint_selection",
            "criterion": "selected adapted and original-control checkpoints are recorded",
            "observed": f"adapted={selected_adapted['checkpoint_path']}; original={selected_original['checkpoint_path']}",
            "required": "two checkpoint paths",
            "status": "PASS",
            "return_to": "15_v2_mlm_control",
            "notes": "selection uses Mark/dev only",
        },
    ]

    score_path = step_dir / "score_table.tsv"
    summary_path = step_dir / "seed_summary.tsv"
    curves_path = step_dir / "mlm_learning_curves.tsv"
    selection_path = step_dir / "checkpoint_selection.md"
    access_path = step_dir / "v2_no_final_access_audit.tsv"
    results_path = step_dir / "results.md"
    file_results_path = step_dir / "file_results.tsv"

    write_tsv(score_path, score_rows, SCORE_FIELDS)
    write_tsv(summary_path, summary_rows, SUMMARY_FIELDS)
    write_tsv(curves_path, curve_rows, CURVE_FIELDS)

    selection_path.write_text(
        f"""# Step 15 Checkpoint Selection

Run id: `{run_id}`

Selection data: `MAR` dev only.

Final data access: `NO_ACT_FINAL_ACCESS`.

## Selected Adapted Checkpoint

| Metric | Value |
| --- | --- |
| model family | `{selected_adapted['model_family']}` |
| seed | `{selected_adapted['seed']}` |
| checkpoint | `{selected_adapted['checkpoint_path']}` |
| zero-step dev loss | `{selected_adapted['zero_step_dev_loss']}` |
| final dev loss | `{selected_adapted['final_dev_loss']}` |
| delta | `{selected_adapted['dev_loss_delta']}` |
| status | `{selected_adapted['status']}` |

## Selected Original-Control Checkpoint

| Metric | Value |
| --- | --- |
| model family | `{selected_original['model_family']}` |
| seed | `{selected_original['seed']}` |
| checkpoint | `{selected_original['checkpoint_path']}` |
| zero-step dev loss | `{selected_original['zero_step_dev_loss']}` |
| final dev loss | `{selected_original['final_dev_loss']}` |
| delta | `{selected_original['dev_loss_delta']}` |
| status | `{selected_original['status']}` |

## Aggregate Diagnostic

| Metric | Value |
| --- | --- |
| adapted mean final dev loss | `{adapted_mean:.6f}` |
| adapted std final dev loss | `{adapted_std:.6f}` |
| original-control mean final dev loss | `{original_mean:.6f}` |
| original-control std final dev loss | `{original_std:.6f}` |
| adapted/original ratio | `{ratio:.6f}` |
| competitive margin | `{args.competitive_margin:.6f}` |
| token budget target | `{args.target_train_tokens}` |
| train token range | `{min_tokens}-{max_tokens}` |
| token budget tolerance | `{args.token_budget_tolerance:.6f}` |
| claim gate | `{'PASS' if claim_gate else 'FAIL'}` |

The loss ratio is diagnostic because tokenizer vocabularies differ. The selected checkpoints still require downstream and translation validation before any final top-tier claim.
""",
        encoding="utf-8",
    )

    access_rows = [
        {
            "run_id": run_id,
            "input_role": "selected_init",
            "path": str(Path(args.selected_init).resolve()),
            "allowed_split": "selected_on_MAR_dev",
            "rows_or_files": str(count_rows(Path(args.selected_init))),
            "md5": md5_file(Path(args.selected_init)),
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
        f"""# Step 15 Results: V2 MLM Control

Status: COMPLETED

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Artifact gate status: {'PASS' if artifact_gate else 'FAIL'}

Claim gate status: {'PASS' if claim_gate else 'FAIL'}

## Summary

Step 15 trained the Step 14 selected adapted checkpoint and an original `xlm-roberta-base` continued-pretraining control on v2 train text. Selection and diagnostics used Mark/dev only. ACT final was not read.

| Metric | Value |
| --- | --- |
| seeds | {','.join(str(seed) for seed in seeds)} |
| train rows loaded | {len(train_texts)} |
| dev rows loaded | {len(dev_texts)} |
| train steps per run | {args.train_steps} |
| target train tokens | {args.target_train_tokens} |
| batch size | {args.batch_size} |
| eval batch size | {args.eval_batch_size} |
| selected Step 14 init | {selected_method} |
| adapted improved seeds | {adapted_improved}/{len(seeds)} |
| original-control completed seeds | {original_complete}/{len(seeds)} |
| adapted mean final dev loss | {adapted_mean:.6f} |
| original-control mean final dev loss | {original_mean:.6f} |
| adapted/original diagnostic ratio | {ratio:.6f} |
| train token range | {min_tokens}-{max_tokens} |
| token budget matched | {'yes' if token_budget_matched else 'no'} |

## Gate Evidence

- `score_table.tsv` records every gate and return target.
- `seed_summary.tsv` records every family/seed result.
- `mlm_learning_curves.tsv` records zero-step and scheduled Mark/dev evaluations.
- `checkpoint_selection.md` records both selected checkpoints using Mark/dev only.
- `v2_no_final_access_audit.tsv` lists only train/dev inputs and reports no final access.

## Failure Return

Failed gate: {'NOT_APPLICABLE' if claim_gate else 'v2_mlm_control_claim_gate'}

Observed evidence: {'NOT_APPLICABLE' if claim_gate else f'adapted_improved={adapted_improved}/{len(seeds)}, diagnostic_ratio={ratio:.6f}, margin={args.competitive_margin:.6f}, token_ratio={token_ratio:.6f}'}

Likely cause: {'NOT_APPLICABLE' if claim_gate else 'adapted MLM control is not yet strong enough for a top-tier model-dependent claim'}

Return-to step: {'NOT_APPLICABLE' if claim_gate else '15_v2_mlm_control or 14_v2_embedding_init'}

Required fix: {'NOT_APPLICABLE' if claim_gate else 'increase adaptation budget, revisit initialization, or downgrade final claim before downstream/translation'}

Runtime minutes: {(time.time() - start) / 60.0:.3f}
""",
        encoding="utf-8",
    )

    file_rows = [
        file_result("score_table", score_path, "gate table"),
        file_result("seed_summary", summary_path, "per-family/per-seed summary"),
        file_result("mlm_learning_curves", curves_path, "scheduled Mark/dev learning curves"),
        file_result("checkpoint_selection", selection_path, "selected checkpoints"),
        file_result("no_final_access_audit", access_path, "train/dev-only access audit"),
        file_result("training_configs", config_dir, "common and per-run configs"),
        file_result("results", results_path, "step result summary"),
    ]
    for checkpoint_dir in checkpoint_dirs:
        file_rows.append(file_result(f"checkpoint_{checkpoint_dir.name}", checkpoint_dir, "trained v2 MLM checkpoint"))
    write_tsv(file_results_path, file_rows, ["file_role", "path", "rows_or_files", "bytes", "md5", "status", "notes"])

    update_matrix(Path(args.execution_matrix), claim_gate)
    update_followups(Path(args.required_followups), artifact_gate, claim_gate, adapted_all_improved, competitive)

    print(f"run_id={run_id}")
    print(f"artifact_gate_status={'PASS' if artifact_gate else 'FAIL'}")
    print(f"claim_gate_status={'PASS' if claim_gate else 'FAIL'}")
    print(f"adapted_improved={adapted_improved}/{len(seeds)}")
    print(f"original_complete={original_complete}/{len(seeds)}")
    print(f"diagnostic_ratio={ratio:.6f}")
    print(f"selected_adapted={selected_adapted['checkpoint_path']}")
    print(f"selected_original={selected_original['checkpoint_path']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--checkpoint-root", default="/home/axt/mnt2/jongha/second_try/checkpoints/15_v2_mlm_control")
    parser.add_argument("--selected-init", default="docs/exp/second_try/14_v2_embedding_init/selected_init.md")
    parser.add_argument("--train-text", default="/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_tokenizer_mlm_train.txt")
    parser.add_argument("--dev-text", default="/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_mlm_dev_mark.txt")
    parser.add_argument("--execution-matrix", default="docs/exp/second_try/12_v2_split_protocol/v2_execution_matrix.tsv")
    parser.add_argument("--required-followups", default="docs/exp/second_try/09_top_tier_validation/required_followups.tsv")
    parser.add_argument("--base-model", default="xlm-roberta-base")
    parser.add_argument("--seeds", default="13,17,23")
    parser.add_argument("--train-limit", type=int, default=0)
    parser.add_argument("--dev-limit", type=int, default=0)
    parser.add_argument("--train-steps", type=int, default=300)
    parser.add_argument("--target-train-tokens", type=int, default=0)
    parser.add_argument("--token-budget-tolerance", type=float, default=1.02)
    parser.add_argument("--eval-every", type=int, default=150)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--eval-batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--learning-rate", type=float, default=5e-5)
    parser.add_argument("--competitive-margin", type=float, default=1.10)
    args = parser.parse_args()
    build_step(args)


if __name__ == "__main__":
    main()
