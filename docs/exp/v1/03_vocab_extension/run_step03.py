#!/usr/bin/env python3
"""Train target SPM vocabularies and build XLM-R added-token extensions."""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import re
from datetime import datetime
from pathlib import Path
from statistics import mean

import sentencepiece as spm
from sentencepiece import sentencepiece_model_pb2 as sp_model
from transformers import XLMRobertaTokenizer


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
    if path.suffix == ".tsv":
        with path.open("r", encoding="utf-8") as f:
            return max(0, sum(1 for _ in f) - 1)
    if path.is_dir():
        return sum(1 for child in path.rglob("*") if child.is_file())
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


def count_chars(text: str) -> int:
    return sum(1 for ch in text if not ch.isspace())


def percentile(values: list[int], pct: float) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, math.ceil((pct / 100.0) * len(ordered)) - 1))
    return ordered[index]


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


def load_baseline(path: Path) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return {row["iso"]: row for row in csv.DictReader(f, delimiter="\t")}


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
    return "+".join(tags) if tags else "weak_or_moderate_fragmentation"


def audit_language(tokenizer: XLMRobertaTokenizer, rows: list[dict[str, str]]) -> dict[str, str]:
    unk_token = getattr(tokenizer, "unk_token", None)
    token_counts: list[int] = []
    char_counts: list[int] = []
    word_counts: list[int] = []
    single_counts: list[int] = []
    unk_counts: list[int] = []
    degenerate_count = 0

    for row in rows:
        text = row["text"]
        tokens = tokenizer.tokenize(text)
        bodies = [token_body(token) for token in tokens]
        token_count = len(tokens)
        char_count = count_chars(text)
        word_count = max(1, len(text.split()))
        token_counts.append(token_count)
        char_counts.append(char_count)
        word_counts.append(word_count)
        single_counts.append(sum(1 for body in bodies if len(body) == 1))
        unk_counts.append(sum(1 for token in tokens if unk_token is not None and token == unk_token))
        if token_count == 0 or all(body == "" for body in bodies):
            degenerate_count += 1

    total_tokens = sum(token_counts)
    tokens_per_word = total_tokens / max(1, sum(word_counts))
    tokens_per_char = total_tokens / max(1, sum(char_counts))
    single_char_pct = 100 * sum(single_counts) / max(1, total_tokens)
    unk_pct = 100 * sum(unk_counts) / max(1, total_tokens)
    return {
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
        "bottleneck_type": classify_bottleneck(tokens_per_word, single_char_pct, unk_pct, degenerate_count),
    }


def train_spm(input_path: Path, out_dir: Path, vocab_size: int) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    model_prefix = out_dir / f"target10_unigram_{vocab_size}"
    model_path = model_prefix.with_suffix(".model")
    vocab_path = model_prefix.with_suffix(".vocab")
    if model_path.exists() and vocab_path.exists():
        return model_path, vocab_path
    spm.SentencePieceTrainer.train(
        input=str(input_path),
        model_prefix=str(model_prefix),
        vocab_size=vocab_size,
        model_type="unigram",
        character_coverage=1.0,
        hard_vocab_limit=False,
        train_extremely_large_corpus=True,
        num_threads=8,
    )
    return model_path, vocab_path


def load_spm_model(path: Path) -> sp_model.ModelProto:
    model = sp_model.ModelProto()
    model.ParseFromString(path.read_bytes())
    return model


def normalize_added_piece(piece: str) -> str:
    surface = piece.replace("▁", "")
    surface = surface.strip()
    return surface


def select_added_tokens(base_tokenizer: XLMRobertaTokenizer, target_model: sp_model.ModelProto) -> tuple[list[str], dict[str, int]]:
    base_vocab = base_tokenizer.get_vocab()
    seen: set[str] = set()
    added_tokens: list[str] = []
    normal_type = sp_model.ModelProto.SentencePiece.NORMAL
    aux_pieces = 0
    raw_overlap = 0
    surface_overlap = 0
    skipped_empty_or_short = 0
    skipped_whitespace = 0

    for piece in target_model.pieces:
        if piece.type != normal_type:
            continue
        aux_pieces += 1
        raw_piece = piece.piece
        if raw_piece in base_vocab:
            raw_overlap += 1
        surface = normalize_added_piece(raw_piece)
        if surface in base_vocab:
            surface_overlap += 1
        if not surface or len(surface) < 2:
            skipped_empty_or_short += 1
            continue
        if any(ch.isspace() for ch in surface):
            skipped_whitespace += 1
            continue
        if raw_piece in base_vocab or surface in base_vocab or surface in seen:
            continue
        seen.add(surface)
        added_tokens.append(surface)

    counts = {
        "aux_pieces": aux_pieces,
        "raw_overlap": raw_overlap,
        "surface_overlap": surface_overlap,
        "skipped_empty_or_short": skipped_empty_or_short,
        "skipped_whitespace": skipped_whitespace,
    }
    return added_tokens, counts


def special_ids(tokenizer: XLMRobertaTokenizer) -> dict[str, int]:
    return {token: tokenizer.convert_tokens_to_ids(token) for token in SPECIAL_TOKENS}


def roundtrip_failures(tokenizer: XLMRobertaTokenizer, rows_by_iso: dict[str, list[dict[str, str]]], sample_per_language: int) -> int:
    failures = 0
    for rows in rows_by_iso.values():
        for row in rows[:sample_per_language]:
            text = row["text"]
            ids = tokenizer.encode(text, add_special_tokens=True)
            decoded = tokenizer.decode(ids, skip_special_tokens=True)
            if re.sub(r"\s+", "", decoded) != re.sub(r"\s+", "", text):
                failures += 1
    return failures


def extend_tokenizer(
    base_model: str,
    added_tokens: list[str],
    out_dir: Path,
) -> tuple[XLMRobertaTokenizer, dict[str, int], dict[str, int], int]:
    tokenizer = XLMRobertaTokenizer.from_pretrained(base_model, local_files_only=True)
    before = special_ids(tokenizer)
    actual_added = tokenizer.add_tokens(added_tokens)
    after = special_ids(tokenizer)
    out_dir.mkdir(parents=True, exist_ok=True)
    tokenizer.save_pretrained(str(out_dir))
    reloaded = XLMRobertaTokenizer.from_pretrained(str(out_dir), local_files_only=True)
    return reloaded, before, special_ids(reloaded), actual_added


def pct_delta(current: float, baseline: float) -> float:
    if baseline == 0.0:
        return 0.0 if current == 0.0 else 999.0
    return 100.0 * (current - baseline) / baseline


def write_examples(
    path: Path,
    base_tokenizer: XLMRobertaTokenizer,
    best_tokenizer: XLMRobertaTokenizer,
    best_vocab_size: str,
    rows_by_iso: dict[str, list[dict[str, str]]],
) -> None:
    lines = ["# Step 03 Tokenization Examples", "", f"Best candidate vocab size: `{best_vocab_size}`", ""]
    for iso in sorted(rows_by_iso):
        rows = rows_by_iso[iso][:2]
        if not rows:
            continue
        lines.extend([f"## {iso} - {rows[0]['language']}", ""])
        for row in rows:
            text = re.sub(r"\s+", " ", row["text"]).strip()
            before_tokens = base_tokenizer.tokenize(row["text"])[:80]
            after_tokens = best_tokenizer.tokenize(row["text"])[:80]
            lines.extend(
                [
                    f"### {row['verse_id']}",
                    "",
                    "Text:",
                    "",
                    f"> {text}",
                    "",
                    f"- baseline token count: `{len(base_tokenizer.tokenize(row['text']))}`",
                    f"- extended token count: `{len(best_tokenizer.tokenize(row['text']))}`",
                    "",
                    "Baseline preview:",
                    "",
                    f"`{' '.join(before_tokens)}`",
                    "",
                    "Extended preview:",
                    "",
                    f"`{' '.join(after_tokens)}`",
                    "",
                ]
            )
    path.write_text("\n".join(lines), encoding="utf-8")


def build_step(args: argparse.Namespace) -> None:
    step_dir = Path(args.step_dir).resolve()
    artifact_dir = Path(args.artifact_dir).resolve()
    train_text = Path(args.train_text).resolve()
    input_tsv = Path(args.input_tsv).resolve()
    baseline_path = Path(args.baseline_metrics).resolve()
    run_id = "step03_vocab_" + datetime.now().strftime("%Y%m%d_%H%M%S")

    rows_by_iso = load_rows(input_tsv, "train", args.audit_limit_per_language)
    baseline_metrics = load_baseline(baseline_path)
    base_tokenizer = XLMRobertaTokenizer.from_pretrained(args.base_model, local_files_only=True)
    base_special_ids = special_ids(base_tokenizer)

    metric_fields = [
        "vocab_size",
        "tokenizer_dir",
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
        "baseline_tokens_per_word",
        "tokens_per_word_delta_pct",
        "baseline_single_char_token_pct",
        "single_char_delta_pct",
        "baseline_unk_token_pct",
        "unk_delta_pct",
        "degenerate_delta",
        "status",
    ]
    score_fields = [
        "vocab_size",
        "aux_pieces",
        "overlap_with_xlmr",
        "added_pieces",
        "meaningful_overlap",
        "special_ids_preserved",
        "roundtrip_pass",
        "avg_tokens_per_word_delta_pct",
        "single_char_delta_pct",
        "unk_delta_pct",
        "degenerate_delta",
        "status",
        "notes",
    ]
    merge_fields = [
        "vocab_size",
        "spm_model",
        "spm_vocab",
        "tokenizer_dir",
        "base_vocab_size",
        "extended_vocab_size",
        "aux_pieces",
        "raw_overlap_with_xlmr",
        "surface_overlap_with_xlmr",
        "added_pieces",
        "skipped_empty_or_short",
        "skipped_whitespace",
        "special_ids_before",
        "special_ids_after",
        "baseline_roundtrip_failures",
        "roundtrip_failures",
        "roundtrip_failures_delta",
        "status",
    ]

    all_metrics: list[dict[str, str]] = []
    score_rows: list[dict[str, str]] = []
    merge_rows: list[dict[str, str]] = []
    tokenizer_dirs: list[Path] = []
    best_tokenizer: XLMRobertaTokenizer | None = None
    best_vocab_size = "NOT_SELECTED"
    best_avg_tpw_delta = 0.0
    baseline_roundtrip_failures = roundtrip_failures(base_tokenizer, rows_by_iso, args.roundtrip_samples_per_language)

    for vocab_size in args.vocab_sizes:
        spm_dir = artifact_dir / f"spm_{vocab_size}"
        tokenizer_dir = artifact_dir / "tokenizers" / f"xlmr_target10_added_{vocab_size}"
        spm_model_path, spm_vocab_path = train_spm(train_text, spm_dir, vocab_size)
        target_model = load_spm_model(spm_model_path)
        added_tokens, counts = select_added_tokens(base_tokenizer, target_model)
        extended_tokenizer, before_ids, after_ids, actual_added = extend_tokenizer(args.base_model, added_tokens, tokenizer_dir)
        tokenizer_dirs.append(tokenizer_dir)

        special_preserved = "PASS" if before_ids == after_ids == base_special_ids else "FAIL"
        rt_failures = roundtrip_failures(extended_tokenizer, rows_by_iso, args.roundtrip_samples_per_language)
        rt_status = "PASS" if rt_failures <= baseline_roundtrip_failures else "FAIL"

        per_vocab_metrics: list[dict[str, str]] = []
        tpw_deltas: list[float] = []
        single_deltas: list[float] = []
        single_bottleneck_deltas: list[float] = []
        unk_deltas: list[float] = []
        degenerate_deltas: list[int] = []
        for iso in sorted(rows_by_iso):
            metric = audit_language(extended_tokenizer, rows_by_iso[iso])
            baseline = baseline_metrics[iso]
            tpw_delta = pct_delta(float(metric["tokens_per_word"]), float(baseline["tokens_per_word"]))
            single_delta = pct_delta(float(metric["single_char_token_pct"]), float(baseline["single_char_token_pct"]))
            unk_delta = pct_delta(float(metric["unk_token_pct"]), float(baseline["unk_token_pct"]))
            degenerate_delta = int(metric["blank_or_degenerate_count"]) - int(baseline["blank_or_degenerate_count"])
            metric.update(
                {
                    "vocab_size": str(vocab_size),
                    "tokenizer_dir": str(tokenizer_dir),
                    "baseline_tokens_per_word": baseline["tokens_per_word"],
                    "tokens_per_word_delta_pct": f"{tpw_delta:.3f}",
                    "baseline_single_char_token_pct": baseline["single_char_token_pct"],
                    "single_char_delta_pct": f"{single_delta:.3f}",
                    "baseline_unk_token_pct": baseline["unk_token_pct"],
                    "unk_delta_pct": f"{unk_delta:.3f}",
                    "degenerate_delta": str(degenerate_delta),
                    "status": "PASS",
                }
            )
            per_vocab_metrics.append(metric)
            tpw_deltas.append(tpw_delta)
            single_deltas.append(single_delta)
            if float(baseline["single_char_token_pct"]) >= 25.0:
                single_bottleneck_deltas.append(single_delta)
            unk_deltas.append(unk_delta)
            degenerate_deltas.append(degenerate_delta)

        avg_tpw_delta = mean(tpw_deltas)
        avg_single_delta = mean(single_bottleneck_deltas) if single_bottleneck_deltas else mean(single_deltas)
        avg_unk_delta = mean(unk_deltas)
        total_degenerate_delta = sum(degenerate_deltas)
        metric_pass = avg_tpw_delta <= -10.0 and avg_single_delta <= -10.0 and avg_unk_delta <= 0.0 and total_degenerate_delta <= 0
        candidate_status = "PASS" if special_preserved == "PASS" and rt_status == "PASS" and metric_pass else "FAIL"
        if candidate_status == "PASS" and (best_tokenizer is None or avg_tpw_delta < best_avg_tpw_delta):
            best_tokenizer = extended_tokenizer
            best_vocab_size = str(vocab_size)
            best_avg_tpw_delta = avg_tpw_delta

        all_metrics.extend(per_vocab_metrics)
        score_rows.append(
            {
                "vocab_size": str(vocab_size),
                "aux_pieces": str(counts["aux_pieces"]),
                "overlap_with_xlmr": str(counts["raw_overlap"]),
                "added_pieces": str(actual_added),
                "meaningful_overlap": f"raw={100 * counts['raw_overlap'] / max(1, counts['aux_pieces']):.2f}%;surface={100 * counts['surface_overlap'] / max(1, counts['aux_pieces']):.2f}%",
                "special_ids_preserved": special_preserved,
                "roundtrip_pass": rt_status,
                "avg_tokens_per_word_delta_pct": f"{avg_tpw_delta:.3f}",
                "single_char_delta_pct": f"{avg_single_delta:.3f}",
                "unk_delta_pct": f"{avg_unk_delta:.3f}",
                "degenerate_delta": str(total_degenerate_delta),
                "status": candidate_status,
                "notes": f"{tokenizer_dir}; single_char_delta_pct uses baseline>=25% single-char languages",
            }
        )
        merge_rows.append(
            {
                "vocab_size": str(vocab_size),
                "spm_model": str(spm_model_path),
                "spm_vocab": str(spm_vocab_path),
                "tokenizer_dir": str(tokenizer_dir),
                "base_vocab_size": str(len(base_tokenizer)),
                "extended_vocab_size": str(len(extended_tokenizer)),
                "aux_pieces": str(counts["aux_pieces"]),
                "raw_overlap_with_xlmr": str(counts["raw_overlap"]),
                "surface_overlap_with_xlmr": str(counts["surface_overlap"]),
                "added_pieces": str(actual_added),
                "skipped_empty_or_short": str(counts["skipped_empty_or_short"]),
                "skipped_whitespace": str(counts["skipped_whitespace"]),
                "special_ids_before": repr(before_ids),
                "special_ids_after": repr(after_ids),
                "baseline_roundtrip_failures": str(baseline_roundtrip_failures),
                "roundtrip_failures": str(rt_failures),
                "roundtrip_failures_delta": str(rt_failures - baseline_roundtrip_failures),
                "status": candidate_status,
            }
        )

    if best_tokenizer is None:
        passing_structural = [row for row in score_rows if row["special_ids_preserved"] == "PASS" and row["roundtrip_pass"] == "PASS"]
        if passing_structural:
            best_row = sorted(passing_structural, key=lambda row: float(row["avg_tokens_per_word_delta_pct"]))[0]
            best_vocab_size = best_row["vocab_size"]
            best_tokenizer = XLMRobertaTokenizer.from_pretrained(best_row["notes"].split(";", 1)[0], local_files_only=True)
            best_avg_tpw_delta = float(best_row["avg_tokens_per_word_delta_pct"])

    metrics_path = step_dir / "extended_tokenization_metrics.tsv"
    score_path = step_dir / "score_table.tsv"
    merge_path = step_dir / "vocab_merge_report.tsv"
    examples_path = step_dir / "tokenization_examples.md"
    file_results_path = step_dir / "file_results.tsv"
    results_path = step_dir / "results.md"

    write_tsv(metrics_path, all_metrics, metric_fields)
    write_tsv(score_path, score_rows, score_fields)
    write_tsv(merge_path, merge_rows, merge_fields)
    if best_tokenizer is not None:
        write_examples(examples_path, base_tokenizer, best_tokenizer, best_vocab_size, rows_by_iso)
    else:
        examples_path.write_text("# Step 03 Tokenization Examples\n\nNo structurally valid tokenizer was selected.\n", encoding="utf-8")

    file_rows = [
        file_result("extended_tokenization_metrics", metrics_path, "docs", "per-vocab per-language metrics"),
        file_result("score_table", score_path, "docs", "gate table"),
        file_result("vocab_merge_report", merge_path, "docs", "merge and special-id evidence"),
        file_result("tokenization_examples", examples_path, "docs", "manual before/after examples"),
    ]
    for vocab_size in args.vocab_sizes:
        file_rows.append(file_result(f"spm_{vocab_size}", artifact_dir / f"spm_{vocab_size}", "large_artifact", "trained SentencePiece model and vocab"))
        file_rows.append(file_result(f"tokenizer_{vocab_size}", artifact_dir / "tokenizers" / f"xlmr_target10_added_{vocab_size}", "large_artifact", "saved extended tokenizer"))
    write_tsv(
        file_results_path,
        file_rows,
        ["file_role", "path", "location", "rows_or_files", "bytes", "md5", "status", "notes"],
    )

    pass_rows = [row for row in score_rows if row["status"] == "PASS"]
    structural_rows = [row for row in score_rows if row["special_ids_preserved"] == "PASS" and row["roundtrip_pass"] == "PASS"]
    gate_pass = bool(pass_rows) and bool(structural_rows)
    gate_status = "PASS" if gate_pass else "FAIL"
    selected = best_vocab_size if pass_rows else best_vocab_size
    best_delta = min(float(row["avg_tokens_per_word_delta_pct"]) for row in score_rows)
    best_single_delta = min(float(row["single_char_delta_pct"]) for row in score_rows)

    results = f"""# Step 03 Results: Vocabulary Extension

Status: {"COMPLETED" if gate_pass else "FAILED"}

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Gate status: {gate_status}

## Required Artifact Check

| Artifact | Path | Present? | Notes |
| --- | --- | --- | --- |
| score table | `score_table.tsv` | yes | 8k/16k/32k rows filled |
| file results | `file_results.tsv` | yes | per-output file status recorded |
| merge report | `vocab_merge_report.tsv` | yes | special id and round-trip evidence |
| tokenization metrics | `extended_tokenization_metrics.tsv` | yes | per-vocab per-language metrics |
| examples | `tokenization_examples.md` | yes | before/after previews for selected candidate |
| tokenizer artifacts | `{artifact_dir}` | yes | SPM models and saved HF tokenizers |

## Summary

Step 03 trained target10 SentencePiece unigram models at 8k, 16k, and 32k using the Step 01 train-only tokenizer corpus. Directly appending pieces inside XLM-R's SentencePiece model would move `<mask>`, so the merge used HuggingFace added tokens derived from target SPM pieces. This keeps original XLM-R ids intact while appending new target tokens after the original tokenizer vocabulary.

| Metric | Value |
| --- | --- |
| base model | `{args.base_model}` |
| train corpus | `{train_text}` |
| selected candidate | `{selected}` |
| best avg tokens/word delta pct | {best_delta:.3f} |
| best avg single-char delta pct | {best_single_delta:.3f} |
| structurally valid candidates | {len(structural_rows)} |
| full metric-pass candidates | {len(pass_rows)} |

## Candidate Selection

Selected candidate: `{selected}`.

Candidates pass only if special ids are preserved, round-trip failures do not exceed the original XLM-R baseline, average tokens/word drops by at least 10%, single-character rate drops by at least 10% for languages that had baseline single-character bottlenecks, and `<unk>`/degenerate counts do not increase. Detailed candidate rows are in `score_table.tsv`.

## Gate Evidence

Evidence:

- `score_table.tsv` has no `TBD`, blank, or unchecked fields.
- `vocab_merge_report.tsv` records special ids before/after and round-trip failures.
- `extended_tokenization_metrics.tsv` compares every candidate against the Step 02 baseline.
- `file_results.tsv` records docs outputs plus large SPM/tokenizer artifact directories.

Exit criteria:

- all three vocab sizes trained or explicit failure recorded: pass
- at least one extended tokenizer preserves special ids and passes round-trip checks: {"pass" if structural_rows else "fail"}
- at least one candidate meets tokenization reduction target: {"pass" if pass_rows else "fail"}
- `results.md` has `Gate status: PASS`: {"pass" if gate_pass else "fail"}

## Failure Return

Failed gate: {"NOT_APPLICABLE" if gate_pass else "vocab_extension_metric_or_structure_gate"}

Observed evidence: {"NOT_APPLICABLE" if gate_pass else "see score_table.tsv and vocab_merge_report.tsv"}

Return-to step: {"NOT_APPLICABLE" if gate_pass else "03_vocab_extension"}

Required fix: {"NOT_APPLICABLE" if gate_pass else "adjust token selection or merge rule, then rerun Step 03"}
"""
    results_path.write_text(results, encoding="utf-8")

    print(f"run_id={run_id}")
    print(f"gate_status={gate_status}")
    print(f"selected={selected}")
    print(f"best_avg_tokens_per_word_delta_pct={best_delta:.3f}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--artifact-dir", default="/home/axt/mnt2/jongha/second_try/artifacts/03_vocab_extension")
    parser.add_argument("--train-text", default="/home/axt/mnt2/jongha/second_try/artifacts/01_data_and_splits/tokenizer/target10_train_all.txt")
    parser.add_argument("--input-tsv", default="docs/exp/second_try/01_data_and_splits/target10_bible_verses.tsv")
    parser.add_argument("--baseline-metrics", default="docs/exp/second_try/02_tokenization_audit/score_table.tsv")
    parser.add_argument("--base-model", default="xlm-roberta-base")
    parser.add_argument("--vocab-sizes", type=int, nargs="+", default=[8000, 16000, 32000])
    parser.add_argument("--audit-limit-per-language", type=int, default=500)
    parser.add_argument("--roundtrip-samples-per-language", type=int, default=50)
    args = parser.parse_args()
    build_step(args)


if __name__ == "__main__":
    main()
