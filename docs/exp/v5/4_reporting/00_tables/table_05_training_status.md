# Table 5. MLM Training Status

Last updated: 2026-06-27

Caption draft:

```text
The main initialization comparison requires matched continued MLM checkpoints.
The paired 10K run has been launched with identical data, tokenizer, schedule,
and checkpoint interval. `v5_random_mlm_10k` has produced its selected 10K
checkpoint, while `v5_fvt_mlm_10k` is still running.
```

| Run | Role | Status | Output path |
| --- | --- | --- | --- |
| `v5_random_mlm_10k` | random-resize baseline | selected 10K checkpoint exists; wrapper-ready | `/home/axt/mnt2/jongha/v5_glot50010/runs/v5_random_mlm_10k` |
| `v5_fvt_mlm_10k` | main initialization method | running; model file pending | `/home/axt/mnt2/jongha/v5_glot50010/runs/v5_fvt_mlm_10k` |

Shared settings:

| Setting | Value |
| --- | --- |
| train corpus | `/home/axt/mnt2/jongha/v5_glot50010/data/Glot500_v5_glot50010_xlmr100.txt` |
| tokenizer | `/home/axt/mnt2/jongha/v5_glot50010/tokenization/output/Glot500_extended_spm` |
| objective | MLM |
| max steps | 10,000 |
| save steps | 10,000 |
| max sequence length | 512 |
| learning rate | 5e-5 |
| GPUs | 2,3 |

Execution caveat:

The inherited training script preprocesses the full corpus before Trainer
optimization. That preprocessing barrier has been crossed for the paired
launcher transition; matched post-checkpoint evaluation still waits on
completion of `v5_fvt_mlm_10k`.

Source artifacts:

- `docs/exp/v5/2_training/README.md`
- `docs/exp/v5/2_training/01_random/README.md`
- `docs/exp/v5/2_training/02_fvt/README.md`
- `/home/axt/mnt2/jongha/v5_glot50010/runs/logs/train_v5_v5_random_mlm_10k_20260627_005616.log`
