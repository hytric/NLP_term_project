# v5.1 Training Status

Last checked: 2026-06-28 21:56:49 KST

Verdict: `not_running`

This file answers whether the live v5.1 MLM run is following the intended
optimizer, learning-rate, batch-size, and sequence-length settings.

## Current Run

| Item | Value |
| --- | --- |
| run | `v51_strict5pct_random_mlm_3k` |
| status | `not_running` |
| latest step | `1869/3000` |
| progress | `62.30%` |
| remaining steps | `1131` |
| seconds / step | `8.06` |
| ETA remaining | `2:31:56` |
| ETA at | `2026-06-29 00:28 KST` |
| launcher PID | `` |
| trainer PID | `` |
| log | `/home/axt/mnt2/jongha/v5_1_glot50010/runs/logs/train_v5_v51_strict5pct_random_mlm_3k_20260628_182508.log` |

## Confirmed Training Configuration

| Field | Expected | Observed | Status | Evidence |
| --- | --- | --- | --- | --- |
| optimizer | `AdamW` | `AdamW` | `ok` | `transformers/optimization.py` AdamW warning in trainer log |
| learning_rate | `initial=5e-5` | `initial=; latest=2.01e-05` | `check` | `--learning_rate 5e-5`; live LR is scheduler value |
| adam_beta1 | `0.9` | `` | `check` | `--adam_beta1` command argument |
| adam_beta2 | `0.999` | `` | `check` | `--adam_beta2` command argument |
| per_device_batch | `8` | `` | `check` | `--per_device_train_batch_size` command argument |
| gpu_count | `3` | `3` | `ok` | `CUDA_VISIBLE_DEVICES=0,1,3` |
| gradient_accumulation | `16` | `` | `check` | `--gradient_accumulation_steps` command argument |
| effective_batch | `384` | `384` | `ok` | 8 per-device x 3 GPUs x 16 grad accumulation |
| sequence_length | `512` | `` | `check` | `--max_seq_length` command argument |
| max_steps | `3000` | `3000` | `ok` | `--max_steps` command argument |
| fp16 | `True` | `` | `check` | `--fp16` command argument |

## GPU Snapshot

| GPU | Role | Memory | GPU util | Memory util | Power |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0 | v5.1_mlm_training | 1842 / 49140 MB (3.7%) | 0% | 0% | 95.39 / 300.00 W |
| 1 | v5.1_mlm_training | 2144 / 49140 MB (4.4%) | 0% | 0% | 19.40 / 300.00 W |
| 2 | other_process_or_available | 11 / 49140 MB (0.0%) | 0% | 0% | 20.47 / 300.00 W |
| 3 | v5.1_mlm_training | 124 / 49140 MB (0.3%) | 0% | 0% | 24.42 / 300.00 W |

## Recent Loss Rows

| Step | Loss | Learning rate | Epoch |
| ---: | ---: | ---: | ---: |
| 700 | 4.364 | 3.8433333e-05 | 0.45 |
| 800 | 4.3285 | 3.6766667e-05 | 0.51 |
| 900 | 4.3007 | 3.51e-05 | 0.57 |
| 1000 | 4.2816 | 3.3433333e-05 | 0.64 |
| 1100 | 4.2519 | 3.1766667e-05 | 0.7 |
| 1200 | 4.2148 | 3.01e-05 | 0.76 |
| 1300 | 4.1905 | 2.8433333e-05 | 0.83 |
| 1400 | 4.159 | 2.6766667e-05 | 0.89 |
| 1500 | 4.1401 | 2.51e-05 | 0.96 |
| 1600 | 4.1208 | 2.3433333e-05 | 1.02 |
| 1700 | 4.0806 | 2.1766667e-05 | 1.08 |
| 1800 | 4.0544 | 2.01e-05 | 1.15 |

## Interpretation

- The optimizer is AdamW from Hugging Face Transformers Trainer, not plain Adam.
- The configured initial learning rate is 5e-5; the live learning rate decays during training.
- Effective batch size is per-device batch times GPU count times gradient accumulation.
- Sequence length is set by `--max_seq_length 512`.
- Training loss is operational evidence only; final metrics must come from held-out PPPL and post-checkpoint evaluations.

Machine-readable files:

```text
training_status.tsv
training_config.tsv
gpu_snapshot.tsv
loss_history.tsv
```
