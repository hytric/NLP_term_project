# Stage 05 Replay-Safe Retry Commands

작성일: 2026-06-13

## Rationale

The 200-step fvt pilot trains stably but fails the high-resource control proxy. This retry keeps the same XLM-R-base append-only tokenizer, fvt initialization, full-model MLM objective, and Stage 01 high-resource replay + target10 mixture. It changes only the optimization schedule:

- learning rate: `5e-5 -> 1e-5`
- steps: `200 -> 1000`
- warmup: `20 -> 100`
- save/eval cadence: every `250` steps

This is a replay-safe positive-claim retry, not a new main protocol.

## Seed 13 First Check

```bash
CUDA_VISIBLE_DEVICES=3 \
WANDB_DISABLED=true \
python3 modeling/run_third_try_stage05.py \
  docs/exp/third_try/05_mlm/training_config_replay_safe_seed13.json
```

## Full 3-Seed Grid

Run these only if seed 13 does not make the target10/control proxy worse.

```bash
CUDA_VISIBLE_DEVICES=3 \
WANDB_DISABLED=true \
python3 modeling/run_third_try_stage05.py \
  docs/exp/third_try/05_mlm/training_config_replay_safe_seed17.json
```

```bash
CUDA_VISIBLE_DEVICES=3 \
WANDB_DISABLED=true \
python3 modeling/run_third_try_stage05.py \
  docs/exp/third_try/05_mlm/training_config_replay_safe_seed23.json
```

## Gate

Promote this retry only if:

- target10 proxy is not worse than the 200-step fvt pilot;
- high-resource control delta is clearly smaller than the 200-step fvt pilot;
- downstream evaluation still keeps the final-test selection rule intact.
