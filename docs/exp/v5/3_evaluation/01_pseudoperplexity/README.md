# 01 Pseudoperplexity

Required Glot500 metric.

## Held-Out Policy

Glot500 computes PPPL on a held-out test set. Current v5 PPPL rows created with
`PPPL_SPLIT=train` are **train-source intrinsic diagnostics**, not final
Glot500-style held-out test rows.

Report labels:

- `PPPL_SPLIT=train`: train-source MLM/PPPL diagnostic
- `PPPL_SPLIT=dev` or `PPPL_SPLIT=test`: held-out PPPL, only valid after a
  deterministic held-out split exists

Execution guard:

```bash
ALLOW_TRAIN_SOURCE_PPPL=1 PPPL_EVAL_ROLE=train_source_diagnostic \
  bash scripts/run_v5_eval_metric.sh pppl v5_fvt 1
```

Strict held-out reproduction is assigned to v5.1:

```bash
PPPL_SPLIT=test PPPL_EVAL_ROLE=heldout_test \
  bash scripts/run_v5_eval_metric.sh pppl v5_fvt 1
```

Report:

- head
- tail
- all
- v5-target subset
- model-wise comparison for `xlmr_base`, `glot500_base`, `v5_random`, `v5_fvt`

## Next Step Gate

Move this metric to `../09_aggregation/` only after all required model/group
summaries are available.

Pass line:

- same evaluation corpus/split is used for all comparable models.
- `xlmr_base`, `glot500_base`, `v5_random`, and `v5_fvt` are included or have
  explicit failure notes.
- head, tail, all, and v5-target subset values are reported.
- command log, raw output, and summary table are saved.
- metric direction is clear: lower PPPL or loss is better.

Required artifacts:

- command log
- raw output
- `summary.tsv` or `results.md`
- coverage reference
- model path list

If PPPL uses a proxy rather than exact pseudo-perplexity, label it clearly in
the result table.

Post-checkpoint v5 execution:

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
RUN_TRAIN_SOURCE_PPPL_DIAGNOSTIC=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 \
  bash scripts/run_v5_post_checkpoint_evals.sh pppl
```

Do not use `v5_random` or `v5_fvt` rows until the status command shows both
models as `ready_for_wrapper=yes` and the completed PPPL outputs are parsed
into `docs/exp/v5/3_evaluation/09_aggregation/`.

## Current Baseline Results

The baseline PPPL jobs use GPU `0` while the v5 MLM run uses GPUs `2,3`.

Completed baselines:

```text
xlmr_base
glot500_base
```

Measured artifacts:

```text
docs/exp/v5/3_evaluation/01_pseudoperplexity/xlmr_base/scores.tsv
docs/exp/v5/3_evaluation/01_pseudoperplexity/xlmr_base/summary.tsv
docs/exp/v5/3_evaluation/01_pseudoperplexity/xlmr_base/meta.json
docs/exp/v5/3_evaluation/01_pseudoperplexity/xlmr_base/results.md
docs/exp/v5/3_evaluation/01_pseudoperplexity/glot500_base/scores.tsv
docs/exp/v5/3_evaluation/01_pseudoperplexity/glot500_base/summary.tsv
docs/exp/v5/3_evaluation/01_pseudoperplexity/glot500_base/meta.json
docs/exp/v5/3_evaluation/01_pseudoperplexity/glot500_base/results.md
```

Earlier chained launch log:

```text
/home/axt/mnt2/jongha/v5_glot50010/logs/pppl_baselines_xlmr_glot500_20260627_012541.log
```

The earlier chained launch completed `xlmr_base` but did not produce
`glot500_base`. The separate detached wrapper run completed `glot500_base`:

```text
/home/axt/mnt2/jongha/v5_glot50010/logs/pppl_glot500_base_20260627_020016.log
```

Measured baseline rows:

| Model | Group | Weighted PPPL | Weighted mean NLL |
| --- | --- | ---: | ---: |
| `xlmr_base` | head | 8.117338 | 2.094002 |
| `xlmr_base` | v5 target | 61.980216 | 4.126815 |
| `xlmr_base` | all | 9.986271 | 2.301211 |
| `glot500_base` | head | 10.213100 | 2.323671 |
| `glot500_base` | v5 target | 15.102934 | 2.714889 |
| `glot500_base` | all | 10.640353 | 2.364654 |

The v5 model rows remain blocked until matched `v5_random` and `v5_fvt`
checkpoints exist.

Current observation:

- `xlmr_base` and `glot500_base` are measured PPPL rows in `09_aggregation/`.
- `v5_random` and `v5_fvt` are still missing from PPPL aggregation.
- `scripts/run_v5_eval_metric.sh` currently passes `bash -n` and is ready for
  the remaining PPPL runs.
- Existing `xlmr_base`, `glot500_base`, and `v5_random` PPPL rows were produced
  from local train-source examples. They should stay in diagnostic tables unless
  strict held-out rows are generated in v5.1.

Operational note:

The PPPL proxy script loads selected examples from the 102 raw Arrow datasets
before model loading. On the full manifest this can be I/O-bound and may show no
metric output until example loading finishes. The script now supports
`--examples-cache`, and the v5 wrapper writes/uses a default cache under:

```text
/home/axt/mnt2/jongha/v5_glot50010/evaluation/cache/
```

This prevents repeated full Arrow reads when running `xlmr_base`,
`glot500_base`, `v5_random`, and `v5_fvt` with the same PPPL example selection.
