# v5.1 Evaluation

v5.1 evaluation is a downstream-aware diagnostic/ablation line. It keeps the
Glot500 metric families, but its target10 is not a genuine low-resource-only
set; the final main low-resource line is v5.

## Current Status

```text
MLM_CHECKPOINTS = running_random_first
LATEST_RANDOM_STEP = 1869/3000 at 2026-06-28 21:56 KST
CHECKPOINT_MODEL_FILE = pending
EVAL_DATA_COVERAGE = prepared
BIBLE_MATERIALIZATION = done
ROUNDTRIP_MATERIALIZATION = done
HELDOUT_PPPL = pending checkpoint
DOWNSTREAM = pending checkpoint
```

Readiness interpretation:

```text
EVAL_BLOCKER = checkpoint availability only
DATA_BLOCKER = no
NEXT_GATE = wait for v51_random checkpoint-3000, then verify v51_fvt starts
```

## Coverage

| Metric | Total / 102 | Head / 92 | Target10 / 10 | Note |
| --- | ---: | ---: | ---: | --- |
| PPPL | 102 | 92 | 10 | held-out test split via strict split indices |
| Tatoeba retrieval | 66 | 63 | 3 | local Tatoeba pairs available |
| Bible retrieval | 80 | 74 | 6 | materialized from Bible corpus |
| Taxi1500 classification | 1 | 1 | 0 | Glot500 metric retained; target claim unavailable |
| NER | 84 | 78 | 6 | local NER data available |
| POS | 58 | 58 | 0 | Glot500 metric retained; target claim unavailable |
| Roundtrip alignment | 80 | 74 | 6 | materialized from Bible corpus |

Source files:

```text
00_coverage/coverage_summary.tsv
00_coverage/dataset_size_audit.tsv
00_coverage/dataset_size_by_language.tsv
03_retrieval_bible/materialization_summary.tsv
07_roundtrip_alignment/materialization_summary.tsv
model_matrix.tsv
```

Dataset-size audit:

```text
../DATASET_SIZE_AUDIT_KO.md
```

Note: `coverage_summary.tsv` records nominal task-list coverage. The dataset
size audit counts current local split/materialized files; this catches gaps
such as POS nominal coverage `58` vs countable local POS split files `9`.

## Model Rows

| Model key | Role |
| --- | --- |
| `xlmr_base` | XLM-R baseline/reference |
| `glot500_base` | external Glot500 reference |
| `v51_random` | strict 5% / 3K random new-token embedding init |
| `v51_fvt` | strict 5% / 3K FVT/source-token-decomposition init |

The report comparison table should include all four rows when feasible. The
main novelty comparison is `v51_random` vs `v51_fvt`.

## Post-Checkpoint Commands

Refresh live status first:

```bash
bash scripts/refresh_v51_live_status.sh
```

Check readiness:

```bash
bash scripts/run_v51_post_checkpoint_evals.sh status
```

Run held-out PPPL:

```bash
PPPL_SPLIT=test PPPL_EVAL_ROLE=heldout_test \
GPU_RANDOM=0 GPU_FVT=1 \
bash scripts/run_v51_post_checkpoint_evals.sh pppl
```

Run downstream metrics:

```bash
GPU_RANDOM=0 GPU_FVT=1 \
bash scripts/run_v51_post_checkpoint_evals.sh downstream
```

Run baseline held-out PPPL for report comparison:

```bash
GPU_BASELINE=0 \
bash scripts/run_v51_post_checkpoint_evals.sh baseline_pppl
```

Aggregate parsed results:

```bash
bash scripts/run_v51_post_checkpoint_evals.sh aggregate
```

## Claim Boundary

- PPPL can be called Glot500-style only when `PPPL_SPLIT=test` and
  `PPPL_EVAL_ROLE=heldout_test` appear in `run_meta.tsv`.
- Target10 downstream claims are valid for Tatoeba, Bible, NER, and Roundtrip
  only on the available target subset.
- POS and Taxi1500 remain Glot500 metric replays over available/head languages;
  they are not target10 evidence.
- v5 train-source PPPL remains diagnostic/fallback evidence only.
