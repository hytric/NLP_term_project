# Stage 05 Training Command

작성일: 2026-06-13

## Smoke Test

Run this before the pilot to verify loader, tokenizer/model shapes, CUDA visibility, fp16, Trainer, and output writing.

```bash
CUDA_VISIBLE_DEVICES=3 \
WANDB_DISABLED=true \
python3 modeling/run_third_try_stage05.py \
  docs/exp/third_try/05_mlm/training_config_smoke.json
```

## First Pilot

The first real Stage 05 pilot starts from the Stage 04 `fvt` checkpoint. This is not the final 3-seed claim run.

```bash
CUDA_VISIBLE_DEVICES=3 \
WANDB_DISABLED=true \
python3 modeling/run_third_try_stage05.py \
  docs/exp/third_try/05_mlm/training_config.json
```

## Pilot Seed Grid

Seed 17:

```bash
CUDA_VISIBLE_DEVICES=3 \
WANDB_DISABLED=true \
python3 modeling/run_third_try_stage05.py \
  docs/exp/third_try/05_mlm/training_config_seed17.json
```

Seed 23:

```bash
CUDA_VISIBLE_DEVICES=3 \
WANDB_DISABLED=true \
python3 modeling/run_third_try_stage05.py \
  docs/exp/third_try/05_mlm/training_config_seed23.json
```

## Inputs

| Item | Path |
| --- | --- |
| init checkpoint | `/home/axt/mnt2/jongha/third_try/checkpoints/04_init/xlmr_v2_48000_fvt` |
| train file | `/home/axt/mnt2/jongha/third_try/text/stage01_20260613_r1/mlm_train_full_mixture.txt` |
| validation file | `/home/axt/mnt2/jongha/third_try/text/stage01_20260613_r1/target10_dev.txt` |
| pilot output | `/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed13_pilot` |
| seed17 pilot output | `/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed17_pilot` |
| seed23 pilot output | `/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed23_pilot` |

## Claim Boundary

The pilot can only check training viability. A positive model claim still requires a final candidate with at least 3 seeds and Stage 06 downstream evidence.
