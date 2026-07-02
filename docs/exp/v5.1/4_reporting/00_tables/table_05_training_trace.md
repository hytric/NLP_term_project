# Table 5. v5.1 Training Trace

Last synced from `docs/exp/v5.1/2_training/training_status.md`.

## Current Run

| Item | Value |
| --- | --- |
| Active run | `v51_strict5pct_random_mlm_3k` |
| Status | not_running |
| Latest checked step | 1869 / 3000 |
| Progress | 62.30% |
| ETA | 2026-06-29 00:28 KST |
| Checkpoint model file | pending |

## Observed Loss Rows

| Step | Loss | Learning rate | Epoch |
| ---: | ---: | ---: | ---: |
| 100 | 6.6875 | 4.843333e-05 | 0.06 |
| 200 | 4.7745 | 4.676667e-05 | 0.13 |
| 300 | 4.6070 | 4.51e-05 | 0.19 |
| 400 | 4.5278 | 4.343333e-05 | 0.25 |
| 500 | 4.4613 | 4.176667e-05 | 0.32 |
| 600 | 4.3998 | 4.01e-05 | 0.38 |
| 700 | 4.3640 | 3.843333e-05 | 0.45 |
| 800 | 4.3285 | 3.676667e-05 | 0.51 |
| 900 | 4.3007 | 3.51e-05 | 0.57 |
| 1000 | 4.2816 | 3.343333e-05 | 0.64 |
| 1100 | 4.2519 | 3.176667e-05 | 0.7 |
| 1200 | 4.2148 | 3.01e-05 | 0.76 |
| 1300 | 4.1905 | 2.843333e-05 | 0.83 |
| 1400 | 4.1590 | 2.676667e-05 | 0.89 |
| 1500 | 4.1401 | 2.51e-05 | 0.96 |
| 1600 | 4.1208 | 2.343333e-05 | 1.02 |
| 1700 | 4.0806 | 2.176667e-05 | 1.08 |
| 1800 | 4.0544 | 2.01e-05 | 1.15 |

## Reporting Rule

Training loss is an optimization trace only. It can be used to show that the
matched MLM run is progressing, but final claims must use held-out PPPL and
downstream/similarity outputs after checkpoint completion.
