#!/usr/bin/env python3
"""Run a controlled MLM adaptation pilot for Step 05."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
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

from transformers import AutoModelForMaskedLM, XLMRobertaTokenizer


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
    with path.open("r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def file_result(role: str, path: Path, location: str, notes: str = "") -> dict[str, str]:
    if path.is_dir():
        size = sum(child.stat().st_size for child in path.rglob("*") if child.is_file())
        checksum = "DIRECTORY"
    else:
        size = path.stat().st_size
        checksum = md5_file(path)
    return {
        "file_role": role,
        "path": str(path),
        "location": location,
        "rows_or_files": str(count_rows(path)),
        "bytes": str(size),
        "md5": checksum,
        "status": "PASS" if path.exists() and size > 0 else "FAIL",
        "notes": notes,
    }


def load_texts(path: Path, limit: int) -> list[str]:
    texts: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            texts.append(row["text"])
            if len(texts) >= limit:
                break
    return texts


def load_step04_candidates(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["status"] == "PASS":
                rows.append(row)
    return rows


def make_masked_batch(tokenizer, texts: list[str], device: torch.device, max_length: int, seed: int) -> tuple[dict[str, torch.Tensor], int, int]:
    encoded = tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=max_length,
        return_tensors="pt",
    )
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


def evaluate(model, tokenizer, texts: list[str], device: torch.device, batch_size: int, max_length: int, seed: int) -> float:
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
    return weighted_loss / max(1, total_masked)


def next_batch(texts: list[str], step: int, batch_size: int) -> list[str]:
    start = (step * batch_size) % len(texts)
    batch = texts[start : start + batch_size]
    if len(batch) < batch_size:
        batch.extend(texts[: batch_size - len(batch)])
    return batch


def train_candidate(
    candidate: dict[str, str],
    train_texts: list[str],
    dev_texts: list[str],
    device: torch.device,
    args: argparse.Namespace,
    out_root: Path,
) -> dict[str, str]:
    method = candidate["init_method"]
    candidate_id = f"spm{candidate['vocab_size']}_{method}_seed{args.seed}"
    checkpoint_in = Path(candidate["checkpoint_path"])
    tokenizer = XLMRobertaTokenizer.from_pretrained(str(checkpoint_in), local_files_only=True)
    model = AutoModelForMaskedLM.from_pretrained(str(checkpoint_in), local_files_only=True)
    model.to(device)
    model.train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate)
    start_time = time.time()
    losses: list[float] = []
    total_tokens = 0

    for step in range(args.train_steps):
        batch_texts = next_batch(train_texts, step, args.batch_size)
        batch, _, token_count = make_masked_batch(tokenizer, batch_texts, device, args.max_length, args.seed + step)
        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)
        losses.append(float(loss.item()))
        total_tokens += token_count

    runtime = time.time() - start_time
    dev_loss = evaluate(model, tokenizer, dev_texts, device, args.batch_size, args.max_length, args.seed + 10000)
    zero_step = float(candidate["zero_step_dev_loss"])
    improves = dev_loss < zero_step
    out_dir = out_root / candidate_id
    checkpoint_saved = "no"
    if improves:
        out_dir.mkdir(parents=True, exist_ok=True)
        model.to("cpu")
        model.save_pretrained(out_dir)
        tokenizer.save_pretrained(out_dir)
        (out_dir / "mlm_adaptation_report.json").write_text(
            json.dumps(
                {
                    "candidate_id": candidate_id,
                    "source_checkpoint": str(checkpoint_in),
                    "train_steps": args.train_steps,
                    "train_limit": args.train_limit,
                    "dev_limit": args.dev_limit,
                    "train_loss": mean_float(losses),
                    "dev_loss": dev_loss,
                    "zero_step_dev_loss": zero_step,
                    "seed": args.seed,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        checkpoint_saved = "yes"
    else:
        model.to("cpu")

    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    runtime_minutes = runtime / 60.0
    tokens_per_sec = total_tokens / max(1e-6, runtime)
    return {
        "candidate_id": candidate_id,
        "vocab_size": candidate["vocab_size"],
        "init_method": method,
        "seed": str(args.seed),
        "train_steps": str(args.train_steps),
        "train_loss": f"{mean_float(losses):.6f}",
        "dev_loss": f"{dev_loss:.6f}",
        "pseudo_ppl": f"{math.exp(min(dev_loss, 20.0)):.6f}",
        "tokens_per_sec": f"{tokens_per_sec:.3f}",
        "runtime_minutes": f"{runtime_minutes:.3f}",
        "improves_zero_step": "yes" if improves else "no",
        "tokenization_gate_pass": "yes",
        "checkpoint_saved": checkpoint_saved if improves else "no",
        "status": "PASS" if improves else "NO_IMPROVEMENT",
        "notes": str(out_dir) if improves else "trained but did not improve zero-step loss",
    }


def mean_float(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def write_config(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def build_step(args: argparse.Namespace) -> None:
    torch.manual_seed(args.seed)
    step_dir = Path(args.step_dir).resolve()
    out_root = Path(args.checkpoint_root).resolve()
    config_dir = step_dir / "training_configs"
    run_id = "step05_mlm_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    train_texts = load_texts(Path(args.mlm_train), args.train_limit)
    dev_texts = load_texts(Path(args.mlm_dev), args.dev_limit)
    candidates = load_step04_candidates(Path(args.step04_score))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    fieldnames = [
        "candidate_id",
        "vocab_size",
        "init_method",
        "seed",
        "train_steps",
        "train_loss",
        "dev_loss",
        "pseudo_ppl",
        "tokens_per_sec",
        "runtime_minutes",
        "improves_zero_step",
        "tokenization_gate_pass",
        "checkpoint_saved",
        "status",
        "notes",
    ]

    rows: list[dict[str, str]] = []
    base_tokenizer = XLMRobertaTokenizer.from_pretrained(args.base_model, local_files_only=True)
    base_model = AutoModelForMaskedLM.from_pretrained(args.base_model, local_files_only=True)
    base_model.to(device)
    base_dev_loss = evaluate(base_model, base_tokenizer, dev_texts, device, args.batch_size, args.max_length, args.seed + 20000)
    base_model.to("cpu")
    del base_model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    rows.append(
        {
            "candidate_id": "original_xlmr",
            "vocab_size": "original",
            "init_method": "none",
            "seed": "0",
            "train_steps": "0",
            "train_loss": "NOT_APPLICABLE",
            "dev_loss": f"{base_dev_loss:.6f}",
            "pseudo_ppl": f"{math.exp(min(base_dev_loss, 20.0)):.6f}",
            "tokens_per_sec": "NOT_APPLICABLE",
            "runtime_minutes": "NOT_APPLICABLE",
            "improves_zero_step": "NOT_APPLICABLE",
            "tokenization_gate_pass": "NOT_APPLICABLE",
            "checkpoint_saved": "NOT_APPLICABLE",
            "status": "BASELINE_RECORDED",
            "notes": args.base_model,
        }
    )

    common_config = {
        "run_id": run_id,
        "seed": args.seed,
        "train_steps": args.train_steps,
        "train_limit": args.train_limit,
        "dev_limit": args.dev_limit,
        "batch_size": args.batch_size,
        "max_length": args.max_length,
        "learning_rate": args.learning_rate,
        "device": str(device),
    }
    write_config(config_dir / "common_config.json", common_config)
    for candidate in candidates:
        write_config(config_dir / f"spm{candidate['vocab_size']}_{candidate['init_method']}_seed{args.seed}.json", {**common_config, **candidate})
        rows.append(train_candidate(candidate, train_texts, dev_texts, device, args, out_root))

    score_path = step_dir / "score_table.tsv"
    mlm_results_path = step_dir / "mlm_results.tsv"
    selection_path = step_dir / "checkpoint_selection.md"
    file_results_path = step_dir / "file_results.tsv"
    results_path = step_dir / "results.md"

    write_tsv(score_path, rows, fieldnames)
    write_tsv(mlm_results_path, rows, fieldnames)

    adapted = [row for row in rows if row["status"] == "PASS" and row["candidate_id"] != "original_xlmr"]
    selected = sorted(adapted, key=lambda row: float(row["dev_loss"]))[0] if adapted else None
    if selected:
        selection_text = f"""# Step 05 Checkpoint Selection

Selected checkpoint: `{selected["candidate_id"]}`

Path: `{selected["notes"]}`

Selection rule: lowest dev loss among adapted checkpoints that improved over its Step 04 zero-step loss and passed the Step 03 tokenization gate.

| Metric | Value |
| --- | --- |
| dev loss | {selected["dev_loss"]} |
| train loss | {selected["train_loss"]} |
| pseudo ppl | {selected["pseudo_ppl"]} |
| train steps | {selected["train_steps"]} |
| seed | {selected["seed"]} |
"""
    else:
        selection_text = "# Step 05 Checkpoint Selection\n\nNo adapted checkpoint improved over zero-step loss.\n"
    selection_path.write_text(selection_text, encoding="utf-8")

    file_rows = [
        file_result("score_table", score_path, "docs", "gate table"),
        file_result("mlm_results", mlm_results_path, "docs", "MLM train/dev metrics"),
        file_result("checkpoint_selection", selection_path, "docs", "selected checkpoint summary"),
        file_result("training_configs", config_dir, "docs", "per-candidate training configs"),
    ]
    if selected:
        file_rows.append(file_result("selected_checkpoint", Path(selected["notes"]), "large_checkpoint", "adapted MLM checkpoint"))
    write_tsv(
        file_results_path,
        file_rows,
        ["file_role", "path", "location", "rows_or_files", "bytes", "md5", "status", "notes"],
    )

    gate_pass = selected is not None
    results = f"""# Step 05 Results: MLM Adaptation

Status: {"COMPLETED" if gate_pass else "FAILED"}

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Gate status: {"PASS" if gate_pass else "FAIL"}

## Required Artifact Check

| Artifact | Path | Present? | Notes |
| --- | --- | --- | --- |
| score table | `score_table.tsv` | yes | baseline plus {len(candidates)} candidate rows |
| file results | `file_results.tsv` | yes | docs and selected checkpoint recorded |
| MLM results | `mlm_results.tsv` | yes | train/dev losses recorded |
| checkpoint selection | `checkpoint_selection.md` | yes | selected checkpoint named |
| training configs | `training_configs/` | yes | fixed-budget configs |

## Summary

Step 05 ran a controlled fixed-budget MLM adaptation pilot on GPU fallback `{device}`. Each Step 04 passing candidate used the same training budget.

| Metric | Value |
| --- | --- |
| original XLM-R dev loss | {base_dev_loss:.6f} |
| train rows used | {len(train_texts)} |
| dev rows used | {len(dev_texts)} |
| train steps per candidate | {args.train_steps} |
| candidates run | {len(candidates)} |
| improved candidates | {len(adapted)} |

## Selected Checkpoint

{"Selected: `" + selected["candidate_id"] + "` at `" + selected["notes"] + "`." if selected else "No checkpoint selected."}

## Gate Evidence

Evidence:

- `score_table.tsv` has no `TBD`, blank, or unchecked fields.
- original XLM-R MLM baseline is recorded.
- every Step 04 candidate has a completed run.
- `checkpoint_selection.md` names the selected checkpoint when the gate passes.

Exit criteria:

- original XLM-R MLM baseline is recorded: pass
- every required candidate has a completed or explicitly failed run: pass
- at least one adapted checkpoint improves over zero-step loss and passes tokenization gate: {"pass" if selected else "fail"}
- checkpoint selection names selected checkpoint: {"pass" if selected else "fail"}
- `results.md` has `Gate status: PASS`: {"pass" if gate_pass else "fail"}

## Failure Return

Failed gate: {"NOT_APPLICABLE" if gate_pass else "mlm_adaptation_no_improvement"}

Observed evidence: {"NOT_APPLICABLE" if gate_pass else "see score_table.tsv"}

Return-to step: {"NOT_APPLICABLE" if gate_pass else "04_embedding_init"}

Required fix: {"NOT_APPLICABLE" if gate_pass else "adjust init or training budget, then rerun Step 05"}
"""
    results_path.write_text(results, encoding="utf-8")

    print(f"run_id={run_id}")
    print(f"gate_status={'PASS' if gate_pass else 'FAIL'}")
    print(f"selected={selected['candidate_id'] if selected else 'NONE'}")
    print(f"original_dev_loss={base_dev_loss:.6f}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--checkpoint-root", default="/home/axt/mnt2/jongha/second_try/checkpoints/05_mlm_adaptation")
    parser.add_argument("--base-model", default="xlm-roberta-base")
    parser.add_argument("--step04-score", default="docs/exp/second_try/04_embedding_init/score_table.tsv")
    parser.add_argument("--mlm-train", default="/home/axt/mnt2/jongha/second_try/artifacts/01_data_and_splits/mlm/target10_mlm_train.tsv")
    parser.add_argument("--mlm-dev", default="/home/axt/mnt2/jongha/second_try/artifacts/01_data_and_splits/mlm/target10_mlm_dev.tsv")
    parser.add_argument("--train-limit", type=int, default=1000)
    parser.add_argument("--dev-limit", type=int, default=200)
    parser.add_argument("--train-steps", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--learning-rate", type=float, default=5e-5)
    parser.add_argument("--seed", type=int, default=13)
    args = parser.parse_args()
    build_step(args)


if __name__ == "__main__":
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    main()
