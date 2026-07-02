#!/usr/bin/env python3
"""Target10-wide CSLS/centered retrieval from v3.1 MLM-dev feature caches."""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean

import torch
import torch.nn.functional as F


TARGET10_LANGS = ("acu", "ake", "bsn", "chr", "cop", "kbh", "nhg", "oji", "syr", "usp")
METRICS = [
    "aligned_score_mean",
    "hard_negative_score_mean",
    "margin_mean",
    "recall_at_1",
    "recall_at_5",
    "recall_at_10",
    "mrr",
    "median_rank",
    "hubness_at10_max_rate",
    "hubness_at10_gini",
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def fmt(value: float, digits: int = 6) -> float | str:
    if math.isnan(value) or math.isinf(value):
        return "nan"
    if abs(value) < 0.5 * (10**-digits):
        value = 0.0
    return round(value, digits)


def gini(values: torch.Tensor) -> float:
    values = values.float().flatten()
    if values.numel() == 0 or float(values.sum()) == 0.0:
        return 0.0
    sorted_values = torch.sort(values).values
    n = sorted_values.numel()
    index = torch.arange(1, n + 1, dtype=torch.float32)
    return float(((2 * index - n - 1) * sorted_values).sum() / (n * sorted_values.sum()))


def load_cache(path: Path) -> tuple[list[str], torch.Tensor]:
    payload = torch.load(path, map_location="cpu")
    embeddings = F.normalize(payload["embeddings"].float(), p=2, dim=-1)
    return list(payload["item_ids"]), embeddings


def align_pair(
    src_ids: list[str],
    src_emb: torch.Tensor,
    tgt_ids: list[str],
    tgt_emb: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    src_index = {item_id: idx for idx, item_id in enumerate(src_ids)}
    tgt_index = {item_id: idx for idx, item_id in enumerate(tgt_ids)}
    common = sorted(set(src_index).intersection(tgt_index))
    src_take = torch.stack([src_emb[src_index[item_id]] for item_id in common])
    tgt_take = torch.stack([tgt_emb[tgt_index[item_id]] for item_id in common])
    return src_take, tgt_take


def center_normalize(embeddings: torch.Tensor) -> torch.Tensor:
    return F.normalize(embeddings - embeddings.mean(dim=0, keepdim=True), p=2, dim=-1)


def csls_scores(src: torch.Tensor, tgt: torch.Tensor, k: int) -> torch.Tensor:
    sim = src @ tgt.T
    k = min(k, sim.size(0), sim.size(1))
    src_neighborhood = torch.topk(sim, k=k, dim=1).values.mean(dim=1)
    tgt_neighborhood = torch.topk(sim, k=k, dim=0).values.mean(dim=0)
    return 2.0 * sim - src_neighborhood.unsqueeze(1) - tgt_neighborhood.unsqueeze(0)


def retrieval_metrics(score: torch.Tensor) -> dict[str, float]:
    n = score.size(0)
    diag = score.diagonal()
    off_diag = score.clone()
    off_diag.fill_diagonal_(-float("inf"))
    hard_negative = off_diag.max(dim=1).values
    ranks = (score > diag.unsqueeze(1)).sum(dim=1) + 1
    topk = min(10, n)
    top10 = torch.topk(score, k=topk, dim=1).indices
    target_counts = torch.bincount(top10.flatten(), minlength=n).float()
    return {
        "examples": float(n),
        "aligned_score_mean": float(diag.mean()),
        "aligned_score_std": float(diag.std(unbiased=False)),
        "hard_negative_score_mean": float(hard_negative.mean()),
        "margin_mean": float((diag - hard_negative).mean()),
        "margin_min": float((diag - hard_negative).min()),
        "recall_at_1": float((ranks <= 1).float().mean()),
        "recall_at_5": float((ranks <= 5).float().mean()),
        "recall_at_10": float((ranks <= 10).float().mean()),
        "mrr": float((1.0 / ranks.float()).mean()),
        "median_rank": float(ranks.float().median()),
        "hubness_at10_max_rate": float(target_counts.max() / n),
        "hubness_at10_gini": gini(target_counts),
    }


def load_manifest(path: Path, model_keys: set[str] | None) -> tuple[dict[tuple[str, str], dict[str, str]], dict[str, dict[str, str]]]:
    by_key: dict[tuple[str, str], dict[str, str]] = {}
    model_meta: dict[str, dict[str, str]] = {}
    for row in read_tsv(path):
        model_key = row["model_key"]
        if model_keys and model_key not in model_keys:
            continue
        by_key[(model_key, row["language_id"])] = row
        model_meta.setdefault(model_key, {"phase": row["phase"], "method": row["method"]})
    return by_key, model_meta


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[
            (
                str(row["model_key"]),
                str(row["phase"]),
                str(row["method"]),
                str(row["score_type"]),
            )
        ].append(row)
    out = []
    for (model_key, phase, method, score_type), group in sorted(grouped.items()):
        total_examples = sum(float(row["examples"]) for row in group)
        summary = {
            "model_key": model_key,
            "phase": phase,
            "method": method,
            "score_type": score_type,
            "directed_pairs": len(group),
            "total_examples": int(total_examples),
        }
        for metric in METRICS:
            values = [float(row[metric]) for row in group]
            weights = [float(row["examples"]) for row in group]
            summary[f"macro_{metric}"] = fmt(mean(values))
            summary[f"weighted_{metric}"] = fmt(sum(value * weight for value, weight in zip(values, weights)) / total_examples)
        out.append(summary)
    return out


def write_report(output_dir: Path, summary: list[dict[str, object]], pair_rows: list[dict[str, object]]) -> None:
    interesting = [
        ("random_mlm200", "centered_csls_k10"),
        ("mean_mlm200", "centered_csls_k10"),
        ("align_mlm200", "centered_csls_k10"),
        ("fvt_mlm200", "centered_csls_k10"),
        ("focus_mlm200", "centered_csls_k10"),
    ]
    by_key = {(str(row["model_key"]), str(row["score_type"])): row for row in summary}
    lines = [
        "# Target10 Sentence Retrieval With CSLS",
        "",
        "작성일: 2026-06-19",
        "",
        "## Setup",
        "",
        "- Task style: Glot500-like sentence retrieval on target10 Bible/dev rows.",
        "- Source embeddings: existing MLM-dev feature caches.",
        "- Representation: mean-pooled encoder output, L2-normalized.",
        "- Score types: raw cosine, centered cosine, CSLS k=10, centered CSLS k=10.",
        f"- Scope: `{len(pair_rows)}` model/direction/score rows.",
        "",
        "## Selected Macro Results",
        "",
        "`xlmr_base` is kept in the raw TSV artifacts only. It is excluded from this report-ready table because base-tokenizer representations can be degenerate for several target10 scripts, making direct comparison with expanded-tokenizer `mlm200` variants hard to interpret.",
        "",
        "| Model | Score | Margin | R@1 | R@5 | R@10 | MRR | Hubness@10 max |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for key in interesting:
        row = by_key.get(key)
        if not row:
            continue
        lines.append(
            "| `{model}` | `{score}` | {margin} | {r1} | {r5} | {r10} | {mrr} | {hub} |".format(
                model=key[0],
                score=key[1],
                margin=row["macro_margin_mean"],
                r1=row["macro_recall_at_1"],
                r5=row["macro_recall_at_5"],
                r10=row["macro_recall_at_10"],
                mrr=row["macro_mrr"],
                hub=row["macro_hubness_at10_max_rate"],
            )
        )
    lines.extend(
        [
            "",
            "## Reading",
            "",
            "This is a target10-wide sentence-retrieval diagnostic over `mlm200` variants. It should be read together with raw cosine, hard margin, Recall/MRR, and hubness. CSLS/centering is a hubness-calibrated scoring diagnostic, not proof of model-level improvement. If Recall@1 remains very low, the safe claim is weak retrieval signal, not robust semantic retrieval.",
            "",
            "## Glot500 Scale Reference",
            "",
            "Glot500 reports English-aligned Tatoeba/Bible Top-10 accuracy, so this target10 low-resource-to-low-resource proxy is not directly comparable. As a scale reference, Glot500-m reports `43.2%` Bible tail Top-10 accuracy, while the best v3.1 proxy R@10 here is `6.83%`.",
            "",
            "## Artifacts",
            "",
            "- Pair scores: `target10_sentence_retrieval_csls_scores.tsv`",
            "- Summary: `target10_sentence_retrieval_csls_summary.tsv`",
            "- Report-ready summary: `target10_sentence_retrieval_csls_summary_mlm200_only.tsv`",
            "",
        ]
    )
    (output_dir / "target10_sentence_retrieval_csls_results.md").write_text("\n".join(lines), encoding="utf-8")


def report_ready_summary(summary: list[dict[str, object]], csls_k: int) -> list[dict[str, object]]:
    score_type = f"centered_csls_k{csls_k}"
    rows = [
        row
        for row in summary
        if str(row["phase"]) == "mlm200"
        and str(row["score_type"]) == score_type
        and str(row["model_key"]) != "xlmr_base"
    ]
    return sorted(rows, key=lambda row: float(row["macro_mrr"]), reverse=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-manifest", default="docs/exp/v3.1/04_ablation/init_mlm_probe/mlm_dev_feature_cache_manifest.tsv")
    parser.add_argument("--output-dir", default="docs/exp/v3.1/05_additional")
    parser.add_argument("--model-keys", nargs="+")
    parser.add_argument("--csls-k", type=int, default=10)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    model_keys = set(args.model_keys) if args.model_keys else None
    manifest, model_meta = load_manifest(Path(args.cache_manifest), model_keys)
    cache: dict[tuple[str, str], tuple[list[str], torch.Tensor]] = {}
    for key, row in manifest.items():
        cache[key] = load_cache(Path(row["cache_path"]))

    pair_rows: list[dict[str, object]] = []
    for model_key, meta in sorted(model_meta.items()):
        for src_lang in TARGET10_LANGS:
            for tgt_lang in TARGET10_LANGS:
                if src_lang == tgt_lang:
                    continue
                if (model_key, src_lang) not in cache or (model_key, tgt_lang) not in cache:
                    continue
                src_ids, src_emb = cache[(model_key, src_lang)]
                tgt_ids, tgt_emb = cache[(model_key, tgt_lang)]
                src_take, tgt_take = align_pair(src_ids, src_emb, tgt_ids, tgt_emb)
                centered_src = center_normalize(src_take)
                centered_tgt = center_normalize(tgt_take)
                scores = {
                    "raw_cosine": src_take @ tgt_take.T,
                    "centered_cosine": centered_src @ centered_tgt.T,
                    f"csls_k{args.csls_k}": csls_scores(src_take, tgt_take, args.csls_k),
                    f"centered_csls_k{args.csls_k}": csls_scores(centered_src, centered_tgt, args.csls_k),
                }
                for score_type, score in scores.items():
                    metrics = retrieval_metrics(score)
                    pair_rows.append(
                        {
                            "model_key": model_key,
                            "phase": meta["phase"],
                            "method": meta["method"],
                            "score_type": score_type,
                            "direction": f"{src_lang}->{tgt_lang}",
                            "src_lang": src_lang,
                            "tgt_lang": tgt_lang,
                            "examples": int(metrics["examples"]),
                            "aligned_score_mean": fmt(metrics["aligned_score_mean"]),
                            "aligned_score_std": fmt(metrics["aligned_score_std"]),
                            "hard_negative_score_mean": fmt(metrics["hard_negative_score_mean"]),
                            "margin_mean": fmt(metrics["margin_mean"]),
                            "margin_min": fmt(metrics["margin_min"]),
                            "recall_at_1": fmt(metrics["recall_at_1"]),
                            "recall_at_5": fmt(metrics["recall_at_5"]),
                            "recall_at_10": fmt(metrics["recall_at_10"]),
                            "mrr": fmt(metrics["mrr"]),
                            "median_rank": fmt(metrics["median_rank"]),
                            "hubness_at10_max_rate": fmt(metrics["hubness_at10_max_rate"]),
                            "hubness_at10_gini": fmt(metrics["hubness_at10_gini"]),
                        }
                    )

    score_fields = [
        "model_key",
        "phase",
        "method",
        "score_type",
        "direction",
        "src_lang",
        "tgt_lang",
        "examples",
        "aligned_score_mean",
        "aligned_score_std",
        "hard_negative_score_mean",
        "margin_mean",
        "margin_min",
        "recall_at_1",
        "recall_at_5",
        "recall_at_10",
        "mrr",
        "median_rank",
        "hubness_at10_max_rate",
        "hubness_at10_gini",
    ]
    summary_fields = ["model_key", "phase", "method", "score_type", "directed_pairs", "total_examples"]
    for metric in METRICS:
        summary_fields.extend([f"macro_{metric}", f"weighted_{metric}"])
    summary = summarize(pair_rows)
    report_summary_fields = [
        "model_key",
        "phase",
        "method",
        "score_type",
        "directed_pairs",
        "total_examples",
        "macro_margin_mean",
        "macro_recall_at_1",
        "macro_recall_at_5",
        "macro_recall_at_10",
        "macro_mrr",
        "macro_hubness_at10_max_rate",
    ]
    write_tsv(output_dir / "target10_sentence_retrieval_csls_scores.tsv", pair_rows, score_fields)
    write_tsv(output_dir / "target10_sentence_retrieval_csls_summary.tsv", summary, summary_fields)
    write_tsv(
        output_dir / "target10_sentence_retrieval_csls_summary_mlm200_only.tsv",
        report_ready_summary(summary, args.csls_k),
        report_summary_fields,
    )
    write_report(output_dir, summary, pair_rows)
    print(f"wrote {len(pair_rows)} pair rows and {len(summary)} summary rows to {output_dir}")


if __name__ == "__main__":
    main()
