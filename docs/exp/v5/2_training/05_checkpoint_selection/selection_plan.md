# v5 Checkpoint Selection Plan

Last updated: 2026-06-27

This file freezes the downstream checkpoint-selection rule before downstream
results are inspected.

## Required Models

| Model key | Selection rule | Expected path |
| --- | --- | --- |
| `xlmr_base` | fixed external baseline | `xlm-roberta-base` |
| `glot500_base` | fixed external reference | `cis-lmu/glot500-base` |
| `v5_random` | final model from the matched 10K full-corpus run | `/home/axt/mnt2/jongha/v5_glot50010/runs/v5_random_mlm_10k` or its complete `checkpoint-10000` fallback |
| `v5_fvt` | final model from the matched 10K full-corpus run | `/home/axt/mnt2/jongha/v5_glot50010/runs/v5_fvt_mlm_10k` or its complete `checkpoint-10000` fallback |

If both `checkpoint-10000` and root-level final model files exist, use the
root-level saved model directory for downstream wrappers and record
`checkpoint-10000` as the corresponding training checkpoint.

If the root-level final files are absent but `checkpoint-10000` contains
`pytorch_model.bin` or `model.safetensors`, the generated model matrix may use
`checkpoint-10000` directly. This is still the fixed 10K selection rule; it is
not post-hoc checkpoint picking.

## Selection Criterion

Primary rule:

```text
Use matched 10K full-corpus checkpoints for `v5_random` and `v5_fvt`.
```

Tie-breaking / exception rule:

```text
If one run fails before 10K, do not compare it as a main novelty result. Either
rerun the failed side or report both as incomplete/exploratory with the exact
stop step.
```

This prevents downstream results from choosing a checkpoint after seeing task
scores.

## Current Run State

Generated selected-checkpoint status is tracked in:

```text
docs/exp/v5/2_training/05_checkpoint_selection/selected_checkpoint_manifest.md
docs/exp/v5/2_training/05_checkpoint_selection/selected_checkpoint_manifest.tsv
```

`v5_random_mlm_10k` has crossed preprocessing and entered Trainer optimization.
The latest generated live snapshot is:

```text
docs/exp/v5/3_evaluation/running_status.md
```

The training log reports:

```text
Num examples = 6893482
Total train batch size (w. parallel, distributed & accumulation) = 384
Total optimization steps = 10000
Number of trainable parameters = 369563951
```

`v5_fvt_mlm_10k` is queued by `modeling/launch_v5_random_fvt_10k.sh` and starts
after the random run finishes.

## Post-Completion Commands

After both v5 model directories contain root-level model files or complete
`checkpoint-10000` fallback directories:

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
```

If both rows are promoted to `ready_for_wrapper=yes` and
`post_checkpoint_preflight.md` reports `post_checkpoint_preflight_ready_to_launch`,
run the paired guarded post-checkpoint pass. `xlmr_base` and `glot500_base` rows
that are already measured should not be rerun unless validating reproducibility:

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
```

Use split phases only when staging long jobs:

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh pppl
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream
```

The downstream execution order and promotion rules are maintained in:

```text
docs/exp/v5/3_evaluation/next_runbook.md
```
