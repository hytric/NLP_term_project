# Stage 05 Results: Multilingual Continued Pretraining

작성일: 2026-06-13

Gate status: PASS_DIAGNOSTIC_READY

## Summary

Stage 05 launch artifacts are prepared. The one-step smoke test using the Stage 04 `fvt` checkpoint and GPU 3 passed.

The 200-step `fvt` pilot grid completed on GPU 3 for seeds 13, 17, and 23. After Stage 06 showed high-resource control degradation, a lower-LR replay-safe 1000-step retry was run for the same three seeds. This replay-safe candidate is the strongest compute-bounded Stage 05 model family now available.

No positive model claim is allowed from this stage alone. The replay-safe checkpoints support Stage 06/07 diagnostic evaluation, but they do not satisfy a full Glot500 training-budget reproduction claim.

## Prepared Inputs

| Item | Path |
| --- | --- |
| selected init checkpoint | `/home/axt/mnt2/jongha/third_try/checkpoints/04_init/xlmr_v2_48000_fvt` |
| full mixture train text | `/home/axt/mnt2/jongha/third_try/text/stage01_20260613_r1/mlm_train_full_mixture.txt` |
| dev text | `/home/axt/mnt2/jongha/third_try/text/stage01_20260613_r1/target10_dev.txt` |
| smoke config | `training_config_smoke.json` |
| seed13 pilot config | `training_config.json` |
| seed17 pilot config | `training_config_seed17.json` |
| seed23 pilot config | `training_config_seed23.json` |
| command doc | `training_command.md` |
| deviation audit | `deviation_from_protocol.tsv` |

## Smoke Test

| Metric | Value |
| --- | ---: |
| train loss | 7.336768 |
| eval loss | 8.1263 |
| perplexity | 3382.426 |
| train samples | 16 |
| eval samples | 8 |

Smoke output:

`/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/smoke_fvt_seed13`

## FVT 200-Step Pilot Grid

Seed-13 command:

```bash
CUDA_VISIBLE_DEVICES=3 \
WANDB_DISABLED=true \
python3 modeling/run_third_try_stage05.py \
  docs/exp/third_try/05_mlm/training_config.json
```

Seed-17/23 commands are recorded in `training_command.md`.

Outputs:

- `/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed13_pilot`
- `/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed17_pilot`
- `/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed23_pilot`

| Run | Seed | Train loss | Final eval loss | Final perplexity | Runtime sec |
| --- | ---: | ---: | ---: | ---: | ---: |
| fvt_seed13_pilot | 13 | 2.748325 | 3.921798 | 50.491170 | 273.2767 |
| fvt_seed17_pilot | 17 | 2.666244 | 4.010451 | 55.171739 | 273.8569 |
| fvt_seed23_pilot | 23 | 2.594898 | 4.011500 | 55.229646 | 275.4349 |
| mean | NA | NA | 3.981250 | 53.630852 | NA |
| range | NA | NA | 0.089701 | 4.738477 | NA |

Seed-13 checkpoint/eval trace:

| Step | Eval loss | Perplexity |
| ---: | ---: | ---: |
| 50 | 4.343924 | 77.009135 |
| 100 | 4.097365 | 60.181494 |
| 150 | 4.045814 | 57.157696 |
| 200 trainer-loop eval | 3.993953 | 54.269004 |
| final eval_results.json | 3.921798 | 50.491170 |

Interpretation:

- The pilot grid is a viable training run: all three seeds completed, checkpoints were saved, and each scheduled eval curve decreased over training.
- This supports only MLM training stability at 200 steps. It does not prove downstream improvement.
- The next Stage 05 gate is a final budget decision: either promote the 200-step checkpoints to Stage 06 pilot evaluation, or extend training before Stage 06.

## Replay-Safe 1000-Step Retry

After Stage 06 showed high-resource control degradation, a lower-LR retry was run with the same Stage 04 `fvt` initialization, same append-only tokenizer, same Stage 01 high-resource replay + target10 mixture, and full-model MLM objective. The retry changes only the optimization schedule: learning rate `5e-5 -> 1e-5`, max steps `200 -> 1000`, and warmup `20 -> 100`.

Outputs:

- `/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_replay_safe_lr1e5_seed13_step1000`
- `/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_replay_safe_lr1e5_seed17_step1000`
- `/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_replay_safe_lr1e5_seed23_step1000`

| Run | Seed | Train loss | Final eval loss | Final perplexity | Runtime sec |
| --- | ---: | ---: | ---: | ---: | ---: |
| fvt replay-safe | 13 | 2.407281 | 3.875830 | 48.222692 | 1157.6308 |
| fvt replay-safe | 17 | 2.383752 | 3.898863 | 49.346314 | 1161.1711 |
| fvt replay-safe | 23 | 2.378278 | 3.934743 | 51.149024 | 1159.3877 |
| mean | NA | 2.389771 | 3.903145 | 49.572677 | 1159.3965 |
| range | NA | 0.029003 | 0.058914 | 2.926332 | 3.5403 |

Interpretation:

- The replay-safe retry improves Stage 05 target10 dev MLM loss over the 200-step fvt pilot mean (`3.903145` vs `3.981250`).
- It is now a stronger 3-seed candidate for Stage 06 evaluation.
- It is still compute-bounded and does not by itself satisfy the full Glot500 training-budget claim.

## Current Decision

`REPLAY_SAFE_1000_STEP_3SEED_COMPLETE_DIAGNOSTIC_READY`

## Next Commands

No immediate Stage 05 command is required for the diagnostic report package.

If pursuing a positive model claim, return here with a stronger replay/control schedule or a larger training budget, keep `CUDA_VISIBLE_DEVICES=3`, preserve 3+ seeds, and rerun Stage 06 high-resource control plus target10 downstream/proxy evaluation.

Original pilot command:

```bash
CUDA_VISIBLE_DEVICES=3 \
WANDB_DISABLED=true \
python3 modeling/run_third_try_stage05.py \
  docs/exp/third_try/05_mlm/training_config.json
```

## Failure Return

- failed gate: NOT_APPLICABLE_YET
- observed evidence: launch files prepared; smoke test passed; 200-step fvt pilot grid passed; replay-safe 1000-step fvt retry passed for seeds 13, 17, and 23
- likely cause: NOT_APPLICABLE_YET
- return-to stage: NOT_APPLICABLE_YET
- required fix before retry: NOT_APPLICABLE for diagnostic report; positive retry requires stronger replay/full-budget evidence and Stage 06 rescue
