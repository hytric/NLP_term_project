#!/usr/bin/env python3
"""Train an added-token-focused repair for the v2 adapted checkpoint."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import torch
import torch.nn.functional as F
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
    "seed",
    "source_checkpoint",
    "train_steps_limit",
    "actual_train_steps",
    "target_train_tokens",
    "train_tokens_seen",
    "batch_size",
    "learning_rate",
    "base_mask_prob",
    "added_mask_prob",
    "base_loss_weight",
    "added_loss_weight",
    "zero_all_loss",
    "final_all_loss",
    "baseline_all_loss",
    "all_loss_delta_vs_baseline",
    "zero_base_loss",
    "final_base_loss",
    "baseline_base_loss",
    "base_loss_delta_vs_baseline",
    "zero_added_loss",
    "final_added_loss",
    "baseline_added_loss",
    "added_loss_delta_vs_baseline",
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


def md5_file(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


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
        "status": "PASS" if size > 0 else "FAIL",
        "notes": notes,
    }


def load_selected_init(path: Path) -> Path:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Checkpoint path:"):
            return Path(line.split("`", 2)[1])
    raise RuntimeError("selected init checkpoint not found")


def read_train_lines(path: Path, limit: int) -> list[str]:
    texts = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            text = line.rstrip("\n")
            if text.strip():
                texts.append(text)
            if limit > 0 and len(texts) >= limit:
                break
    return texts


def read_dev_texts(path: Path, limit: int) -> list[str]:
    rows = read_tsv(path)
    texts = []
    for row in rows:
        if row["v2_split"] != "dev" or row["book"] != "MAR":
            raise RuntimeError(f"non-dev row in dev manifest: {row.get('verse_id')}")
        texts.append(row["text"])
        if limit > 0 and len(texts) >= limit:
            break
    return texts


def load_baseline_category(path: Path) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = defaultdict(dict)
    for row in read_tsv(path):
        if row["model_family"] != "adapted_extended":
            continue
        if row["category"] not in {"all", "base", "added"}:
            continue
        out[row["seed"]][row["category"]] = float(row["mean_loss"])
    if len(out) != 3:
        raise RuntimeError("expected three adapted baseline seeds in Step17 category loss")
    return out


def make_order(num_texts: int, max_examples: int, seed: int) -> list[int]:
    order = []
    epoch = 0
    while len(order) < max_examples:
        generator = torch.Generator()
        generator.manual_seed(seed + epoch * 7919)
        order.extend(torch.randperm(num_texts, generator=generator).tolist())
        epoch += 1
    return order[:max_examples]


def special_mask_for(tokenizer, labels: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
    special_mask = torch.zeros_like(labels, dtype=torch.bool)
    for special_id in tokenizer.all_special_ids:
        special_mask |= labels.eq(special_id)
    special_mask |= attention_mask.eq(0)
    return special_mask


def make_train_batch(tokenizer, texts: list[str], device: torch.device, max_length: int, seed: int, base_vocab_size: int, base_prob: float, added_prob: float):
    encoded = tokenizer(texts, padding=True, truncation=True, max_length=max_length, return_tensors="pt")
    input_ids = encoded["input_ids"]
    attention_mask = encoded["attention_mask"]
    labels = input_ids.clone()
    special_mask = special_mask_for(tokenizer, labels, attention_mask)
    added_positions = labels.ge(base_vocab_size) & (~special_mask)
    generator = torch.Generator()
    generator.manual_seed(seed)
    probability = torch.full(labels.shape, base_prob)
    probability[added_positions] = added_prob
    probability.masked_fill_(special_mask, 0.0)
    masked = torch.bernoulli(probability, generator=generator).bool()
    if masked.sum().item() == 0:
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


def weighted_mlm_loss(logits: torch.Tensor, labels: torch.Tensor, base_vocab_size: int, base_weight: float, added_weight: float) -> torch.Tensor:
    losses = F.cross_entropy(
        logits.view(-1, logits.shape[-1]),
        labels.view(-1),
        reduction="none",
        ignore_index=-100,
    ).view(labels.shape)
    mask = labels.ne(-100)
    weights = torch.ones_like(losses)
    weights[labels.ge(base_vocab_size)] = added_weight
    weights[labels.lt(base_vocab_size)] = base_weight
    weights = weights * mask.float()
    return (losses * weights).sum() / torch.clamp(weights.sum(), min=1.0)


def blank_stats() -> dict[str, float]:
    return {"loss_sum": 0.0, "masked": 0.0, "non_special": 0.0}


def safe_mean(stats: dict[str, float]) -> str:
    if stats["masked"] <= 0:
        return "NOT_APPLICABLE"
    return f"{stats['loss_sum'] / stats['masked']:.6f}"


def pct(num: float, den: float) -> str:
    if den <= 0:
        return "0.000000"
    return f"{100.0 * num / den:.6f}"


def evaluate_categories(model, tokenizer, texts: list[str], device: torch.device, args: argparse.Namespace, base_vocab_size: int, seed: int, run_id: str, checkpoint_path: str, stage: str) -> list[dict[str, str]]:
    stats = {"all": blank_stats(), "base": blank_stats(), "added": blank_stats()}
    model.eval()
    with torch.no_grad():
        for start in range(0, len(texts), args.eval_batch_size):
            batch_texts = texts[start : start + args.eval_batch_size]
            encoded = tokenizer(batch_texts, padding=True, truncation=True, max_length=args.max_length, return_tensors="pt")
            input_ids = encoded["input_ids"]
            attention_mask = encoded["attention_mask"]
            labels = input_ids.clone()
            special_mask = special_mask_for(tokenizer, labels, attention_mask)
            generator = torch.Generator()
            generator.manual_seed(args.seed + seed * 100000 + start)
            probability = torch.full(labels.shape, args.eval_mask_prob)
            probability.masked_fill_(special_mask, 0.0)
            masked = torch.bernoulli(probability, generator=generator).bool()
            labels[~masked] = -100
            input_ids = input_ids.clone()
            input_ids[masked] = tokenizer.mask_token_id
            batch = {
                "input_ids": input_ids.to(device),
                "attention_mask": attention_mask.to(device),
                "labels": labels.to(device),
            }
            outputs = model(**batch)
            losses = F.cross_entropy(
                outputs.logits.view(-1, outputs.logits.shape[-1]),
                batch["labels"].view(-1),
                reduction="none",
                ignore_index=-100,
            ).view(batch["labels"].shape).detach().cpu()
            labels = batch["labels"].detach().cpu()
            masked = labels.ne(-100)
            base_mask = masked & labels.lt(base_vocab_size)
            added_mask = masked & labels.ge(base_vocab_size)
            non_special = ~special_mask
            for name, mask in [("all", masked), ("base", base_mask), ("added", added_mask)]:
                if mask.any():
                    stats[name]["loss_sum"] += float(losses[mask].sum().item())
                    stats[name]["masked"] += float(mask.sum().item())
            stats["all"]["non_special"] += float(non_special.sum().item())
            stats["base"]["non_special"] += float((non_special & encoded["input_ids"].lt(base_vocab_size)).sum().item())
            stats["added"]["non_special"] += float((non_special & encoded["input_ids"].ge(base_vocab_size)).sum().item())
    all_loss_sum = stats["all"]["loss_sum"]
    total_non_special = stats["all"]["non_special"]
    rows = []
    for category, item in stats.items():
        rows.append(
            {
                "run_id": run_id,
                "seed": str(seed),
                "checkpoint_path": checkpoint_path,
                "stage": stage,
                "category": category,
                "non_special_tokens": str(int(item["non_special"])),
                "masked_tokens": str(int(item["masked"])),
                "mean_loss": safe_mean(item),
                "loss_share_pct": pct(item["loss_sum"], all_loss_sum),
                "token_share_pct": pct(item["non_special"], total_non_special),
                "status": "PASS",
            }
        )
    return rows


def cat_value(rows: list[dict[str, str]], stage: str, category: str) -> float:
    for row in rows:
        if row["stage"] == stage and row["category"] == category:
            if row["mean_loss"] == "NOT_APPLICABLE":
                return float("nan")
            return float(row["mean_loss"])
    raise KeyError((stage, category))


def train_seed(seed: int, run_id: str, source_checkpoint: Path, train_texts: list[str], dev_texts: list[str], baseline: dict[str, dict[str, float]], base_vocab_size: int, device: torch.device, args: argparse.Namespace, checkpoint_root: Path):
    torch.manual_seed(seed)
    tokenizer = XLMRobertaTokenizer.from_pretrained(str(source_checkpoint), local_files_only=True)
    model = AutoModelForMaskedLM.from_pretrained(str(source_checkpoint), local_files_only=True)
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate)
    checkpoint_path = checkpoint_root / f"added_weighted_seed{seed}"
    zero_rows = evaluate_categories(model, tokenizer, dev_texts, device, args, base_vocab_size, seed, run_id, str(source_checkpoint), "zero_step")
    curve_rows = [
        {
            "run_id": run_id,
            "seed": str(seed),
            "stage": "zero_step",
            "step": "0",
            "train_tokens_seen": "0",
            "all_loss": f"{cat_value(zero_rows, 'zero_step', 'all'):.6f}",
            "base_loss": f"{cat_value(zero_rows, 'zero_step', 'base'):.6f}",
            "added_loss": f"{cat_value(zero_rows, 'zero_step', 'added'):.6f}",
            "added_base_ratio": f"{cat_value(zero_rows, 'zero_step', 'added') / max(1e-12, cat_value(zero_rows, 'zero_step', 'base')):.6f}",
            "status": "PASS",
            "notes": "standard eval mask",
        }
    ]
    order = make_order(len(train_texts), args.train_steps * args.batch_size, seed)
    train_tokens = 0
    actual_steps = 0
    start_time = time.time()
    model.train()
    for step in range(1, args.train_steps + 1):
        batch_indices = order[(step - 1) * args.batch_size : step * args.batch_size]
        batch_texts = [train_texts[idx] for idx in batch_indices]
        batch, token_count = make_train_batch(
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
        loss = weighted_mlm_loss(outputs.logits, batch["labels"], base_vocab_size, args.base_loss_weight, args.added_loss_weight)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)
        train_tokens += token_count
        actual_steps = step
        if train_tokens >= args.target_train_tokens:
            break
    final_rows = evaluate_categories(model, tokenizer, dev_texts, device, args, base_vocab_size, seed, run_id, str(checkpoint_path), "final")
    checkpoint_path.mkdir(parents=True, exist_ok=True)
    model.to("cpu")
    model.save_pretrained(checkpoint_path)
    tokenizer.save_pretrained(checkpoint_path)
    report = {
        "run_id": run_id,
        "seed": seed,
        "objective": "added_token_weighted_mlm",
        "source_checkpoint": str(source_checkpoint),
        "actual_train_steps": actual_steps,
        "target_train_tokens": args.target_train_tokens,
        "train_tokens_seen": train_tokens,
        "base_mask_prob": args.base_mask_prob,
        "added_mask_prob": args.added_mask_prob,
        "base_loss_weight": args.base_loss_weight,
        "added_loss_weight": args.added_loss_weight,
        "selection_data": "MAR_dev_only",
        "final_access": "NO_ACT_FINAL_ACCESS",
    }
    (checkpoint_path / "added_token_repair_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    runtime = time.time() - start_time
    final_all = cat_value(final_rows, "final", "all")
    final_base = cat_value(final_rows, "final", "base")
    final_added = cat_value(final_rows, "final", "added")
    zero_all = cat_value(zero_rows, "zero_step", "all")
    zero_base = cat_value(zero_rows, "zero_step", "base")
    zero_added = cat_value(zero_rows, "zero_step", "added")
    baseline_all = baseline[str(seed)]["all"]
    baseline_base = baseline[str(seed)]["base"]
    baseline_added = baseline[str(seed)]["added"]
    status = "PASS" if final_added < baseline_added and final_all <= baseline_all else "NO_REPAIR"
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
            "notes": "standard eval mask",
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
        "base_mask_prob": f"{args.base_mask_prob:.6f}",
        "added_mask_prob": f"{args.added_mask_prob:.6f}",
        "base_loss_weight": f"{args.base_loss_weight:.6f}",
        "added_loss_weight": f"{args.added_loss_weight:.6f}",
        "zero_all_loss": f"{zero_all:.6f}",
        "final_all_loss": f"{final_all:.6f}",
        "baseline_all_loss": f"{baseline_all:.6f}",
        "all_loss_delta_vs_baseline": f"{final_all - baseline_all:.6f}",
        "zero_base_loss": f"{zero_base:.6f}",
        "final_base_loss": f"{final_base:.6f}",
        "baseline_base_loss": f"{baseline_base:.6f}",
        "base_loss_delta_vs_baseline": f"{final_base - baseline_base:.6f}",
        "zero_added_loss": f"{zero_added:.6f}",
        "final_added_loss": f"{final_added:.6f}",
        "baseline_added_loss": f"{baseline_added:.6f}",
        "added_loss_delta_vs_baseline": f"{final_added - baseline_added:.6f}",
        "final_added_base_ratio": f"{final_added / max(1e-12, final_base):.6f}",
        "checkpoint_path": str(checkpoint_path),
        "status": status,
        "notes": f"runtime_minutes={runtime / 60.0:.3f}; no_ACT_final_access",
    }
    return summary, zero_rows + final_rows, curve_rows, checkpoint_path


def mean(rows: list[dict[str, str]], column: str) -> float:
    return sum(float(row[column]) for row in rows) / max(1, len(rows))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--checkpoint-root", default="/home/axt/mnt2/jongha/second_try/checkpoints/18_v2_added_token_repair")
    parser.add_argument("--selected-init", default="docs/exp/second_try/14_v2_embedding_init/selected_init.md")
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
    parser.add_argument("--base-mask-prob", type=float, default=0.15)
    parser.add_argument("--added-mask-prob", type=float, default=0.30)
    parser.add_argument("--eval-mask-prob", type=float, default=0.15)
    parser.add_argument("--base-loss-weight", type=float, default=1.0)
    parser.add_argument("--added-loss-weight", type=float, default=3.0)
    parser.add_argument("--seed", type=int, default=9090)
    args = parser.parse_args()

    transformers_logging.set_verbosity_error()
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    start = time.time()
    run_id = "step18_v2_added_token_repair_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    step_dir = Path(args.step_dir).resolve()
    checkpoint_root = Path(args.checkpoint_root).resolve()
    checkpoint_root.mkdir(parents=True, exist_ok=True)
    source_checkpoint = load_selected_init(Path(args.selected_init))
    train_texts = read_train_lines(Path(args.train_text), args.train_limit)
    dev_texts = read_dev_texts(Path(args.dev_manifest), args.dev_limit)
    baseline = load_baseline_category(Path(args.baseline_category))
    base_vocab_size = len(XLMRobertaTokenizer.from_pretrained(args.base_model, local_files_only=True))
    seeds = [int(seed.strip()) for seed in args.seeds.split(",") if seed.strip()]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    summary_rows: list[dict[str, str]] = []
    category_rows: list[dict[str, str]] = []
    curve_rows: list[dict[str, str]] = []
    checkpoint_dirs: list[Path] = []
    for seed in seeds:
        print(f"training added-token repair seed={seed}", flush=True)
        summary, categories, curves, checkpoint_path = train_seed(
            seed,
            run_id,
            source_checkpoint,
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
        checkpoint_dirs.append(checkpoint_path)

    completed = len(summary_rows)
    improved_added = sum(1 for row in summary_rows if float(row["added_loss_delta_vs_baseline"]) < 0.0)
    nonworse_all = sum(1 for row in summary_rows if float(row["all_loss_delta_vs_baseline"]) <= 0.0)
    repaired = sum(1 for row in summary_rows if row["status"] == "PASS")
    artifact_gate = completed == len(seeds)
    repair_gate = artifact_gate and improved_added == len(seeds) and nonworse_all == len(seeds)
    best = sorted(summary_rows, key=lambda row: float(row["final_added_loss"]))[0]

    score_rows = [
        {
            "run_id": run_id,
            "gate_id": "G01_required_repair_runs",
            "criterion": "all added-token repair seeds complete",
            "observed": f"{completed}/{len(seeds)}",
            "required": f"{len(seeds)}/{len(seeds)}",
            "status": "PASS" if artifact_gate else "FAIL",
            "return_to": "18_v2_added_token_repair",
            "notes": "adapted repair only; original control reused from Step15",
        },
        {
            "run_id": run_id,
            "gate_id": "G02_no_final_access",
            "criterion": "ACT final data not read",
            "observed": "NO_ACT_FINAL_ACCESS",
            "required": "NO_ACT_FINAL_ACCESS",
            "status": "PASS",
            "return_to": "12_v2_split_protocol",
            "notes": "train text, Mark/dev manifest, and Step17 baseline only",
        },
        {
            "run_id": run_id,
            "gate_id": "G03_added_loss_improves",
            "criterion": "added-token dev loss improves over Step17 baseline in every seed",
            "observed": f"{improved_added}/{len(seeds)}",
            "required": f"{len(seeds)}/{len(seeds)}",
            "status": "PASS" if improved_added == len(seeds) else "FAIL",
            "return_to": "18_v2_added_token_repair",
            "notes": f"mean_delta={mean(summary_rows, 'added_loss_delta_vs_baseline'):.6f}",
        },
        {
            "run_id": run_id,
            "gate_id": "G04_all_loss_nonworse",
            "criterion": "all-token dev loss does not worsen versus Step17 baseline in every seed",
            "observed": f"{nonworse_all}/{len(seeds)}",
            "required": f"{len(seeds)}/{len(seeds)}",
            "status": "PASS" if nonworse_all == len(seeds) else "FAIL",
            "return_to": "18_v2_added_token_repair",
            "notes": f"mean_delta={mean(summary_rows, 'all_loss_delta_vs_baseline'):.6f}",
        },
        {
            "run_id": run_id,
            "gate_id": "G05_repair_checkpoint_selection",
            "criterion": "best repaired checkpoint selected by lowest added-token dev loss",
            "observed": best["checkpoint_path"],
            "required": "one checkpoint path",
            "status": "PASS",
            "return_to": "18_v2_added_token_repair",
            "notes": f"seed={best['seed']}; final_added_loss={best['final_added_loss']}",
        },
    ]

    score_path = step_dir / "score_table.tsv"
    summary_path = step_dir / "repair_summary.tsv"
    category_path = step_dir / "repair_category_loss.tsv"
    curves_path = step_dir / "repair_learning_curves.tsv"
    selection_path = step_dir / "checkpoint_selection.md"
    access_path = step_dir / "v2_no_final_access_audit.tsv"
    results_path = step_dir / "results.md"
    file_results_path = step_dir / "file_results.tsv"

    write_tsv(score_path, score_rows, SCORE_FIELDS)
    write_tsv(summary_path, summary_rows, SUMMARY_FIELDS)
    write_tsv(category_path, category_rows, CATEGORY_FIELDS)
    write_tsv(curves_path, curve_rows, CURVE_FIELDS)
    selection_path.write_text(
        f"""# Step 18 Checkpoint Selection

Run id: `{run_id}`

Selection data: `MAR` dev only.

Final data access: `NO_ACT_FINAL_ACCESS`.

Selected repaired checkpoint: `{best['checkpoint_path']}`

| Metric | Value |
| --- | --- |
| selected seed | `{best['seed']}` |
| final all loss | `{best['final_all_loss']}` |
| baseline all loss | `{best['baseline_all_loss']}` |
| all loss delta | `{best['all_loss_delta_vs_baseline']}` |
| final added loss | `{best['final_added_loss']}` |
| baseline added loss | `{best['baseline_added_loss']}` |
| added loss delta | `{best['added_loss_delta_vs_baseline']}` |
| final added/base ratio | `{best['final_added_base_ratio']}` |
| repair gate | `{'PASS' if repair_gate else 'FAIL'}` |
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
            "input_role": "dev_manifest",
            "path": str(Path(args.dev_manifest).resolve()),
            "allowed_split": "MAR_dev",
            "rows_or_files": str(count_rows(Path(args.dev_manifest))),
            "md5": md5_file(Path(args.dev_manifest)),
            "final_access": "NO",
            "status": "PASS",
        },
        {
            "run_id": run_id,
            "input_role": "baseline_category",
            "path": str(Path(args.baseline_category).resolve()),
            "allowed_split": "diagnostic_metadata",
            "rows_or_files": str(count_rows(Path(args.baseline_category))),
            "md5": md5_file(Path(args.baseline_category)),
            "final_access": "NO",
            "status": "PASS",
        },
    ]
    write_tsv(access_path, access_rows, ["run_id", "input_role", "path", "allowed_split", "rows_or_files", "md5", "final_access", "status"])

    results_path.write_text(
        f"""# Step 18 Results: V2 Added-Token-Focused Repair

Status: COMPLETED

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Artifact gate status: {'PASS' if artifact_gate else 'FAIL'}

Repair gate status: {'PASS' if repair_gate else 'FAIL'}

## Summary

Step 18 trains the Step 14 selected adapted checkpoint with an added-token-focused MLM objective. Evaluation uses the standard unweighted Mark/dev MLM diagnostic. ACT final was not read.

| Metric | Value |
| --- | ---: |
| completed seeds | {completed}/{len(seeds)} |
| added-token improved seeds | {improved_added}/{len(seeds)} |
| all-token nonworse seeds | {nonworse_all}/{len(seeds)} |
| repaired seeds | {repaired}/{len(seeds)} |
| mean added loss delta vs Step17 | {mean(summary_rows, 'added_loss_delta_vs_baseline'):.6f} |
| mean all loss delta vs Step17 | {mean(summary_rows, 'all_loss_delta_vs_baseline'):.6f} |
| selected seed | {best['seed']} |
| selected checkpoint | {best['checkpoint_path']} |

## Interpretation

If repair gate passes, rerun Step 15-style original-control comparison with the repaired checkpoint family. If repair gate fails, this weighted objective is insufficient and the next repair should change initialization or use a staged/frozen-base objective.

## Failure Return

Failed gate: {'NOT_APPLICABLE' if repair_gate else 'added_token_repair_gate'}

Observed evidence: {'NOT_APPLICABLE' if repair_gate else f"improved_added={improved_added}/{len(seeds)}, nonworse_all={nonworse_all}/{len(seeds)}"}

Return-to step: {'NOT_APPLICABLE' if repair_gate else '14_v2_embedding_init or 18_v2_added_token_repair'}

Required fix: {'NOT_APPLICABLE' if repair_gate else 'try frequency-aware initialization, staged training, or stronger added-token objective'}

Runtime minutes: {(time.time() - start) / 60.0:.3f}
""",
        encoding="utf-8",
    )
    file_rows = [
        file_result("score_table", score_path, "repair gate table"),
        file_result("repair_summary", summary_path, "per-seed repair summary"),
        file_result("repair_category_loss", category_path, "zero/final category losses"),
        file_result("repair_learning_curves", curves_path, "zero/final category curves"),
        file_result("checkpoint_selection", selection_path, "selected repair checkpoint"),
        file_result("no_final_access_audit", access_path, "input access audit"),
        file_result("results", results_path, "step result summary"),
    ]
    for checkpoint_dir in checkpoint_dirs:
        file_rows.append(file_result(f"checkpoint_{checkpoint_dir.name}", checkpoint_dir, "repaired adapted checkpoint"))
    write_tsv(file_results_path, file_rows, ["file_role", "path", "rows_or_files", "bytes", "md5", "status", "notes"])

    print(f"run_id={run_id}")
    print(f"artifact_gate_status={'PASS' if artifact_gate else 'FAIL'}")
    print(f"repair_gate_status={'PASS' if repair_gate else 'FAIL'}")
    print(f"improved_added={improved_added}/{len(seeds)}")
    print(f"nonworse_all={nonworse_all}/{len(seeds)}")
    print(f"selected_checkpoint={best['checkpoint_path']}")


if __name__ == "__main__":
    main()
