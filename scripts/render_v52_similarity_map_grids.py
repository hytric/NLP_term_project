#!/usr/bin/env python3
"""Render v5.2 10k-50k similarity map grids from existing checkpoint PNGs."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Any


METHODS = ("random", "mean", "fvt", "weighted_fvt", "family_mean")
STEPS = (10000, 20000, 30000, 40000, 50000)
TARGET_LANGUAGES = ("dtp_Latn", "xav_Latn", "bam_Latn", "csb_Latn", "ile_Latn", "lij_Latn", "fur_Latn")
KEY_RE = re.compile(r"^v52_(random|mean|fvt|weighted_fvt|family_mean)_conv5way_step(\d+)$")

MAP_SPECS = {
    "tail7_by_language": "family_point_map_tail_by_language_{model_key}.png",
    "family39_all_tail_highlight": "family_point_map_all_tail_highlight_{model_key}.png",
}

for language in TARGET_LANGUAGES:
    MAP_SPECS[f"target_{language}"] = f"family_point_map_target_{language}_{{model_key}}.png"


def parse_csv_list(value: str) -> list[str]:
    return [item.strip() for chunk in value.split(",") for item in chunk.split() if item.strip()]


def write_tsv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


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


def model_key(method: str, step: int, fair_targets: dict[str, str]) -> str:
    if step == 50000 and method in fair_targets:
        return fair_targets[method]
    return f"v52_{method}_conv5way_step{step}"


def resolved_model(method: str, step: int, fair_targets: dict[str, str]) -> tuple[str, int]:
    key = model_key(method, step, fair_targets)
    match = KEY_RE.match(key)
    if match:
        return key, int(match.group(2))
    return key, step


def cell_label(label: str, display_step: int, local_step: int) -> str:
    if display_step == local_step:
        return label
    return f"{label}\nlocal {local_step}"


def image_path(root: Path, map_name: str, method: str, step: int, fair_targets: dict[str, str]) -> tuple[Path, str, int]:
    key, local_step = resolved_model(method, step, fair_targets)
    path = root / method / f"checkpoint-{local_step}" / "family_similarity" / MAP_SPECS[map_name].format(model_key=key)
    return path, key, local_step


def draw_grid(path: Path, cells: list[tuple[str, Path]], cols: int, title: str) -> None:
    import matplotlib.pyplot as plt

    rows = (len(cells) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4.2, rows * 3.3), squeeze=False)
    for ax in axes.ravel():
        ax.axis("off")
    for ax, (label, img_path) in zip(axes.ravel(), cells):
        ax.set_title(label, fontsize=10)
        if img_path.exists():
            image = plt.imread(img_path)
            ax.imshow(image)
        else:
            ax.text(0.5, 0.5, "missing", ha="center", va="center", fontsize=14)
            ax.text(0.5, 0.38, str(img_path), ha="center", va="center", fontsize=6, wrap=True)
    fig.suptitle(title, fontsize=14)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_summary_tables(
    root: Path,
    out_dir: Path,
    methods: list[str],
    steps: list[int],
    fair_targets: dict[str, str],
) -> None:
    rows = []
    target_keys: dict[str, int] = {}
    for method in methods:
        for step in steps:
            key, _ = resolved_model(method, step, fair_targets)
            target_keys[key] = step
    for row in read_tsv(root / "summary.tsv"):
        key = row.get("model_key", "")
        if row.get("method") not in methods or key not in target_keys:
            continue
        next_row = dict(row)
        next_row["display_step"] = str(target_keys[key])
        rows.append(next_row)
    fields = [
        "metric",
        "method",
        "display_step",
        "local_step",
        "model_key",
        "summary_type",
        "group",
        "pairs",
        "mean_cosine",
        "mean_centered_cosine",
        "source_file",
    ]
    write_tsv(out_dir / "similarity_10k50k_summary.tsv", rows, fields)
    lines = [
        "# v5.2 Similarity 10k-50k Summary",
        "",
        "Generated by `scripts/render_v52_similarity_map_grids.py`.",
        "",
        "| Metric | Method | Display step | Local step | Summary | Group | Pairs | Mean cosine | Mean centered cosine |",
        "| --- | --- | ---: | ---: | --- | --- | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| {metric} | {method} | {display_step} | {local_step} | {summary_type} | {group} | {pairs} | {mean_cosine} | {mean_centered_cosine} |".format(
                **row
            )
        )
    (out_dir / "similarity_10k50k_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="docs/exp/v5.2/3_evaluation/10_convergence_similarity")
    parser.add_argument("--out-dir", default="docs/exp/v5.2/3_evaluation/11_inference/similarity_maps")
    parser.add_argument("--methods", default=",".join(METHODS))
    parser.add_argument("--steps", default=",".join(str(step) for step in STEPS))
    parser.add_argument("--fair-targets", default="docs/exp/v5.2/3_evaluation/convergence_5way_fair_inference_targets.tsv")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root)
    out_dir = Path(args.out_dir)
    methods = parse_csv_list(args.methods)
    steps = [int(item) for item in parse_csv_list(args.steps)]
    fair_targets = fair_target_keys(Path(args.fair_targets))

    manifest: list[dict[str, Any]] = []
    for map_name in MAP_SPECS:
        for step in steps:
            cells = []
            for method in methods:
                path, key, local_step = image_path(root, map_name, method, step, fair_targets)
                cells.append((cell_label(method, step, local_step), path))
                manifest.append(
                    {
                        "map_set": map_name,
                        "grid_type": "step_by_methods",
                        "method": method,
                        "step": step,
                        "local_step": local_step,
                        "model_key": key,
                        "image_path": path,
                        "exists": "yes" if path.exists() else "no",
                    }
                )
            draw_grid(
                out_dir / map_name / f"{map_name}_step{step}_methods.png",
                cells,
                cols=len(methods),
                title=f"{map_name}: step {step} by init method",
            )

        for method in methods:
            cells = []
            for step in steps:
                path, key, local_step = image_path(root, map_name, method, step, fair_targets)
                cells.append((cell_label(f"{step}", step, local_step), path))
                manifest.append(
                    {
                        "map_set": map_name,
                        "grid_type": "method_by_steps",
                        "method": method,
                        "step": step,
                        "local_step": local_step,
                        "model_key": key,
                        "image_path": path,
                        "exists": "yes" if path.exists() else "no",
                    }
                )
            draw_grid(
                out_dir / map_name / f"{map_name}_{method}_steps.png",
                cells,
                cols=len(steps),
                title=f"{map_name}: {method} over 10k-50k",
            )

        all_cells = []
        for method in methods:
            for step in steps:
                path, _, local_step = image_path(root, map_name, method, step, fair_targets)
                all_cells.append((cell_label(f"{method}\n{step}", step, local_step), path))
        draw_grid(
            out_dir / map_name / f"{map_name}_all_methods_steps.png",
            all_cells,
            cols=len(steps),
            title=f"{map_name}: all init methods and 10k-50k checkpoints",
        )

    write_tsv(
        out_dir / "map_grid_manifest.tsv",
        manifest,
        ["map_set", "grid_type", "method", "step", "local_step", "model_key", "image_path", "exists"],
    )
    write_summary_tables(root, out_dir, methods, steps, fair_targets)
    print(f"wrote similarity map grids to {out_dir}")


if __name__ == "__main__":
    main()
