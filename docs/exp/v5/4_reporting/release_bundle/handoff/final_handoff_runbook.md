# v5 Final Handoff Runbook

Last checked: 2026-06-28 18:08 KST

Verdict: `handoff_ready_for_post_checkpoint_eval`

This generated runbook is the shortest path from the current execution
state to the final paper-style report and PPT handoff. It is dynamic:
statuses are derived from checkpoint gates, metric queues, and report/PPT
audits rather than copied by hand.

| Phase | Status | Trigger | Command | Proof | Promotion rule |
| --- | --- | --- | --- | --- | --- |
| 0_current_status_refresh | needs_doc_repair | Any time before checking live status or editing report/PPT prose. | `python3 scripts/refresh_v5_reporting.py` | docs/exp/v5/4_reporting/reporting_package_audit.md; narrative_quality_audit.md; claim_promotion_matrix.md | Do not edit final claims until this command leaves stale/live guards clean. |
| 1_checkpoint_wait | ready | Both selected v5 model rows are ready. | `POLL_SECONDS=300 bash scripts/watch_v5_mlm_handoff.sh` | docs/exp/v5/3_evaluation/running_status.md; docs/exp/v5/2_training/05_checkpoint_selection/selected_checkpoint_manifest.md; docs/exp/v5/2_training/paired_launcher_transition.md | Use watcher as status-only polling unless RUN_ALL=1 is intentionally set; automatic RUN_ALL resume defaults to SKIP_MEASURED=1. |
| 2_checkpoint_handoff | ready | Run immediately after both model directories contain a final model or complete checkpoint-10000. | `cat docs/exp/v5/4_reporting/post_checkpoint_trigger_card_ko.md && bash scripts/run_v5_post_checkpoint_evals.sh status` | docs/exp/v5/4_reporting/post_checkpoint_trigger_card_ko.md; docs/exp/v5/3_evaluation/model_matrix.tsv; docs/exp/v5/2_training/05_checkpoint_selection/selected_checkpoint_manifest.md; docs/exp/v5/3_evaluation/post_checkpoint_eval_queue.tsv; docs/exp/v5/3_evaluation/post_checkpoint_command_consistency.md; docs/exp/v5/3_evaluation/post_checkpoint_parser_contract.md; docs/exp/v5/3_evaluation/post_checkpoint_preflight.md | Proceed only when status prints `READY_TO_LAUNCH=yes`; this summarizes `ready_for_wrapper=yes` for both v5 models and `post_checkpoint_preflight_ready_to_launch`. |
| 2b_ready_to_final_package_launcher | ready | Optional one-shot path after `READY_TO_LAUNCH=yes` when evaluation, refresh, and final packet audit should run together. | `SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_ready_to_final_package.sh` | docs/exp/v5/4_reporting/final_evidence_packet_audit.md; docs/exp/v5/4_reporting/final_deliverable_audit.md; docs/exp/v5/4_reporting/release_bundle_audit.md | The launcher refuses evaluation unless status prints `READY_TO_LAUNCH=yes`; final claims still require `final_evidence_packet_ready`. |
| 3_paired_post_checkpoint_eval | pending_results | queue_counts={'measured': 24, 'ready': 4}; gates matched=ready, pppl=pending, downstream=pending | `SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all` | docs/exp/v5/3_evaluation/09_aggregation/metric_completion.tsv; main_head_tail_all.tsv; v5_target_subset.tsv | Use split `pppl` and `downstream` modes only for staging/debugging; current queue already has measured rows, so skip them and promote only refreshed aggregation rows; final claims come from aggregation. Canonical full rerun command: `WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all`. |
| 4_blocked_metric_accounting | accepted_or_pending | Bible=pending; Roundtrip=pending | `python3 scripts/audit_v5_roundtrip_blocker.py` | docs/exp/v5/3_evaluation/07_roundtrip_alignment/blocker_audit.md; 4_reporting/00_tables/table_09_blocked_metric_notes.md | If runnable, execute available-language Roundtrip rows; otherwise keep explicit pending/blocker accounting. |
| 5_reporting_refresh_with_plots | ready_after_results | Run after every new measured metric output or coverage/source-data change. | `python3 scripts/refresh_v5_reporting.py --with-plots` | docs/exp/v5/4_reporting/01_figures/generated/figure_manifest.tsv; table_sync_audit.md | Refresh before editing report/PPT prose; do not hand-copy live logs into result tables. |
| 5b_post_result_patch_plan | waiting_results | Run after refresh has parsed new metric outputs and regenerated report/PPT audits. | `sed -n '1,120p' docs/exp/v5/4_reporting/post_result_patch_plan_ko.md` | docs/exp/v5/4_reporting/post_result_patch_plan_ko.md; post_result_patch_plan.tsv; post_result_update_manifest.md | Patch only rows whose status is `ready_for_patch`; keep waiting/checkpoint rows locked. |
| 6_claim_and_narrative_review | waiting_result_claims | claim_matrix=claim_boundaries_ready_pending_results; narrative=narrative_ready_pending_results; table_sync=needs_table_sync | `python3 scripts/refresh_v5_reporting.py` | docs/exp/v5/4_reporting/claim_promotion_matrix.md; narrative_quality_audit.md; reporting_package_audit.md | Promote only `promotable_now` or result-unlocked claims; keep target10 downstream coverage caveats. |
| 7_final_report_ppt_freeze | pending_final_results | assembly=execution_draft_not_final; package=needs_document_cleanup; narrative=narrative_ready_pending_results | `python3 scripts/refresh_v5_reporting.py --with-plots` | docs/exp/v5/4_reporting/final_assembly_manifest.md; final_package_checklist.md; final_deliverable_audit.md; final_deliverable_audit.tsv | Freeze only when final assembly is ready or when any remaining limitation is explicitly accepted as blocked-data. |

Safety rules:

- Do not run the long paired evaluation until both v5 model rows are
  ready for the wrapper and the preflight verdict is
  `post_checkpoint_preflight_ready_to_launch`.
- Treat `READY_TO_LAUNCH=yes` at the end of
  `bash scripts/run_v5_post_checkpoint_evals.sh status` as the
  human-facing launch gate; `READY_TO_LAUNCH=no` means keep waiting
  or follow the printed `NEXT_COMMAND`.
- Do not promote after-MLM or downstream claims from live logs, dev
  scores, empty outputs, or unparsed files.
- If Roundtrip remains pending or blocked, keep the status row and
  limitation text; do not silently remove the metric family.
- If a previous paired pass measured only some rows, prefix the next
  launch with `SKIP_MEASURED=1` so measured queue rows are skipped;
  do not use this as a claim shortcut.
- Run a persistent watcher from a user-managed shell or tmux session;
  do not assume a transient non-interactive launcher will keep a
  background watcher alive.
- The final report/PPT can be called final only after this runbook, the
  final assembly manifest, and the reporting package audit agree.

Waiting-state checks:

```bash
python3 scripts/refresh_v5_reporting.py
# Prints model matrix, queue, guards, live MLM progress, checkpoint contract, and READY_TO_LAUNCH.
bash scripts/run_v5_post_checkpoint_evals.sh status
# Optional deeper live-state reads if the status output is surprising.
sed -n '1,45p' docs/exp/v5/3_evaluation/running_status.md
sed -n '1,90p' docs/exp/v5/2_training/paired_launcher_transition.md
```

Move from waiting to evaluation only when `model_matrix.tsv`,
`selected_checkpoint_manifest.md`, `post_checkpoint_eval_queue.md`,
`post_checkpoint_command_consistency.md`,
`post_checkpoint_parser_contract.md`, and
`post_checkpoint_preflight.md` agree that both `v5_random`
and `v5_fvt` have `ready_for_wrapper=yes` and the preflight verdict
is `post_checkpoint_preflight_ready_to_launch`. Until then, the
correct state is `waiting_model`, not a failed experiment.
