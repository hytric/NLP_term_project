# v5 Result Insertion Matrix

Last updated: 2026-06-28 12:08 KST

This matrix defines how new experimental outputs become report and slide
content. A value is promoted only after the required evidence exists and
`scripts/aggregate_v5_metrics.py` can parse it, unless the row is explicitly a
pending/blocker accounting row.

## Promotion Rule

```text
running log -> live status only
launcher/process/storage state -> operational gate only
dev score -> live status only
completed raw metric file + run_meta/command log -> provenance audit -> aggregation -> table/report/slide value
coverage/blocker audit -> limitation row
```

Single-model v5 rows, such as current `v5_random` diagnostic rows, may be
reported as measured pipeline evidence but do not unlock method win/loss
claims. Paired method claims require both `v5_random` and `v5_fvt` rows for the
same metric/scope, followed by the claim gates.

## Insertion Matrix

| New evidence | First command | Aggregation/table target | Report target | Slide target | Claim unlocked |
| --- | --- | --- | --- | --- | --- |
| live random progress, GPU/process activity, storage, or random-to-FVT transition evidence | `python3 scripts/write_v5_mlm_progress_eta.py`; `python3 scripts/audit_v5_live_training_health.py`; `python3 scripts/audit_v5_storage_readiness.py`; `python3 scripts/audit_v5_paired_launcher_transition.py` | `../2_training/mlm_progress_eta.md`, `../2_training/live_training_health.md`, `../2_training/storage_readiness.md`, `../2_training/paired_launcher_transition.md` | training status only | slide 10 status only | none; operational evidence is not model-quality evidence |
| `v5_random_mlm_10k` root model or complete `checkpoint-10000` | `python3 scripts/write_v5_eval_model_matrix.py`; `python3 scripts/write_v5_checkpoint_selection_manifest.py` | `2_training/05_checkpoint_selection/selected_checkpoint_manifest.md` | training method and checkpoint selection | slide 10 | random checkpoint is selectable |
| `v5_fvt_mlm_10k` root model or complete `checkpoint-10000` | `python3 scripts/write_v5_eval_model_matrix.py`; `python3 scripts/write_v5_checkpoint_selection_manifest.py` | `2_training/05_checkpoint_selection/selected_checkpoint_manifest.md` | training method and checkpoint selection | slide 10 | matched random/FVT checkpoints exist |
| both `v5_random` and `v5_fvt` are `ready_for_wrapper=yes`, and `post_checkpoint_preflight.md` reports `post_checkpoint_preflight_ready_to_launch` | `bash scripts/run_v5_post_checkpoint_evals.sh status` | `model_matrix.tsv`, `selected_checkpoint_manifest.md`, `post_checkpoint_eval_queue.md`, `post_checkpoint_command_consistency.md`, `post_checkpoint_parser_contract.md`, `post_checkpoint_provenance_audit.md`, and `post_checkpoint_preflight.md` | handoff from training to evaluation | slide 10 and backup Q&A | evaluation may start, but no result claim yet |
| PPPL `v5_random` output | `python3 scripts/aggregate_v5_metrics.py` | `00_tables/table_06_pppl_partial.md` | main result table, PPPL paragraph | slides 11-12 | after-MLM random intrinsic row |
| PPPL `v5_fvt` output | `python3 scripts/aggregate_v5_metrics.py` | `00_tables/table_06_pppl_partial.md` | main result table, PPPL paragraph | slides 11-12 | after-MLM FVT-vs-random PPPL comparison |
| Tatoeba `v5_random`/`v5_fvt` outputs | `python3 scripts/aggregate_v5_metrics.py` | `00_tables/table_07_tatoeba_partial.md` | downstream result paragraph | slide 11 status and slide 12 result values | available-language retrieval comparison |
| Taxi1500 `v5_random`/`v5_fvt` outputs | `python3 scripts/aggregate_v5_metrics.py` | `00_tables/table_08_text_classification_partial.md` macro-F1 rows | downstream result paragraph | slide 11 status and slide 12 result values | limited text-classification comparison |
| NER `glot500_base` `test_results.txt` | `python3 scripts/aggregate_v5_metrics.py` | `00_tables/table_10_ner_partial.md` | external reference tagging row | slide 12 result values | Glot500-base NER reference row |
| POS `glot500_base` `test_results.txt` | `python3 scripts/aggregate_v5_metrics.py` | `00_tables/table_11_pos_partial.md` | external reference tagging row | slide 12 result values | Glot500-base POS reference row |
| NER/POS `v5_random`/`v5_fvt` outputs | `python3 scripts/aggregate_v5_metrics.py` | `table_10_ner_partial.md`, `table_11_pos_partial.md` | downstream result paragraph | slide 11 status and slide 12 result values | available-language tagging comparison with the POS `TRAIN_LANGS` caveat |
| Bible `v5_random`/`v5_fvt` outputs | `python3 scripts/aggregate_v5_metrics.py` | `00_tables/table_12_bible_partial.md` and aggregation rows | downstream result paragraph | slide 11 status, slide 12 result values, and slide 13 caveat | available-language Bible retrieval comparison |
| Roundtrip `xlmr_base`/`glot500_base` outputs | `python3 scripts/aggregate_v5_metrics.py` | `00_tables/table_14_roundtrip_partial.md`, aggregation rows, and `00_tables/table_09_blocked_metric_notes.md` | baseline/reference result paragraph and limitations | slide 12 result values and slide 13 caveat | available-language reference rows, not v5 method claim |
| Roundtrip `v5_random`/`v5_fvt` outputs | `python3 scripts/aggregate_v5_metrics.py` | `00_tables/table_14_roundtrip_partial.md`, aggregation rows, and `00_tables/table_09_blocked_metric_notes.md` | downstream result paragraph | slide 11 status, slide 12 result values, and slide 13 caveat | available-language Roundtrip method comparison |

## Required Refresh Sequence

After any new result file appears, run:

```bash
python3 scripts/refresh_v5_reporting.py
```

The canonical sequence is maintained in `scripts/refresh_v5_reporting.py`.
Do not hand-replay the full script list unless debugging a failed refresh. If a
manual replay is required, use the dependency order below only as a diagnostic
mirror of `scripts/refresh_v5_reporting.py`, then return to the canonical
refresh command so rendered PDFs, PPTX, release manifest, and bundle are rebuilt
from one source of truth. The repeated final-deliverable, smoke, manifest,
bundle, and release-bundle audit calls are intentional stabilization passes:
the reporting package audit, final handoff files, and release bundle summarize
one another, so the final package is rebuilt after those summaries are fresh.

```bash
python3 scripts/write_v5_eval_model_matrix.py
python3 scripts/write_v5_checkpoint_selection_manifest.py
python3 scripts/audit_v5_checkpoint_selection_contract.py
python3 scripts/audit_v5_eval_coverage.py
python3 scripts/audit_v5_roundtrip_blocker.py
python3 scripts/aggregate_v5_metrics.py
python3 scripts/audit_v5_aggregation_schema.py
python3 scripts/write_v5_finalization_gate_status.py
python3 scripts/write_v5_post_checkpoint_eval_queue.py
python3 scripts/write_v5_post_checkpoint_execution_plan.py
python3 scripts/audit_v5_post_checkpoint_command_consistency.py
python3 scripts/audit_v5_post_checkpoint_parser_contract.py
python3 scripts/audit_v5_post_checkpoint_provenance.py
python3 scripts/audit_v5_post_checkpoint_preflight.py
python3 scripts/write_v5_current_result_snapshot.py
python3 scripts/write_v5_result_slot_inventory.py
python3 scripts/write_v5_post_result_update_manifest.py
python3 scripts/write_v5_post_result_patch_plan.py
python3 scripts/audit_v5_result_insertion_contract.py
python3 scripts/audit_v5_refresh_sequence_sync.py
python3 scripts/audit_v5_reporting_table_sync.py
python3 scripts/audit_v5_metric_fidelity.py
python3 scripts/audit_v5_reproducibility_package.py
python3 scripts/write_v5_method_comparison_summary.py
python3 scripts/audit_v5_comparison_materiality.py
python3 scripts/write_v5_claim_promotion_matrix.py
python3 scripts/write_v5_final_claim_decision_tree.py
python3 scripts/audit_v5_result_promotion_readiness.py
python3 scripts/audit_v5_claim_evidence_trace.py
python3 scripts/audit_v5_final_claim_freeze.py
python3 scripts/write_v5_objective_completion_audit.py
python3 scripts/write_v5_final_deliverable_audit.py
python3 scripts/audit_v5_final_submission_smoke.py
python3 scripts/write_v5_release_manifest.py
python3 scripts/build_v5_release_bundle.py
python3 scripts/audit_v5_release_bundle.py
python3 scripts/audit_v5_reporting_package.py
python3 scripts/write_v5_final_handoff_runbook.py
python3 scripts/write_v5_final_action_dashboard.py
python3 scripts/write_v5_final_deliverable_audit.py
python3 scripts/audit_v5_final_submission_smoke.py
python3 scripts/write_v5_release_manifest.py
python3 scripts/build_v5_release_bundle.py
python3 scripts/audit_v5_release_bundle.py
python3 scripts/write_v5_objective_completion_audit.py
python3 scripts/write_v5_final_deliverable_audit.py
python3 scripts/audit_v5_final_submission_smoke.py
python3 scripts/write_v5_release_manifest.py
python3 scripts/build_v5_release_bundle.py
python3 scripts/audit_v5_release_bundle.py
python3 scripts/refresh_v5_reporting.py --with-plots
```

If figure source data changed, use:

```bash
python3 scripts/refresh_v5_reporting.py --with-plots
```

Then update, in order:

1. metric-specific `README.md`
2. `2_training/05_checkpoint_selection/selected_checkpoint_manifest.md` when model paths changed
3. relevant `00_tables/table_*.md`, including `table_13_metric_fidelity_matrix.md` when coverage or blocker status changed
4. `current_result_snapshot.md`, `finalization_gate_status.md`,
   `post_checkpoint_execution_plan.md`, `post_checkpoint_command_consistency.md`,
   `post_checkpoint_parser_contract.md`, `post_checkpoint_provenance_audit.md`,
   `post_result_update_manifest.md`, `post_result_patch_plan_ko.md`,
   `final_handoff_runbook.md`, `method_comparison_summary.md`,
   `comparison_materiality_audit.md`,
   `claim_promotion_matrix.md`, `final_claim_decision_tree.md`,
   `narrative_quality_audit.md`, `objective_completion_audit.md`, and
   `final_deliverable_audit.md`
5. `result_slot_inventory.md`, `post_result_update_manifest.md`, and
   `post_result_patch_plan_ko.md` to identify exact report/PPT replacement
   targets and file-by-file patch order
6. `Report.md`
7. `03_final_report/paper_draft.md`
8. `03_final_report/paper_draft_ko.md`
9. `03_final_report/claim_ledger.md`
10. `comparison_materiality_audit.md` to keep `small` and `tie_band` deltas out of strong claims
11. `final_claim_decision_tree.md` to choose the allowed outcome block
12. `final_claim_freeze_audit.md` to verify claim locks before freezing prose
13. `03_final_report/result_interpretation_blocks.md` if the outcome language changes
14. `03_final_report/citation_source_map.md` if related-work or citation boundaries change
15. `02_slides/ppt_content.md`
16. `02_slides/presenter_script_ko.md`
17. `02_slides/slide_claim_checklist.md`
18. `02_slides/slide_citation_map.md` if slide citation boundaries change
19. `report_slide_crosswalk.md`
20. `02_slides/slide_asset_manifest.md`
21. `final_package_checklist.md`

Finally run a stale-value search for old live snapshots and stale unresolved
result-slot rows.

## Non-Promotion Examples

| Evidence | Why it is not final |
| --- | --- |
| `v5_random` current step count | training progress, no selected checkpoint |
| `paired_launcher_transition_random_running_fvt_waiting` | launcher/handoff health, no completed FVT model or parsed metric |
| `storage_readiness_ready_current` | output paths are writable, but no quality result is produced |
| NER/POS dev F1 during training | checkpoint-selection signal, not final test evaluation |
| empty or partially written `test_results.txt` | not parse-safe |
| target10 downstream missing rows | coverage limitation, not negative performance |
