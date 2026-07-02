# v5 Training Loss Snapshot

Last checked: 2026-06-28 18:08 KST

Verdict: `training_loss_snapshot_ready`

This file parses Trainer log loss rows for the paired 10K MLM run.
It is operational training evidence only. It does not unlock after-MLM
PPPL or downstream method claims; those remain gated by matched
`v5_random`/`v5_fvt` checkpoints and parsed evaluation rows.

## Summary

| Model | Status | Records | First step | Latest step | First loss | Latest loss | Delta | Min | Max |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `v5_random` | loss_rows_observed | 100 | 100 | 10000 | 6.6207 | 3.0720 | -3.5487 | 3.0720 | 6.6207 |
| `v5_fvt` | loss_rows_observed | 100 | 100 | 10000 | 5.1318 | 2.8113 | -2.3205 | 2.8110 | 5.1318 |

## Recent Rows

| Model | Step | Loss | Learning rate | Epoch |
| --- | ---: | ---: | ---: | ---: |
| `v5_fvt` | 8900 | 2.8195 | 0.00000553 | 0.5000 |
| `v5_fvt` | 9000 | 2.8256 | 0.00000503 | 0.5000 |
| `v5_fvt` | 9100 | 2.8208 | 0.00000452 | 0.5100 |
| `v5_fvt` | 9200 | 2.8110 | 0.00000403 | 0.5100 |
| `v5_fvt` | 9300 | 2.8112 | 0.00000352 | 0.5200 |
| `v5_fvt` | 9400 | 2.8188 | 0.00000303 | 0.5200 |
| `v5_fvt` | 9500 | 2.8182 | 0.00000253 | 0.5300 |
| `v5_fvt` | 9600 | 2.8191 | 0.00000203 | 0.5300 |
| `v5_fvt` | 9700 | 2.8120 | 0.00000153 | 0.5400 |
| `v5_fvt` | 9800 | 2.8127 | 0.00000103 | 0.5500 |
| `v5_fvt` | 9900 | 2.8200 | 0.00000053 | 0.5500 |
| `v5_fvt` | 10000 | 2.8113 | 0.00000003 | 0.5600 |

## Source Logs

- `v5_random`: `/home/axt/mnt2/jongha/v5_glot50010/runs/logs/train_v5_v5_random_mlm_10k_20260627_005616.log`
- `v5_fvt`: `/home/axt/mnt2/jongha/v5_glot50010/runs/logs/train_v5_v5_fvt_mlm_10k_20260627_203139.log`

Claim rule:

- Use this only to show that the paired MLM run is progressing.
- Do not copy training loss into final result tables as a PPPL/downstream metric.
- Final method claims still require `run_v5_post_checkpoint_evals.sh` outputs and aggregation.

Machine-readable TSV:

```text
training_loss_snapshot.tsv
```
