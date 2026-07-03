# v5.2 5-Way Loss Curve

Updated: `2026-07-03 00:20:07`

![v5.2 convergence loss curve](convergence_5way_loss_curve.png)

## Latest Loss

| Method | Latest step | Latest loss | Points |
| --- | ---: | ---: | ---: |
| random | 5 | 3.1664 | 42 |
| mean | 5 | 3.3209 | 45 |
| fvt | 6 | 2.8044 | 50 |
| weighted_fvt | 5 | 2.7254 | 50 |
| family_mean | 5 | 2.9140 | 50 |

Notes:

- The plot is drawn from the curated loss-curve TSV, not re-derived from the checkpoint index.
- If the TSV contains `display_step`/`display_loss`, those presentation values are used.
- Otherwise the x-axis uses `exposure_aligned_step` first, then falls back to `local_step`.
- Curve TSV: `convergence_5way_loss_curve.tsv`
