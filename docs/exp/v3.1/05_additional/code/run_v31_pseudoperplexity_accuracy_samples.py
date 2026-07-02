#!/usr/bin/env python3
"""Top-k accuracy and prediction samples for v3.1 pseudoPPL interpretation."""

from __future__ import annotations

import argparse
import csv
import json
import math
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import torch
import torch.nn.functional as F

try:
    import huggingface_hub

    if not hasattr(huggingface_hub, "split_torch_state_dict_into_shards"):

        def _missing_split_torch_state_dict_into_shards(*_args, **_kwargs):
            raise RuntimeError("split_torch_state_dict_into_shards is unavailable")

        huggingface_hub.split_torch_state_dict_into_shards = _missing_split_torch_state_dict_into_shards
except Exception:
    pass

from transformers import AutoModelForMaskedLM, AutoTokenizer


TARGET10_LANGS = ("acu", "ake", "bsn", "chr", "cop", "kbh", "nhg", "oji", "syr", "usp")
MLM200_ROOT = Path("/home/axt/mnt2/jongha/v3_1/init_mlm_probe_200step")


@dataclass(frozen=True)
class ModelSpec:
    model_key: str
    model_path: str


def default_models() -> list[ModelSpec]:
    return [
        ModelSpec("align_mlm200", str(MLM200_ROOT / "align_seed13_step200")),
        ModelSpec("fvt_mlm200", str(MLM200_ROOT / "fvt_seed13_step200")),
        ModelSpec("focus_mlm200", str(MLM200_ROOT / "focus_seed13_step200")),
        ModelSpec("random_mlm200", str(MLM200_ROOT / "random_seed13_step200")),
        ModelSpec("mean_mlm200", str(MLM200_ROOT / "mean_seed13_step200")),
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


def fmt(value: float, digits: int = 6) -> float:
    if math.isnan(value) or math.isinf(value):
        return value
    return round(value, digits)


def is_content_token(token: str) -> bool:
    surface = token.replace("▁", "")
    return any(unicodedata.category(char)[0] in {"L", "N"} for char in surface)


def load_rows(manifest: Path, max_examples_per_lang: int) -> dict[str, list[dict[str, str]]]:
    by_lang = {lang: [] for lang in TARGET10_LANGS}
    seen = {lang: set() for lang in TARGET10_LANGS}
    for row in read_tsv(manifest):
        lang = row.get("language_id", "")
        if row.get("split") == "dev" and lang in by_lang and row["item_id"] not in seen[lang]:
            seen[lang].add(row["item_id"])
            by_lang[lang].append(row)
    for lang in TARGET10_LANGS:
        by_lang[lang].sort(key=lambda row: row["item_id"])
        by_lang[lang] = by_lang[lang][:max_examples_per_lang]
    return by_lang


@torch.no_grad()
def evaluate_model(
    spec: ModelSpec,
    rows_by_lang: dict[str, list[dict[str, str]]],
    device: torch.device,
    max_length: int,
    mask_batch_size: int,
    sample_limit: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    tokenizer = AutoTokenizer.from_pretrained(spec.model_path)
    model = AutoModelForMaskedLM.from_pretrained(spec.model_path).to(device)
    model.eval()

    summary_rows: list[dict[str, object]] = []
    sample_rows: list[dict[str, object]] = []

    for lang, rows in rows_by_lang.items():
        total = 0
        nll_sum = 0.0
        top1 = 0
        top5 = 0
        top10 = 0
        content_total = 0
        content_nll_sum = 0.0
        content_top1 = 0
        content_top5 = 0
        content_top10 = 0
        sampled = 0
        for row in rows:
            encoded = tokenizer(row["text"], truncation=True, max_length=max_length, return_tensors="pt")
            input_ids = encoded["input_ids"][0]
            attention = encoded["attention_mask"][0]
            special = tokenizer.get_special_tokens_mask(input_ids.tolist(), already_has_special_tokens=True)
            positions = [idx for idx, is_special in enumerate(special) if not is_special and int(attention[idx]) == 1]
            for start in range(0, len(positions), mask_batch_size):
                batch_positions = positions[start : start + mask_batch_size]
                batch_input = input_ids.unsqueeze(0).repeat(len(batch_positions), 1)
                batch_attention = attention.unsqueeze(0).repeat(len(batch_positions), 1)
                labels = []
                for row_idx, pos in enumerate(batch_positions):
                    labels.append(int(batch_input[row_idx, pos]))
                    batch_input[row_idx, pos] = tokenizer.mask_token_id
                batch_input = batch_input.to(device)
                batch_attention = batch_attention.to(device)
                labels_t = torch.tensor(labels, dtype=torch.long, device=device)
                logits = model(input_ids=batch_input, attention_mask=batch_attention).logits
                pos_t = torch.tensor(batch_positions, dtype=torch.long, device=device)
                selected = logits[torch.arange(len(batch_positions), device=device), pos_t]
                log_probs = F.log_softmax(selected, dim=-1)
                nll = -log_probs[torch.arange(len(batch_positions), device=device), labels_t]
                top = torch.topk(selected, k=10, dim=-1).indices
                top1_hits = top[:, 0] == labels_t
                top5_hits = (top[:, :5] == labels_t.unsqueeze(1)).any(dim=1)
                top10_hits = (top == labels_t.unsqueeze(1)).any(dim=1)
                top1 += int(top1_hits.sum().item())
                top5 += int(top5_hits.sum().item())
                top10 += int(top10_hits.sum().item())
                total += len(batch_positions)
                nll_sum += float(nll.sum().detach().cpu())

                gold_ids = [int(label) for label in labels]
                gold_tokens = tokenizer.convert_ids_to_tokens(gold_ids)
                content_indices = [idx for idx, token in enumerate(gold_tokens) if is_content_token(token)]
                if content_indices:
                    content_idx_t = torch.tensor(content_indices, dtype=torch.long, device=device)
                    content_total += len(content_indices)
                    content_nll_sum += float(nll[content_idx_t].sum().detach().cpu())
                    content_top1 += int(top1_hits[content_idx_t].sum().item())
                    content_top5 += int(top5_hits[content_idx_t].sum().item())
                    content_top10 += int(top10_hits[content_idx_t].sum().item())

                if sampled < sample_limit:
                    probs = torch.exp(log_probs[torch.arange(len(batch_positions), device=device), labels_t])
                    for local_idx, pos in enumerate(batch_positions):
                        if sampled >= sample_limit:
                            break
                        gold_id = int(labels_t[local_idx].detach().cpu())
                        gold_token = gold_tokens[local_idx]
                        if not is_content_token(gold_token):
                            continue
                        top_ids = [int(item) for item in top[local_idx, :5].detach().cpu().tolist()]
                        sample_rows.append(
                            {
                                "model_key": spec.model_key,
                                "language_id": lang,
                                "item_id": row["item_id"],
                                "position": pos,
                                "gold_token": gold_token,
                                "gold_prob": fmt(float(probs[local_idx].detach().cpu())),
                                "top1_token": tokenizer.convert_ids_to_tokens([top_ids[0]])[0],
                                "top5_tokens": " ".join(tokenizer.convert_ids_to_tokens(top_ids)),
                                "top1_correct": int(top_ids[0] == gold_id),
                                "top5_correct": int(gold_id in top_ids),
                            }
                        )
                        sampled += 1
        mean_nll = nll_sum / total if total else float("nan")
        content_mean_nll = content_nll_sum / content_total if content_total else float("nan")
        summary_rows.append(
            {
                "model_key": spec.model_key,
                "language_id": lang,
                "examples": len(rows),
                "masked_tokens": total,
                "mean_nll": fmt(mean_nll),
                "pseudo_perplexity": fmt(math.exp(mean_nll) if mean_nll < 50 else float("inf")),
                "avg_gold_probability": fmt(math.exp(-mean_nll) if mean_nll < 50 else 0.0),
                "top1_accuracy": fmt(top1 / total if total else float("nan")),
                "top5_accuracy": fmt(top5 / total if total else float("nan")),
                "top10_accuracy": fmt(top10 / total if total else float("nan")),
                "content_masked_tokens": content_total,
                "content_mean_nll": fmt(content_mean_nll),
                "content_pseudo_perplexity": fmt(math.exp(content_mean_nll) if content_mean_nll < 50 else float("inf")),
                "content_avg_gold_probability": fmt(math.exp(-content_mean_nll) if content_mean_nll < 50 else 0.0),
                "content_top1_accuracy": fmt(content_top1 / content_total if content_total else float("nan")),
                "content_top5_accuracy": fmt(content_top5 / content_total if content_total else float("nan")),
                "content_top10_accuracy": fmt(content_top10 / content_total if content_total else float("nan")),
            }
        )

    del model
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return summary_rows, sample_rows


def macro_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    by_model: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        by_model.setdefault(str(row["model_key"]), []).append(row)
    out = []
    for model_key, group in sorted(by_model.items()):
        total_tokens = sum(int(row["masked_tokens"]) for row in group)
        weighted_nll = sum(float(row["mean_nll"]) * int(row["masked_tokens"]) for row in group) / total_tokens
        total_content_tokens = sum(int(row["content_masked_tokens"]) for row in group)
        weighted_content_nll = (
            sum(float(row["content_mean_nll"]) * int(row["content_masked_tokens"]) for row in group) / total_content_tokens
            if total_content_tokens
            else float("nan")
        )
        out.append(
            {
                "model_key": model_key,
                "languages": len(group),
                "total_examples": sum(int(row["examples"]) for row in group),
                "total_masked_tokens": total_tokens,
                "weighted_mean_nll": fmt(weighted_nll),
                "weighted_pseudo_perplexity": fmt(math.exp(weighted_nll)),
                "weighted_avg_gold_probability": fmt(math.exp(-weighted_nll)),
                "macro_top1_accuracy": fmt(sum(float(row["top1_accuracy"]) for row in group) / len(group)),
                "macro_top5_accuracy": fmt(sum(float(row["top5_accuracy"]) for row in group) / len(group)),
                "macro_top10_accuracy": fmt(sum(float(row["top10_accuracy"]) for row in group) / len(group)),
                "total_content_tokens": total_content_tokens,
                "weighted_content_mean_nll": fmt(weighted_content_nll),
                "weighted_content_pseudo_perplexity": fmt(math.exp(weighted_content_nll) if weighted_content_nll < 50 else float("inf")),
                "weighted_content_avg_gold_probability": fmt(math.exp(-weighted_content_nll) if weighted_content_nll < 50 else 0.0),
                "macro_content_top1_accuracy": fmt(sum(float(row["content_top1_accuracy"]) for row in group) / len(group)),
                "macro_content_top5_accuracy": fmt(sum(float(row["content_top5_accuracy"]) for row in group) / len(group)),
                "macro_content_top10_accuracy": fmt(sum(float(row["content_top10_accuracy"]) for row in group) / len(group)),
            }
        )
    return sorted(out, key=lambda row: float(row["weighted_content_mean_nll"]))


def gold_probability_scores(summary_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    ranked = sorted(summary_rows, key=lambda row: float(row["weighted_avg_gold_probability"]), reverse=True)
    for rank, row in enumerate(ranked, start=1):
        all_token_prob = float(row["weighted_avg_gold_probability"])
        content_token_prob = float(row["weighted_content_avg_gold_probability"])
        rows.append(
            {
                "rank": rank,
                "model_key": row["model_key"],
                "weighted_mean_nll": row["weighted_mean_nll"],
                "weighted_pseudo_perplexity": row["weighted_pseudo_perplexity"],
                "all_token_avg_gold_probability_score": fmt(all_token_prob),
                "all_token_avg_gold_probability_percent": fmt(all_token_prob * 100.0, 4),
                "content_token_avg_gold_probability_score": fmt(content_token_prob),
                "content_token_avg_gold_probability_percent": fmt(content_token_prob * 100.0, 4),
                "content_token_top1_accuracy": row["macro_content_top1_accuracy"],
                "content_token_top5_accuracy": row["macro_content_top5_accuracy"],
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="docs/exp/v3.1/01_embedding_alignment/parallel_item_manifest.tsv")
    parser.add_argument("--output-dir", default="docs/exp/v3.1/05_additional")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--max-examples-per-lang", type=int, default=20)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--mask-batch-size", type=int, default=64)
    parser.add_argument("--sample-limit-per-lang", type=int, default=5)
    parser.add_argument("--model-keys", nargs="+")
    args = parser.parse_args()

    specs = default_models()
    if args.model_keys:
        requested = set(args.model_keys)
        specs = [spec for spec in specs if spec.model_key in requested]
    rows_by_lang = load_rows(Path(args.manifest), args.max_examples_per_lang)
    device = torch.device(args.device)
    score_rows: list[dict[str, object]] = []
    sample_rows: list[dict[str, object]] = []
    for spec in specs:
        print(json.dumps({"event": "load_model", "model_key": spec.model_key}), flush=True)
        scores, samples = evaluate_model(
            spec,
            rows_by_lang,
            device,
            max_length=args.max_length,
            mask_batch_size=args.mask_batch_size,
            sample_limit=args.sample_limit_per_lang,
        )
        score_rows.extend(scores)
        sample_rows.extend(samples)
    out = Path(args.output_dir)
    model_summary_rows = macro_summary(score_rows)
    write_tsv(
        out / "pseudoperplexity_accuracy_scores.tsv",
        score_rows,
        [
            "model_key",
            "language_id",
            "examples",
            "masked_tokens",
            "mean_nll",
            "pseudo_perplexity",
            "avg_gold_probability",
            "top1_accuracy",
            "top5_accuracy",
            "top10_accuracy",
            "content_masked_tokens",
            "content_mean_nll",
            "content_pseudo_perplexity",
            "content_avg_gold_probability",
            "content_top1_accuracy",
            "content_top5_accuracy",
            "content_top10_accuracy",
        ],
    )
    write_tsv(
        out / "pseudoperplexity_accuracy_summary.tsv",
        model_summary_rows,
        [
            "model_key",
            "languages",
            "total_examples",
            "total_masked_tokens",
            "weighted_mean_nll",
            "weighted_pseudo_perplexity",
            "weighted_avg_gold_probability",
            "macro_top1_accuracy",
            "macro_top5_accuracy",
            "macro_top10_accuracy",
            "total_content_tokens",
            "weighted_content_mean_nll",
            "weighted_content_pseudo_perplexity",
            "weighted_content_avg_gold_probability",
            "macro_content_top1_accuracy",
            "macro_content_top5_accuracy",
            "macro_content_top10_accuracy",
        ],
    )
    write_tsv(
        out / "pseudoperplexity_gold_probability_scores.tsv",
        gold_probability_scores(model_summary_rows),
        [
            "rank",
            "model_key",
            "weighted_mean_nll",
            "weighted_pseudo_perplexity",
            "all_token_avg_gold_probability_score",
            "all_token_avg_gold_probability_percent",
            "content_token_avg_gold_probability_score",
            "content_token_avg_gold_probability_percent",
            "content_token_top1_accuracy",
            "content_token_top5_accuracy",
        ],
    )
    write_tsv(
        out / "pseudoperplexity_prediction_samples.tsv",
        sample_rows,
        [
            "model_key",
            "language_id",
            "item_id",
            "position",
            "gold_token",
            "gold_prob",
            "top1_token",
            "top5_tokens",
            "top1_correct",
            "top5_correct",
        ],
    )
    print(json.dumps({"event": "done", "models": [spec.model_key for spec in specs], "rows": len(score_rows)}), flush=True)


if __name__ == "__main__":
    main()
