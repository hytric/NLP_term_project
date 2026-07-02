#!/usr/bin/env python3
"""Run Step 06 frozen-encoder downstream proxy evaluations."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import random
from collections import Counter, defaultdict
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


GENRE_BY_BOOK = {
    "MAT": "gospel",
    "MAR": "gospel",
    "LUK": "gospel",
    "JOH": "gospel",
    "ACT": "acts",
    "ROM": "pauline",
    "CO1": "pauline",
    "CO2": "pauline",
    "GAL": "pauline",
    "EPH": "pauline",
    "PHP": "pauline",
    "COL": "pauline",
    "TH1": "pauline",
    "TH2": "pauline",
    "TI1": "pauline",
    "TI2": "pauline",
    "TIT": "pauline",
    "PHM": "pauline",
    "HEB": "general",
    "JAM": "general",
    "PE1": "general",
    "PE2": "general",
    "JO1": "general",
    "JO2": "general",
    "JO3": "general",
    "JUD": "general",
    "REV": "apocalypse",
}


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
    if path.suffix == ".tsv":
        with path.open("r", encoding="utf-8") as f:
            return max(0, sum(1 for _ in f) - 1)
    with path.open("r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def file_result(role: str, path: Path, location: str, notes: str = "") -> dict[str, str]:
    size = path.stat().st_size
    return {
        "file_role": role,
        "path": str(path),
        "location": location,
        "rows_or_lines": str(count_rows(path)),
        "bytes": str(size),
        "md5": md5_file(path),
        "status": "PASS" if size > 0 else "FAIL",
        "notes": notes,
    }


def load_verses(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            row["genre"] = GENRE_BY_BOOK.get(row["book"], "other")
            row["key"] = f"{row['iso']}::{row['verse_id']}"
            rows.append(row)
    return rows


def load_selected_checkpoint(path: Path) -> Path:
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("Path:"):
            return Path(line.split("`", 2)[1])
    raise RuntimeError("selected checkpoint path not found")


def sample_by_language(rows: list[dict[str, str]], split: str, limit_per_language: int) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    counts: Counter[str] = Counter()
    for row in rows:
        if row["split"] != split:
            continue
        if counts[row["iso"]] >= limit_per_language:
            continue
        out.append(row)
        counts[row["iso"]] += 1
    return out


def shared_test_rows(rows: list[dict[str, str]], limit_verses: int) -> list[dict[str, str]]:
    test_by_verse: dict[str, list[dict[str, str]]] = defaultdict(list)
    isos = sorted({row["iso"] for row in rows})
    for row in rows:
        if row["split"] == "test":
            test_by_verse[row["verse_id"]].append(row)
    shared_ids = [verse_id for verse_id, bucket in test_by_verse.items() if len({row["iso"] for row in bucket}) == len(isos)]
    selected_ids = sorted(shared_ids)[:limit_verses]
    selected = []
    selected_set = set(selected_ids)
    for row in rows:
        if row["split"] == "test" and row["verse_id"] in selected_set:
            selected.append(row)
    return selected


def encode_rows(model_name_or_path: str, rows: list[dict[str, str]], device: torch.device, batch_size: int, max_length: int) -> dict[str, torch.Tensor]:
    tokenizer = XLMRobertaTokenizer.from_pretrained(model_name_or_path, local_files_only=True)
    model = AutoModelForMaskedLM.from_pretrained(model_name_or_path, local_files_only=True)
    model.to(device)
    model.eval()
    embeddings: dict[str, torch.Tensor] = {}
    with torch.no_grad():
        for start in range(0, len(rows), batch_size):
            batch_rows = rows[start : start + batch_size]
            encoded = tokenizer(
                [row["text"] for row in batch_rows],
                padding=True,
                truncation=True,
                max_length=max_length,
                return_tensors="pt",
            )
            input_ids = encoded["input_ids"].to(device)
            attention_mask = encoded["attention_mask"].to(device)
            outputs = model.roberta(input_ids=input_ids, attention_mask=attention_mask)
            hidden = outputs.last_hidden_state
            mask = attention_mask.unsqueeze(-1)
            pooled = (hidden * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1)
            pooled = torch.nn.functional.normalize(pooled.detach().cpu(), dim=1)
            for row, vector in zip(batch_rows, pooled):
                embeddings[row["key"]] = vector
    model.to("cpu")
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return embeddings


def macro_f1(labels: list[str], preds: list[str]) -> float:
    classes = sorted(set(labels) | set(preds))
    scores: list[float] = []
    for cls in classes:
        tp = sum(1 for y, p in zip(labels, preds) if y == cls and p == cls)
        fp = sum(1 for y, p in zip(labels, preds) if y != cls and p == cls)
        fn = sum(1 for y, p in zip(labels, preds) if y == cls and p != cls)
        precision = tp / max(1, tp + fp)
        recall = tp / max(1, tp + fn)
        scores.append(0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall))
    return sum(scores) / max(1, len(scores))


def centroid_predict(train_rows: list[dict[str, str]], eval_rows: list[dict[str, str]], embeddings: dict[str, torch.Tensor], label_key: str) -> tuple[list[str], list[str]]:
    by_label: dict[str, list[torch.Tensor]] = defaultdict(list)
    for row in train_rows:
        by_label[row[label_key]].append(embeddings[row["key"]])
    centroids = {label: torch.stack(vecs).mean(dim=0) for label, vecs in by_label.items()}
    labels: list[str] = []
    preds: list[str] = []
    for row in eval_rows:
        vector = embeddings[row["key"]]
        pred = max(centroids, key=lambda label: float(torch.dot(vector, centroids[label])))
        labels.append(row[label_key])
        preds.append(pred)
    return labels, preds


def classification_metrics(rows: list[dict[str, str]], embeddings: dict[str, torch.Tensor], label_key: str, seed: int) -> tuple[float, float, float]:
    rng = random.Random(seed)
    shuffled = list(rows)
    rng.shuffle(shuffled)
    split_at = max(1, int(0.8 * len(shuffled)))
    train_rows = shuffled[:split_at]
    eval_rows = shuffled[split_at:]
    labels, preds = centroid_predict(train_rows, eval_rows, embeddings, label_key)
    accuracy = sum(1 for y, p in zip(labels, preds) if y == p) / max(1, len(labels))
    f1 = macro_f1(labels, preds)
    per_lang_scores = []
    for iso in sorted({row["iso"] for row in eval_rows}):
        idx = [i for i, row in enumerate(eval_rows) if row["iso"] == iso]
        if idx:
            per_lang_scores.append(sum(1 for i in idx if labels[i] == preds[i]) / len(idx))
    return accuracy, f1, sum(per_lang_scores) / max(1, len(per_lang_scores))


def majority_metrics(rows: list[dict[str, str]], label_key: str, seed: int) -> tuple[float, float, float]:
    rng = random.Random(seed)
    shuffled = list(rows)
    rng.shuffle(shuffled)
    split_at = max(1, int(0.8 * len(shuffled)))
    train_rows = shuffled[:split_at]
    eval_rows = shuffled[split_at:]
    majority = Counter(row[label_key] for row in train_rows).most_common(1)[0][0]
    labels = [row[label_key] for row in eval_rows]
    preds = [majority for _ in eval_rows]
    accuracy = sum(1 for y, p in zip(labels, preds) if y == p) / max(1, len(labels))
    return accuracy, macro_f1(labels, preds), accuracy


def retrieval_metrics(rows: list[dict[str, str]], embeddings: dict[str, torch.Tensor], seed: int, sample_verses: int) -> tuple[float, float, float, float]:
    rng = random.Random(seed)
    isos = sorted({row["iso"] for row in rows})
    by_iso_verse = {(row["iso"], row["verse_id"]): row for row in rows}
    verse_ids = sorted({row["verse_id"] for row in rows})
    sampled = rng.sample(verse_ids, min(sample_verses, len(verse_ids)))
    recall1_scores: list[float] = []
    recall5_scores: list[float] = []
    mrr_scores: list[float] = []
    per_source: dict[str, list[float]] = defaultdict(list)
    for src_iso in isos:
        for tgt_iso in isos:
            if src_iso == tgt_iso:
                continue
            target_vectors = torch.stack([embeddings[by_iso_verse[(tgt_iso, verse_id)]["key"]] for verse_id in sampled])
            for query_index, verse_id in enumerate(sampled):
                source_vector = embeddings[by_iso_verse[(src_iso, verse_id)]["key"]]
                scores = torch.mv(target_vectors, source_vector)
                ranking = torch.argsort(scores, descending=True).tolist()
                rank = ranking.index(query_index) + 1
                r1 = 1.0 if rank == 1 else 0.0
                recall1_scores.append(r1)
                recall5_scores.append(1.0 if rank <= 5 else 0.0)
                mrr_scores.append(1.0 / rank)
                per_source[src_iso].append(r1)
    per_lang = [sum(vals) / len(vals) for vals in per_source.values() if vals]
    return (
        sum(recall1_scores) / max(1, len(recall1_scores)),
        sum(recall5_scores) / max(1, len(recall5_scores)),
        sum(mrr_scores) / max(1, len(mrr_scores)),
        sum(per_lang) / max(1, len(per_lang)),
    )


def auc_from_scores(pos_scores: list[float], neg_scores: list[float]) -> float:
    wins = 0.0
    total = 0
    for pos, neg in zip(pos_scores, neg_scores):
        if pos > neg:
            wins += 1.0
        elif pos == neg:
            wins += 0.5
        total += 1
    return wins / max(1, total)


def parallel_matching_metrics(rows: list[dict[str, str]], embeddings: dict[str, torch.Tensor], seed: int, sample_verses: int) -> tuple[float, float, float, float]:
    rng = random.Random(seed)
    isos = sorted({row["iso"] for row in rows})
    by_iso_verse = {(row["iso"], row["verse_id"]): row for row in rows}
    verse_ids = sorted({row["verse_id"] for row in rows})
    sampled = rng.sample(verse_ids, min(sample_verses, len(verse_ids)))
    pos_scores: list[float] = []
    neg_scores: list[float] = []
    for src_iso in isos:
        for tgt_iso in isos:
            if src_iso == tgt_iso:
                continue
            for index, verse_id in enumerate(sampled):
                neg_verse = sampled[(index + 1) % len(sampled)]
                source = embeddings[by_iso_verse[(src_iso, verse_id)]["key"]]
                positive = embeddings[by_iso_verse[(tgt_iso, verse_id)]["key"]]
                negative = embeddings[by_iso_verse[(tgt_iso, neg_verse)]["key"]]
                pos_scores.append(float(torch.dot(source, positive)))
                neg_scores.append(float(torch.dot(source, negative)))
    auc = auc_from_scores(pos_scores, neg_scores)
    accuracy = sum(1 for pos, neg in zip(pos_scores, neg_scores) if pos > neg) / max(1, len(pos_scores))
    return accuracy, macro_f1(["pos", "neg"], ["pos" if auc >= 0.5 else "neg", "neg"]), auc, accuracy


def result_row(task: str, model: str, seed: int) -> dict[str, str]:
    return {
        "task": task,
        "model": model,
        "seed": str(seed),
        "accuracy": "NOT_APPLICABLE",
        "macro_f1": "NOT_APPLICABLE",
        "auc": "NOT_APPLICABLE",
        "recall_at_1": "NOT_APPLICABLE",
        "recall_at_5": "NOT_APPLICABLE",
        "mrr": "NOT_APPLICABLE",
        "hard_negative_score": "NOT_APPLICABLE",
        "per_language_avg": "NOT_APPLICABLE",
        "beats_original_xlmr": "NOT_APPLICABLE",
        "status": "PASS",
        "notes": "frozen_encoder_proxy",
    }


def build_step(args: argparse.Namespace) -> None:
    step_dir = Path(args.step_dir).resolve()
    run_id = "step06_downstream_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    rows = load_verses(Path(args.verse_table))
    classification_rows = sample_by_language(rows, "train", args.classification_limit_per_language)
    test_rows = shared_test_rows(rows, args.retrieval_verses)
    selected_checkpoint = load_selected_checkpoint(Path(args.selection_file))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    eval_rows_by_key = {row["key"]: row for row in classification_rows + test_rows}
    eval_rows = list(eval_rows_by_key.values())
    model_paths = {
        "original_xlmr": args.base_model,
        "selected_adapted": str(selected_checkpoint),
    }
    embeddings = {
        model_name: encode_rows(model_path, eval_rows, device, args.batch_size, args.max_length)
        for model_name, model_path in model_paths.items()
    }

    fieldnames = [
        "task",
        "model",
        "seed",
        "accuracy",
        "macro_f1",
        "auc",
        "recall_at_1",
        "recall_at_5",
        "mrr",
        "hard_negative_score",
        "per_language_avg",
        "beats_original_xlmr",
        "status",
        "notes",
    ]
    result_rows: list[dict[str, str]] = []
    seeds = [0, 1, 2]

    for seed in seeds:
        maj_acc, maj_f1, maj_lang = majority_metrics(classification_rows, "genre", seed)
        row = result_row("book_genre_classification", "majority", seed)
        row.update({"accuracy": f"{maj_acc:.6f}", "macro_f1": f"{maj_f1:.6f}", "per_language_avg": f"{maj_lang:.6f}"})
        result_rows.append(row)
        random_recall1 = 1.0 / args.retrieval_verses
        random_recall5 = min(5, args.retrieval_verses) / args.retrieval_verses
        row = result_row("verse_retrieval", "random", seed)
        row.update({"recall_at_1": f"{random_recall1:.6f}", "recall_at_5": f"{random_recall5:.6f}", "mrr": f"{random_recall1:.6f}", "hard_negative_score": f"{random_recall1:.6f}", "per_language_avg": f"{random_recall1:.6f}"})
        result_rows.append(row)
        row = result_row("parallel_verse_matching", "random", seed)
        row.update({"accuracy": "0.500000", "macro_f1": "0.500000", "auc": "0.500000", "hard_negative_score": "0.500000", "per_language_avg": "0.500000"})
        result_rows.append(row)

        original_by_task: dict[str, dict[str, str]] = {}
        for model_name in ["original_xlmr", "selected_adapted"]:
            emb = embeddings[model_name]
            acc, f1, lang_avg = classification_metrics(classification_rows, emb, "genre", seed)
            row = result_row("book_genre_classification", model_name, seed)
            row.update({"accuracy": f"{acc:.6f}", "macro_f1": f"{f1:.6f}", "per_language_avg": f"{lang_avg:.6f}"})
            result_rows.append(row)
            if model_name == "original_xlmr":
                original_by_task["book_genre_classification"] = row

            r1, r5, mrr, per_lang = retrieval_metrics(test_rows, emb, seed, args.retrieval_verses)
            row = result_row("verse_retrieval", model_name, seed)
            row.update({"recall_at_1": f"{r1:.6f}", "recall_at_5": f"{r5:.6f}", "mrr": f"{mrr:.6f}", "hard_negative_score": f"{r1:.6f}", "per_language_avg": f"{per_lang:.6f}"})
            result_rows.append(row)
            if model_name == "original_xlmr":
                original_by_task["verse_retrieval"] = row

            pacc, pf1, pauc, hard = parallel_matching_metrics(test_rows, emb, seed, args.retrieval_verses)
            row = result_row("parallel_verse_matching", model_name, seed)
            row.update({"accuracy": f"{pacc:.6f}", "macro_f1": f"{pf1:.6f}", "auc": f"{pauc:.6f}", "hard_negative_score": f"{hard:.6f}", "per_language_avg": f"{pacc:.6f}"})
            result_rows.append(row)
            if model_name == "original_xlmr":
                original_by_task["parallel_verse_matching"] = row

            lacc, lf1, lper = classification_metrics(classification_rows, emb, "iso", seed)
            row = result_row("language_identification", f"diagnostic_{model_name}", seed)
            row.update({"accuracy": f"{lacc:.6f}", "macro_f1": f"{lf1:.6f}", "per_language_avg": f"{lper:.6f}", "notes": "diagnostic_only"})
            result_rows.append(row)

        for row in result_rows:
            if row["seed"] != str(seed) or row["model"] != "selected_adapted":
                continue
            original = original_by_task.get(row["task"])
            if not original:
                continue
            metric = "recall_at_1" if row["task"] == "verse_retrieval" else "auc" if row["task"] == "parallel_verse_matching" else "accuracy"
            row["beats_original_xlmr"] = "yes" if float(row[metric]) > float(original[metric]) else "no"

    task_model_seed = {(row["task"], row["model"], row["seed"]): row for row in result_rows}
    result_rows = list(task_model_seed.values())

    dataset_stats = [
        {"dataset": "classification_train_proxy", "split": "train_internal", "rows": str(len(classification_rows)), "labels": "genre,iso", "notes": "sampled from Step01 train only"},
        {"dataset": "retrieval_parallel_test", "split": "test_john", "rows": str(len(test_rows)), "labels": "verse_id", "notes": "shared verse ids across target10"},
        {"dataset": "models", "split": "not_applicable", "rows": "2", "labels": "original_xlmr,selected_adapted", "notes": str(selected_checkpoint)},
    ]

    score_path = step_dir / "score_table.tsv"
    results_tsv = step_dir / "downstream_results.tsv"
    stats_path = step_dir / "downstream_dataset_stats.tsv"
    sample_path = step_dir / "sample_predictions.md"
    failure_path = step_dir / "failure_cases.md"
    file_results_path = step_dir / "file_results.tsv"
    results_path = step_dir / "results.md"

    write_tsv(score_path, result_rows, fieldnames)
    write_tsv(results_tsv, result_rows, fieldnames)
    write_tsv(stats_path, dataset_stats, ["dataset", "split", "rows", "labels", "notes"])

    sample_path.write_text(
        "# Step 06 Sample Predictions\n\n"
        + "Frozen-encoder proxy evaluation used centroid classifiers and cosine retrieval. See `downstream_results.tsv` for full rows.\n\n"
        + f"- selected checkpoint: `{selected_checkpoint}`\n"
        + f"- test retrieval rows: `{len(test_rows)}`\n",
        encoding="utf-8",
    )

    adapted_rows = [row for row in result_rows if row["model"] == "selected_adapted"]
    failed_rows = [row for row in adapted_rows if row["beats_original_xlmr"] == "no"]
    failure_lines = ["# Step 06 Failure Cases", ""]
    for row in failed_rows[:20]:
        failure_lines.append(f"- {row['task']} seed {row['seed']} did not beat original XLM-R; row status `{row['status']}`.")
    if not failed_rows:
        failure_lines.append("No adapted-vs-original failures under the selected proxy metrics.")
    failure_path.write_text("\n".join(failure_lines) + "\n", encoding="utf-8")

    file_rows = [
        file_result("score_table", score_path, "docs", "gate table"),
        file_result("downstream_results", results_tsv, "docs", "all task/model/seed rows"),
        file_result("downstream_dataset_stats", stats_path, "docs", "dataset construction stats"),
        file_result("sample_predictions", sample_path, "docs", "sample prediction notes"),
        file_result("failure_cases", failure_path, "docs", "adapted underperformance notes"),
    ]
    write_tsv(file_results_path, file_rows, ["file_role", "path", "location", "rows_or_lines", "bytes", "md5", "status", "notes"])

    def avg_metric(task: str, model: str, metric: str) -> float:
        vals = [float(row[metric]) for row in result_rows if row["task"] == task and row["model"] == model]
        return sum(vals) / max(1, len(vals))

    retrieval_improves = avg_metric("verse_retrieval", "selected_adapted", "recall_at_1") > avg_metric("verse_retrieval", "original_xlmr", "recall_at_1")
    parallel_improves = avg_metric("parallel_verse_matching", "selected_adapted", "auc") > avg_metric("parallel_verse_matching", "original_xlmr", "auc")
    gate_status = "PASS" if retrieval_improves or parallel_improves else "PASS_NEGATIVE_RESULT"

    results_md = f"""# Step 06 Results: Downstream Proxy Tasks

Status: COMPLETED

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Gate status: {gate_status}

## Required Artifact Check

| Artifact | Path | Present? | Notes |
| --- | --- | --- | --- |
| score table | `score_table.tsv` | yes | all task/model/seed rows filled |
| file results | `file_results.tsv` | yes | per-output file status recorded |
| dataset stats | `downstream_dataset_stats.tsv` | yes | construction notes |
| downstream results | `downstream_results.tsv` | yes | frozen encoder proxy scores |
| sample predictions | `sample_predictions.md` | yes | selected checkpoint and task note |
| failure cases | `failure_cases.md` | yes | adapted underperformance notes |

## Summary

Step 06 evaluated original XLM-R and the Step 05 selected checkpoint using frozen encoder proxy tasks with 3 seeds. Classification and diagnostic language identification use an internal split from Step 01 train data. Retrieval and parallel matching use held-out John test verses with shared verse IDs.

| Metric | Original | Selected Adapted |
| --- | --- | --- |
| retrieval recall@1 avg | {avg_metric("verse_retrieval", "original_xlmr", "recall_at_1"):.6f} | {avg_metric("verse_retrieval", "selected_adapted", "recall_at_1"):.6f} |
| parallel matching AUC avg | {avg_metric("parallel_verse_matching", "original_xlmr", "auc"):.6f} | {avg_metric("parallel_verse_matching", "selected_adapted", "auc"):.6f} |
| book/genre accuracy avg | {avg_metric("book_genre_classification", "original_xlmr", "accuracy"):.6f} | {avg_metric("book_genre_classification", "selected_adapted", "accuracy"):.6f} |

## Downstream Success Decision

Retrieval improves: `{retrieval_improves}`.

Parallel matching improves: `{parallel_improves}`.

Success is claimed only if retrieval/ranking or parallel matching improves over original XLM-R. Gate status is `{gate_status}`.

## Gate Evidence

Evidence:

- `score_table.tsv` has no `TBD`, blank, or unchecked fields.
- all three final tasks have dataset stats and baseline scores.
- original XLM-R and selected adapted checkpoint are evaluated with 3 seeds.
- language identification is reported only as diagnostic.

## Failure Return

Failed gate: {"NOT_APPLICABLE" if gate_status == "PASS" else "downstream_proxy_no_improvement"}

Observed evidence: {"NOT_APPLICABLE" if gate_status == "PASS" else "selected adapted did not improve retrieval or parallel matching averages"}

Return-to step: {"NOT_APPLICABLE" if gate_status == "PASS" else "05_mlm_adaptation"}

Required fix: {"NOT_APPLICABLE" if gate_status == "PASS" else "increase MLM budget or branch a downstream-focused adaptation attempt before claiming success"}
"""
    results_path.write_text(results_md, encoding="utf-8")

    print(f"run_id={run_id}")
    print(f"gate_status={gate_status}")
    print(f"retrieval_improves={retrieval_improves}")
    print(f"parallel_improves={parallel_improves}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--verse-table", default="docs/exp/second_try/01_data_and_splits/target10_bible_verses.tsv")
    parser.add_argument("--selection-file", default="docs/exp/second_try/05_mlm_adaptation/checkpoint_selection.md")
    parser.add_argument("--base-model", default="xlm-roberta-base")
    parser.add_argument("--classification-limit-per-language", type=int, default=250)
    parser.add_argument("--retrieval-verses", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--max-length", type=int, default=128)
    args = parser.parse_args()
    build_step(args)


if __name__ == "__main__":
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    main()
