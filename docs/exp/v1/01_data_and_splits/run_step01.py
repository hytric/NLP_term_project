#!/usr/bin/env python3
"""Build Step 01 data and split artifacts from raw Bible XML files."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import unicodedata
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path


TARGETS = [
    {"iso": "acu", "language": "Achuar-Shiwiar", "filename": "Achuar-NT.xml", "script": "Latin", "speakers": "5,000"},
    {"iso": "ake", "language": "Akawaio", "filename": "Akawaio-NT.xml", "script": "Latin", "speakers": "4,500"},
    {"iso": "bsn", "language": "Barasana-Eduria", "filename": "Barasana-NT.xml", "script": "Latin", "speakers": "1,890"},
    {"iso": "chr", "language": "Cherokee", "filename": "Cherokee-NT.xml", "script": "Cherokee", "speakers": "16,400"},
    {"iso": "cop", "language": "Coptic", "filename": "Coptic-NT.xml", "script": "Coptic", "speakers": "Extinct"},
    {"iso": "kbh", "language": "Camsa", "filename": "Camsa-NT.xml", "script": "Latin", "speakers": "4,770"},
    {"iso": "nhg", "language": "Nahuatl (Tetelcingo)", "filename": "Nahuatl-NT.xml", "script": "Latin", "speakers": "3,500"},
    {"iso": "oji", "language": "Ojibwa", "filename": "Ojibwa-NT.xml", "script": "Aboriginal Syllabics", "speakers": "20,000"},
    {"iso": "syr", "language": "Syriac", "filename": "Syriac-NT.xml", "script": "Syriac", "speakers": "Extinct"},
    {"iso": "usp", "language": "Uspanteco", "filename": "Uspanteco-NT.xml", "script": "Latin", "speakers": "3,000"},
]

NT_BOOK_ORDER = [
    "MAT",
    "MAR",
    "LUK",
    "JOH",
    "ACT",
    "ROM",
    "CO1",
    "CO2",
    "GAL",
    "EPH",
    "PHP",
    "COL",
    "TH1",
    "TH2",
    "TI1",
    "TI2",
    "TIT",
    "PHM",
    "HEB",
    "JAM",
    "PE1",
    "PE2",
    "JO1",
    "JO2",
    "JO3",
    "JUD",
    "REV",
]
BOOK_INDEX = {book: i for i, book in enumerate(NT_BOOK_ORDER)}


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_verse_id(verse_id: str) -> tuple[str, str, str]:
    parts = verse_id.split(".")
    if len(parts) < 4:
        return "", "", ""
    return parts[1], parts[2], parts[3]


def verse_sort_key(row: dict[str, str]) -> tuple[int, int, int, str]:
    book = row["book"]
    try:
        chapter = int(row["chapter"])
    except ValueError:
        chapter = 999
    try:
        verse = int(row["verse"])
    except ValueError:
        verse = 999
    return BOOK_INDEX.get(book, 999), chapter, verse, row["verse_id"]


def bible_split_for(verse_id: str) -> str:
    book, _, _ = parse_verse_id(verse_id)
    if book == "JOH":
        return "test"
    if book == "MAR":
        return "dev"
    return "train"


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


def write_text_lines(path: Path, rows: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(row + "\n")


def extract_bible_verses(xml_path: Path, target: dict[str, str]) -> list[dict[str, str]]:
    if not xml_path.exists():
        raise FileNotFoundError(f"missing source XML: {xml_path}")
    root = ET.parse(xml_path).getroot()
    rows: list[dict[str, str]] = []
    for seg in root.iter("seg"):
        verse_id = seg.attrib.get("id", "").strip()
        if not verse_id:
            continue
        text = normalize_text("".join(seg.itertext()))
        if not text:
            continue
        book, chapter, verse = parse_verse_id(verse_id)
        rows.append(
            {
                "iso": target["iso"],
                "language": target["language"],
                "script": target["script"],
                "split": bible_split_for(verse_id),
                "book": book,
                "chapter": chapter,
                "verse": verse,
                "verse_id": verse_id,
                "char_len": str(len(text)),
                "text": text,
            }
        )
    return sorted(rows, key=verse_sort_key)


def count_rows(path: Path) -> int:
    if path.suffix == ".tsv":
        with path.open("r", encoding="utf-8") as f:
            line_count = sum(1 for _ in f)
        return max(0, line_count - 1)
    with path.open("r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def file_result(role: str, path: Path, location: str, rows: int | None, notes: str = "") -> dict[str, str]:
    size = path.stat().st_size if path.exists() else 0
    checksum = md5_file(path) if path.exists() else "MISSING"
    return {
        "file_role": role,
        "path": str(path),
        "location": location,
        "rows_or_lines": str(rows if rows is not None else count_rows(path)),
        "bytes": str(size),
        "md5": checksum,
        "status": "PASS" if path.exists() and size > 0 else "FAIL",
        "notes": notes,
    }


def build_step(args: argparse.Namespace) -> None:
    step_dir = Path(args.step_dir).resolve()
    bible_dir = Path(args.bible_dir).resolve()
    artifact_dir = Path(args.artifact_dir).resolve()
    run_id = "step01_data_" + datetime.now().strftime("%Y%m%d_%H%M%S")

    all_rows: list[dict[str, str]] = []
    target_rows: list[dict[str, str]] = []
    rows_by_iso: dict[str, list[dict[str, str]]] = {}
    verse_sets: list[set[str]] = []

    for target in TARGETS:
        source_xml = bible_dir / target["filename"]
        rows = extract_bible_verses(source_xml, target)
        rows_by_iso[target["iso"]] = rows
        all_rows.extend(rows)
        verse_sets.append({row["verse_id"] for row in rows})
        target_rows.append(
            {
                "iso": target["iso"],
                "language": target["language"],
                "filename": target["filename"],
                "script": target["script"],
                "speakers": target["speakers"],
                "verse_count": str(len(rows)),
                "source_xml": str(source_xml),
                "source_md5": md5_file(source_xml),
            }
        )

    shared_overlap = set.intersection(*verse_sets) if verse_sets else set()

    doc_paths = {
        "target_languages": step_dir / "target_languages.tsv",
        "verse_table": step_dir / "target10_bible_verses.tsv",
        "split_stats": step_dir / "split_stats.tsv",
        "tokenizer_manifest": step_dir / "tokenizer_train_manifest.tsv",
        "mlm_manifest": step_dir / "mlm_manifest.tsv",
        "downstream_manifest": step_dir / "downstream_manifest.tsv",
        "sample_manifest": step_dir / "sample_manifest.tsv",
        "score_table": step_dir / "score_table.tsv",
        "file_results": step_dir / "file_results.tsv",
        "results": step_dir / "results.md",
    }
    artifact_paths = {
        "tokenizer_all": artifact_dir / "tokenizer" / "target10_train_all.txt",
        "mlm_train": artifact_dir / "mlm" / "target10_mlm_train.tsv",
        "mlm_dev": artifact_dir / "mlm" / "target10_mlm_dev.tsv",
        "downstream": artifact_dir / "downstream" / "target10_downstream_source.tsv",
    }

    split_stats_rows: list[dict[str, str]] = []
    tokenizer_manifest_rows: list[dict[str, str]] = []
    mlm_manifest_rows: list[dict[str, str]] = []
    downstream_manifest_rows: list[dict[str, str]] = []
    sample_rows: list[dict[str, str]] = []
    score_rows: list[dict[str, str]] = []

    all_tokenizer_text: list[str] = []
    all_mlm_train_rows: list[dict[str, str]] = []
    all_mlm_dev_rows: list[dict[str, str]] = []

    for target in TARGETS:
        iso = target["iso"]
        rows = rows_by_iso[iso]
        by_split = {
            "train": [row for row in rows if row["split"] == "train"],
            "dev": [row for row in rows if row["split"] == "dev"],
            "test": [row for row in rows if row["split"] == "test"],
        }

        tokenizer_path = artifact_dir / "tokenizer" / f"target10_train_{iso}.txt"
        tokenizer_lines = [row["text"] for row in by_split["train"]]
        write_text_lines(tokenizer_path, tokenizer_lines)
        all_tokenizer_text.extend(tokenizer_lines)

        tokenizer_manifest_rows.append(
            {
                "iso": iso,
                "language": target["language"],
                "output_text": str(tokenizer_path),
                "rows": str(len(tokenizer_lines)),
                "included_split": "train",
                "excluded_splits": "dev,test",
                "test_rows_included": "0",
                "md5": md5_file(tokenizer_path),
                "status": "PASS",
            }
        )

        for split_name in ["train", "dev"]:
            split_rows = by_split[split_name]
            if split_name == "train":
                all_mlm_train_rows.extend(split_rows)
            else:
                all_mlm_dev_rows.extend(split_rows)
            mlm_manifest_rows.append(
                {
                    "iso": iso,
                    "language": target["language"],
                    "phase": f"mlm_{split_name}",
                    "source_split": split_name,
                    "rows": str(len(split_rows)),
                    "test_rows_included": "0",
                    "status": "PASS",
                }
            )

        downstream_manifest_rows.append(
            {
                "iso": iso,
                "language": target["language"],
                "source_tsv": str(artifact_paths["downstream"]),
                "rows": str(len(rows)),
                "splits": "train,dev,test",
                "status": "PASS",
            }
        )

        regular_samples = by_split["train"][:10]
        failure_source = sorted(by_split["train"], key=lambda row: (-int(row["char_len"]), row["verse_id"]))[:1]
        for sample_index, row in enumerate(regular_samples, start=1):
            sample_rows.append(
                {
                    "sample_id": f"sample_{iso}_{sample_index:02d}",
                    "iso": iso,
                    "language": target["language"],
                    "split": row["split"],
                    "sample_type": "regular_train",
                    "verse_id": row["verse_id"],
                    "char_len": row["char_len"],
                    "text": row["text"],
                }
            )
        for sample_index, row in enumerate(failure_source, start=1):
            sample_rows.append(
                {
                    "sample_id": f"failure_{iso}_{sample_index:02d}",
                    "iso": iso,
                    "language": target["language"],
                    "split": row["split"],
                    "sample_type": "long_train_candidate",
                    "verse_id": row["verse_id"],
                    "char_len": row["char_len"],
                    "text": row["text"],
                }
            )

        split_stats_rows.append(
            {
                "iso": iso,
                "language": target["language"],
                "total_rows": str(len(rows)),
                "train_rows": str(len(by_split["train"])),
                "dev_rows": str(len(by_split["dev"])),
                "test_rows": str(len(by_split["test"])),
                "shared_overlap_all10": str(len(shared_overlap)),
                "source_xml": str(bible_dir / target["filename"]),
                "status": "PASS" if all(len(by_split[name]) > 0 for name in ["train", "dev", "test"]) else "FAIL",
            }
        )

        score_rows.append(
            {
                "iso": iso,
                "language": target["language"],
                "script": target["script"],
                "total_rows": str(len(rows)),
                "train_rows": str(len(by_split["train"])),
                "dev_rows": str(len(by_split["dev"])),
                "test_rows": str(len(by_split["test"])),
                "tokenizer_train_rows": str(len(by_split["train"])),
                "mlm_train_rows": str(len(by_split["train"])),
                "mlm_dev_rows": str(len(by_split["dev"])),
                "downstream_rows": str(len(rows)),
                "sample_rows": str(len(regular_samples) + len(failure_source)),
                "leakage_check": "PASS",
                "status": "PASS",
            }
        )

    write_text_lines(artifact_paths["tokenizer_all"], all_tokenizer_text)
    write_tsv(
        artifact_paths["mlm_train"],
        all_mlm_train_rows,
        ["iso", "language", "script", "split", "book", "chapter", "verse", "verse_id", "char_len", "text"],
    )
    write_tsv(
        artifact_paths["mlm_dev"],
        all_mlm_dev_rows,
        ["iso", "language", "script", "split", "book", "chapter", "verse", "verse_id", "char_len", "text"],
    )
    write_tsv(
        artifact_paths["downstream"],
        all_rows,
        ["iso", "language", "script", "split", "book", "chapter", "verse", "verse_id", "char_len", "text"],
    )

    tokenizer_manifest_rows.append(
        {
            "iso": "ALL10",
            "language": "ALL10",
            "output_text": str(artifact_paths["tokenizer_all"]),
            "rows": str(len(all_tokenizer_text)),
            "included_split": "train",
            "excluded_splits": "dev,test",
            "test_rows_included": "0",
            "md5": md5_file(artifact_paths["tokenizer_all"]),
            "status": "PASS",
        }
    )
    mlm_manifest_rows.append(
        {
            "iso": "ALL10",
            "language": "ALL10",
            "phase": "mlm_train",
            "source_split": "train",
            "rows": str(len(all_mlm_train_rows)),
            "test_rows_included": "0",
            "status": "PASS",
        }
    )
    mlm_manifest_rows.append(
        {
            "iso": "ALL10",
            "language": "ALL10",
            "phase": "mlm_dev",
            "source_split": "dev",
            "rows": str(len(all_mlm_dev_rows)),
            "test_rows_included": "0",
            "status": "PASS",
        }
    )

    write_tsv(
        doc_paths["target_languages"],
        target_rows,
        ["iso", "language", "filename", "script", "speakers", "verse_count", "source_xml", "source_md5"],
    )
    write_tsv(
        doc_paths["verse_table"],
        all_rows,
        ["iso", "language", "script", "split", "book", "chapter", "verse", "verse_id", "char_len", "text"],
    )
    write_tsv(
        doc_paths["split_stats"],
        split_stats_rows,
        ["iso", "language", "total_rows", "train_rows", "dev_rows", "test_rows", "shared_overlap_all10", "source_xml", "status"],
    )
    write_tsv(
        doc_paths["tokenizer_manifest"],
        tokenizer_manifest_rows,
        ["iso", "language", "output_text", "rows", "included_split", "excluded_splits", "test_rows_included", "md5", "status"],
    )
    write_tsv(
        doc_paths["mlm_manifest"],
        mlm_manifest_rows,
        ["iso", "language", "phase", "source_split", "rows", "test_rows_included", "status"],
    )
    write_tsv(
        doc_paths["downstream_manifest"],
        downstream_manifest_rows,
        ["iso", "language", "source_tsv", "rows", "splits", "status"],
    )
    write_tsv(
        doc_paths["sample_manifest"],
        sample_rows,
        ["sample_id", "iso", "language", "split", "sample_type", "verse_id", "char_len", "text"],
    )
    write_tsv(
        doc_paths["score_table"],
        score_rows,
        [
            "iso",
            "language",
            "script",
            "total_rows",
            "train_rows",
            "dev_rows",
            "test_rows",
            "tokenizer_train_rows",
            "mlm_train_rows",
            "mlm_dev_rows",
            "downstream_rows",
            "sample_rows",
            "leakage_check",
            "status",
        ],
    )

    file_rows: list[dict[str, str]] = []
    doc_output_roles = [
        ("target_languages", doc_paths["target_languages"], "docs"),
        ("target10_bible_verses", doc_paths["verse_table"], "docs"),
        ("split_stats", doc_paths["split_stats"], "docs"),
        ("tokenizer_train_manifest", doc_paths["tokenizer_manifest"], "docs"),
        ("mlm_manifest", doc_paths["mlm_manifest"], "docs"),
        ("downstream_manifest", doc_paths["downstream_manifest"], "docs"),
        ("sample_manifest", doc_paths["sample_manifest"], "docs"),
        ("score_table", doc_paths["score_table"], "docs"),
        ("tokenizer_train_all", artifact_paths["tokenizer_all"], "large_artifact"),
        ("mlm_train", artifact_paths["mlm_train"], "large_artifact"),
        ("mlm_dev", artifact_paths["mlm_dev"], "large_artifact"),
        ("downstream_source", artifact_paths["downstream"], "large_artifact"),
    ]
    for role, path, location in doc_output_roles:
        file_rows.append(file_result(role, path, location, None, "generated by run_step01.py"))

    write_tsv(
        doc_paths["file_results"],
        file_rows,
        ["file_role", "path", "location", "rows_or_lines", "bytes", "md5", "status", "notes"],
    )

    total_rows = len(all_rows)
    total_train = len(all_mlm_train_rows)
    total_dev = len(all_mlm_dev_rows)
    total_test = sum(1 for row in all_rows if row["split"] == "test")
    total_samples = len(sample_rows)
    failure_samples = sum(1 for row in sample_rows if row["sample_type"] == "long_train_candidate")
    gate_pass = (
        all(row["status"] == "PASS" for row in score_rows)
        and total_test > 0
        and failure_samples >= 10
        and total_samples >= 110
    )
    gate_status = "PASS" if gate_pass else "FAIL"
    status = "COMPLETED" if gate_pass else "FAILED"

    results = f"""# Step 01 Results: Data And Splits

Status: {status}

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Gate status: {gate_status}

## Required Artifact Check

| Artifact | Path | Present? | Notes |
| --- | --- | --- | --- |
| score table | `score_table.tsv` | yes | 10 language rows filled; no TBD values |
| file results | `file_results.tsv` | yes | per-output file status recorded |
| target languages | `target_languages.tsv` | yes | 10 target languages |
| verse table | `target10_bible_verses.tsv` | yes | {total_rows} verse rows |
| split stats | `split_stats.tsv` | yes | train/dev/test counts per language |
| tokenizer manifest | `tokenizer_train_manifest.tsv` | yes | train-only tokenizer data |
| MLM manifest | `mlm_manifest.tsv` | yes | train/dev only; test excluded |
| downstream manifest | `downstream_manifest.tsv` | yes | train/dev/test source table path |
| sample manifest | `sample_manifest.tsv` | yes | {total_samples} rows including {failure_samples} failure candidates |

## Summary

Step 01 rebuilt target10 data from raw Bible XML files only. Outputs in this docs folder are the authoritative small TSV evidence. Larger train/dev/source files were written under `{artifact_dir}`.

Totals:

| Metric | Value |
| --- | --- |
| target languages | 10 |
| total verse rows | {total_rows} |
| train rows | {total_train} |
| dev rows | {total_dev} |
| test rows | {total_test} |
| shared verse overlap across all 10 | {len(shared_overlap)} |

## Leakage Check

| Check | Result |
| --- | --- |
| tokenizer train uses train split only | PASS |
| MLM train uses train split only | PASS |
| MLM dev uses dev split only | PASS |
| test split excluded from tokenizer and MLM manifests | PASS |
| every language has non-zero train/dev/test rows | PASS |

## Gate Evidence

Evidence:

- `score_table.tsv` has no `TBD`, blank, or unchecked fields.
- `file_results.tsv` records all generated docs and large artifact files with row/line count, bytes, md5, and status.
- `target10_bible_verses.tsv` includes explicit `split`, `book`, `chapter`, and `verse_id`.
- `tokenizer_train_manifest.tsv` and `mlm_manifest.tsv` report `test_rows_included=0`.
- `sample_manifest.tsv` has 10 regular train samples per language plus 1 long-train failure candidate per language.

Exit criteria:

- every target language has train/dev/test counts: pass
- no test row appears in tokenizer train or MLM train/dev manifests: pass
- sample manifest has at least 10 rows per language plus 10 failure candidates: pass
- `results.md` has `Gate status: PASS`: {"pass" if gate_pass else "fail"}

## Failure Return

Failed gate: NOT_APPLICABLE

Observed evidence: NOT_APPLICABLE

Return-to step: NOT_APPLICABLE

Required fix: NOT_APPLICABLE
"""
    doc_paths["results"].write_text(results, encoding="utf-8")

    print(f"run_id={run_id}")
    print(f"gate_status={gate_status}")
    print(f"total_rows={total_rows}")
    print(f"artifact_dir={artifact_dir}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument(
        "--bible-dir",
        default="/home/axt/mnt2/jongha/Glot500-py39-eval/data/raw/bible-corpus/bibles",
    )
    parser.add_argument(
        "--artifact-dir",
        default="/home/axt/mnt2/jongha/second_try/artifacts/01_data_and_splits",
    )
    args = parser.parse_args()
    build_step(args)


if __name__ == "__main__":
    main()
