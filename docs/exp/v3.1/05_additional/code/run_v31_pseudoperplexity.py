#!/usr/bin/env python3
"""Sampled pseudo-perplexity evaluation for v3.1 target10 dev text."""

from __future__ import annotations

import argparse
import csv
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

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
INIT_ROOT = Path("/home/axt/mnt2/jongha/third_try/checkpoints/04_init")
MLM200_ROOT = Path("/home/axt/mnt2/jongha/v3_1/init_mlm_probe_200step")


@dataclass(frozen=True)
class ModelSpec:
    model_key: str
    phase: str
    method: str
    model_path: str
    tokenizer_path: str


def default_models(include_zero: bool) -> list[ModelSpec]:
    specs = [ModelSpec("xlmr_base", "baseline", "xlmr_base", "xlm-roberta-base", "xlm-roberta-base")]
    if include_zero:
        for method in ("random", "mean", "fvt", "align", "focus"):
            init_path = INIT_ROOT / f"xlmr_v2_48000_{method}"
            specs.append(ModelSpec(f"{method}_zero", "zero_step_init", method, str(init_path), str(init_path)))
    for method in ("random", "mean", "fvt", "align", "focus"):
        mlm_path = MLM200_ROOT / f"{method}_seed13_step200"
        specs.append(ModelSpec(f"{method}_mlm200", "mlm200", method, str(mlm_path), str(mlm_path)))
    return specs


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
    return round(value, digits)


def exp_safe(value: float) -> float:
    if value > 50:
        return float("inf")
    return math.exp(value)


def load_dev_rows(manifest_path: Path, max_examples_per_lang: int) -> dict[str, list[dict[str, str]]]:
    by_lang = {lang: [] for lang in TARGET10_LANGS}
    seen = {lang: set() for lang in TARGET10_LANGS}
    for row in read_tsv(manifest_path):
        lang = row.get("language_id", "")
        if row.get("split") != "dev" or lang not in by_lang:
            continue
        item_id = row["item_id"]
        if item_id in seen[lang]:
            continue
        seen[lang].add(item_id)
        by_lang[lang].append({"item_id": item_id, "language_id": lang, "text": row["text"]})
    for lang, rows in by_lang.items():
        rows.sort(key=lambda item: item["item_id"])
        if max_examples_per_lang > 0:
            by_lang[lang] = rows[:max_examples_per_lang]
    return by_lang


@torch.no_grad()
def sentence_nll(
    text: str,
    tokenizer,
    model,
    device: torch.device,
    max_length: int,
    mask_batch_size: int,
) -> tuple[float, int]:
    encoded = tokenizer(
        text,
        truncation=True,
        max_length=max_length,
        return_tensors="pt",
    )
    input_ids = encoded["input_ids"][0]
    attention_mask = encoded["attention_mask"][0]
    special_mask = tokenizer.get_special_tokens_mask(input_ids.tolist(), already_has_special_tokens=True)
    positions = [idx for idx, is_special in enumerate(special_mask) if not is_special and int(attention_mask[idx]) == 1]
    if not positions:
        return 0.0, 0

    total_nll = 0.0
    total_tokens = 0
    for start in range(0, len(positions), mask_batch_size):
        batch_positions = positions[start : start + mask_batch_size]
        batch_input = input_ids.unsqueeze(0).repeat(len(batch_positions), 1)
        batch_attention = attention_mask.unsqueeze(0).repeat(len(batch_positions), 1)
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
        nll = -F.log_softmax(selected, dim=-1)[torch.arange(len(batch_positions), device=device), labels_t]
        total_nll += float(nll.sum().detach().cpu())
        total_tokens += len(batch_positions)
    return total_nll, total_tokens


def evaluate_model(
    spec: ModelSpec,
    by_lang: dict[str, list[dict[str, str]]],
    device: torch.device,
    max_length: int,
    mask_batch_size: int,
) -> list[dict[str, object]]:
    print(json.dumps({"event": "load_model", "model_key": spec.model_key}, ensure_ascii=False), flush=True)
    tokenizer = AutoTokenizer.from_pretrained(spec.tokenizer_path)
    model = AutoModelForMaskedLM.from_pretrained(spec.model_path).to(device)
    model.eval()

    rows_out: list[dict[str, object]] = []
    for lang, rows in by_lang.items():
        lang_nll = 0.0
        lang_tokens = 0
        used_examples = 0
        started = time.time()
        for idx, row in enumerate(rows, start=1):
            nll, tokens = sentence_nll(
                row["text"],
                tokenizer,
                model,
                device,
                max_length=max_length,
                mask_batch_size=mask_batch_size,
            )
            if tokens:
                lang_nll += nll
                lang_tokens += tokens
                used_examples += 1
            if idx % 25 == 0:
                print(
                    json.dumps(
                        {
                            "event": "progress",
                            "model_key": spec.model_key,
                            "language_id": lang,
                            "examples_seen": idx,
                            "tokens": lang_tokens,
                        },
                        ensure_ascii=False,
                    ),
                    flush=True,
                )
        mean_nll = lang_nll / lang_tokens if lang_tokens else float("nan")
        rows_out.append(
            {
                "model_key": spec.model_key,
                "phase": spec.phase,
                "method": spec.method,
                "language_id": lang,
                "examples": used_examples,
                "masked_tokens": lang_tokens,
                "mean_nll": fmt(mean_nll),
                "pseudo_perplexity": fmt(exp_safe(mean_nll)),
                "elapsed_sec": fmt(time.time() - started, 3),
            }
        )
    del model
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return rows_out


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    by_model: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        by_model.setdefault(str(row["model_key"]), []).append(row)
    out = []
    for model_key, group in sorted(by_model.items()):
        total_tokens = sum(int(row["masked_tokens"]) for row in group)
        weighted_nll = sum(float(row["mean_nll"]) * int(row["masked_tokens"]) for row in group) / total_tokens
        macro_nll = mean(float(row["mean_nll"]) for row in group)
        first = group[0]
        out.append(
            {
                "model_key": model_key,
                "phase": first["phase"],
                "method": first["method"],
                "languages": len(group),
                "total_examples": sum(int(row["examples"]) for row in group),
                "total_masked_tokens": total_tokens,
                "macro_mean_nll": fmt(macro_nll),
                "macro_pseudo_perplexity": fmt(exp_safe(macro_nll)),
                "weighted_mean_nll": fmt(weighted_nll),
                "weighted_pseudo_perplexity": fmt(exp_safe(weighted_nll)),
            }
        )
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="docs/exp/v3.1/01_embedding_alignment/parallel_item_manifest.tsv")
    parser.add_argument("--output-dir", default="docs/exp/v3.1/05_additional")
    parser.add_argument("--output-prefix", default="pseudoperplexity")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--max-examples-per-lang", type=int, default=100)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--mask-batch-size", type=int, default=64)
    parser.add_argument("--model-keys", nargs="+")
    parser.add_argument("--include-zero", action="store_true")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    device = torch.device(args.device)
    by_lang = load_dev_rows(Path(args.manifest), args.max_examples_per_lang)

    specs = default_models(include_zero=args.include_zero)
    if args.model_keys:
        requested = set(args.model_keys)
        specs = [spec for spec in specs if spec.model_key in requested]
        missing = requested.difference({spec.model_key for spec in specs})
        if missing:
            raise ValueError(f"Unknown model keys: {sorted(missing)}")

    all_rows: list[dict[str, object]] = []
    started = time.time()
    for spec in specs:
        all_rows.extend(
            evaluate_model(
                spec,
                by_lang,
                device,
                max_length=args.max_length,
                mask_batch_size=args.mask_batch_size,
            )
        )

    score_fields = [
        "model_key",
        "phase",
        "method",
        "language_id",
        "examples",
        "masked_tokens",
        "mean_nll",
        "pseudo_perplexity",
        "elapsed_sec",
    ]
    summary_fields = [
        "model_key",
        "phase",
        "method",
        "languages",
        "total_examples",
        "total_masked_tokens",
        "macro_mean_nll",
        "macro_pseudo_perplexity",
        "weighted_mean_nll",
        "weighted_pseudo_perplexity",
    ]
    write_tsv(output_dir / f"{args.output_prefix}_scores.tsv", all_rows, score_fields)
    write_tsv(output_dir / f"{args.output_prefix}_summary.tsv", summarize(all_rows), summary_fields)
    meta = {
        "event": "done",
        "output_prefix": args.output_prefix,
        "models": [spec.model_key for spec in specs],
        "max_examples_per_lang": args.max_examples_per_lang,
        "max_length": args.max_length,
        "mask_batch_size": args.mask_batch_size,
        "elapsed_sec": round(time.time() - started, 3),
    }
    (output_dir / f"{args.output_prefix}_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
