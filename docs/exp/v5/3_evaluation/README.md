# v5 Evaluation

This stage stores every Glot500-required metric. All metrics are mandatory.
If task coverage is incomplete, write coverage and exclusion notes rather than
dropping the metric.

Subfolders:

- `00_coverage/`: task-language coverage audits
- `01_pseudoperplexity/`
- `02_retrieval_tatoeba/`
- `03_retrieval_bible/`
- `04_text_classification/`
- `05_ner/`
- `06_pos/`
- `07_roundtrip_alignment/`
- `08_embedding_similarity/`: extra novelty diagnostics
- `09_aggregation/`: final head/tail/all and target-subset tables

Canonical requirement file:

- `glot500_metric_requirements.md`

Execution warning: several inherited evaluation shell scripts default to v4
output directories. For v5, set `EVAL_OUTPUT_DIR` explicitly or create v5
wrappers before running each metric. Also run `00_coverage/` first because local
evaluation data may be partially materialized.

Current coverage audit command:

```bash
python3 scripts/audit_v5_eval_coverage.py
```

Current target10 coverage boundary: PPPL has `10/10` raw-text coverage. The
official Glot500 task lists also include partial v5 target membership
(`8/10`, mainly Bible plus one NER and one POS case). Earlier local
coverage/materialization files undercounted these tail tasks because the
task-list `0/1` column was treated as availability instead of head/tail flag.
Keep the metrics mandatory, but separate available-language downstream replay
and pending target-materialization repair from target10 intrinsic/MLM analysis.

Current data materialization note:

```text
00_coverage/data_materialization.md
```

Current execution queue:

```text
execution_queue.md
```

Generated post-checkpoint queue:

```text
post_checkpoint_eval_queue.md
```

Generated post-checkpoint execution plan:

```text
post_checkpoint_execution_plan.md
```

One-page post-checkpoint trigger card:

```text
../4_reporting/post_checkpoint_trigger_card_ko.md
```

Post-checkpoint command consistency audit:

```text
post_checkpoint_command_consistency.md
```

Post-checkpoint recovery runbook:

```text
post_checkpoint_eval_recovery.md
```

Post-checkpoint parser contract audit:

```text
post_checkpoint_parser_contract.md
```

Post-checkpoint provenance audit:

```text
post_checkpoint_provenance_audit.md
```

Post-checkpoint preflight audit:

```text
post_checkpoint_preflight.md
```

Next-run operational runbook:

```text
next_runbook.md
```

Live running status:

```text
running_status.md
```

Metric-to-runner mapping:

```text
metric_mapping.md
```

Tatoeba retrieval, PAN-X/NER, and UD-POS are now locally materialized for
available task languages. Current refreshed coverage is Tatoeba `63/102`, NER
`78/102`, and POS `58/102`; target10 remains `0/10` for these downstream
tasks.

Current model matrix:

```text
docs/exp/v5/3_evaluation/model_matrix.tsv
```

Regenerate it with:

```bash
python3 scripts/write_v5_eval_model_matrix.py
```

The canonical refresh command also regenerates this matrix before aggregation,
so new checkpoint files are picked up automatically:

```bash
python3 scripts/refresh_v5_reporting.py
```

Metric execution wrapper:

```bash
bash scripts/run_v5_eval_metric.sh <metric> <model_key> 2
```

The third argument is passed directly to `CUDA_VISIBLE_DEVICES`, so it is a
physical GPU id. The wrapper refreshes `model_matrix.tsv` by default before
checking model readiness, so newly created checkpoint files are picked up
without a manual matrix refresh. Set `REFRESH_MODEL_MATRIX=0` only when
intentionally replaying against a frozen matrix snapshot.

Post-checkpoint paired execution wrapper:

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh pppl
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream
```

Use the paired wrapper after both `v5_random` and `v5_fvt` are marked
`ready_for_wrapper=yes` in `model_matrix.tsv` and
`post_checkpoint_preflight.md` reports `post_checkpoint_preflight_ready_to_launch`.
It refuses to run while either model is still missing or preflight is not
ready-to-launch, refreshes `model_matrix.tsv`,
`selected_checkpoint_manifest.md`, `post_checkpoint_eval_queue.tsv`, the
post-checkpoint command consistency audit, and the parser contract audit, runs
required v5 rows in random/FVT pairs, and refreshes reporting after each metric
family. `GPU_RANDOM` and `GPU_FVT` are physical GPU ids; confirm free devices
with `nvidia-smi` and override them if GPU `0` or `1` is occupied. Prefer `all`
for the final post-checkpoint pass; use `pppl` and `downstream` separately only
when staging long jobs.

Supported required metric ids:

```text
pppl
retrieval_tatoeba
retrieval_bible
text_classification
ner
pos
roundtrip_alignment
```

Refresh completion tables:

```bash
python3 scripts/refresh_v5_reporting.py
```

Equivalent manual refresh sequence:

```bash
python3 scripts/write_v5_eval_model_matrix.py
python3 scripts/write_v5_checkpoint_selection_manifest.py
python3 scripts/aggregate_v5_metrics.py
python3 scripts/write_v5_running_status.py
python3 scripts/write_v5_mlm_progress_eta.py
python3 scripts/audit_v5_live_training_health.py
python3 scripts/audit_v5_storage_readiness.py
python3 scripts/audit_v5_paired_launcher_transition.py
python3 scripts/write_v5_finalization_gate_status.py
python3 scripts/write_v5_post_checkpoint_eval_queue.py
python3 scripts/write_v5_post_checkpoint_execution_plan.py
python3 scripts/audit_v5_post_checkpoint_command_consistency.py
python3 scripts/audit_v5_post_checkpoint_parser_contract.py
python3 scripts/audit_v5_post_checkpoint_preflight.py
python3 scripts/audit_v5_goal_readiness.py
python3 scripts/write_v5_current_result_snapshot.py
python3 scripts/audit_v5_reporting_table_sync.py
python3 scripts/audit_v5_result_promotion_readiness.py
python3 scripts/write_v5_objective_completion_audit.py
python3 scripts/write_v5_slide_asset_manifest.py
python3 scripts/audit_v5_reporting_package.py
```

## Stage Exit Line

Move to `../4_reporting/` only after all of the following are true:

- `00_coverage/` has one coverage file per required metric.
- every Glot500-required metric folder has command logs, raw outputs, and a
  summary TSV/JSON/Markdown result.
- missing target languages are listed with exclusion reasons.
- `09_aggregation/` has head/tail/all and v5-target subset tables.
- `xlmr_base`, `glot500_base`, `v5_random`, and `v5_fvt` are all accounted for.
- `model_matrix.tsv` marks required v5 checkpoints as ready, not missing.

Minimum artifact line:

```text
all required metrics measured or explicitly excluded + aggregation ready
```

If this line is not met, reporting should mark the experiment as incomplete
rather than claiming downstream improvement.
