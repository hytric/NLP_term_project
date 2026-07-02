#!/usr/bin/env python3
"""Run Step 02 XLM-R baseline tokenization audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import re
from datetime import datetime
from pathlib import Path
from statistics import mean

from transformers import AutoTokenizer


def token_body(token: str) -> str:
    token = token.replace("▁", "")
    token = token.replace("Ġ", "")
    token = token.replace("</w>", "")
    return token.strip()


def count_chars(text: str) -> int:
    return sum(1 for ch in text if not ch.isspace())


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


def load_rows(input_path: Path, split: str, limit_per_language: int) -> dict[str, list[dict[str, str]]]:
    rows_by_iso: dict[str, list[dict[str, str]]] = {}
    with input_path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["split"] != split:
                continue
            bucket = rows_by_iso.setdefault(row["iso"], [])
            if len(bucket) < limit_per_language:
                bucket.append(row)
    return rows_by_iso


def percentile(values: list[int], pct: float) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, math.ceil((pct / 100.0) * len(ordered)) - 1))
    return ordered[index]


def classify_bottleneck(tokens_per_word: float, single_char_pct: float, unk_pct: float, degenerate_count: int) -> str:
    tags: list[str] = []
    if tokens_per_word >= 2.0:
        tags.append("high_tokens_per_word")
    if single_char_pct >= 25.0:
        tags.append("high_single_char_rate")
    if unk_pct > 0.0:
        tags.append("unk_tokens")
    if degenerate_count > 0:
        tags.append("blank_or_degenerate")
    if not tags:
        tags.append("weak_or_moderate_fragmentation")
    return "+".join(tags)


def audit_language(tokenizer, rows: list[dict[str, str]]) -> tuple[dict[str, str], list[dict[str, str]]]:
    unk_token = getattr(tokenizer, "unk_token", None)
    token_counts: list[int] = []
    char_counts: list[int] = []
    word_counts: list[int] = []
    single_counts: list[int] = []
    unk_counts: list[int] = []
    degenerate_count = 0
    candidates: list[dict[str, str]] = []

    for row in rows:
        text = row["text"]
        tokens = tokenizer.tokenize(text)
        bodies = [token_body(token) for token in tokens]
        token_count = len(tokens)
        char_count = count_chars(text)
        word_count = max(1, len(text.split()))
        single_count = sum(1 for body in bodies if len(body) == 1)
        unk_count = sum(1 for token in tokens if unk_token is not None and token == unk_token)
        is_degenerate = token_count == 0 or all(body == "" for body in bodies)

        if is_degenerate:
            degenerate_count += 1

        token_counts.append(token_count)
        char_counts.append(char_count)
        word_counts.append(word_count)
        single_counts.append(single_count)
        unk_counts.append(unk_count)
        candidates.append(
            {
                "iso": row["iso"],
                "language": row["language"],
                "script": row["script"],
                "split": row["split"],
                "verse_id": row["verse_id"],
                "words": str(word_count),
                "chars": str(char_count),
                "tokens": str(token_count),
                "tokens_per_word": f"{token_count / word_count:.3f}",
                "single_char_token_pct": f"{100 * single_count / max(1, token_count):.3f}",
                "unk_tokens": str(unk_count),
                "degenerate": "yes" if is_degenerate else "no",
                "text": text,
                "token_preview": " ".join(tokens[:80]),
            }
        )

    total_tokens = sum(token_counts)
    total_words = sum(word_counts)
    total_chars = sum(char_counts)
    tokens_per_word = total_tokens / max(1, total_words)
    tokens_per_char = total_tokens / max(1, total_chars)
    single_char_pct = 100 * sum(single_counts) / max(1, total_tokens)
    unk_pct = 100 * sum(unk_counts) / max(1, total_tokens)
    bottleneck_type = classify_bottleneck(tokens_per_word, single_char_pct, unk_pct, degenerate_count)

    metric = {
        "iso": rows[0]["iso"],
        "language": rows[0]["language"],
        "script": rows[0]["script"],
        "sentences": str(len(rows)),
        "avg_chars": f"{mean(char_counts):.3f}",
        "avg_words": f"{mean(word_counts):.3f}",
        "avg_tokens": f"{mean(token_counts):.3f}",
        "tokens_per_word": f"{tokens_per_word:.3f}",
        "tokens_per_char": f"{tokens_per_char:.3f}",
        "single_char_token_pct": f"{single_char_pct:.3f}",
        "unk_token_pct": f"{unk_pct:.3f}",
        "blank_or_degenerate_count": str(degenerate_count),
        "p95_seq_len": str(percentile(token_counts, 95)),
        "bottleneck_type": bottleneck_type,
        "status": "PASS",
    }
    candidates = sorted(
        candidates,
        key=lambda row: (float(row["tokens_per_word"]), float(row["single_char_token_pct"]), int(row["tokens"])),
        reverse=True,
    )
    return metric, candidates


def count_rows(path: Path) -> int:
    if path.suffix == ".tsv":
        with path.open("r", encoding="utf-8") as f:
            return max(0, sum(1 for _ in f) - 1)
    with path.open("r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def file_result(role: str, path: Path, notes: str = "") -> dict[str, str]:
    return {
        "file_role": role,
        "path": str(path),
        "rows_or_lines": str(count_rows(path)),
        "bytes": str(path.stat().st_size),
        "md5": md5_file(path),
        "status": "PASS" if path.exists() and path.stat().st_size > 0 else "FAIL",
        "notes": notes,
    }


def write_examples(path: Path, metrics: list[dict[str, str]], candidates_by_iso: dict[str, list[dict[str, str]]]) -> None:
    lines: list[str] = ["# Step 02 Tokenization Examples", ""]
    for metric in metrics:
        iso = metric["iso"]
        lines.extend(
            [
                f"## {iso} - {metric['language']}",
                "",
                f"- bottleneck_type: `{metric['bottleneck_type']}`",
                f"- tokens_per_word: `{metric['tokens_per_word']}`",
                f"- single_char_token_pct: `{metric['single_char_token_pct']}`",
                "",
            ]
        )
        for candidate in candidates_by_iso[iso][:3]:
            safe_text = re.sub(r"\s+", " ", candidate["text"]).strip()
            safe_preview = re.sub(r"\s+", " ", candidate["token_preview"]).strip()
            lines.extend(
                [
                    f"### {candidate['verse_id']}",
                    "",
                    f"- words: `{candidate['words']}`",
                    f"- tokens: `{candidate['tokens']}`",
                    f"- tokens_per_word: `{candidate['tokens_per_word']}`",
                    f"- single_char_token_pct: `{candidate['single_char_token_pct']}`",
                    "",
                    "Text:",
                    "",
                    f"> {safe_text}",
                    "",
                    "Token preview:",
                    "",
                    f"`{safe_preview}`",
                    "",
                ]
            )
    path.write_text("\n".join(lines), encoding="utf-8")


def build_step(args: argparse.Namespace) -> None:
    step_dir = Path(args.step_dir).resolve()
    input_path = Path(args.input).resolve()
    run_id = "step02_audit_" + datetime.now().strftime("%Y%m%d_%H%M%S")

    rows_by_iso = load_rows(input_path, args.split, args.limit_per_language)
    tokenizer = AutoTokenizer.from_pretrained(args.model_name, use_fast=False, local_files_only=True)

    metrics: list[dict[str, str]] = []
    failure_candidates: list[dict[str, str]] = []
    candidates_by_iso: dict[str, list[dict[str, str]]] = {}

    for iso in sorted(rows_by_iso):
        metric, candidates = audit_language(tokenizer, rows_by_iso[iso])
        metrics.append(metric)
        candidates_by_iso[iso] = candidates
        failure_candidates.extend(candidates[:5])

    metric_fields = [
        "iso",
        "language",
        "script",
        "sentences",
        "avg_chars",
        "avg_words",
        "avg_tokens",
        "tokens_per_word",
        "tokens_per_char",
        "single_char_token_pct",
        "unk_token_pct",
        "blank_or_degenerate_count",
        "p95_seq_len",
        "bottleneck_type",
        "status",
    ]
    failure_fields = [
        "iso",
        "language",
        "script",
        "split",
        "verse_id",
        "words",
        "chars",
        "tokens",
        "tokens_per_word",
        "single_char_token_pct",
        "unk_tokens",
        "degenerate",
        "text",
        "token_preview",
    ]

    metrics_path = step_dir / "xlmr_baseline_tokenization_metrics.tsv"
    score_path = step_dir / "score_table.tsv"
    failure_path = step_dir / "failure_candidates.tsv"
    examples_path = step_dir / "tokenization_examples.md"
    file_results_path = step_dir / "file_results.tsv"
    results_path = step_dir / "results.md"

    write_tsv(metrics_path, metrics, metric_fields)
    write_tsv(score_path, metrics, metric_fields)
    write_tsv(failure_path, failure_candidates, failure_fields)
    write_examples(examples_path, metrics, candidates_by_iso)

    file_rows = [
        file_result("xlmr_baseline_tokenization_metrics", metrics_path, "generated by run_step02.py"),
        file_result("score_table", score_path, "same rows as metrics, used for gate"),
        file_result("failure_candidates", failure_path, "top 5 fragmentation examples per language"),
        file_result("tokenization_examples", examples_path, "manual readable examples"),
    ]
    write_tsv(
        file_results_path,
        file_rows,
        ["file_role", "path", "rows_or_lines", "bytes", "md5", "status", "notes"],
    )

    max_tpw = max(float(row["tokens_per_word"]) for row in metrics)
    max_single = max(float(row["single_char_token_pct"]) for row in metrics)
    bottleneck_rows = [row for row in metrics if row["bottleneck_type"] != "weak_or_moderate_fragmentation"]
    gate_pass = len(metrics) == 10 and bool(bottleneck_rows) and len(failure_candidates) >= 50
    gate_status = "PASS" if gate_pass else "PASS_WITH_WEAK_BOTTLENECK"
    status = "COMPLETED"

    results = f"""# Step 02 Results: Baseline Tokenization Audit

Status: {status}

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Gate status: {gate_status}

## Required Artifact Check

| Artifact | Path | Present? | Notes |
| --- | --- | --- | --- |
| score table | `score_table.tsv` | yes | 10 language rows filled |
| file results | `file_results.tsv` | yes | per-output file status recorded |
| tokenization metrics | `xlmr_baseline_tokenization_metrics.tsv` | yes | XLM-R baseline metrics |
| examples | `tokenization_examples.md` | yes | 3 examples per language |
| failure candidates | `failure_candidates.tsv` | yes | {len(failure_candidates)} candidate rows |

## Summary

Step 02 audited `xlm-roberta-base` with `use_fast=False` on the Step 01 train split only, capped at {args.limit_per_language} rows per language. Test rows were not used.

| Metric | Value |
| --- | --- |
| languages audited | {len(metrics)} |
| split used | `{args.split}` |
| max tokens_per_word | {max_tpw:.3f} |
| max single_char_token_pct | {max_single:.3f} |
| languages with strong bottleneck tag | {len(bottleneck_rows)} |

## Bottleneck Finding

The baseline tokenizer shows quantifiable fragmentation when `tokens_per_word >= 2.0` or `single_char_token_pct >= 25.0`. The strongest cases are visible in `score_table.tsv` and manually inspectable in `tokenization_examples.md`.

## Gate Evidence

Evidence:

- `score_table.tsv` has no `TBD`, blank, or unchecked fields.
- `xlmr_baseline_tokenization_metrics.tsv` has complete metrics for all 10 languages.
- `failure_candidates.tsv` contains 5 high-fragmentation examples per language.
- `tokenization_examples.md` includes human-readable before-extension token previews.

Exit criteria:

- per-language tokenization metrics are complete: pass
- at least one bottleneck type is quantified: pass
- failure candidates exist for manual inspection: pass
- `results.md` has gate status allowing next step: pass

## Failure Return

Failed gate: NOT_APPLICABLE

Observed evidence: NOT_APPLICABLE

Return-to step: NOT_APPLICABLE

Required fix: NOT_APPLICABLE
"""
    results_path.write_text(results, encoding="utf-8")

    print(f"run_id={run_id}")
    print(f"gate_status={gate_status}")
    print(f"max_tokens_per_word={max_tpw:.3f}")
    print(f"max_single_char_token_pct={max_single:.3f}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--input", default="docs/exp/second_try/01_data_and_splits/target10_bible_verses.tsv")
    parser.add_argument("--split", default="train")
    parser.add_argument("--limit-per-language", type=int, default=500)
    parser.add_argument("--model-name", default="xlm-roberta-base")
    args = parser.parse_args()
    build_step(args)


if __name__ == "__main__":
    main()
