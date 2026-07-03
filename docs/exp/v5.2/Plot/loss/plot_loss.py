#!/usr/bin/env python3
from pathlib import Path
import csv

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Edit here.
TSV = Path(__file__).with_name("convergence_5way_loss_curve.tsv")
OUT = Path(__file__).with_name("convergence_5way_loss_curve.png")
X_COL = "step"
Y_COL = "loss"
TITLE = ""      # "5-Init method MLM Loss"
X_LABEL = "Training step"
Y_LABEL = "MLM loss"
FIGSIZE = (12, 6.2)
DPI = 180
X_LIM = None
Y_LIM = None
SHOW_GRID = True
SHOW_LEGEND = True

METHOD_ORDER = ["family_mean", "weighted_fvt", "fvt", "mean", "random"]
LABEL = {
    "random": "Random init",
    "mean": "Mean init",
    "fvt": "FVT init",
    "weighted_fvt": "Weighted FVT",
    "family_mean": "Family-aware mean",
}
COLOR = {
    "random": "#666666",
    "mean": "#1f77b4",
    "fvt": "#2ca02c",
    "weighted_fvt": "#9467bd",
    "family_mean": "#d62728",
}
MARKER = {
    "random": "o",
    "mean": "o",
    "fvt": "o",
    "weighted_fvt": "o",
    "family_mean": "o",
}
LINESTYLE = {
    "random": "-",
    "mean": "-",
    "fvt": "-",
    "weighted_fvt": "-",
    "family_mean": "-",
}


def load_rows(path):
    rows = {}
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            method = row["method"]
            rows.setdefault(method, []).append((float(row[X_COL]), float(row[Y_COL])))
    for method in rows:
        rows[method].sort()
    return rows


def main():
    rows = load_rows(TSV)
    fig, ax = plt.subplots(figsize=FIGSIZE)

    for method in METHOD_ORDER:
        points = rows.get(method)
        if not points:
            continue
        xs, ys = zip(*points)
        ax.plot(
            xs,
            ys,
            label=LABEL.get(method, method),
            color=COLOR.get(method),
            marker=MARKER.get(method, "o"),
            linestyle=LINESTYLE.get(method, "-"),
            linewidth=2.0,
            markersize=4.5,
            alpha=0.95,
        )

    ax.set_title(TITLE)
    ax.set_xlabel(X_LABEL)
    ax.set_ylabel(Y_LABEL)
    if X_LIM:
        ax.set_xlim(*X_LIM)
    if Y_LIM:
        ax.set_ylim(*Y_LIM)
    if SHOW_GRID:
        ax.grid(True, alpha=0.24)
    if SHOW_LEGEND:
        ax.legend(loc="upper right", ncol=2, fontsize=9)

    fig.tight_layout()
    fig.savefig(OUT, dpi=DPI)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
