# v5 Next-Run Runbook

Last updated: 2026-06-27 16:32 KST

This runbook records what to do immediately after the currently running jobs
finish. It is intentionally operational: final claims still come only from
parsed artifacts in `09_aggregation/`.

## Current Active Line

Live status is maintained in:

```text
docs/exp/v5/3_evaluation/running_status.md
```

Current active jobs:

| Job | Current role | Result gate |
| --- | --- | --- |
| `v5_random_mlm_10k` | first half of matched random/FVT MLM pair | checkpoint written under `/home/axt/mnt2/jongha/v5_glot50010/runs/v5_random_mlm_10k` |
| `v5_fvt_mlm_10k` | queued second half of matched pair | same 10K budget and checkpoint rule as random |
| NER `glot500_base` | completed external-reference tagging row | already parsed by aggregation |
| POS `glot500_base` | completed external-reference tagging row with `TRAIN_LANGS=tur_Latn` | already parsed by aggregation; all F1 `0.567542`, head F1 `0.573832` |

## POS Completion Note

The Glot500-base POS reference row has been promoted. If the POS files are
regenerated later, execute the canonical refresh:

```bash
python3 scripts/refresh_v5_reporting.py --with-plots
```

Then update from aggregation only:

- `docs/exp/v5/3_evaluation/running_status.md`
- `docs/exp/v5/3_evaluation/06_pos/README.md`
- `docs/exp/v5/4_reporting/00_tables/table_11_pos_partial.md`
- `docs/exp/v5/Report.md`
- `docs/exp/v5/4_reporting/02_slides/ppt_content.md`
- `docs/exp/v5/4_reporting/03_final_report/report_sections_draft.md`
- `docs/exp/v5/4_reporting/03_final_report/claim_ledger.md`

Promotion rule:

```text
dev F1 is live progress only; final tagging rows require non-empty completed
test_results.txt.
```

## After A Tagging GPU Frees

If GPU `0` or `1` becomes free before v5 MLM checkpoints are ready, continue
external-reference downstream baselines that are not already running or
measured. This keeps the downstream reference table moving while GPUs `2,3`
remain occupied by MLM.

Taxi1500 text classification:

```bash
bash scripts/run_v5_eval_metric.sh text_classification glot500_base 0
```

Status: measured; do not rerun unless validating reproducibility.

Tagging baselines:

NER:

```bash
TRAIN_LANGS=eng_Latn bash scripts/run_v5_eval_metric.sh ner glot500_base 0
```

Status: measured; do not rerun unless validating reproducibility.

POS:

```bash
TRAIN_LANGS=tur_Latn bash scripts/run_v5_eval_metric.sh pos glot500_base 1
```

Status: measured; do not rerun unless validating reproducibility.

Bible retrieval:

```bash
bash scripts/run_v5_eval_metric.sh retrieval_bible xlmr_base 0
bash scripts/run_v5_eval_metric.sh retrieval_bible glot500_base 1
```

Status: ready to run after materialization; coverage is `74/102`,
target10 `0/10`. XLM-R-base and Glot500-base rows are already measured; rerun
only for reproducibility validation. The remaining Bible execution is for
`v5_random` and `v5_fvt` after matched checkpoints exist and post-checkpoint
preflight is ready-to-launch. This is an
available-language Glot500 metric replay, not a target10 downstream claim.

After any deliberately rerun tagging job:

```bash
python3 scripts/refresh_v5_reporting.py --with-plots
```

Do not start v5 tagging runs until `model_matrix.tsv` marks `v5_random` and
`v5_fvt` as `ready_for_wrapper=yes` and `post_checkpoint_preflight.md` reports
`post_checkpoint_preflight_ready_to_launch`.

## When Matched V5 Checkpoints Exist

First refresh the model matrix, selected checkpoint manifest, evaluation queue,
post-checkpoint command guards, and reporting gates:

```bash
python3 scripts/refresh_v5_reporting.py
```

Confirm both rows are ready:

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
```

Optional watcher:

```bash
POLL_SECONDS=300 bash scripts/watch_v5_mlm_handoff.sh
```

By default this watcher only polls, refreshes the model matrix/checkpoint
manifest, live progress/health audits, result-promotion readiness audit, and
runs the guarded `status` handoff once both v5 rows are `ready_for_wrapper=yes`.
Use `RUN_ALL=1` only when you intentionally want it to launch the long paired
PPPL/downstream pass after readiness and preflight ready-to-launch are detected.

The model matrix uses this path rule:

- root-level final Trainer model directory first;
- if root-level model files are absent, complete fixed `checkpoint-10000`
  fallback directory;
- no earlier checkpoint for the main novelty comparison unless the run is
  explicitly downgraded from final to exploratory.

The guarded paired launcher refuses to run until both required v5 models are
ready. The preferred full execution line is:

```bash
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
```

This runs PPPL first, because it has `102/102` raw coverage and `10/10`
target10 coverage, and then runs the available downstream replay. If the run
needs to be split for machine-time or debugging reasons, use the same wrapper
in phases:

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh pppl
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream
```

The wrapper refreshes reporting after each metric family. The `status` mode also
refreshes the command consistency audit and parser contract audit before any
long paired launch. Use `running_status.md` only for progress snapshots; promote
report/PPT values only after `metric_completion.tsv` and
`main_head_tail_all.tsv` include the completed rows.

The paired launcher is only a convenience wrapper around
`scripts/run_v5_eval_metric.sh`; for debugging or reruns, the individual
commands may still be used with the same environment variables:

```bash
MAX_EXAMPLES_PER_LANGUAGE=100 MAX_LENGTH=128 MASK_BATCH_SIZE=64 \
  bash scripts/run_v5_eval_metric.sh pppl v5_random 0

TRAIN_LANGS=eng_Latn bash scripts/run_v5_eval_metric.sh ner v5_fvt 1
```

## Blocked Metrics

Bible retrieval and roundtrip alignment remain required metric families. Bible
retrieval is no longer data-blocked for available languages; only the v5 model
rows wait for checkpoints. Roundtrip is also materialized and measured for
available baseline/reference rows; only the v5 model rows wait for checkpoints:

| Metric | Current blocker | Report handling |
| --- | --- | --- |
| Bible retrieval | v5 model checkpoints or preflight not ready | keep measured XLM-R/Glot500-base rows; run v5 rows after checkpoints and post-checkpoint preflight |
| Roundtrip alignment | v5 model checkpoints or preflight not ready; target10 0/10 | keep measured XLM-R/Glot500-base rows; run v5 rows after checkpoints and post-checkpoint preflight |

If either data source is materialized later, update coverage first:

```bash
python3 scripts/audit_v5_eval_coverage.py
python3 scripts/write_v5_eval_model_matrix.py
```

## Final Reporting Sync

After every new measured result, refresh these before editing prose:

```bash
python3 scripts/refresh_v5_reporting.py --with-plots
```

Then update report artifacts in this order:

1. metric folder `README.md`
2. `4_reporting/00_tables/`
3. `Report.md`
4. `4_reporting/03_final_report/paper_draft.md`
5. `4_reporting/03_final_report/claim_ledger.md`
6. `4_reporting/03_final_report/result_interpretation_blocks.md`
7. `4_reporting/02_slides/ppt_content.md`
8. `4_reporting/02_slides/presenter_script_ko.md`
9. `4_reporting/02_slides/slide_claim_checklist.md`
10. `4_reporting/report_slide_crosswalk.md`
11. `4_reporting/result_promotion_readiness_audit.md`
