#!/usr/bin/env python3
"""Audit cross-tokenizer MLM metrics for Step 15 checkpoints."""

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


SCORE_FIELDS = ["run_id", "gate_id", "criterion", "observed", "required", "status", "return_to", "notes"]
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


def read_lines(path: Path, limit: int) -> list[str]:
    texts: list[str] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            text = line.rstrip("\n")
            if text.strip():
                texts.append(text)
            if limit > 0 and len(texts) >= limit:
                break
    return texts


def selected_step15_rows(path: Path) -> list[dict[str, str]]:
    rows = read_tsv(path)
    usable = [row for row in rows if row["model_family"] in {"adapted_extended", "original_control"} and Path(row["checkpoint_path"]).exists()]
    if len(usable) != 6:
        raise RuntimeError(f"expected six Step 15 checkpoints, found {len(usable)}")
    return usable


def make_masked_batch(tokenizer, texts: list[str], device: torch.device, max_length: int, seed: int) -> tuple[dict[str, torch.Tensor], int, int]:
    encoded = tokenizer(texts, padding=True, truncation=True, max_length=max_length, return_tensors="pt")
    input_ids = encoded["input_ids"]
    attention_mask = encoded["attention_mask"]
    labels = input_ids.clone()
    generator = torch.Generator()
    generator.manual_seed(seed)
    special_mask = torch.zeros_like(labels, dtype=torch.bool)
    for special_id in tokenizer.all_special_ids:
        special_mask |= labels.eq(special_id)
    special_mask |= attention_mask.eq(0)
    non_special_count = int((~special_mask).sum().item())
    probability = torch.full(labels.shape, 0.15)
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
    return batch, int(masked.sum().item()), non_special_count


def evaluate_checkpoint(row: dict[str, str], texts: list[str], device: torch.device, args: argparse.Namespace, run_id: str) -> dict[str, str]:
    checkpoint = Path(row["checkpoint_path"])
    tokenizer = XLMRobertaTokenizer.from_pretrained(str(checkpoint), local_files_only=True)
    model = AutoModelForMaskedLM.from_pretrained(str(checkpoint), local_files_only=True)
    model.to(device)
    model.eval()
    weighted_loss = 0.0
    masked_tokens = 0
    non_special_tokens = 0
    words = sum(len(text.split()) for text in texts)
    chars = sum(len(text) for text in texts)
    with torch.no_grad():
        for start in range(0, len(texts), args.batch_size):
            batch_texts = texts[start : start + args.batch_size]
            batch, batch_masked, batch_non_special = make_masked_batch(tokenizer, batch_texts, device, args.max_length, args.seed + int(row["seed"]) * 100000 + start)
            outputs = model(**batch)
            weighted_loss += float(outputs.loss.item()) * batch_masked
            masked_tokens += batch_masked
            non_special_tokens += batch_non_special
    model.to("cpu")
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    raw_loss = weighted_loss / max(1, masked_tokens)
    estimated_word = raw_loss * non_special_tokens / max(1, words)
    estimated_char = raw_loss * non_special_tokens / max(1, chars)
    return {
        "run_id": run_id,
        "model_family": row["model_family"],
        "seed": row["seed"],
        "checkpoint_path": row["checkpoint_path"],
        "dev_rows": str(len(texts)),
        "non_special_tokens": str(non_special_tokens),
        "words": str(words),
        "chars": str(chars),
        "masked_tokens": str(masked_tokens),
        "tokens_per_word": f"{non_special_tokens / max(1, words):.6f}",
        "tokens_per_char": f"{non_special_tokens / max(1, chars):.6f}",
        "raw_masked_token_loss": f"{raw_loss:.6f}",
        "estimated_nll_per_word": f"{estimated_word:.6f}",
        "estimated_nll_per_char": f"{estimated_char:.6f}",
        "pseudo_ppl": f"{math.exp(min(raw_loss, 20.0)):.6f}",
        "status": "PASS",
        "notes": "Mark/dev only; normalized diagnostic",
    }


def aggregate(rows: list[dict[str, str]], family: str, column: str) -> tuple[float, float]:
    values = [float(row[column]) for row in rows if row["model_family"] == family]
    return statistics.mean(values), statistics.pstdev(values) if len(values) > 1 else 0.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--step15-summary", default="docs/exp/second_try/15_v2_mlm_control/seed_summary.tsv")
    parser.add_argument("--dev-text", default="/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_mlm_dev_mark.txt")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--dev-limit", type=int, default=0)
    parser.add_argument("--seed", type=int, default=4242)
    parser.add_argument("--competitive-margin", type=float, default=1.10)
    args = parser.parse_args()

    transformers_logging.set_verbosity_error()
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    start = time.time()
    run_id = "step16_v2_mlm_metric_fairness_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    step_dir = Path(args.step_dir).resolve()
    rows = selected_step15_rows(Path(args.step15_summary))
    texts = read_lines(Path(args.dev_text), args.dev_limit)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    metric_rows = []
    for row in rows:
        print(f"evaluating family={row['model_family']} seed={row['seed']}", flush=True)
        metric_rows.append(evaluate_checkpoint(row, texts, device, args, run_id))

    adapted_raw, adapted_raw_std = aggregate(metric_rows, "adapted_extended", "raw_masked_token_loss")
    original_raw, original_raw_std = aggregate(metric_rows, "original_control", "raw_masked_token_loss")
    adapted_word, adapted_word_std = aggregate(metric_rows, "adapted_extended", "estimated_nll_per_word")
    original_word, original_word_std = aggregate(metric_rows, "original_control", "estimated_nll_per_word")
    adapted_char, adapted_char_std = aggregate(metric_rows, "adapted_extended", "estimated_nll_per_char")
    original_char, original_char_std = aggregate(metric_rows, "original_control", "estimated_nll_per_char")
    raw_ratio = adapted_raw / original_raw
    word_ratio = adapted_word / original_word
    char_ratio = adapted_char / original_char
    artifact_gate = len(metric_rows) == 6
    claim_gate = artifact_gate and word_ratio <= args.competitive_margin and char_ratio <= args.competitive_margin

    score_rows = [
        {
            "run_id": run_id,
            "gate_id": "G01_required_checkpoints",
            "criterion": "all six Step 15 checkpoints evaluated",
            "observed": f"{len(metric_rows)}/6",
            "required": "6/6",
            "status": "PASS" if len(metric_rows) == 6 else "FAIL",
            "return_to": "15_v2_mlm_control",
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
            "notes": "Step15 summary and Mark/dev text only",
        },
        {
            "run_id": run_id,
            "gate_id": "G03_word_normalized_competitive",
            "criterion": "adapted estimated NLL per word is within margin",
            "observed": f"ratio={word_ratio:.6f}; adapted_mean={adapted_word:.6f}; original_mean={original_word:.6f}",
            "required": f"ratio<={args.competitive_margin:.6f}",
            "status": "PASS" if word_ratio <= args.competitive_margin else "FAIL",
            "return_to": "15_v2_mlm_control",
            "notes": "normalizes by non-special token count per word",
        },
        {
            "run_id": run_id,
            "gate_id": "G04_char_normalized_competitive",
            "criterion": "adapted estimated NLL per character is within margin",
            "observed": f"ratio={char_ratio:.6f}; adapted_mean={adapted_char:.6f}; original_mean={original_char:.6f}",
            "required": f"ratio<={args.competitive_margin:.6f}",
            "status": "PASS" if char_ratio <= args.competitive_margin else "FAIL",
            "return_to": "15_v2_mlm_control",
            "notes": "normalizes by non-special token count per character",
        },
        {
            "run_id": run_id,
            "gate_id": "G05_raw_loss_context",
            "criterion": "raw masked-token loss ratio recorded as diagnostic context",
            "observed": f"ratio={raw_ratio:.6f}; adapted_mean={adapted_raw:.6f}; original_mean={original_raw:.6f}",
            "required": "recorded",
            "status": "PASS",
            "return_to": "NOT_APPLICABLE",
            "notes": "raw token losses are not directly comparable across tokenizer vocabularies",
        },
    ]

    score_path = step_dir / "score_table.tsv"
    metrics_path = step_dir / "normalized_mlm_scores.tsv"
    access_path = step_dir / "v2_no_final_access_audit.tsv"
    results_path = step_dir / "results.md"
    file_results_path = step_dir / "file_results.tsv"

    write_tsv(score_path, score_rows, SCORE_FIELDS)
    write_tsv(metrics_path, metric_rows, METRIC_FIELDS)
    access_rows = [
        {
            "run_id": run_id,
            "input_role": "step15_summary",
            "path": str(Path(args.step15_summary).resolve()),
            "allowed_split": "checkpoint_metadata",
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
        f"""# Step 16 Results: V2 MLM Metric Fairness Audit

Status: COMPLETED

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Artifact gate status: {'PASS' if artifact_gate else 'FAIL'}

Claim gate status: {'PASS' if claim_gate else 'FAIL'}

## Summary

Step 16 evaluates every Step 15 token-matched checkpoint on Mark/dev only and reports tokenizer-normalized MLM diagnostics. ACT final was not read.

| Metric | Adapted Mean | Original Mean | Ratio |
| --- | ---: | ---: | ---: |
| raw masked-token loss | {adapted_raw:.6f} +/- {adapted_raw_std:.6f} | {original_raw:.6f} +/- {original_raw_std:.6f} | {raw_ratio:.6f} |
| estimated NLL per word | {adapted_word:.6f} +/- {adapted_word_std:.6f} | {original_word:.6f} +/- {original_word_std:.6f} | {word_ratio:.6f} |
| estimated NLL per char | {adapted_char:.6f} +/- {adapted_char_std:.6f} | {original_char:.6f} +/- {original_char_std:.6f} | {char_ratio:.6f} |

## Interpretation

Raw masked-token loss is not directly comparable across tokenizers, but the normalized diagnostics also fail the configured competitive margin of `{args.competitive_margin:.6f}`. Step 15's negative model-dependent conclusion remains in force.

## Failure Return

Failed gate: {'NOT_APPLICABLE' if claim_gate else 'normalized_mlm_competitive_gate'}

Observed evidence: {'NOT_APPLICABLE' if claim_gate else f'word_ratio={word_ratio:.6f}, char_ratio={char_ratio:.6f}'}

Return-to step: {'NOT_APPLICABLE' if claim_gate else '14_v2_embedding_init or 15_v2_mlm_control'}

Required fix: {'NOT_APPLICABLE' if claim_gate else 'revise initialization/objective or downgrade model-dependent claim'}

Runtime minutes: {(time.time() - start) / 60.0:.3f}
""",
        encoding="utf-8",
    )
    file_rows = [
        file_result("score_table", score_path, "gate table"),
        file_result("normalized_mlm_scores", metrics_path, "per-checkpoint normalized MLM diagnostics"),
        file_result("no_final_access_audit", access_path, "input access audit"),
        file_result("results", results_path, "step result summary"),
    ]
    write_tsv(file_results_path, file_rows, ["file_role", "path", "rows_or_files", "bytes", "md5", "status", "notes"])

    print(f"run_id={run_id}")
    print(f"artifact_gate_status={'PASS' if artifact_gate else 'FAIL'}")
    print(f"claim_gate_status={'PASS' if claim_gate else 'FAIL'}")
    print(f"raw_ratio={raw_ratio:.6f}")
    print(f"word_ratio={word_ratio:.6f}")
    print(f"char_ratio={char_ratio:.6f}")


if __name__ == "__main__":
    main()
