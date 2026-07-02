# v5 Post-Checkpoint Command Consistency Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `post_checkpoint_command_consistency_ready`

This generated audit keeps the post-checkpoint paired evaluation command
consistent across report/PPT, runbooks, and reproducibility files. The
canonical paired launch includes explicit random/FVT GPU bindings:

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
```

| Item | Status | Evidence | Action |
| --- | --- | --- | --- |
| legacy_command_scan | ready | no legacy post-checkpoint paired commands found | none |
| required_command_file:docs/exp/v5/2_training/mlm_progress_eta.md | ready | all canonical command tokens present | none |
| required_command_file:docs/exp/v5/3_evaluation/post_checkpoint_execution_plan.md | ready | all canonical command tokens present | none |
| required_command_file:docs/exp/v5/goal_readiness.md | ready | all canonical command tokens present | none |
| required_command_file:docs/exp/v5/4_reporting/final_handoff_runbook.md | ready | all canonical command tokens present | none |
| required_command_file:docs/exp/v5/4_reporting/post_result_update_manifest.md | ready | all canonical command tokens present | none |
| required_command_file:docs/exp/v5/4_reporting/02_slides/defense_qa.md | ready | all canonical command tokens present | none |
| required_command_file:docs/exp/v5/4_reporting/02_slides/defense_qa_ko.md | ready | all canonical command tokens present | none |
| required_command_file:docs/exp/v5/4_reporting/03_final_report/reproducibility_appendix.md | ready | all canonical command tokens present | none |
| wrapper_preflight_launch_guard | ready | preflight ready-to-launch guard present | none |
| wrapper_long_mode_ready_guards | ready | long modes call require_ready_pair before evaluation | none |
| wrapper_status_launch_summary | ready | status mode prints READY_TO_LAUNCH and NEXT_COMMAND summary | none |
| wrapper_skip_measured_resume_guard | ready | SKIP_MEASURED=1 can resume a partial paired pass without rerunning measured queue rows | none |
| wrapper_all_mode_metric_family_coverage | ready | all mode runs available downstream metrics and runs PPPL only when held-out or explicitly diagnostic | none |
| eval_metric_dispatch_coverage | ready | dispatcher has cases for PPPL, Tatoeba, Bible, Taxi1500, NER, POS, and Roundtrip | none |
| execution_plan_dependency | ready | post_checkpoint_execution_plan=post_checkpoint_execution_plan_ready_to_launch | none |

Split canonical commands:

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh pppl
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream
```

Optional partial-run resume command:

```bash
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
```

`SKIP_MEASURED=1` is only a resume guard: it skips metric/model
rows already marked `measured` in `post_checkpoint_eval_queue.tsv`
and still refuses long modes until the matched-checkpoint preflight
is ready.

Rule: `bash scripts/run_v5_post_checkpoint_evals.sh status` is safe
while waiting. The paired `all`, `pppl`, and `downstream` commands
must still be run only after both v5 model rows are
`ready_for_wrapper=yes` and the generated preflight verdict is
`post_checkpoint_preflight_ready_to_launch`.
