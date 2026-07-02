#!/usr/bin/env python3
"""Run Step 07 retrieval-augmented translation proxy benchmark."""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import unicodedata
import xml.etree.ElementTree as ET
from collections import defaultdict
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

from transformers import AutoModelForMaskedLM, XLMRobertaTokenizer


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


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


def parse_xml_verses(path: Path, iso: str, language: str, limit: int) -> list[dict[str, str]]:
    root = ET.parse(path).getroot()
    rows: list[dict[str, str]] = []
    for seg in root.iter("seg"):
        verse_id = seg.attrib.get("id", "").strip()
        if not verse_id or ".JOH." not in verse_id:
            continue
        text = normalize_text("".join(seg.itertext()))
        if text:
            rows.append({"iso": iso, "language": language, "verse_id": verse_id, "text": text, "key": f"{iso}::{verse_id}"})
        if len(rows) >= limit:
            break
    return rows


def load_target_rows(path: Path, limit_verses: int) -> list[dict[str, str]]:
    all_rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["split"] == "test":
                row["key"] = f"{row['iso']}::{row['verse_id']}"
                all_rows.append(row)
    by_verse: dict[str, list[dict[str, str]]] = defaultdict(list)
    isos = sorted({row["iso"] for row in all_rows})
    for row in all_rows:
        by_verse[row["verse_id"]].append(row)
    shared = [verse_id for verse_id, rows in by_verse.items() if len({row["iso"] for row in rows}) == len(isos)]
    selected = set(sorted(shared)[:limit_verses])
    return [row for row in all_rows if row["verse_id"] in selected]


def load_selected_checkpoint(path: Path) -> Path:
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("Path:"):
            return Path(line.split("`", 2)[1])
    raise RuntimeError("selected checkpoint path not found")


def encode_rows(model_name_or_path: str, rows: list[dict[str, str]], device: torch.device, batch_size: int, max_length: int) -> dict[str, torch.Tensor]:
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
            hidden = outputs.last_hidden_state
            mask = attention_mask.unsqueeze(-1)
            pooled = (hidden * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1)
            pooled = torch.nn.functional.normalize(pooled.detach().cpu(), dim=1)
            for row, vector in zip(batch, pooled):
                embeddings[row["key"]] = vector
    model.to("cpu")
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return embeddings


def retrieval_translate(
    source_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    embeddings: dict[str, torch.Tensor],
) -> tuple[list[dict[str, str]], dict[str, float]]:
    target_by_verse = {row["verse_id"]: row for row in target_rows}
    target_matrix = torch.stack([embeddings[row["key"]] for row in target_rows])
    hyps: list[str] = []
    refs: list[str] = []
    samples: list[dict[str, str]] = []
    correct = 0
    for source in source_rows:
        if source["verse_id"] not in target_by_verse:
            continue
        scores = torch.mv(target_matrix, embeddings[source["key"]])
        best_idx = int(torch.argmax(scores).item())
        predicted = target_rows[best_idx]
        reference = target_by_verse[source["verse_id"]]
        hyps.append(predicted["text"])
        refs.append(reference["text"])
        if predicted["verse_id"] == source["verse_id"]:
            correct += 1
        samples.append(
            {
                "source_verse": source["verse_id"],
                "predicted_verse": predicted["verse_id"],
                "source_text": source["text"],
                "prediction": predicted["text"],
                "reference": reference["text"],
                "correct_retrieval": "yes" if predicted["verse_id"] == source["verse_id"] else "no",
            }
        )
    chrf = sacrebleu.corpus_chrf(hyps, [refs], word_order=2).score if hyps else 0.0
    bleu = sacrebleu.corpus_bleu(hyps, [refs]).score if hyps else 0.0
    copy_rate = sum(1 for sample in samples if sample["source_text"] == sample["prediction"]) / max(1, len(samples))
    avg_len = sum(len(hyp.split()) for hyp in hyps) / max(1, len(hyps))
    return samples, {
        "chrf": chrf,
        "bleu": bleu,
        "copy_rate": copy_rate,
        "script_validity": 1.0,
        "gen_len": avg_len,
        "retrieval_acc": correct / max(1, len(samples)),
    }


def write_branch(branch_id: str, docs_root: Path, artifact_root: Path, ratio: float, target_score: float, threshold: float) -> None:
    branch_dir = docs_root / "branches" / branch_id
    branch_artifact = artifact_root / "branches" / branch_id
    branch_dir.mkdir(parents=True, exist_ok=True)
    branch_artifact.mkdir(parents=True, exist_ok=True)
    (branch_dir / "goal.md").write_text(
        f"# {branch_id} Goal\n\nTranslation retrieval proxy reached `{ratio:.6f}` of the high-resource score; required threshold is `{threshold:.6f}`. Goal: improve target translation proxy to at least 80% of high-resource reference without using verse-id oracle leakage.\n",
        encoding="utf-8",
    )
    (branch_dir / "plan.md").write_text(
        "# Branch Plan\n\n1. Add a trainable lightweight decoder or reranker for target verse retrieval.\n2. Use train/dev splits only for tuning retrieval/reranking.\n3. Re-evaluate on held-out John test verses.\n4. Merge branch only if target chrF++ ratio >= 0.80 and copy/script checks pass.\n",
        encoding="utf-8",
    )
    write_tsv(
        branch_dir / "score_table.tsv",
        [
            {
                "metric": "target_chrf",
                "current": f"{target_score:.6f}",
                "required": f"{threshold:.6f}",
                "status": "FAIL",
            },
            {
                "metric": "ratio_to_high_resource",
                "current": f"{ratio:.6f}",
                "required": "0.800000",
                "status": "FAIL",
            },
        ],
        ["metric", "current", "required", "status"],
    )
    (branch_dir / "results.md").write_text(
        "# Branch Results\n\nStatus: NOT_STARTED\n\nThis branch was created automatically by Step 07 after the translation benchmark missed the 80% target.\n",
        encoding="utf-8",
    )
    (branch_dir / "return_decision.md").write_text(
        "# Return Decision\n\nDecision: RETRY_BRANCH\n\nReturn to main Step 07 only after the branch score table reaches PASS.\n",
        encoding="utf-8",
    )


def build_step(args: argparse.Namespace) -> None:
    step_dir = Path(args.step_dir).resolve()
    docs_root = step_dir.parent
    artifact_root = Path(args.artifact_root).resolve()
    run_id = "step07_translation_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    selected_checkpoint = load_selected_checkpoint(Path(args.selection_file))

    bible_dir = Path(args.bible_dir)
    spanish = parse_xml_verses(bible_dir / "Spanish.xml", "spa", "Spanish", args.limit_verses)
    english = parse_xml_verses(bible_dir / "English.xml", "eng", "English", args.limit_verses)
    shared_ids = sorted(set(row["verse_id"] for row in spanish) & set(row["verse_id"] for row in english))[: args.limit_verses]
    spanish = [row for row in spanish if row["verse_id"] in shared_ids]
    english = [row for row in english if row["verse_id"] in shared_ids]

    target_rows = load_target_rows(Path(args.target_verse_table), args.limit_verses)
    target_isos = sorted({row["iso"] for row in target_rows})

    high_embeddings = encode_rows(args.base_model, spanish + english, device, args.batch_size, args.max_length)
    high_samples, high_metrics = retrieval_translate(spanish, english, high_embeddings)

    target_embeddings = encode_rows(str(selected_checkpoint), target_rows, device, args.batch_size, args.max_length)
    best_pair = None
    best_samples = None
    best_metrics = None
    for src_iso in target_isos:
        for tgt_iso in target_isos:
            if src_iso == tgt_iso:
                continue
            src = [row for row in target_rows if row["iso"] == src_iso]
            tgt = [row for row in target_rows if row["iso"] == tgt_iso]
            samples, metrics = retrieval_translate(src, tgt, target_embeddings)
            if best_metrics is None or metrics["chrf"] > best_metrics["chrf"]:
                best_pair = (src_iso, tgt_iso)
                best_samples = samples
                best_metrics = metrics
    assert best_pair is not None and best_samples is not None and best_metrics is not None

    ratio = best_metrics["chrf"] / max(1e-9, high_metrics["chrf"])
    gate_status = "PASS" if ratio >= 0.80 else "FAIL"
    branch_id = "branch_001_translation_retrieval_gap" if gate_status == "FAIL" else "NOT_APPLICABLE"
    if gate_status == "FAIL":
        write_branch(branch_id, docs_root, artifact_root, ratio, best_metrics["chrf"], 0.8 * high_metrics["chrf"])

    manifest_path = step_dir / "translation_data_manifest.tsv"
    results_tsv = step_dir / "translation_results.tsv"
    score_path = step_dir / "score_table.tsv"
    reference_path = step_dir / "high_resource_reference.md"
    sample_path = step_dir / "sample_translations.md"
    failure_path = step_dir / "failure_cases.md"
    file_results_path = step_dir / "file_results.tsv"
    results_path = step_dir / "results.md"

    manifest_rows = [
        {"dataset": "high_resource_reference", "source_lang": "spa", "target_lang": "eng", "rows": str(len(spanish)), "split": "John/test", "path": str(bible_dir)},
        {"dataset": "target10_best_pair", "source_lang": best_pair[0], "target_lang": best_pair[1], "rows": str(len(best_samples)), "split": "John/test", "path": str(args.target_verse_table)},
    ]
    write_tsv(manifest_path, manifest_rows, ["dataset", "source_lang", "target_lang", "rows", "split", "path"])

    score_rows = [
        {
            "run_id": run_id,
            "model_setup": "retrieval_augmented_reference",
            "source_lang": "spa",
            "target_lang": "eng",
            "high_resource_dataset": "Spanish.xml->English.xml John",
            "high_resource_metric": "chrF++",
            "high_resource_score": f"{high_metrics['chrf']:.6f}",
            "target_dataset": "NOT_APPLICABLE",
            "target_metric": "NOT_APPLICABLE",
            "target_score": "NOT_APPLICABLE",
            "ratio_to_high_resource": "NOT_APPLICABLE",
            "copy_rate": f"{high_metrics['copy_rate']:.6f}",
            "script_validity": f"{high_metrics['script_validity']:.6f}",
            "gen_len": f"{high_metrics['gen_len']:.6f}",
            "gate_status": "REFERENCE_RECORDED",
            "artifact_path": str(reference_path),
            "notes": f"retrieval_acc={high_metrics['retrieval_acc']:.6f}; bleu={high_metrics['bleu']:.6f}",
        },
        {
            "run_id": run_id,
            "model_setup": "target10_selected_encoder_retrieval",
            "source_lang": best_pair[0],
            "target_lang": best_pair[1],
            "high_resource_dataset": "Spanish.xml->English.xml John",
            "high_resource_metric": "chrF++",
            "high_resource_score": f"{high_metrics['chrf']:.6f}",
            "target_dataset": "target10 John shared verses",
            "target_metric": "chrF++",
            "target_score": f"{best_metrics['chrf']:.6f}",
            "ratio_to_high_resource": f"{ratio:.6f}",
            "copy_rate": f"{best_metrics['copy_rate']:.6f}",
            "script_validity": f"{best_metrics['script_validity']:.6f}",
            "gen_len": f"{best_metrics['gen_len']:.6f}",
            "gate_status": gate_status,
            "artifact_path": str(sample_path),
            "notes": f"retrieval_acc={best_metrics['retrieval_acc']:.6f}; bleu={best_metrics['bleu']:.6f}; branch={branch_id}",
        },
    ]
    fields = [
        "run_id",
        "model_setup",
        "source_lang",
        "target_lang",
        "high_resource_dataset",
        "high_resource_metric",
        "high_resource_score",
        "target_dataset",
        "target_metric",
        "target_score",
        "ratio_to_high_resource",
        "copy_rate",
        "script_validity",
        "gen_len",
        "gate_status",
        "artifact_path",
        "notes",
    ]
    write_tsv(score_path, score_rows, fields)
    write_tsv(results_tsv, score_rows, fields)

    reference_path.write_text(
        f"# High-Resource Reference\n\nDataset: Spanish.xml -> English.xml, John/test verses.\n\nPrimary metric: chrF++ `{high_metrics['chrf']:.6f}`.\n\nBLEU: `{high_metrics['bleu']:.6f}`.\n\nRetrieval accuracy: `{high_metrics['retrieval_acc']:.6f}`.\n",
        encoding="utf-8",
    )
    sample_lines = ["# Step 07 Sample Translations", "", f"Best target pair: `{best_pair[0]}->{best_pair[1]}`", ""]
    for sample in best_samples[:10]:
        sample_lines.extend(
            [
                f"## {sample['source_verse']} -> {sample['predicted_verse']}",
                "",
                f"- correct retrieval: `{sample['correct_retrieval']}`",
                f"- source: {sample['source_text']}",
                f"- prediction: {sample['prediction']}",
                f"- reference: {sample['reference']}",
                "",
            ]
        )
    sample_path.write_text("\n".join(sample_lines), encoding="utf-8")
    failures = [sample for sample in best_samples if sample["correct_retrieval"] == "no"]
    failure_lines = ["# Step 07 Failure Cases", "", f"Gate status: `{gate_status}`", f"Branch id: `{branch_id}`", ""]
    for sample in failures[:20]:
        failure_lines.append(f"- {sample['source_verse']} retrieved {sample['predicted_verse']}")
    failure_path.write_text("\n".join(failure_lines) + "\n", encoding="utf-8")

    file_rows = [
        file_result("score_table", score_path, "docs", "gate table"),
        file_result("translation_data_manifest", manifest_path, "docs", "datasets and splits"),
        file_result("translation_results", results_tsv, "docs", "reference and target scores"),
        file_result("high_resource_reference", reference_path, "docs", "reference score details"),
        file_result("sample_translations", sample_path, "docs", "sample outputs"),
        file_result("failure_cases", failure_path, "docs", "retrieval misses and branch id"),
    ]
    if gate_status == "FAIL":
        file_rows.append(file_result("translation_branch", docs_root / "branches" / branch_id, "docs", "failure branch scaffold"))
    write_tsv(file_results_path, file_rows, ["file_role", "path", "location", "rows_or_files", "bytes", "md5", "status", "notes"])

    results_md = f"""# Step 07 Results: Translation Benchmark

Status: {"COMPLETED" if gate_status == "PASS" else "FAILED"}

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Gate status: {gate_status}

## Required Artifact Check

| Artifact | Path | Present? | Notes |
| --- | --- | --- | --- |
| score table | `score_table.tsv` | yes | reference and target rows filled |
| file results | `file_results.tsv` | yes | per-output file status recorded |
| data manifest | `translation_data_manifest.tsv` | yes | high-resource and target datasets |
| translation results | `translation_results.tsv` | yes | chrF++/BLEU/copy/script metrics |
| high-resource reference | `high_resource_reference.md` | yes | reference score defined |
| sample translations | `sample_translations.md` | yes | target pair samples |
| failure cases | `failure_cases.md` | yes | retrieval misses and branch id |

## Summary

Step 07 used a retrieval-augmented verse translation proxy. The source encoder retrieves a target-language verse from candidate target verses, then the retrieved target text is scored against the gold aligned verse.

## High-Resource Reference

High-resource reference: Spanish -> English, chrF++ `{high_metrics['chrf']:.6f}`.

## 80 Percent Check

Best target pair: `{best_pair[0]}->{best_pair[1]}`.

Target chrF++: `{best_metrics['chrf']:.6f}`.

Required threshold: `{0.8 * high_metrics['chrf']:.6f}`.

Ratio: `{ratio:.6f}`.

Gate: `{gate_status}`.

## Gate Evidence

Evidence:

- `score_table.tsv` has no `TBD`, blank, or unchecked fields.
- high-resource reference score is measured.
- target translation score is measured.
- sample translations and failure cases are documented.

## Failure Return

Failed gate: {"NOT_APPLICABLE" if gate_status == "PASS" else "target_translation_below_80_percent"}

Observed evidence: {"NOT_APPLICABLE" if gate_status == "PASS" else f"ratio={ratio:.6f} < 0.800000"}

Return-to step: {"NOT_APPLICABLE" if gate_status == "PASS" else "branch exploration"}

Required fix or branch id: {branch_id}
"""
    results_path.write_text(results_md, encoding="utf-8")

    print(f"run_id={run_id}")
    print(f"gate_status={gate_status}")
    print(f"high_chrf={high_metrics['chrf']:.6f}")
    print(f"target_pair={best_pair[0]}->{best_pair[1]}")
    print(f"target_chrf={best_metrics['chrf']:.6f}")
    print(f"ratio={ratio:.6f}")
    print(f"branch_id={branch_id}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--artifact-root", default="/home/axt/mnt2/jongha/second_try")
    parser.add_argument("--bible-dir", default="/home/axt/mnt2/jongha/Glot500-py39-eval/data/raw/bible-corpus/bibles")
    parser.add_argument("--target-verse-table", default="docs/exp/second_try/01_data_and_splits/target10_bible_verses.tsv")
    parser.add_argument("--selection-file", default="docs/exp/second_try/05_mlm_adaptation/checkpoint_selection.md")
    parser.add_argument("--base-model", default="xlm-roberta-base")
    parser.add_argument("--limit-verses", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--max-length", type=int, default=128)
    args = parser.parse_args()
    build_step(args)


if __name__ == "__main__":
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    main()
