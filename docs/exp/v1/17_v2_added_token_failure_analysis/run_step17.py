#!/usr/bin/env python3
"""Decompose Step 15 MLM loss into base-token and added-token losses."""

from __future__ import annotations

import argparse
import csv
import hashlib
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
CATEGORY_FIELDS = [
    "run_id",
    "model_family",
    "seed",
    "checkpoint_path",
    "category",
    "non_special_tokens",
    "masked_tokens",
    "mean_loss",
    "loss_share_pct",
    "token_share_pct",
    "status",
    "notes",
]
LANG_FIELDS = [
    "run_id",
    "model_family",
    "seed",
    "iso",
    "language",
    "script",
    "rows",
    "words",
    "chars",
    "non_special_tokens",
    "added_non_special_tokens",
    "added_token_pct",
    "tokens_per_word",
    "masked_all",
    "loss_all",
    "masked_base",
    "loss_base",
    "masked_added",
    "loss_added",
    "status",
]
NEW_TOKEN_FIELDS = [
    "run_id",
    "token_id",
    "token",
    "masked_count",
    "avg_loss",
    "max_loss",
    "observed_seeds",
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


def step15_rows(path: Path) -> list[dict[str, str]]:
    rows = read_tsv(path)
    usable = [row for row in rows if row["model_family"] in {"adapted_extended", "original_control"} and Path(row["checkpoint_path"]).exists()]
    if len(usable) != 6:
        raise RuntimeError(f"expected six Step 15 checkpoint rows, found {len(usable)}")
    return usable


def dev_rows(path: Path, limit: int) -> list[dict[str, str]]:
    rows = read_tsv(path)
    out = []
    for row in rows:
        if row["v2_split"] != "dev" or row["book"] != "MAR":
            raise RuntimeError(f"non-dev row in dev manifest: {row.get('verse_id')}")
        out.append(row)
        if limit > 0 and len(out) >= limit:
            break
    return out


def blank_stats() -> dict[str, float]:
    return {"loss_sum": 0.0, "loss_max": 0.0, "masked": 0.0, "non_special": 0.0, "added_non_special": 0.0, "words": 0.0, "chars": 0.0, "rows": 0.0}


def add_loss(stats: dict[str, float], losses: torch.Tensor) -> None:
    if losses.numel() == 0:
        return
    stats["loss_sum"] += float(losses.sum().item())
    stats["loss_max"] = max(float(stats["loss_max"]), float(losses.max().item()))
    stats["masked"] += float(losses.numel())


def make_batch(tokenizer, rows: list[dict[str, str]], device: torch.device, max_length: int, seed: int):
    texts = [row["text"] for row in rows]
    encoded = tokenizer(texts, padding=True, truncation=True, max_length=max_length, return_tensors="pt")
    original_input_ids = encoded["input_ids"]
    attention_mask = encoded["attention_mask"]
    labels = original_input_ids.clone()
    generator = torch.Generator()
    generator.manual_seed(seed)
    special_mask = torch.zeros_like(labels, dtype=torch.bool)
    for special_id in tokenizer.all_special_ids:
        special_mask |= labels.eq(special_id)
    special_mask |= attention_mask.eq(0)
    probability = torch.full(labels.shape, 0.15)
    probability.masked_fill_(special_mask, 0.0)
    masked = torch.bernoulli(probability, generator=generator).bool()
    if masked.sum().item() == 0:
        available = (special_mask == 0).nonzero(as_tuple=False)
        if len(available) > 0:
            masked[available[0, 0], available[0, 1]] = True
    labels[~masked] = -100
    input_ids = original_input_ids.clone()
    input_ids[masked] = tokenizer.mask_token_id
    batch = {
        "input_ids": input_ids.to(device),
        "attention_mask": attention_mask.to(device),
        "labels": labels.to(device),
    }
    return batch, original_input_ids, labels, special_mask, masked


def safe_mean(stats: dict[str, float]) -> str:
    if stats["masked"] <= 0:
        return "NOT_APPLICABLE"
    return f"{stats['loss_sum'] / stats['masked']:.6f}"


def pct(numerator: float, denominator: float) -> str:
    if denominator <= 0:
        return "0.000000"
    return f"{100.0 * numerator / denominator:.6f}"


def evaluate_checkpoint(row: dict[str, str], rows: list[dict[str, str]], base_vocab_size: int, device: torch.device, args: argparse.Namespace, run_id: str):
    checkpoint = Path(row["checkpoint_path"])
    tokenizer = XLMRobertaTokenizer.from_pretrained(str(checkpoint), local_files_only=True)
    model = AutoModelForMaskedLM.from_pretrained(str(checkpoint), local_files_only=True)
    model.to(device)
    model.eval()
    family = row["model_family"]
    seed = row["seed"]
    category = {"all": blank_stats(), "base": blank_stats(), "added": blank_stats()}
    lang_stats: dict[tuple[str, str, str], dict[str, float]] = defaultdict(blank_stats)
    token_stats: dict[int, dict[str, object]] = defaultdict(lambda: {"loss_sum": 0.0, "loss_max": 0.0, "count": 0, "seeds": set()})

    with torch.no_grad():
        for start in range(0, len(rows), args.batch_size):
            batch_rows = rows[start : start + args.batch_size]
            batch, original_ids_cpu, labels_cpu, special_mask_cpu, _ = make_batch(tokenizer, batch_rows, device, args.max_length, args.seed + int(seed) * 100000 + start)
            outputs = model(**batch)
            labels = batch["labels"]
            losses = F.cross_entropy(
                outputs.logits.view(-1, outputs.logits.shape[-1]),
                labels.view(-1),
                reduction="none",
                ignore_index=-100,
            ).view(labels.shape).detach().cpu()
            labels = labels.detach().cpu()
            masked = labels.ne(-100)
            base_mask = masked & labels.lt(base_vocab_size)
            added_mask = masked & labels.ge(base_vocab_size)
            add_loss(category["all"], losses[masked])
            add_loss(category["base"], losses[base_mask])
            add_loss(category["added"], losses[added_mask])
            non_special = ~special_mask_cpu
            category["all"]["non_special"] += float(non_special.sum().item())
            category["base"]["non_special"] += float((non_special & original_ids_cpu.lt(base_vocab_size)).sum().item())
            category["added"]["non_special"] += float((non_special & original_ids_cpu.ge(base_vocab_size)).sum().item())
            category["all"]["added_non_special"] += float((non_special & original_ids_cpu.ge(base_vocab_size)).sum().item())

            for idx, item in enumerate(batch_rows):
                key = (item["iso"], item["language"], item["script"])
                stats = lang_stats[key]
                row_non_special = non_special[idx]
                row_added_non_special = row_non_special & original_ids_cpu[idx].ge(base_vocab_size)
                stats["rows"] += 1.0
                stats["words"] += float(len(item["text"].split()))
                stats["chars"] += float(len(item["text"]))
                stats["non_special"] += float(row_non_special.sum().item())
                stats["added_non_special"] += float(row_added_non_special.sum().item())
                row_mask = masked[idx]
                row_base = base_mask[idx]
                row_added = added_mask[idx]
                add_loss(stats, losses[idx][row_mask])
                stats.setdefault("base_loss_sum", 0.0)
                stats.setdefault("base_masked", 0.0)
                stats.setdefault("added_loss_sum", 0.0)
                stats.setdefault("added_masked", 0.0)
                stats["base_loss_sum"] += float(losses[idx][row_base].sum().item()) if row_base.any() else 0.0
                stats["base_masked"] += float(row_base.sum().item())
                stats["added_loss_sum"] += float(losses[idx][row_added].sum().item()) if row_added.any() else 0.0
                stats["added_masked"] += float(row_added.sum().item())

            if family == "adapted_extended":
                added_positions = added_mask.nonzero(as_tuple=False)
                for pos in added_positions.tolist():
                    token_id = int(labels[pos[0], pos[1]].item())
                    loss_value = float(losses[pos[0], pos[1]].item())
                    token_stats[token_id]["loss_sum"] = float(token_stats[token_id]["loss_sum"]) + loss_value
                    token_stats[token_id]["loss_max"] = max(float(token_stats[token_id]["loss_max"]), loss_value)
                    token_stats[token_id]["count"] = int(token_stats[token_id]["count"]) + 1
                    token_stats[token_id]["seeds"].add(seed)

    model.to("cpu")
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    category_rows = []
    all_loss_sum = category["all"]["loss_sum"]
    total_non_special = category["all"]["non_special"]
    for name, stats in category.items():
        category_rows.append(
            {
                "run_id": run_id,
                "model_family": family,
                "seed": seed,
                "checkpoint_path": str(checkpoint),
                "category": name,
                "non_special_tokens": str(int(stats["non_special"])),
                "masked_tokens": str(int(stats["masked"])),
                "mean_loss": safe_mean(stats),
                "loss_share_pct": pct(stats["loss_sum"], all_loss_sum),
                "token_share_pct": pct(stats["non_special"], total_non_special),
                "status": "PASS",
                "notes": "base_vocab_size=%d" % base_vocab_size,
            }
        )

    language_rows = []
    for (iso, language, script), stats in sorted(lang_stats.items()):
        base_loss = "NOT_APPLICABLE" if stats.get("base_masked", 0.0) <= 0 else f"{stats['base_loss_sum'] / stats['base_masked']:.6f}"
        added_loss = "NOT_APPLICABLE" if stats.get("added_masked", 0.0) <= 0 else f"{stats['added_loss_sum'] / stats['added_masked']:.6f}"
        language_rows.append(
            {
                "run_id": run_id,
                "model_family": family,
                "seed": seed,
                "iso": iso,
                "language": language,
                "script": script,
                "rows": str(int(stats["rows"])),
                "words": str(int(stats["words"])),
                "chars": str(int(stats["chars"])),
                "non_special_tokens": str(int(stats["non_special"])),
                "added_non_special_tokens": str(int(stats["added_non_special"])),
                "added_token_pct": pct(stats["added_non_special"], stats["non_special"]),
                "tokens_per_word": f"{stats['non_special'] / max(1.0, stats['words']):.6f}",
                "masked_all": str(int(stats["masked"])),
                "loss_all": safe_mean(stats),
                "masked_base": str(int(stats.get("base_masked", 0.0))),
                "loss_base": base_loss,
                "masked_added": str(int(stats.get("added_masked", 0.0))),
                "loss_added": added_loss,
                "status": "PASS",
            }
        )

    token_rows = []
    if family == "adapted_extended":
        for token_id, stats in token_stats.items():
            count = int(stats["count"])
            if count <= 0:
                continue
            token_rows.append(
                {
                    "run_id": run_id,
                    "token_id": str(token_id),
                    "token": tokenizer.convert_ids_to_tokens(token_id),
                    "masked_count": str(count),
                    "avg_loss": f"{float(stats['loss_sum']) / count:.6f}",
                    "max_loss": f"{float(stats['loss_max']):.6f}",
                    "observed_seeds": ",".join(sorted(stats["seeds"])),
                    "status": "PASS",
                    "notes": "adapted checkpoints only",
                }
            )
    return category_rows, language_rows, token_rows


def mean_category(rows: list[dict[str, str]], family: str, category: str) -> float:
    values = [float(row["mean_loss"]) for row in rows if row["model_family"] == family and row["category"] == category and row["mean_loss"] != "NOT_APPLICABLE"]
    return sum(values) / max(1, len(values))


def mean_share(rows: list[dict[str, str]], family: str, category: str, column: str) -> float:
    values = [float(row[column]) for row in rows if row["model_family"] == family and row["category"] == category]
    return sum(values) / max(1, len(values))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--step15-summary", default="docs/exp/second_try/15_v2_mlm_control/seed_summary.tsv")
    parser.add_argument("--dev-manifest", default="docs/exp/second_try/12_v2_split_protocol/v2_dev_manifest.tsv")
    parser.add_argument("--base-model", default="xlm-roberta-base")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--dev-limit", type=int, default=0)
    parser.add_argument("--seed", type=int, default=7777)
    parser.add_argument("--added-loss-ratio-threshold", type=float, default=1.25)
    args = parser.parse_args()

    transformers_logging.set_verbosity_error()
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    start = time.time()
    run_id = "step17_v2_added_token_failure_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    step_dir = Path(args.step_dir).resolve()
    rows = step15_rows(Path(args.step15_summary))
    dev = dev_rows(Path(args.dev_manifest), args.dev_limit)
    base_tokenizer = XLMRobertaTokenizer.from_pretrained(args.base_model, local_files_only=True)
    base_vocab_size = len(base_tokenizer)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    category_rows: list[dict[str, str]] = []
    language_rows: list[dict[str, str]] = []
    token_rows: list[dict[str, str]] = []
    for row in rows:
        print(f"evaluating family={row['model_family']} seed={row['seed']}", flush=True)
        cats, langs, toks = evaluate_checkpoint(row, dev, base_vocab_size, device, args, run_id)
        category_rows.extend(cats)
        language_rows.extend(langs)
        token_rows.extend(toks)

    adapted_base_loss = mean_category(category_rows, "adapted_extended", "base")
    adapted_added_loss = mean_category(category_rows, "adapted_extended", "added")
    original_all_loss = mean_category(category_rows, "original_control", "all")
    added_base_ratio = adapted_added_loss / max(1e-12, adapted_base_loss)
    adapted_all_loss = mean_category(category_rows, "adapted_extended", "all")
    adapted_original_ratio = adapted_all_loss / max(1e-12, original_all_loss)
    added_token_share = mean_share(category_rows, "adapted_extended", "added", "token_share_pct")
    added_loss_share = mean_share(category_rows, "adapted_extended", "added", "loss_share_pct")
    diagnostic_gate = added_base_ratio > args.added_loss_ratio_threshold
    artifact_gate = len([row for row in category_rows if row["category"] == "all"]) == 6

    top_loss_tokens = sorted(token_rows, key=lambda row: (float(row["avg_loss"]), int(row["masked_count"])), reverse=True)[:50]
    top_count_tokens = sorted(token_rows, key=lambda row: (int(row["masked_count"]), float(row["avg_loss"])), reverse=True)[:50]
    merged_tokens = {}
    for row in top_loss_tokens + top_count_tokens:
        merged_tokens[row["token_id"]] = row
    token_rows_out = list(merged_tokens.values())
    token_rows_out.sort(key=lambda row: (float(row["avg_loss"]), int(row["masked_count"])), reverse=True)

    score_rows = [
        {
            "run_id": run_id,
            "gate_id": "G01_required_checkpoints",
            "criterion": "all six Step15 checkpoints evaluated",
            "observed": f"{len([row for row in category_rows if row['category'] == 'all'])}/6",
            "required": "6/6",
            "status": "PASS" if artifact_gate else "FAIL",
            "return_to": "15_v2_mlm_control",
            "notes": "3 seeds x 2 families",
        },
        {
            "run_id": run_id,
            "gate_id": "G02_no_final_access",
            "criterion": "ACT final data not read",
            "observed": "NO_ACT_FINAL_ACCESS",
            "required": "NO_ACT_FINAL_ACCESS",
            "status": "PASS",
            "return_to": "12_v2_split_protocol",
            "notes": "Step15 summary and Mark/dev manifest only",
        },
        {
            "run_id": run_id,
            "gate_id": "G03_added_loss_hotspot",
            "criterion": "added-token loss materially exceeds adapted base-token loss",
            "observed": f"added/base={added_base_ratio:.6f}; added_loss={adapted_added_loss:.6f}; base_loss={adapted_base_loss:.6f}",
            "required": f"ratio>{args.added_loss_ratio_threshold:.6f} to localize failure to added tokens",
            "status": "PASS" if diagnostic_gate else "FAIL",
            "return_to": "14_v2_embedding_init",
            "notes": "diagnostic gate only; PASS means repair should target added-token learning",
        },
        {
            "run_id": run_id,
            "gate_id": "G04_adapted_vs_original_context",
            "criterion": "adapted all-token loss remains above original all-token loss",
            "observed": f"adapted/original={adapted_original_ratio:.6f}; adapted_all={adapted_all_loss:.6f}; original_all={original_all_loss:.6f}",
            "required": "recorded",
            "status": "PASS",
            "return_to": "15_v2_mlm_control",
            "notes": "context for Step15/16 negative result",
        },
    ]

    score_path = step_dir / "score_table.tsv"
    category_path = step_dir / "token_category_loss.tsv"
    language_path = step_dir / "language_token_breakdown.tsv"
    token_path = step_dir / "new_token_loss_samples.tsv"
    access_path = step_dir / "v2_no_final_access_audit.tsv"
    results_path = step_dir / "results.md"
    file_results_path = step_dir / "file_results.tsv"

    write_tsv(score_path, score_rows, SCORE_FIELDS)
    write_tsv(category_path, category_rows, CATEGORY_FIELDS)
    write_tsv(language_path, language_rows, LANG_FIELDS)
    write_tsv(token_path, token_rows_out, NEW_TOKEN_FIELDS)
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
            "input_role": "dev_manifest",
            "path": str(Path(args.dev_manifest).resolve()),
            "allowed_split": "MAR_dev",
            "rows_or_files": str(count_rows(Path(args.dev_manifest))),
            "md5": md5_file(Path(args.dev_manifest)),
            "final_access": "NO",
            "status": "PASS",
        },
    ]
    write_tsv(access_path, access_rows, ["run_id", "input_role", "path", "allowed_split", "rows_or_files", "md5", "final_access", "status"])

    repair_target = "added-token learning/init/objective" if diagnostic_gate else "broader encoder/objective, not only added-token rows"
    results_path.write_text(
        f"""# Step 17 Results: V2 Added-Token Failure Analysis

Status: COMPLETED

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Artifact gate status: {'PASS' if artifact_gate else 'FAIL'}

Diagnostic gate status: {'PASS' if diagnostic_gate else 'FAIL'}

## Summary

Step 17 decomposes Step 15 Mark/dev MLM loss into original-XLM-R base-token rows and appended-token rows. ACT final was not read.

| Metric | Value |
| --- | ---: |
| adapted base-token mean loss | {adapted_base_loss:.6f} |
| adapted added-token mean loss | {adapted_added_loss:.6f} |
| added/base loss ratio | {added_base_ratio:.6f} |
| adapted added-token share | {added_token_share:.6f}% |
| adapted added-token loss share | {added_loss_share:.6f}% |
| adapted all-token mean loss | {adapted_all_loss:.6f} |
| original all-token mean loss | {original_all_loss:.6f} |
| adapted/original all-token ratio | {adapted_original_ratio:.6f} |

## Interpretation

Next repair target: `{repair_target}`.

If the diagnostic gate passes, the adapted failure is concentrated in added-token prediction and the next method revision should prioritize added-token-specific objectives, frequency-aware initialization, or staged/frozen-base training. If it fails, the repair should focus on broader encoder degradation or the experimental claim should be downgraded.

## Failure Return

Failed gate: NOT_APPLICABLE

Observed evidence: added/base ratio `{added_base_ratio:.6f}`; adapted/original ratio `{adapted_original_ratio:.6f}`

Return-to step: `14_v2_embedding_init` / `15_v2_mlm_control`

Required fix: revise initialization/objective before positive model-dependent claims.

Runtime minutes: {(time.time() - start) / 60.0:.3f}
""",
        encoding="utf-8",
    )
    file_rows = [
        file_result("score_table", score_path, "diagnostic gate table"),
        file_result("token_category_loss", category_path, "base vs added token loss"),
        file_result("language_token_breakdown", language_path, "per-language token/loss breakdown"),
        file_result("new_token_loss_samples", token_path, "high-loss/frequent added token samples"),
        file_result("no_final_access_audit", access_path, "input access audit"),
        file_result("results", results_path, "step result summary"),
    ]
    write_tsv(file_results_path, file_rows, ["file_role", "path", "rows_or_files", "bytes", "md5", "status", "notes"])

    print(f"run_id={run_id}")
    print(f"artifact_gate_status={'PASS' if artifact_gate else 'FAIL'}")
    print(f"diagnostic_gate_status={'PASS' if diagnostic_gate else 'FAIL'}")
    print(f"added_base_ratio={added_base_ratio:.6f}")
    print(f"added_token_share_pct={added_token_share:.6f}")
    print(f"added_loss_share_pct={added_loss_share:.6f}")
    print(f"repair_target={repair_target}")


if __name__ == "__main__":
    main()
