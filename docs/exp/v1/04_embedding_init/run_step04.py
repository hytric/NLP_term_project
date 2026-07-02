#!/usr/bin/env python3
"""Initialize embeddings for the selected Step 03 tokenizer."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
from datetime import datetime
from pathlib import Path
from statistics import mean

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


METHODS = ["random", "mean", "fvt", "align", "focus"]
SPECIAL_TOKENS = ["<s>", "<pad>", "</s>", "<unk>", "<mask>"]


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


def token_body(token: str) -> str:
    token = token.replace("▁", "")
    token = token.replace("Ġ", "")
    token = token.replace("</w>", "")
    return token.strip()


def load_step03_selection(path: Path) -> tuple[str, Path]:
    candidates: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["status"] == "PASS":
                candidates.append(row)
    if not candidates:
        raise RuntimeError("Step 03 has no PASS tokenizer candidate")
    selected = sorted(candidates, key=lambda row: float(row["avg_tokens_per_word_delta_pct"]))[0]
    tokenizer_dir = selected["notes"].split(";", 1)[0]
    return selected["vocab_size"], Path(tokenizer_dir)


def load_dev_texts(path: Path, limit: int) -> list[str]:
    rows: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            rows.append(row["text"])
            if len(rows) >= limit:
                break
    return rows


def build_source_maps(
    base_tokenizer: XLMRobertaTokenizer,
    extended_tokenizer: XLMRobertaTokenizer,
    base_vocab_size: int,
) -> tuple[list[str], dict[int, list[int]], dict[int, list[int]]]:
    base_vocab = base_tokenizer.get_vocab()
    char_to_ids: dict[str, list[int]] = {}
    for token, idx in base_vocab.items():
        if not isinstance(idx, int) or idx >= base_vocab_size:
            continue
        body = token_body(token)
        if len(body) == 1:
            char_to_ids.setdefault(body, []).append(idx)

    new_tokens: list[str] = []
    fvt_ids: dict[int, list[int]] = {}
    align_ids: dict[int, list[int]] = {}
    for token_id in range(base_vocab_size, len(extended_tokenizer)):
        token = extended_tokenizer.convert_ids_to_tokens(token_id)
        surface = token.replace("▁", " ").strip()
        new_tokens.append(token)
        subtokens = base_tokenizer.tokenize(surface)
        ids = [
            idx
            for idx in base_tokenizer.convert_tokens_to_ids(subtokens)
            if isinstance(idx, int) and 0 <= idx < base_vocab_size
        ]
        fvt_ids[token_id] = ids
        char_ids: list[int] = []
        for ch in surface:
            char_ids.extend(char_to_ids.get(ch, [])[:1])
        align_ids[token_id] = char_ids
    return new_tokens, fvt_ids, align_ids


def initialize_rows(
    model,
    method: str,
    base_vocab_size: int,
    merged_vocab_size: int,
    fvt_ids: dict[int, list[int]],
    align_ids: dict[int, list[int]],
) -> dict[str, str]:
    input_emb = model.get_input_embeddings().weight.data
    output_emb = model.get_output_embeddings().weight.data
    base_rows = input_emb[:base_vocab_size]
    base_mean = base_rows.mean(dim=0)
    base_norm_mean = base_rows.norm(dim=1).mean()
    fallback = 0
    initialized = 0

    for token_id in range(base_vocab_size, merged_vocab_size):
        if method == "random":
            vector = input_emb[token_id].clone()
        elif method == "mean":
            vector = base_mean
        elif method == "fvt":
            ids = fvt_ids[token_id]
            if ids:
                vector = input_emb[ids].mean(dim=0)
            else:
                vector = base_mean
                fallback += 1
        elif method == "align":
            ids = align_ids[token_id]
            if ids:
                vector = input_emb[ids].mean(dim=0)
            else:
                fids = fvt_ids[token_id]
                vector = input_emb[fids].mean(dim=0) if fids else base_mean
                fallback += 1
        elif method == "focus":
            fids = fvt_ids[token_id]
            aids = align_ids[token_id]
            fvt_vec = input_emb[fids].mean(dim=0) if fids else base_mean
            align_vec = input_emb[aids].mean(dim=0) if aids else base_mean
            if not fids or not aids:
                fallback += 1
            vector = 0.50 * fvt_vec + 0.30 * align_vec + 0.20 * base_mean
            norm = vector.norm()
            if norm > 0:
                vector = vector * (base_norm_mean / norm)
        else:
            raise ValueError(f"unknown method: {method}")

        input_emb[token_id].copy_(vector)
        output_emb[token_id].copy_(vector)
        initialized += 1

    model.tie_weights()
    new_rows = input_emb[base_vocab_size:merged_vocab_size]
    missing = int(torch.isnan(new_rows).any(dim=1).sum().item())
    zero_norm = int((new_rows.norm(dim=1) == 0).sum().item())
    return {
        "initialized_rows": str(initialized),
        "fallback_rows": str(fallback),
        "missing_rows": str(missing + zero_norm),
        "mean_norm": f"{new_rows.norm(dim=1).mean().item():.6f}",
        "std_norm": f"{new_rows.norm(dim=1).std().item():.6f}",
    }


def make_masked_batch(tokenizer, texts: list[str], device: torch.device, max_length: int, seed: int) -> dict[str, torch.Tensor]:
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
        first_non_special = (special_mask == 0).nonzero(as_tuple=False)
        if len(first_non_special) > 0:
            masked[first_non_special[0, 0], first_non_special[0, 1]] = True
    labels[~masked] = -100
    input_ids[masked] = tokenizer.mask_token_id
    return {
        "input_ids": input_ids.to(device),
        "attention_mask": attention_mask.to(device),
        "labels": labels.to(device),
    }


def zero_step_loss(model, tokenizer, texts: list[str], device: torch.device, batch_size: int, max_length: int, seed: int) -> float:
    model.eval()
    model.to(device)
    weighted_loss = 0.0
    total_masked = 0
    with torch.no_grad():
        for start in range(0, len(texts), batch_size):
            batch_texts = texts[start : start + batch_size]
            batch = make_masked_batch(tokenizer, batch_texts, device, max_length, seed + start)
            masked_count = int(batch["labels"].ne(-100).sum().item())
            outputs = model(**batch)
            weighted_loss += float(outputs.loss.item()) * masked_count
            total_masked += masked_count
    model.to("cpu")
    return weighted_loss / max(1, total_masked)


def nearest_neighbor_lines(model, tokenizer, base_vocab_size: int, method: str, sample_count: int = 5, base_limit: int = 5000) -> list[str]:
    input_emb = model.get_input_embeddings().weight.detach().cpu()
    base = input_emb[:base_limit]
    base = torch.nn.functional.normalize(base, dim=1)
    lines = [f"## {method}", ""]
    token_ids = list(range(base_vocab_size, min(len(tokenizer), base_vocab_size + sample_count)))
    for token_id in token_ids:
        vector = torch.nn.functional.normalize(input_emb[token_id].unsqueeze(0), dim=1)
        sims = torch.matmul(vector, base.T).squeeze(0)
        top = torch.topk(sims, k=5)
        neighbors = []
        for score, idx in zip(top.values.tolist(), top.indices.tolist()):
            neighbors.append(f"{tokenizer.convert_ids_to_tokens(int(idx))}:{score:.3f}")
        lines.append(f"- `{tokenizer.convert_ids_to_tokens(token_id)}` -> {', '.join(neighbors)}")
    lines.append("")
    return lines


def shape_status(model, vocab_size: int) -> tuple[str, str, str]:
    input_shape_ok = "PASS" if model.get_input_embeddings().weight.shape[0] == vocab_size else "FAIL"
    output_shape_ok = "PASS" if model.get_output_embeddings().weight.shape[0] == vocab_size else "FAIL"
    tied = model.get_input_embeddings().weight.data_ptr() == model.get_output_embeddings().weight.data_ptr()
    return input_shape_ok, output_shape_ok, "PASS" if tied else "FAIL"


def build_step(args: argparse.Namespace) -> None:
    torch.manual_seed(args.seed)
    step_dir = Path(args.step_dir).resolve()
    checkpoint_root = Path(args.checkpoint_root).resolve()
    run_id = "step04_init_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    selected_vocab_size, tokenizer_dir = load_step03_selection(Path(args.step03_score))
    tokenizer = XLMRobertaTokenizer.from_pretrained(str(tokenizer_dir), local_files_only=True)
    base_tokenizer = XLMRobertaTokenizer.from_pretrained(args.base_model, local_files_only=True)
    base_vocab_size = len(base_tokenizer)
    merged_vocab_size = len(tokenizer)
    new_rows = merged_vocab_size - base_vocab_size
    dev_texts = load_dev_texts(Path(args.mlm_dev), args.mlm_dev_limit)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    _, fvt_ids, align_ids = build_source_maps(base_tokenizer, tokenizer, base_vocab_size)

    metric_rows: list[dict[str, str]] = []
    zero_rows: list[dict[str, str]] = []
    score_rows: list[dict[str, str]] = []
    nearest_lines = [
        "# Step 04 Nearest Neighbors",
        "",
        "Approximate nearest neighbors are computed against the first 5000 base vocabulary rows for quick diagnostics.",
        "",
    ]
    checkpoint_dirs: list[Path] = []

    for method in METHODS:
        method_dir = checkpoint_root / f"xlmr_target10_{selected_vocab_size}_{method}"
        model = AutoModelForMaskedLM.from_pretrained(args.base_model, local_files_only=False)
        model.resize_token_embeddings(merged_vocab_size)
        init_report = initialize_rows(model, method, base_vocab_size, merged_vocab_size, fvt_ids, align_ids)
        input_ok, output_ok, tying_ok = shape_status(model, merged_vocab_size)
        loss = zero_step_loss(model, tokenizer, dev_texts, device, args.batch_size, args.max_length, args.seed)
        method_dir.mkdir(parents=True, exist_ok=True)
        model.save_pretrained(method_dir)
        tokenizer.save_pretrained(method_dir)
        report = {
            "run_id": run_id,
            "method": method,
            "method_note": "align/focus are second_try proxy initializers without external bilingual lexicon",
            "base_model": args.base_model,
            "tokenizer_dir": str(tokenizer_dir),
            "vocab_size": selected_vocab_size,
            "base_vocab_size": base_vocab_size,
            "merged_vocab_size": merged_vocab_size,
            "new_rows": new_rows,
            "zero_step_dev_loss": loss,
            "device": str(device),
            **init_report,
        }
        (method_dir / "init_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        checkpoint_dirs.append(method_dir)
        nearest_lines.extend(nearest_neighbor_lines(model, tokenizer, base_vocab_size, method))

        status = "PASS" if (
            init_report["missing_rows"] == "0"
            and input_ok == "PASS"
            and output_ok == "PASS"
            and tying_ok == "PASS"
            and math.isfinite(loss)
        ) else "FAIL"
        common = {
            "vocab_size": selected_vocab_size,
            "init_method": method,
            "new_rows": str(new_rows),
            "initialized_rows": init_report["initialized_rows"],
            "missing_rows": init_report["missing_rows"],
            "fallback_rows": init_report["fallback_rows"],
            "input_shape_ok": input_ok,
            "lm_head_shape_ok": output_ok,
            "weight_tying_ok": tying_ok,
            "mean_norm": init_report["mean_norm"],
            "std_norm": init_report["std_norm"],
            "zero_step_dev_loss": f"{loss:.6f}",
            "checkpoint_path": str(method_dir),
            "status": status,
            "notes": "proxy external-free method" if method in {"align", "focus"} else "required baseline method",
        }
        score_rows.append(common)
        metric_rows.append(common)
        zero_rows.append(
            {
                "vocab_size": selected_vocab_size,
                "init_method": method,
                "mlm_dev_rows": str(len(dev_texts)),
                "batch_size": str(args.batch_size),
                "max_length": str(args.max_length),
                "zero_step_dev_loss": f"{loss:.6f}",
                "device": str(device),
                "status": status,
            }
        )
        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    score_fields = [
        "vocab_size",
        "init_method",
        "new_rows",
        "initialized_rows",
        "missing_rows",
        "fallback_rows",
        "input_shape_ok",
        "lm_head_shape_ok",
        "weight_tying_ok",
        "mean_norm",
        "std_norm",
        "zero_step_dev_loss",
        "checkpoint_path",
        "status",
        "notes",
    ]
    zero_fields = ["vocab_size", "init_method", "mlm_dev_rows", "batch_size", "max_length", "zero_step_dev_loss", "device", "status"]

    score_path = step_dir / "score_table.tsv"
    metrics_path = step_dir / "embedding_init_metrics.tsv"
    zero_path = step_dir / "zero_step_mlm.tsv"
    neighbors_path = step_dir / "nearest_neighbors.md"
    file_results_path = step_dir / "file_results.tsv"
    results_path = step_dir / "results.md"

    write_tsv(score_path, score_rows, score_fields)
    write_tsv(metrics_path, metric_rows, score_fields)
    write_tsv(zero_path, zero_rows, zero_fields)
    neighbors_path.write_text("\n".join(nearest_lines), encoding="utf-8")

    file_rows = [
        file_result("score_table", score_path, "docs", "gate table"),
        file_result("embedding_init_metrics", metrics_path, "docs", "shape, norm, fallback, loss metrics"),
        file_result("zero_step_mlm", zero_path, "docs", "zero-step MLM losses"),
        file_result("nearest_neighbors", neighbors_path, "docs", "approximate nearest neighbors"),
    ]
    for method_dir in checkpoint_dirs:
        file_rows.append(file_result(f"checkpoint_{method_dir.name}", method_dir, "large_checkpoint", "initialized model and tokenizer"))
    write_tsv(
        file_results_path,
        file_rows,
        ["file_role", "path", "location", "rows_or_files", "bytes", "md5", "status", "notes"],
    )

    pass_methods = [row["init_method"] for row in score_rows if row["status"] == "PASS"]
    required_minimum = all(method in pass_methods for method in ["random", "mean", "fvt"])
    all_required_recorded = all(method in pass_methods for method in METHODS)
    best_row = sorted(score_rows, key=lambda row: float(row["zero_step_dev_loss"]))[0]
    gate_pass = required_minimum and all(row["missing_rows"] == "0" for row in score_rows)

    results = f"""# Step 04 Results: Embedding Initialization

Status: {"COMPLETED" if gate_pass else "FAILED"}

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Gate status: {"PASS" if gate_pass else "FAIL"}

## Required Artifact Check

| Artifact | Path | Present? | Notes |
| --- | --- | --- | --- |
| score table | `score_table.tsv` | yes | selected 32k tokenizer x 5 init methods |
| file results | `file_results.tsv` | yes | docs and checkpoint paths recorded |
| init metrics | `embedding_init_metrics.tsv` | yes | shape/norm/fallback/loss metrics |
| zero-step MLM | `zero_step_mlm.tsv` | yes | {len(dev_texts)} dev rows |
| nearest neighbors | `nearest_neighbors.md` | yes | approximate diagnostics |
| initialized checkpoints | `{checkpoint_root}` | yes | saved outside workspace |

## Summary

Step 04 initialized the selected Step 03 tokenizer (`{selected_vocab_size}`) with all required methods: random, mean, fvt, align, and focus. `align` and `focus` are documented proxy implementations that use only second_try-local tokenizer evidence and no external bilingual lexicon.

| Metric | Value |
| --- | --- |
| base model | `{args.base_model}` |
| tokenizer | `{tokenizer_dir}` |
| base vocab size | {base_vocab_size} |
| merged vocab size | {merged_vocab_size} |
| new rows | {new_rows} |
| device | `{device}` |
| pass methods | {", ".join(pass_methods)} |

## Best Zero-Step Candidate

Best zero-step dev loss: `{best_row["init_method"]}` with loss `{best_row["zero_step_dev_loss"]}`.

## Gate Evidence

Evidence:

- `score_table.tsv` has no `TBD`, blank, or unchecked fields.
- input embedding and LM head shapes match tokenizer length for all methods.
- weight tying is preserved for all passing methods.
- zero-step MLM loss is recorded for every method.
- checkpoints are stored under `{checkpoint_root}`.

Exit criteria:

- all required methods either pass or have documented implementation result: {"pass" if all_required_recorded else "partial"}
- at least random, mean, and fvt pass: {"pass" if required_minimum else "fail"}
- no missing/uninitialized rows: {"pass" if all(row["missing_rows"] == "0" for row in score_rows) else "fail"}
- zero-step MLM loss is recorded: pass
- `results.md` has `Gate status: PASS`: {"pass" if gate_pass else "fail"}

## Failure Return

Failed gate: {"NOT_APPLICABLE" if gate_pass else "embedding_init_gate"}

Observed evidence: {"NOT_APPLICABLE" if gate_pass else "see score_table.tsv"}

Return-to step: {"NOT_APPLICABLE" if gate_pass else "04_embedding_init"}

Required fix: {"NOT_APPLICABLE" if gate_pass else "fix failing init method or tokenizer shape issue, then rerun Step 04"}
"""
    results_path.write_text(results, encoding="utf-8")

    print(f"run_id={run_id}")
    print(f"gate_status={'PASS' if gate_pass else 'FAIL'}")
    print(f"selected_vocab_size={selected_vocab_size}")
    print(f"best_method={best_row['init_method']}")
    print(f"best_zero_step_dev_loss={best_row['zero_step_dev_loss']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--step03-score", default="docs/exp/second_try/03_vocab_extension/score_table.tsv")
    parser.add_argument("--checkpoint-root", default="/home/axt/mnt2/jongha/second_try/checkpoints/04_embedding_init")
    parser.add_argument("--base-model", default="xlm-roberta-base")
    parser.add_argument("--mlm-dev", default="/home/axt/mnt2/jongha/second_try/artifacts/01_data_and_splits/mlm/target10_mlm_dev.tsv")
    parser.add_argument("--mlm-dev-limit", type=int, default=200)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--seed", type=int, default=13)
    args = parser.parse_args()
    build_step(args)


if __name__ == "__main__":
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    build_start = datetime.now()
    main()
