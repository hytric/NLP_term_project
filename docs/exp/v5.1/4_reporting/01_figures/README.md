# v5.1 Reporting Figures

This folder stores figures intended for the report and PPT.

## Current Figures

| Figure | Source | Meaning |
| --- | --- | --- |
| `training_loss_lr.svg` | `docs/exp/v5.1/2_training/loss_history.tsv` | Live optimization trace for the active MLM run |

Regenerate through the standard live refresh:

```bash
bash scripts/refresh_v51_live_status.sh
```

The figure renderer can still be run directly when only the SVG needs to be
refreshed:

```bash
python3 scripts/render_v51_training_plots.py
```

Training curves are not final evidence for the method claim. Final claims must
come from held-out PPPL, downstream metrics, and similarity outputs after
checkpoint completion.
