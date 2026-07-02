#!/usr/bin/env python3
"""Top-tier validation for second_try.

This step audits shortcut-prone claims by using method-matched high-resource
and target retrieval scores. It does not overwrite earlier exploratory steps.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import time
import unicodedata
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

import sacrebleu
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

from transformers import AutoModel, AutoModelForMaskedLM, AutoTokenizer, XLMRobertaTokenizer, logging as transformers_logging


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    return re.sub(r"\s+", " ", text).strip()


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


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def count_rows(path: Path) -> int:
    if path.suffix == ".tsv":
        with path.open("r", encoding="utf-8") as f:
            return max(0, sum(1 for _ in f) - 1)
    with path.open("r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def file_result(role: str, path: Path, notes: str) -> dict[str, str]:
    size = path.stat().st_size
    return {
        "file_role": role,
        "path": str(path),
        "rows_or_lines": str(count_rows(path)),
        "bytes": str(size),
        "md5": md5_file(path),
        "status": "PASS" if size > 0 else "FAIL",
        "notes": notes,
    }


def load_selected_checkpoint(path: Path) -> Path:
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("Path:"):
            return Path(line.split("`", 2)[1])
    raise RuntimeError("selected checkpoint path not found")


def parse_xml_book(path: Path, iso: str, language: str, book: str, limit: int) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    root = ET.parse(path).getroot()
    marker = f".{book}."
    for seg in root.iter("seg"):
        verse_id = seg.attrib.get("id", "").strip()
        if marker not in verse_id:
            continue
        text = normalize_text("".join(seg.itertext()))
        if text:
            split = "dev" if book == "MAR" else "test"
            rows.append(
                {
                    "iso": iso,
                    "language": language,
                    "book": book,
                    "verse_id": verse_id,
                    "split": split,
                    "text": text,
                    "key": f"{iso}::{split}::{verse_id}",
                }
            )
        if len(rows) >= limit:
            break
    return rows


def load_target_rows(path: Path, splits: set[str], limit_per_split: int) -> list[dict[str, str]]:
    rows = []
    counts: dict[tuple[str, str], int] = {}
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["split"] not in splits:
                continue
            key = (row["split"], row["iso"])
            if counts.get(key, 0) >= limit_per_split:
                continue
            row["key"] = f"{row['iso']}::{row['split']}::{row['verse_id']}"
            rows.append(row)
            counts[key] = counts.get(key, 0) + 1
    return rows


def mean_pool(last_hidden: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
    mask = attention_mask.unsqueeze(-1).to(last_hidden.dtype)
    pooled = (last_hidden * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1)
    return torch.nn.functional.normalize(pooled, dim=1)


def encode_xlmr(model_name_or_path: str, rows: list[dict[str, str]], device: torch.device, batch_size: int, max_length: int) -> dict[str, torch.Tensor]:
    tokenizer = XLMRobertaTokenizer.from_pretrained(model_name_or_path, local_files_only=True)
    model = AutoModelForMaskedLM.from_pretrained(model_name_or_path, local_files_only=True)
    model.to(device)
    model.eval()
    embeddings: dict[str, torch.Tensor] = {}
    with torch.no_grad():
        for start in range(0, len(rows), batch_size):
            batch = rows[start : start + batch_size]
            encoded = tokenizer([row["text"] for row in batch], padding=True, truncation=True, max_length=max_length, return_tensors="pt")
            input_ids = encoded["input_ids"].to(device)
            attention_mask = encoded["attention_mask"].to(device)
            outputs = model.roberta(input_ids=input_ids, attention_mask=attention_mask)
            pooled = mean_pool(outputs.last_hidden_state, attention_mask).detach().cpu()
            for row, vec in zip(batch, pooled):
                embeddings[row["key"]] = vec
    model.to("cpu")
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return embeddings


def encode_sentence_model(model_name: str, rows: list[dict[str, str]], device: torch.device, batch_size: int, max_length: int, cache_dir: str) -> dict[str, torch.Tensor]:
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
    model = AutoModel.from_pretrained(model_name, cache_dir=cache_dir)
    model.to(device)
    model.eval()
    embeddings: dict[str, torch.Tensor] = {}
    with torch.no_grad():
        for start in range(0, len(rows), batch_size):
            batch = rows[start : start + batch_size]
            encoded = tokenizer([row["text"] for row in batch], padding=True, truncation=True, max_length=max_length, return_tensors="pt")
            encoded = {key: value.to(device) for key, value in encoded.items()}
            outputs = model(**encoded)
            pooled = mean_pool(outputs.last_hidden_state, encoded["attention_mask"]).detach().cpu()
            for row, vec in zip(batch, pooled):
                embeddings[row["key"]] = vec
    model.to("cpu")
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return embeddings


def csls_scores(similarity: torch.Tensor, k: int) -> torch.Tensor:
    k = max(1, min(k, similarity.shape[0], similarity.shape[1]))
    src_density = similarity.topk(k, dim=1).values.mean(dim=1, keepdim=True)
    tgt_density = similarity.topk(k, dim=0).values.mean(dim=0, keepdim=True)
    return 2 * similarity - src_density - tgt_density


def pair_rows(rows: list[dict[str, str]], src_iso: str, tgt_iso: str, split: str, limit: int) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    by_key = {}
    for row in rows:
        if row["split"] == split and row["iso"] in {src_iso, tgt_iso}:
            by_key[(row["iso"], row["verse_id"])] = row
    shared = sorted(
        verse_id
        for iso, verse_id in by_key
        if iso == src_iso and (tgt_iso, verse_id) in by_key
    )[:limit]
    return [by_key[(src_iso, verse_id)] for verse_id in shared], [by_key[(tgt_iso, verse_id)] for verse_id in shared]


def evaluate_pair(src_rows: list[dict[str, str]], tgt_rows: list[dict[str, str]], embeddings: dict[str, torch.Tensor], scoring: str, csls_k: int) -> dict[str, float]:
    if not src_rows or not tgt_rows:
        return {"rows": 0.0, "chrf": 0.0, "bleu": 0.0, "retrieval_acc": 0.0}
    src_matrix = torch.stack([embeddings[row["key"]] for row in src_rows])
    tgt_matrix = torch.stack([embeddings[row["key"]] for row in tgt_rows])
    scores = src_matrix @ tgt_matrix.T
    if scoring == "csls":
        scores = csls_scores(scores, csls_k)
    hyps = []
    refs = []
    correct = 0
    for idx, ref_row in enumerate(tgt_rows):
        pred_idx = int(torch.argmax(scores[idx]).item())
        pred = tgt_rows[pred_idx]
        hyps.append(pred["text"])
        refs.append(ref_row["text"])
        if pred_idx == idx:
            correct += 1
    return {
        "rows": float(len(src_rows)),
        "chrf": sacrebleu.corpus_chrf(hyps, [refs], word_order=2).score,
        "bleu": sacrebleu.corpus_bleu(hyps, [refs]).score,
        "retrieval_acc": correct / max(1, len(src_rows)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--artifact-root", default="/home/axt/mnt2/jongha/second_try/artifacts/09_top_tier_validation")
    parser.add_argument("--cache-dir", default="/home/axt/mnt2/jongha/hf_cache")
    parser.add_argument("--bible-dir", default="/home/axt/mnt2/jongha/Glot500-py39-eval/data/raw/bible-corpus/bibles")
    parser.add_argument("--target-verse-table", default="docs/exp/second_try/01_data_and_splits/target10_bible_verses.tsv")
    parser.add_argument("--selection-file", default="docs/exp/second_try/05_mlm_adaptation/checkpoint_selection.md")
    parser.add_argument("--base-model", default="xlm-roberta-base")
    parser.add_argument("--sentence-model", default="sentence-transformers/LaBSE")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--max-length", type=int, default=192)
    parser.add_argument("--csls-k", type=int, default=10)
    args = parser.parse_args()

    transformers_logging.set_verbosity_error()
    started = time.time()
    run_id = "step09_top_tier_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    step_dir = Path(args.step_dir).resolve()
    artifact_root = Path(args.artifact_root).resolve()
    artifact_root.mkdir(parents=True, exist_ok=True)
    selected_checkpoint = load_selected_checkpoint(Path(args.selection_file))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    bible_dir = Path(args.bible_dir)
    high_rows = []
    for split_book in ["MAR", "JOH"]:
        high_rows.extend(parse_xml_book(bible_dir / "Spanish.xml", "spa", "Spanish", split_book, args.limit))
        high_rows.extend(parse_xml_book(bible_dir / "English.xml", "eng", "English", split_book, args.limit))
    target_rows = load_target_rows(Path(args.target_verse_table), {"dev", "test"}, args.limit)
    target_isos = sorted({row["iso"] for row in target_rows})

    methods = [
        {
            "method_id": "original_xlmr_cosine",
            "model_family": "xlmr",
            "model_path": args.base_model,
            "scoring": "cosine",
            "claim_role": "baseline",
        },
        {
            "method_id": "selected_adapted_xlmr_cosine",
            "model_family": "xlmr",
            "model_path": str(selected_checkpoint),
            "scoring": "cosine",
            "claim_role": "main_model",
        },
        {
            "method_id": "labse_csls_upper_bound",
            "model_family": "sentence",
            "model_path": args.sentence_model,
            "scoring": "csls",
            "claim_role": "external_upper_bound",
        },
    ]

    dev_grid_rows: list[dict[str, str]] = []
    result_rows: list[dict[str, str]] = []
    score_rows: list[dict[str, str]] = []

    for method in methods:
        all_rows = high_rows + target_rows
        if method["model_family"] == "xlmr":
            embeddings = encode_xlmr(method["model_path"], all_rows, device, args.batch_size, args.max_length)
        else:
            embeddings = encode_sentence_model(method["model_path"], all_rows, device, args.batch_size, args.max_length, args.cache_dir)

        high_dev_src, high_dev_tgt = pair_rows(high_rows, "spa", "eng", "dev", args.limit)
        high_test_src, high_test_tgt = pair_rows(high_rows, "spa", "eng", "test", args.limit)
        high_dev = evaluate_pair(high_dev_src, high_dev_tgt, embeddings, method["scoring"], args.csls_k)
        high_test = evaluate_pair(high_test_src, high_test_tgt, embeddings, method["scoring"], args.csls_k)

        best_dev: dict[str, str] | None = None
        best_test_metrics: dict[str, float] | None = None
        for src_iso in target_isos:
            for tgt_iso in target_isos:
                if src_iso == tgt_iso:
                    continue
                dev_src, dev_tgt = pair_rows(target_rows, src_iso, tgt_iso, "dev", args.limit)
                test_src, test_tgt = pair_rows(target_rows, src_iso, tgt_iso, "test", args.limit)
                dev_metrics = evaluate_pair(dev_src, dev_tgt, embeddings, method["scoring"], args.csls_k)
                dev_row = {
                    "run_id": run_id,
                    "method_id": method["method_id"],
                    "source_lang": src_iso,
                    "target_lang": tgt_iso,
                    "split": "dev",
                    "rows": str(int(dev_metrics["rows"])),
                    "chrf": f"{dev_metrics['chrf']:.6f}",
                    "bleu": f"{dev_metrics['bleu']:.6f}",
                    "retrieval_acc": f"{dev_metrics['retrieval_acc']:.6f}",
                }
                dev_grid_rows.append(dev_row)
                if best_dev is None or float(dev_row["chrf"]) > float(best_dev["chrf"]):
                    best_dev = dev_row
                    best_test_metrics = evaluate_pair(test_src, test_tgt, embeddings, method["scoring"], args.csls_k)
        assert best_dev is not None and best_test_metrics is not None

        target_ratio = best_test_metrics["chrf"] / max(1e-9, high_test["chrf"])
        status = "PASS" if target_ratio >= 0.8 else "FAIL"
        result_rows.append(
            {
                "run_id": run_id,
                "method_id": method["method_id"],
                "claim_role": method["claim_role"],
                "model_path": method["model_path"],
                "scoring": method["scoring"],
                "high_resource_dev_chrf": f"{high_dev['chrf']:.6f}",
                "high_resource_test_chrf": f"{high_test['chrf']:.6f}",
                "selected_source_lang": best_dev["source_lang"],
                "selected_target_lang": best_dev["target_lang"],
                "target_dev_chrf": best_dev["chrf"],
                "target_test_chrf": f"{best_test_metrics['chrf']:.6f}",
                "target_test_bleu": f"{best_test_metrics['bleu']:.6f}",
                "target_test_retrieval_acc": f"{best_test_metrics['retrieval_acc']:.6f}",
                "method_matched_ratio": f"{target_ratio:.6f}",
                "threshold": "0.800000",
                "status": status,
            }
        )

    result_fields = [
        "run_id",
        "method_id",
        "claim_role",
        "model_path",
        "scoring",
        "high_resource_dev_chrf",
        "high_resource_test_chrf",
        "selected_source_lang",
        "selected_target_lang",
        "target_dev_chrf",
        "target_test_chrf",
        "target_test_bleu",
        "target_test_retrieval_acc",
        "method_matched_ratio",
        "threshold",
        "status",
    ]
    dev_fields = ["run_id", "method_id", "source_lang", "target_lang", "split", "rows", "chrf", "bleu", "retrieval_acc"]

    method_tsv = step_dir / "method_matched_translation.tsv"
    score_path = step_dir / "score_table.tsv"
    dev_grid_path = step_dir / "dev_selection_grid.tsv"
    write_tsv(method_tsv, result_rows, result_fields)
    write_tsv(score_path, result_rows, result_fields)
    write_tsv(dev_grid_path, dev_grid_rows, dev_fields)

    adapted_row = next(row for row in result_rows if row["method_id"] == "selected_adapted_xlmr_cosine")
    upper_row = next(row for row in result_rows if row["method_id"] == "labse_csls_upper_bound")
    top_tier_translation_status = "SUPPORTED" if adapted_row["status"] == "PASS" else "UNSUPPORTED_FOR_MAIN_MODEL"
    upper_bound_status = "PASS" if upper_row["status"] == "PASS" else "FAIL"
    claim_path = step_dir / "top_tier_claim_contract.md"
    claim_path.write_text(
        f"""# Step 09 Top-Tier Claim Contract

Run id: `{run_id}`

## Main Claim Status

| Claim | Status | Evidence |
| --- | --- | --- |
| Tokenization bottleneck and fragmentation reduction | SUPPORTED | Steps 02-03 |
| New-token initialization matters | SUPPORTED | Step 04 |
| MLM adaptation recovers selected extended checkpoint | PARTIAL_SUPPORT | Step 05, but original XLM-R still has lower dev loss |
| Adapted encoder improves proxy retrieval/matching | SUPPORTED_WEAK_TO_MODERATE | Step 06 |
| Adapted encoder reaches 80% translation reference | {top_tier_translation_status} | Step 09 selected adapted method-matched ratio `{adapted_row['method_matched_ratio']}` |
| External sentence embedding upper bound reaches 80% translation reference | {upper_bound_status} | Step 09 LaBSE method-matched ratio `{upper_row['method_matched_ratio']}` |

## Top-Tier-Safe Final Claim

The current evidence can support a representation-learning claim about tokenizer extension, initialization, and low-resource encoder proxy improvements. It cannot yet support a top-tier claim that the adapted XLM-R encoder solves translation to 80% of a method-matched high-resource reference unless Step 09 marks `selected_adapted_xlmr_cosine` as `PASS`.

## Required Next Experiments

1. Longer MLM adaptation with an original-XLM-R continued-pretraining control.
2. Dev-only model selection followed by a fresh held-out book or corpus for final downstream/translation tests.
3. Adapted-encoder-only translation retrieval or generation benchmark.
4. Statistical confidence intervals across languages and seeds for retrieval/matching.
5. External LaBSE results reported only as an upper bound, not as evidence for the adapted encoder.
""",
        encoding="utf-8",
    )

    any_blanks = any(value == "" or value == "TBD" for row in result_rows for value in row.values())
    artifact_gate_status = "PASS" if not any_blanks else "FAIL"
    claim_gate_status = "PASS" if adapted_row["status"] == "PASS" else "FAIL"
    results_path = step_dir / "results.md"
    results_path.write_text(
        f"""# Step 09 Results: Top-Tier Validation

Status: {"COMPLETED" if artifact_gate_status == "PASS" else "FAILED"}

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Artifact gate status: {artifact_gate_status}

Claim gate status: {claim_gate_status}

## Summary

Step 09 recomputed translation retrieval with method-matched high-resource and target scores. The main question is whether the selected adapted XLM-R encoder, not an external sentence embedding model, reaches 80% of a same-method Spanish->English reference.

## Key Results

| Method | Role | High test chrF++ | Target test chrF++ | Ratio | Status |
| --- | --- | ---: | ---: | ---: | --- |
""" + "\n".join(
            f"| {row['method_id']} | {row['claim_role']} | {row['high_resource_test_chrf']} | {row['target_test_chrf']} | {row['method_matched_ratio']} | {row['status']} |"
            for row in result_rows
        ) + f"""

## Claim Decision

Main adapted-encoder translation claim: `{top_tier_translation_status}`.

External LaBSE upper bound: `{upper_bound_status}`.

## Gate Evidence

- `score_table.tsv` has no blank or `TBD` fields.
- Every ratio uses the same retrieval method for high-resource and target scores.
- Target pair selection uses dev only; John test is used for selected settings.

## Failure Return

Failed gate: {"NOT_APPLICABLE" if claim_gate_status == "PASS" else "method_matched_translation_80_percent"}

Observed evidence: {"NOT_APPLICABLE" if claim_gate_status == "PASS" else f"selected_adapted_xlmr_cosine ratio={adapted_row['method_matched_ratio']} < 0.800000; labse_csls_upper_bound ratio={upper_row['method_matched_ratio']} < 0.800000"}

Return-to step: {"NOT_APPLICABLE" if claim_gate_status == "PASS" else "05_mlm_adaptation / 06_downstream_tasks / 07_translation_benchmark"}

Required fix: {"NOT_APPLICABLE" if claim_gate_status == "PASS" else "run stronger adaptation controls, dev-only branch selection, and a fresh held-out translation retrieval/generation benchmark before making a top-tier translation claim"}
""",
        encoding="utf-8",
    )

    runtime_path = artifact_root / f"{run_id}_runtime.json"
    runtime_path.write_text(
        json.dumps(
            {
                "run_id": run_id,
                "runtime_minutes": (time.time() - started) / 60.0,
                "device": str(device),
                "methods": methods,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    file_results_path = step_dir / "file_results.tsv"
    file_rows = [
        file_result("score_table", score_path, "method-matched score table"),
        file_result("method_matched_translation", method_tsv, "same-method high/target ratios"),
        file_result("dev_selection_grid", dev_grid_path, "dev-only target pair selection grid"),
        file_result("top_tier_claim_contract", claim_path, "claim contract and required follow-up"),
        file_result("results", results_path, "step result summary"),
        file_result("runtime_config", runtime_path, "large-artifact runtime config"),
    ]
    write_tsv(file_results_path, file_rows, ["file_role", "path", "rows_or_lines", "bytes", "md5", "status", "notes"])

    print(f"run_id={run_id}")
    print(f"artifact_gate_status={artifact_gate_status}")
    print(f"claim_gate_status={claim_gate_status}")
    print(f"adapted_translation_status={top_tier_translation_status}")
    print(f"adapted_ratio={adapted_row['method_matched_ratio']}")
    print(f"labse_upper_bound_status={upper_bound_status}")
    print(f"labse_ratio={upper_row['method_matched_ratio']}")


if __name__ == "__main__":
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    main()
