#!/usr/bin/env python3
"""Render v5.2 downstream inference tables for 5-way checkpoints."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from pathlib import Path
from statistics import mean
from typing import Any


METHODS = ("random", "mean", "fvt", "weighted_fvt", "family_mean")
STEPS = (10000, 20000, 30000, 40000, 50000)
TARGET7 = {"dtp_Latn", "xav_Latn", "bam_Latn", "csb_Latn", "ile_Latn", "lij_Latn", "fur_Latn"}

TASKS: dict[str, dict[str, Any]] = {
    "pppl": {
        "folder": "01_pseudoperplexity",
        "score_name": "weighted_pseudo_perplexity",
        "block_key": "weighted_pseudo_perplexity",
        "direction": "lower_is_better",
        "tail_languages": ("dtp_Latn", "xav_Latn", "bam_Latn", "csb_Latn", "ile_Latn", "lij_Latn", "fur_Latn"),
    },
    "retrieval_tatoeba": {
        "folder": "retrieval_tatoeba",
        "score_name": "top10_accuracy",
        "block_key": "Acc10",
        "direction": "higher_is_better",
        "tail_languages": ("csb_Latn", "dtp_Latn", "ile_Latn"),
    },
    "retrieval_bible": {
        "folder": "retrieval_bible",
        "score_name": "top10_accuracy",
        "block_key": "Acc10",
        "direction": "higher_is_better",
        "tail_languages": ("dtp_Latn", "xav_Latn", "bam_Latn"),
    },
    "roundtrip_alignment": {
        "folder": "roundtrip_alignment",
        "score_name": "accuracy",
        "block_key": "accuracy",
        "direction": "higher_is_better",
        "tail_languages": ("dtp_Latn", "xav_Latn", "bam_Latn"),
    },
    "ner": {
        "folder": "ner",
        "score_name": "f1",
        "block_key": "f1",
        "direction": "higher_is_better",
        "tail_languages": ("csb_Latn", "lij_Latn", "fur_Latn"),
    },
    "pos": {
        "folder": "pos",
        "score_name": "f1",
        "block_key": "f1",
        "direction": "higher_is_better",
        "tail_languages": ("xav_Latn", "bam_Latn", "lij_Latn"),
    },
    "text_classification": {
        "folder": "text_classification/taxi1500",
        "score_name": "macro_f1",
        "block_key": "macro_f1",
        "direction": "higher_is_better",
        "tail_languages": (),
    },
}


def parse_csv_list(value: str) -> list[str]:
    return [item.strip() for chunk in value.split(",") for item in chunk.split() if item.strip()]


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def ready_models(path: Path) -> set[str]:
    ready: set[str] = set()
    for row in read_tsv(path):
        if row.get("ready_for_wrapper") == "yes":
            ready.add(row.get("model_key", ""))
    return ready


def write_tsv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def fmt(value: float | None) -> str:
    if value is None or math.isnan(value) or math.isinf(value):
        return ""
    return f"{value:.6f}"


def fair_target_keys(path: Path) -> dict[str, str]:
    targets: dict[str, str] = {}
    for row in read_tsv(path):
        if row.get("comparison_group") != "exposure_aligned_50k":
            continue
        if row.get("ready_for_inference") != "yes":
            continue
        method = row.get("method", "")
        key = row.get("target_model_key", "")
        if method and key:
            targets[method] = key
    return targets


def model_key(method: str, step: int, conv5way: bool, fair_targets: dict[str, str]) -> str:
    if conv5way:
        if step == 50000 and method in fair_targets:
            return fair_targets[method]
        return f"v52_{method}_conv5way_step{step}"
    return f"v52_{method}_step{step}"


def coverage_lookup(eval_dir: Path, task: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for row in read_tsv(eval_dir / "00_coverage" / f"coverage_{task}.tsv"):
        lang = row.get("language_script") or row.get("language")
        group = row.get("group", "")
        if lang and group:
            out[lang] = "tail" if group == "v5_target" else group
    return out


def group_for_language(language: str, lookup: dict[str, str]) -> str:
    if language in TARGET7:
        return "tail"
    return lookup.get(language, "head")


def first_nonempty(paths: list[Path]) -> Path | None:
    for path in paths:
        if path.exists() and path.stat().st_size > 0:
            return path
    return None


def find_test_results(base: Path, model: str) -> Path | None:
    model_dir = base / model
    if not model_dir.exists():
        return None
    return first_nonempty([model_dir / "test_results.txt"] + sorted(model_dir.glob("*/test_results.txt")))


def parse_block_results(path: Path, score_key: str, aux_keys: tuple[str, ...] = ()) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    current: dict[str, Any] = {}
    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("="):
            continue
        if line.startswith("language="):
            if current.get("language"):
                rows.append(current)
            current = {"language": line.split("=", 1)[1].strip()}
            continue
        if "=" not in line or not current.get("language"):
            continue
        key, value = [part.strip() for part in line.split("=", 1)]
        if key == score_key or key in aux_keys:
            try:
                current[key] = float(value)
            except ValueError:
                current[key] = value
    if current.get("language"):
        rows.append(current)
    return rows


def collect_block_metric(
    eval_root: Path,
    eval_dir: Path,
    task: str,
    model: str,
) -> tuple[list[dict[str, Any]], str]:
    spec = TASKS[task]
    path = find_test_results(eval_root / spec["folder"], model)
    if path is None:
        return [], ""
    lookup = coverage_lookup(eval_dir, task)
    raw_rows = parse_block_results(path, spec["block_key"], ("Acc1", "Acc5", "precision", "recall", "loss"))
    rows: list[dict[str, Any]] = []
    for row in raw_rows:
        language = str(row.get("language", ""))
        value = row.get(spec["block_key"])
        if not isinstance(value, float):
            continue
        rows.append(
            {
                "language": language,
                "group": group_for_language(language, lookup),
                "score_value": value,
                "source_file": str(path),
            }
        )
    return rows, str(path)


def collect_roundtrip(eval_root: Path, eval_dir: Path, model: str) -> tuple[list[dict[str, Any]], str]:
    summary = eval_root / "roundtrip_alignment" / model / "summary.tsv"
    lookup = coverage_lookup(eval_dir, "roundtrip_alignment")
    rows: list[dict[str, Any]] = []
    if summary.exists() and summary.stat().st_size > 0:
        for row in read_tsv(summary):
            try:
                value = float(row["accuracy"])
            except (KeyError, ValueError):
                continue
            language = row.get("language", "")
            rows.append(
                {
                    "language": language,
                    "group": group_for_language(language, lookup),
                    "score_value": value,
                    "source_file": str(summary),
                }
            )
        return rows, str(summary)
    return collect_block_metric(eval_root, eval_dir, "roundtrip_alignment", model)


def collect_text_classification(eval_root: Path, model: str) -> tuple[list[dict[str, Any]], str]:
    path = eval_root / "text_classification" / "taxi1500" / model / "summary.json"
    if not path.exists() or path.stat().st_size == 0:
        return [], ""
    data = json.loads(path.read_text(encoding="utf-8"))
    test = data.get("test", {})
    try:
        value = float(test["macro_f1"])
    except (KeyError, TypeError, ValueError):
        return [], str(path)
    return (
        [
            {
                "language": "eng_Latn",
                "group": "head",
                "score_value": value,
                "source_file": str(path),
            }
        ],
        str(path),
    )


def collect_pppl(eval_dir: Path, model: str) -> tuple[list[dict[str, Any]], str]:
    path = eval_dir / "01_pseudoperplexity" / model / "scores.tsv"
    if not path.exists() or path.stat().st_size == 0:
        return [], ""
    rows: list[dict[str, Any]] = []
    for row in read_tsv(path):
        language = row.get("language_script", "")
        try:
            value = float(row["pseudo_perplexity"])
        except (KeyError, TypeError, ValueError):
            continue
        rows.append(
            {
                "language": language,
                "group": "tail" if language in TARGET7 else "head",
                "score_value": value,
                "source_file": str(path),
            }
        )
    return rows, str(path)


def collect_language_rows(eval_root: Path, eval_dir: Path, task: str, model: str) -> tuple[list[dict[str, Any]], str]:
    if task == "pppl":
        return collect_pppl(eval_dir, model)
    if task == "text_classification":
        return collect_text_classification(eval_root, model)
    if task == "roundtrip_alignment":
        return collect_roundtrip(eval_root, eval_dir, model)
    return collect_block_metric(eval_root, eval_dir, task, model)


def summarize_groups(
    task: str,
    method: str,
    step: int,
    model: str,
    language_rows: list[dict[str, Any]],
    source_file: str,
    empty_status: str = "pending",
) -> list[dict[str, Any]]:
    spec = TASKS[task]
    if task == "pppl":
        summary = Path(source_file).with_name("summary.tsv") if source_file else Path()
        summary_rows = {row.get("summary_group", ""): row for row in read_tsv(summary)}
        complete_group = summary_rows.get("v5_target") or summary_rows.get("all")
        out: list[dict[str, Any]] = []
        for group in ("head", "tail", "all"):
            if group == "head":
                out.append(
                    {
                        "metric": task,
                        "method": method,
                        "step": step,
                        "model_key": model,
                        "summary_group": group,
                        "score_name": spec["score_name"],
                        "score_value": "",
                        "languages": 0,
                        "expected_tail_languages": ",".join(spec["tail_languages"]),
                        "tail_languages_scored": "",
                        "direction": spec["direction"],
                        "status": "not_applicable" if language_rows else empty_status,
                        "source_file": str(summary) if summary else source_file,
                    }
                )
                continue
            if complete_group:
                score_value = complete_group.get(spec["score_name"], "")
                languages = complete_group.get("languages", "")
                status = "complete"
            else:
                score_value = ""
                languages = 0
                status = empty_status
            out.append(
                {
                    "metric": task,
                    "method": method,
                    "step": step,
                    "model_key": model,
                    "summary_group": group,
                    "score_name": spec["score_name"],
                    "score_value": score_value,
                    "languages": languages,
                    "expected_tail_languages": ",".join(spec["tail_languages"]),
                    "tail_languages_scored": ",".join(spec["tail_languages"]) if complete_group else "",
                    "direction": spec["direction"],
                    "status": status,
                    "source_file": str(summary) if summary else source_file,
                }
            )
        return out

    out: list[dict[str, Any]] = []
    expected_tail = set(spec["tail_languages"])
    groups = {
        "head": [row for row in language_rows if row["group"] == "head"],
        "tail": [row for row in language_rows if row["group"] == "tail"],
        "all": list(language_rows),
    }
    for group in ("head", "tail", "all"):
        values = [float(row["score_value"]) for row in groups[group]]
        present_tail = sorted({row["language"] for row in groups[group] if row["language"] in expected_tail})
        if values:
            status = "complete"
            if group in {"tail", "all"} and expected_tail and set(present_tail) != expected_tail:
                status = "partial"
        else:
            status = empty_status
        out.append(
            {
                "metric": task,
                "method": method,
                "step": step,
                "model_key": model,
                "summary_group": group,
                "score_name": spec["score_name"],
                "score_value": fmt(mean(values) if values else None),
                "languages": len(values),
                "expected_tail_languages": ",".join(spec["tail_languages"]),
                "tail_languages_scored": ",".join(present_tail),
                "direction": spec["direction"],
                "status": status,
                "source_file": source_file,
            }
        )
    return out


def add_pending_language_rows(
    rows: list[dict[str, Any]],
    task: str,
    method: str,
    step: int,
    model: str,
    status: str = "pending",
) -> None:
    for language in TASKS[task]["tail_languages"]:
        rows.append(
            {
                "metric": task,
                "method": method,
                "step": step,
                "model_key": model,
                "language": language,
                "group": "tail",
                "score_name": TASKS[task]["score_name"],
                "score_value": "",
                "status": status,
                "source_file": "",
            }
        )


def matrix_cell(row: dict[str, Any] | None) -> str:
    if row is None or row.get("status") != "complete":
        return ""
    return str(row.get("score_value", ""))


def all_matrix_rows(summary_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows_by_key = {
        (row["metric"], row["method"], str(row["step"])): row
        for row in summary_rows
        if row.get("summary_group") == "all"
    }
    metric_order = []
    method_order = []
    for row in summary_rows:
        metric = row.get("metric", "")
        method = row.get("method", "")
        if metric and metric not in metric_order:
            metric_order.append(metric)
        if method and method not in method_order:
            method_order.append(method)

    matrix: list[dict[str, Any]] = []
    for metric in metric_order:
        for method in method_order:
            first = next(
                (
                    row
                    for step in STEPS
                    for row in [rows_by_key.get((metric, method, str(step)))]
                    if row is not None
                ),
                {},
            )
            item = {
                "metric": metric,
                "method": method,
                "score_name": first.get("score_name", ""),
                "direction": first.get("direction", ""),
            }
            for step in STEPS:
                item[f"step_{step}"] = matrix_cell(rows_by_key.get((metric, method, str(step))))
            matrix.append(item)
    return matrix


def append_all_matrix(lines: list[str], summary_rows: list[dict[str, Any]]) -> None:
    lines.extend(
        [
            "## All Score Matrix",
            "",
            "Blank cells are not available yet.",
            "",
            "| Metric | Method | Score | Direction | 10k | 20k | 30k | 40k | 50k |",
            "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in all_matrix_rows(summary_rows):
        lines.append(
            "| {metric} | {method} | {score_name} | {direction} | {step_10000} | {step_20000} | {step_30000} | {step_40000} | {step_50000} |".format(
                **row
            )
        )
    lines.append("")


def render_md(path: Path, summary_rows: list[dict[str, Any]], language_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# v5.2 Downstream Inference Tables",
        "",
        "Generated by `scripts/render_v52_inference_tables.py`.",
        "",
        "Blank score cells mean the renderer did not find a non-empty local result file yet.",
        "",
    ]
    append_all_matrix(lines, summary_rows)
    lines.extend(
        [
        "## Head/Tail/All",
        "",
        "| Metric | Method | Step | Group | Score | Value | Langs | Status |",
        "| --- | --- | ---: | --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in summary_rows:
        lines.append(
            "| {metric} | {method} | {step} | {summary_group} | {score_name} | {score_value} | {languages} | {status} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Tail Language Rows",
            "",
            "| Metric | Method | Step | Language | Score | Value | Status |",
            "| --- | --- | ---: | --- | --- | ---: | --- |",
        ]
    )
    tail_rows = [row for row in language_rows if row.get("group") == "tail"]
    for row in tail_rows:
        lines.append(
            "| {metric} | {method} | {step} | {language} | {score_name} | {score_value} | {status} |".format(
                **row
            )
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-dir", default="docs/exp/v5.2/3_evaluation")
    parser.add_argument("--eval-root", default="/home/axt/mnt2/jongha/v5.2_glot5007/evaluation")
    parser.add_argument("--out-dir", default="docs/exp/v5.2/3_evaluation/11_inference")
    parser.add_argument("--model-matrix", default="docs/exp/v5.2/3_evaluation/model_matrix.tsv")
    parser.add_argument("--fair-targets", default="docs/exp/v5.2/3_evaluation/convergence_5way_fair_inference_targets.tsv")
    parser.add_argument("--methods", default=",".join(METHODS))
    parser.add_argument("--steps", default=",".join(str(step) for step in STEPS))
    parser.add_argument("--tasks", default=",".join(TASKS))
    parser.add_argument("--legacy-step-keys", action="store_true", help="Use v52_<method>_stepN keys instead of conv5way keys.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    eval_dir = Path(args.eval_dir)
    eval_root = Path(args.eval_root)
    out_dir = Path(args.out_dir)
    methods = parse_csv_list(args.methods)
    steps = [int(item) for item in parse_csv_list(args.steps)]
    tasks = parse_csv_list(args.tasks)
    conv5way = not args.legacy_step_keys
    available_models = ready_models(Path(args.model_matrix))
    fair_targets = fair_target_keys(Path(args.fair_targets)) if conv5way else {}

    summary_rows: list[dict[str, Any]] = []
    language_rows_out: list[dict[str, Any]] = []
    for task in tasks:
        if task not in TASKS:
            raise ValueError(f"unknown task: {task}")
        for method in methods:
            for step in steps:
                key = model_key(method, step, conv5way, fair_targets)
                rows, source = collect_language_rows(eval_root, eval_dir, task, key)
                empty_status = "pending" if key in available_models else "missing_model"
                if rows:
                    for row in rows:
                        language_rows_out.append(
                            {
                                "metric": task,
                                "method": method,
                                "step": step,
                                "model_key": key,
                                "language": row["language"],
                                "group": row["group"],
                                "score_name": TASKS[task]["score_name"],
                                "score_value": fmt(float(row["score_value"])),
                                "status": "complete",
                                "source_file": row["source_file"],
                            }
                        )
                else:
                    add_pending_language_rows(language_rows_out, task, method, step, key, empty_status)
                summary_rows.extend(summarize_groups(task, method, step, key, rows, source, empty_status))

    summary_fields = [
        "metric",
        "method",
        "step",
        "model_key",
        "summary_group",
        "score_name",
        "score_value",
        "languages",
        "expected_tail_languages",
        "tail_languages_scored",
        "direction",
        "status",
        "source_file",
    ]
    language_fields = [
        "metric",
        "method",
        "step",
        "model_key",
        "language",
        "group",
        "score_name",
        "score_value",
        "status",
        "source_file",
    ]
    write_tsv(out_dir / "downstream_head_tail_all.tsv", summary_rows, summary_fields)
    write_tsv(out_dir / "downstream_language_scores.tsv", language_rows_out, language_fields)
    write_tsv(
        out_dir / "downstream_all_matrix.tsv",
        all_matrix_rows(summary_rows),
        ["metric", "method", "score_name", "direction"] + [f"step_{step}" for step in STEPS],
    )
    render_md(out_dir / "downstream_tables.md", summary_rows, language_rows_out)
    print(f"wrote downstream inference tables to {out_dir}")


if __name__ == "__main__":
    main()
