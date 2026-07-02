# v5 Final Assembly Manifest

Last checked: 2026-06-28 18:08 KST

Verdict: `execution_draft_not_final`

This generated manifest is the final handoff map for assembling the
paper-style report and PPT package. It does not promote claims by itself;
it points to the gates and source files that decide whether a section is
final-ready or still an execution draft.

| Artifact | Status | Source files | Final gate | Action |
| --- | --- | --- | --- | --- |
| paper_style_report | execution_draft_ready | Report.md; 4_reporting/03_final_report/paper_draft.md; paper_draft_ko.md; paper_build_spec.md; manuscript_completion_matrix.md; narrative_quality_audit.md | matched=ready; pppl=pending; downstream=pending; guards=False | replace pending v5 method rows only after matched checkpoints and parsed metrics |
| ppt_content_package | execution_draft_ready | 4_reporting/02_slides/ppt_content.md; final_deck_ko.md; presenter_script_ko.md; deck_build_spec.md; slide_completion_matrix.md; narrative_quality_audit.md | matched=ready; pppl=pending; downstream=pending; guards=False; slide_rendering=slide_rendering_ready | update slides 11/12/14 only from aggregation and claim ledger |
| tables_and_metric_rows | current_rows_ready_v5_pending | 4_reporting/00_tables/; 3_evaluation/09_aggregation/; table_sync_audit.md; metric_fidelity_audit.md | pppl=pending; downstream=pending; table_sync=needs_sync; metric_fidelity=metric_fidelity_needs_repair | run refresh after every metric output and keep pending rows explicit |
| figures | ready_current | 4_reporting/01_figures/generated/ | refresh with --with-plots after figure-source data changes | regenerate figures after final v5 rows if plotted sources change |
| citation_and_source_boundaries | ready | references.bib; citation_source_map.md; external_source_verification.md; slide_citation_map.md | citation maps synchronized | keep literature support separate from local measured-result evidence |
| presentation_handoff | ready_current | presentation_readiness_checklist_ko.md; submission_file_index_ko.md; one_page_summary_ko.md; final_action_dashboard_ko.md; post_checkpoint_trigger_card_ko.md | first-open files synchronized | open presentation_readiness_checklist_ko.md first before rehearsal, sharing, or claim changes |
| roundtrip_alignment_accounting | accepted_or_pending | 3_evaluation/07_roundtrip_alignment/blocker_audit.md; table_09_blocked_metric_notes.md | roundtrip=pending; bible=pending | do not omit Roundtrip; report measured, pending, or blocked status explicitly |
| reproducibility_handoff | ready_current | reproducibility_appendix.md; source_map.md; final_handoff_runbook.md; post_checkpoint_eval_queue.md; selected_checkpoint_manifest.md | matched=ready | add selected checkpoint paths and final command logs after model promotion |
| final_claim_boundary | needs_review | claim_ledger.md; method_comparison_summary.md; claim_promotion_matrix.md; final_claim_decision_tree.md; final_claim_freeze_audit.md; final_deliverable_audit.md; reporting_package_audit.md; objective_completion_audit.md | stale_guard=ready; live_guard=ready; decision_tree=decision_tree_waiting_for_results; claim_freeze=claim_freeze_needs_update | keep unsupported after-MLM/downstream claims pending until gates close |
| final_conclusion_decision_tree | ready_current | 4_reporting/final_claim_decision_tree.md; result_interpretation_blocks.md | decision_tree=decision_tree_waiting_for_results | choose the final conclusion block from this generated tree after v5 rows are parsed |

Final promotion rule:

- The report/PPT package is final only when matched `v5_random` and
  `v5_fvt` checkpoints are selected, after-MLM PPPL and available
  downstream rows are parsed, blocked-data metrics remain explicit,
  and stale/live-result guards are clean.
- Until then, the package is intentionally an execution draft with
  current measured baseline/reference rows and locked pending claims.
