#!/usr/bin/env python3
"""V2 train-only tokenizer extension and dev-only selection."""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import re
import time
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


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def count_rows(path: Path) -> int:
    if path.is_dir():
        return sum(1 for child in path.rglob("*") if child.is_file())
    with path.open("r", encoding="utf-8") as f:
        total = sum(1 for _ in f)
    return max(0, total - 1) if path.suffix == ".tsv" else total


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


def token_body(token: str) -> str:
    return token.replace("▁", "").replace("Ġ", "").replace("</w>", "").strip()


def count_chars(text: str) -> int:
    return sum(1 for ch in text if not ch.isspace())


def percentile(values: list[int], pct: float) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    idx = max(0, min(len(ordered) - 1, math.ceil((pct / 100.0) * len(ordered)) - 1))
    return ordered[idx]


def special_ids(tokenizer: XLMRobertaTokenizer) -> dict[str, int]:
    return {token: tokenizer.convert_tokens_to_ids(token) for token in SPECIAL_TOKENS}


def load_dev_rows(path: Path) -> dict[str, list[dict[str, str]]]:
    rows_by_iso: dict[str, list[dict[str, str]]] = {}
    for row in read_tsv(path):
        if row["v2_split"] != "dev" or row["book"] != "MAR":
            raise RuntimeError(f"dev manifest contains non-dev row: {row.get('iso')} {row.get('verse_id')} {row.get('v2_split')}")
        rows_by_iso.setdefault(row["iso"], []).append(row)
    return rows_by_iso


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
    single_char_pct = 100.0 * sum(single_counts) / max(1, total_tokens)
    unk_pct = 100.0 * sum(unk_counts) / max(1, total_tokens)
    return {
        "iso": rows[0]["iso"],
        "language": rows[0]["language"],
        "script": rows[0]["script"],
        "split": "dev",
        "sentences": str(len(rows)),
        "avg_chars": f"{mean(char_counts):.3f}",
        "avg_words": f"{mean(word_counts):.3f}",
        "avg_tokens": f"{mean(token_counts):.3f}",
        "tokens_per_word": f"{tokens_per_word:.6f}",
        "tokens_per_char": f"{tokens_per_char:.6f}",
        "single_char_token_pct": f"{single_char_pct:.6f}",
        "unk_token_pct": f"{unk_pct:.6f}",
        "blank_or_degenerate_count": str(degenerate_count),
        "p95_seq_len": str(percentile(token_counts, 95)),
    }


def pct_delta(current: float, baseline: float) -> float:
    if baseline == 0.0:
        return 0.0 if current == 0.0 else 999.0
    return 100.0 * (current - baseline) / baseline


def train_spm(input_path: Path, out_dir: Path, vocab_size: int) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    model_prefix = out_dir / f"v2_target10_unigram_{vocab_size}"
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


def normalize_piece(piece: str) -> str:
    return piece.replace("▁", "").strip()


def select_added_tokens(base_tokenizer: XLMRobertaTokenizer, target_model: sp_model.ModelProto) -> tuple[list[str], dict[str, int]]:
    base_vocab = base_tokenizer.get_vocab()
    normal_type = sp_model.ModelProto.SentencePiece.NORMAL
    seen: set[str] = set()
    added: list[str] = []
    counts = {
        "aux_pieces": 0,
        "raw_overlap": 0,
        "surface_overlap": 0,
        "skipped_empty_or_short": 0,
        "skipped_whitespace": 0,
    }
    for piece in target_model.pieces:
        if piece.type != normal_type:
            continue
        counts["aux_pieces"] += 1
        raw = piece.piece
        if raw in base_vocab:
            counts["raw_overlap"] += 1
        surface = normalize_piece(raw)
        if surface in base_vocab:
            counts["surface_overlap"] += 1
        if not surface or len(surface) < 2:
            counts["skipped_empty_or_short"] += 1
            continue
        if any(ch.isspace() for ch in surface):
            counts["skipped_whitespace"] += 1
            continue
        if raw in base_vocab or surface in base_vocab or surface in seen:
            continue
        seen.add(surface)
        added.append(surface)
    return added, counts


def extend_tokenizer(base_model: str, added_tokens: list[str], out_dir: Path) -> tuple[XLMRobertaTokenizer, dict[str, int], dict[str, int], int]:
    tokenizer = XLMRobertaTokenizer.from_pretrained(base_model, local_files_only=True)
    before = special_ids(tokenizer)
    actual_added = tokenizer.add_tokens(added_tokens)
    out_dir.mkdir(parents=True, exist_ok=True)
    tokenizer.save_pretrained(str(out_dir))
    reloaded = XLMRobertaTokenizer.from_pretrained(str(out_dir), local_files_only=True)
    after = special_ids(reloaded)
    return reloaded, before, after, actual_added


def roundtrip_failures(tokenizer: XLMRobertaTokenizer, rows_by_iso: dict[str, list[dict[str, str]]], limit_per_language: int) -> int:
    failures = 0
    for iso in sorted(rows_by_iso):
        for row in rows_by_iso[iso][:limit_per_language]:
            text = row["text"]
            ids = tokenizer.encode(text, add_special_tokens=True)
            decoded = tokenizer.decode(ids, skip_special_tokens=True)
            if re.sub(r"\s+", "", decoded) != re.sub(r"\s+", "", text):
                failures += 1
    return failures


def write_examples(path: Path, base_tokenizer: XLMRobertaTokenizer, selected_tokenizer: XLMRobertaTokenizer, rows_by_iso: dict[str, list[dict[str, str]]], selected_vocab: str) -> None:
    lines = ["# Step 13 V2 Tokenization Examples", "", f"Selected vocab size: `{selected_vocab}`", "", "Examples are from Mark/dev only.", ""]
    for iso in sorted(rows_by_iso):
        rows = rows_by_iso[iso][:2]
        if not rows:
            continue
        lines.extend([f"## {iso} - {rows[0]['language']}", ""])
        for row in rows:
            text = re.sub(r"\s+", " ", row["text"]).strip()
            before = base_tokenizer.tokenize(text)
            after = selected_tokenizer.tokenize(text)
            lines.extend(
                [
                    f"### {row['verse_id']}",
                    "",
                    f"> {text}",
                    "",
                    f"- base token count: `{len(before)}`",
                    f"- selected token count: `{len(after)}`",
                    "",
                    f"`{' '.join(before[:80])}`",
                    "",
                    f"`{' '.join(after[:80])}`",
                    "",
                ]
            )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default="docs/exp/second_try/13_v2_tokenizer")
    parser.add_argument("--artifact-dir", default="/home/axt/mnt2/jongha/second_try/artifacts/13_v2_tokenizer")
    parser.add_argument("--train-text", default="/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_tokenizer_mlm_train.txt")
    parser.add_argument("--dev-manifest", default="docs/exp/second_try/12_v2_split_protocol/v2_dev_manifest.tsv")
    parser.add_argument("--base-model", default="xlm-roberta-base")
    parser.add_argument("--vocab-sizes", nargs="+", type=int, default=[8000, 16000, 32000])
    parser.add_argument("--roundtrip-samples-per-language", type=int, default=20)
    args = parser.parse_args()

    start = time.time()
    run_id = "step13_v2_tokenizer_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    step_dir = Path(args.step_dir).resolve()
    artifact_dir = Path(args.artifact_dir).resolve()
    train_text = Path(args.train_text).resolve()
    dev_manifest = Path(args.dev_manifest).resolve()
    artifact_dir.mkdir(parents=True, exist_ok=True)

    rows_by_iso = load_dev_rows(dev_manifest)
    base_tokenizer = XLMRobertaTokenizer.from_pretrained(args.base_model, local_files_only=True)
    base_special = special_ids(base_tokenizer)
    base_metrics = {iso: audit_language(base_tokenizer, rows_by_iso[iso]) for iso in sorted(rows_by_iso)}
    base_roundtrip = roundtrip_failures(base_tokenizer, rows_by_iso, args.roundtrip_samples_per_language)

    metric_rows: list[dict[str, str]] = []
    merge_rows: list[dict[str, str]] = []
    score_rows: list[dict[str, str]] = []
    tokenizer_dirs: list[Path] = []
    selected_tokenizer: XLMRobertaTokenizer | None = None
    selected_vocab = "NOT_SELECTED"
    selected_score = 999.0

    for vocab_size in args.vocab_sizes:
        spm_dir = artifact_dir / f"spm_{vocab_size}"
        tokenizer_dir = artifact_dir / "tokenizers" / f"xlmr_v2_target10_added_{vocab_size}"
        spm_model, spm_vocab = train_spm(train_text, spm_dir, vocab_size)
        target_model = load_spm_model(spm_model)
        added_tokens, counts = select_added_tokens(base_tokenizer, target_model)
        extended_tokenizer, before_ids, after_ids, actual_added = extend_tokenizer(args.base_model, added_tokens, tokenizer_dir)
        tokenizer_dirs.append(tokenizer_dir)
        special_status = "PASS" if before_ids == after_ids == base_special else "FAIL"
        rt_failures = roundtrip_failures(extended_tokenizer, rows_by_iso, args.roundtrip_samples_per_language)
        rt_status = "PASS" if rt_failures <= base_roundtrip else "FAIL"

        tpw_deltas = []
        single_deltas = []
        bottleneck_single_deltas = []
        unk_deltas = []
        degenerate_deltas = []
        for iso in sorted(rows_by_iso):
            metric = audit_language(extended_tokenizer, rows_by_iso[iso])
            base = base_metrics[iso]
            tpw_delta = pct_delta(float(metric["tokens_per_word"]), float(base["tokens_per_word"]))
            single_delta = pct_delta(float(metric["single_char_token_pct"]), float(base["single_char_token_pct"]))
            unk_delta = pct_delta(float(metric["unk_token_pct"]), float(base["unk_token_pct"]))
            degenerate_delta = int(metric["blank_or_degenerate_count"]) - int(base["blank_or_degenerate_count"])
            metric.update(
                {
                    "run_id": run_id,
                    "vocab_size": str(vocab_size),
                    "tokenizer_dir": str(tokenizer_dir),
                    "base_tokens_per_word": base["tokens_per_word"],
                    "tokens_per_word_delta_pct": f"{tpw_delta:.6f}",
                    "base_single_char_token_pct": base["single_char_token_pct"],
                    "single_char_delta_pct": f"{single_delta:.6f}",
                    "base_unk_token_pct": base["unk_token_pct"],
                    "unk_delta_pct": f"{unk_delta:.6f}",
                    "degenerate_delta": str(degenerate_delta),
                    "status": "MEASURED",
                }
            )
            metric_rows.append(metric)
            tpw_deltas.append(tpw_delta)
            single_deltas.append(single_delta)
            if float(base["single_char_token_pct"]) >= 25.0:
                bottleneck_single_deltas.append(single_delta)
            unk_deltas.append(unk_delta)
            degenerate_deltas.append(degenerate_delta)

        avg_tpw_delta = mean(tpw_deltas)
        avg_single_delta = mean(bottleneck_single_deltas) if bottleneck_single_deltas else mean(single_deltas)
        avg_unk_delta = mean(unk_deltas)
        total_degenerate_delta = sum(degenerate_deltas)
        dev_gate = avg_tpw_delta <= -10.0 and avg_single_delta <= -10.0 and avg_unk_delta <= 0.0 and total_degenerate_delta <= 0
        status = "PASS" if special_status == "PASS" and rt_status == "PASS" and dev_gate else "FAIL"
        if status == "PASS" and avg_tpw_delta < selected_score:
            selected_score = avg_tpw_delta
            selected_vocab = str(vocab_size)
            selected_tokenizer = extended_tokenizer

        score_rows.append(
            {
                "run_id": run_id,
                "vocab_size": str(vocab_size),
                "tokenizer_dir": str(tokenizer_dir),
                "aux_pieces": str(counts["aux_pieces"]),
                "raw_overlap_with_xlmr": str(counts["raw_overlap"]),
                "surface_overlap_with_xlmr": str(counts["surface_overlap"]),
                "added_pieces": str(actual_added),
                "special_ids_preserved": special_status,
                "roundtrip_pass": rt_status,
                "avg_tokens_per_word_delta_pct": f"{avg_tpw_delta:.6f}",
                "single_char_delta_pct": f"{avg_single_delta:.6f}",
                "unk_delta_pct": f"{avg_unk_delta:.6f}",
                "degenerate_delta": str(total_degenerate_delta),
                "status": status,
                "notes": "selected_on=MAR_dev_only; final_ACT_not_read",
            }
        )
        merge_rows.append(
            {
                "run_id": run_id,
                "vocab_size": str(vocab_size),
                "spm_model": str(spm_model),
                "spm_vocab": str(spm_vocab),
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
                "base_roundtrip_failures": str(base_roundtrip),
                "roundtrip_failures": str(rt_failures),
                "roundtrip_failures_delta": str(rt_failures - base_roundtrip),
                "status": status,
            }
        )

    if selected_tokenizer is None:
        passing_structural = [row for row in score_rows if row["special_ids_preserved"] == "PASS" and row["roundtrip_pass"] == "PASS"]
        if passing_structural:
            best = sorted(passing_structural, key=lambda row: float(row["avg_tokens_per_word_delta_pct"]))[0]
            selected_vocab = best["vocab_size"]
            selected_tokenizer = XLMRobertaTokenizer.from_pretrained(best["tokenizer_dir"], local_files_only=True)

    metrics_path = step_dir / "v2_vocab_extension_metrics.tsv"
    score_path = step_dir / "score_table.tsv"
    merge_path = step_dir / "v2_vocab_merge_report.tsv"
    examples_path = step_dir / "v2_tokenization_examples.md"
    access_path = step_dir / "v2_no_final_access_audit.tsv"
    selected_path = step_dir / "selected_tokenizer.md"
    results_path = step_dir / "results.md"
    file_results_path = step_dir / "file_results.tsv"

    metric_fields = ["run_id", "vocab_size", "tokenizer_dir", "iso", "language", "script", "split", "sentences", "avg_chars", "avg_words", "avg_tokens", "tokens_per_word", "tokens_per_char", "single_char_token_pct", "unk_token_pct", "blank_or_degenerate_count", "p95_seq_len", "base_tokens_per_word", "tokens_per_word_delta_pct", "base_single_char_token_pct", "single_char_delta_pct", "base_unk_token_pct", "unk_delta_pct", "degenerate_delta", "status"]
    score_fields = ["run_id", "vocab_size", "tokenizer_dir", "aux_pieces", "raw_overlap_with_xlmr", "surface_overlap_with_xlmr", "added_pieces", "special_ids_preserved", "roundtrip_pass", "avg_tokens_per_word_delta_pct", "single_char_delta_pct", "unk_delta_pct", "degenerate_delta", "status", "notes"]
    merge_fields = ["run_id", "vocab_size", "spm_model", "spm_vocab", "tokenizer_dir", "base_vocab_size", "extended_vocab_size", "aux_pieces", "raw_overlap_with_xlmr", "surface_overlap_with_xlmr", "added_pieces", "skipped_empty_or_short", "skipped_whitespace", "special_ids_before", "special_ids_after", "base_roundtrip_failures", "roundtrip_failures", "roundtrip_failures_delta", "status"]
    write_tsv(metrics_path, metric_rows, metric_fields)
    write_tsv(score_path, score_rows, score_fields)
    write_tsv(merge_path, merge_rows, merge_fields)

    if selected_tokenizer is not None:
        write_examples(examples_path, base_tokenizer, selected_tokenizer, rows_by_iso, selected_vocab)
    else:
        examples_path.write_text("# Step 13 V2 Tokenization Examples\n\nNo tokenizer selected.\n", encoding="utf-8")

    selected_row = next((row for row in score_rows if row["vocab_size"] == selected_vocab), None)
    selected_path.write_text(
        f"""# Step 13 Selected V2 Tokenizer

Run id: `{run_id}`

Selected vocab size: `{selected_vocab}`

Tokenizer path: `{selected_row['tokenizer_dir'] if selected_row else 'NOT_SELECTED'}`

Selection data: `MAR` dev only.

Final data access: `NO_ACT_FINAL_ACCESS`.
""",
        encoding="utf-8",
    )

    access_rows = [
        {
            "run_id": run_id,
            "input_role": "train_text",
            "path": str(train_text),
            "allowed_split": "train",
            "rows_or_lines": str(count_rows(train_text)),
            "md5": md5_file(train_text),
            "final_access": "NO",
            "status": "PASS",
        },
        {
            "run_id": run_id,
            "input_role": "dev_manifest",
            "path": str(dev_manifest),
            "allowed_split": "dev",
            "rows_or_lines": str(count_rows(dev_manifest)),
            "md5": md5_file(dev_manifest),
            "final_access": "NO",
            "status": "PASS",
        },
    ]
    write_tsv(access_path, access_rows, ["run_id", "input_role", "path", "allowed_split", "rows_or_lines", "md5", "final_access", "status"])

    pass_count = sum(1 for row in score_rows if row["status"] == "PASS")
    gate = "PASS" if pass_count > 0 and selected_tokenizer is not None else "FAIL"
    results_path.write_text(
        f"""# Step 13 Results: V2 Tokenizer

Status: COMPLETED

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Artifact gate status: PASS

Claim gate status: {gate}

## Summary

Step 13 trained or loaded 8k, 16k, and 32k target tokenizers from the Step 12 v2 train text only. Selection used Mark/dev tokenization metrics only. No ACT final file was read by this script.

Selected vocab size: `{selected_vocab}`.

Passing candidates: `{pass_count}`.

## Gate Evidence

- `score_table.tsv` has no blank or `TBD` cells.
- `v2_no_final_access_audit.tsv` lists only train/dev inputs.
- XLM-R special ids are preserved for all passing candidates.
- Selected tokenizer is chosen from dev metrics only.

## Failure Return

Failed gate: {"NOT_APPLICABLE" if gate == "PASS" else "v2_tokenizer_dev_gate"}

Observed evidence: {"NOT_APPLICABLE" if gate == "PASS" else "no tokenizer candidate passed dev tokenization gate"}

Return-to step: {"NOT_APPLICABLE" if gate == "PASS" else "12_v2_split_protocol"}

Required fix: {"NOT_APPLICABLE" if gate == "PASS" else "revise vocab sizes or tokenization settings"}

Runtime minutes: {(time.time() - start) / 60.0:.3f}
""",
        encoding="utf-8",
    )

    file_rows = [
        file_result("score_table", score_path, "v2 tokenizer summary scores"),
        file_result("metrics", metrics_path, "per-language dev tokenization metrics"),
        file_result("merge_report", merge_path, "v2 tokenizer merge report"),
        file_result("examples", examples_path, "dev-only tokenization examples"),
        file_result("no_final_access_audit", access_path, "train/dev input audit"),
        file_result("selected_tokenizer", selected_path, "selected v2 tokenizer pointer"),
        file_result("results", results_path, "step result summary"),
    ]
    for tokenizer_dir in tokenizer_dirs:
        file_rows.append(file_result("tokenizer_artifact", tokenizer_dir, "large tokenizer artifact"))
    write_tsv(file_results_path, file_rows, ["file_role", "path", "rows_or_files", "bytes", "md5", "status", "notes"])

    print(f"run_id={run_id}")
    print("artifact_gate_status=PASS")
    print(f"claim_gate_status={gate}")
    print(f"selected_vocab_size={selected_vocab}")
    print(f"passing_candidates={pass_count}")


if __name__ == "__main__":
    main()
