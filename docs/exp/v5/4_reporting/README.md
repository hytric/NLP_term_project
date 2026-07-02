# 4 Reporting

Use this folder for presentation and report deliverables derived from the
experiment logs.

Subfolders:

- `00_tables/`
- `01_figures/`
- `02_slides/`
- `03_final_report/`

Current reusable reporting assets:

- Korean one-page summary: `one_page_summary_ko.md`
- Korean submission file index: `submission_file_index_ko.md`
- tables/source map: `00_tables/source_map.md`
- generated figures: `01_figures/generated/figure_manifest.tsv`
- slide draft: `02_slides/ppt_content.md`
- Korean final deck source: `02_slides/final_deck_ko.md`
- talk track: `02_slides/talk_track.md`
- Korean presenter script: `02_slides/presenter_script_ko.md`
- Korean rehearsal plan: `02_slides/rehearsal_plan_ko.md`
- slide claim checklist: `02_slides/slide_claim_checklist.md`
- slide asset manifest: `02_slides/slide_asset_manifest.md`
- slide citation map: `02_slides/slide_citation_map.md`
- novelty/reproduction defense matrix: `02_slides/novelty_defense_matrix_ko.md`
- report prose blocks: `03_final_report/report_sections_draft.md`
- standalone paper draft: `03_final_report/paper_draft.md`
- Korean paper-style draft: `03_final_report/paper_draft_ko.md`
- paper build spec: `03_final_report/paper_build_spec.md`
- citation source map: `03_final_report/citation_source_map.md`
- contribution summary: `03_final_report/contribution_summary.md`
- report claim ledger: `03_final_report/claim_ledger.md`
- reproducibility appendix: `03_final_report/reproducibility_appendix.md`
- report-slide crosswalk: `report_slide_crosswalk.md`
- pending result registry: `pending_result_registry.md`
- current result snapshot: `current_result_snapshot.md`
- result slot inventory: `result_slot_inventory.md`
- post-result update manifest: `post_result_update_manifest.md`
- post-result patch plan: `post_result_patch_plan_ko.md`
- post-checkpoint trigger card: `post_checkpoint_trigger_card_ko.md`
- Korean post-checkpoint outcome matrix: `post_checkpoint_outcome_matrix_ko.md`
- Korean final result update checklist: `final_result_update_checklist_ko.md`
- refresh sequence sync audit: `refresh_sequence_sync_audit.md`
- metric fidelity audit: `metric_fidelity_audit.md`
- reproducibility audit: `reproducibility_audit.md`
- method comparison summary: `method_comparison_summary.md`
- final assembly manifest: `final_assembly_manifest.md`
- final claim decision tree: `final_claim_decision_tree.md`
- conclusion selection contract audit: `conclusion_selection_contract_audit.md`
- final claim freeze audit: `final_claim_freeze_audit.md`
- final handoff runbook: `final_handoff_runbook.md`
- final Korean freeze protocol: `final_freeze_protocol_ko.md`
- Korean final freeze evidence checklist: `final_freeze_evidence_checklist_ko.md`
- final Korean submission handoff: `final_submission_handoff_ko.md`
- Korean result-delay contingency: `result_delay_contingency_ko.md`
- Korean final goal acceptance rubric: `final_goal_acceptance_rubric_ko.md`
- Korean reviewer response crosswalk: `reviewer_response_crosswalk_ko.md`
- Korean execution readiness review: `execution_readiness_review_ko.md`
- feedback alignment audit: `feedback_alignment_audit.md`
- artifact reference audit: `artifact_reference_audit.md`
- claim promotion matrix: `claim_promotion_matrix.md`
- narrative quality audit: `narrative_quality_audit.md`
- section-slide sync audit: `section_slide_sync_audit.md`
- claim-evidence trace audit: `claim_evidence_trace_audit.md`
- post-checkpoint eval queue: `../3_evaluation/post_checkpoint_eval_queue.md`
- post-checkpoint execution plan: `../3_evaluation/post_checkpoint_execution_plan.md`
- post-checkpoint command consistency audit: `../3_evaluation/post_checkpoint_command_consistency.md`
- post-checkpoint preflight audit: `../3_evaluation/post_checkpoint_preflight.md`
- post-checkpoint paired runner: `../../../../scripts/run_v5_post_checkpoint_evals.sh`
- table sync audit: `table_sync_audit.md`
- objective completion audit: `objective_completion_audit.md`
- final deliverable audit: `final_deliverable_audit.md`
- finalization gate status: `finalization_gate_status.md`
- reporting package audit: `reporting_package_audit.md`
- final package checklist: `final_package_checklist.md`
- folder README audit: `../folder_readme_audit.md`

Canonical refresh command:

```bash
python3 scripts/refresh_v5_reporting.py
```

## Stage Exit Line

The report package is complete only after all of the following are true:

- `00_tables/` contains final tables copied or generated from measured results.
- `current_result_snapshot.md` summarizes current measured rows and open gates.
- `table_sync_audit.md` says `ready` after every measured result is promoted.
- `feedback_alignment_audit.md` confirms the local feedback requirements are
  mapped to concrete evidence and remaining gates.
- `artifact_reference_audit.md` confirms local report/PPT artifact references
  resolve to existing files.
- `claim_promotion_matrix.md` says which claims are currently promotable,
  still locked, or disallowed for the final report/PPT.
- `final_claim_decision_tree.md` selects the allowed final conclusion block
  from parsed v5 rows and current coverage gates.
- `final_claim_freeze_audit.md` confirms that pending/disallowed claims remain
  locked and that report/PPT conclusion wording follows the decision tree.
- `metric_fidelity_audit.md` confirms every Glot500 metric family is linked to
  requirements, wrapper/mapping, coverage, aggregation completion, and the
  metric fidelity table.
- `reproducibility_audit.md` confirms local roots, target set, canonical
  commands, model keys, metric families, promotion rules, and handoff commands
  are present in the final reproducibility package.
- `method_comparison_summary.md` centralizes FVT-vs-random zero-step evidence
  and later after-MLM/downstream comparisons.
- `result_slot_inventory.md` lists the exact report/PPT slots that must be
  replaced after post-checkpoint results are parsed.
- `post_result_update_manifest.md` gives the metric-by-metric first command,
  evidence, report target, slide target, and claim rule for post-result edits.
- `post_result_patch_plan_ko.md` gives the file-by-file report/PPT patch order
  after parsed post-checkpoint rows and provenance checks.
- `post_checkpoint_trigger_card_ko.md` gives the one-page Go/No-Go and command
  sequence after `v5_fvt` reaches wrapper-ready and the post-checkpoint preflight
  verdict is ready-to-launch.
- `post_checkpoint_outcome_matrix_ko.md` fixes the Korean report/PPT conclusion
  wording for positive, mixed, early-only, negative, and incomplete outcomes.
- `final_result_update_checklist_ko.md` gives the Korean Go/No-Go checklist
  and exact report/PPT replacement slots after matched checkpoints.
- `refresh_sequence_sync_audit.md` confirms the result insertion matrix and
  `scripts/refresh_v5_reporting.py` agree on the post-result refresh path.
- `../3_evaluation/post_checkpoint_execution_plan.md` gives the exact guarded
  launch line, runtime env, output/log locations, and promotion rule for the
  post-checkpoint pass.
- `../3_evaluation/post_checkpoint_command_consistency.md` checks that the
  canonical post-checkpoint command does not drift across runbooks, report, or
  slide files.
- `../3_evaluation/post_checkpoint_preflight.md` checks that the paired model
  rows, selected checkpoint manifest, metric queue, parser contract, and
  handoff links agree before the long paired evaluation is launched.
- `narrative_quality_audit.md` confirms the report/PPT prose has complete
  sections, slide/script coverage, source boundaries, and no stale draft markers.
- `final_handoff_runbook.md` gives the dynamic phase-by-phase command path from
  current gates to final report/PPT freeze.
- `final_freeze_protocol_ko.md` gives the Korean freeze/no-freeze checklist for
  report/PPT submission.
- `final_freeze_evidence_checklist_ko.md` gives the short evidence checklist
  for deciding whether final report/PPT freeze is actually proven.
- `final_submission_handoff_ko.md` gives the Korean report/PPT assembly order,
  safe current conclusion, and post-checkpoint replacement targets.
- `result_delay_contingency_ko.md` defines what may be shared as an execution
  draft if matched post-checkpoint v5 rows are delayed, without weakening the
  final objective.
- `final_goal_acceptance_rubric_ko.md` maps the user's original objective to
  acceptance criteria, evidence, current status, and final gates.
- `reviewer_response_crosswalk_ko.md` maps likely reviewer/presentation
  questions to short answers, evidence files, claim locks, and post-result
  update rules.
- `execution_readiness_review_ko.md` gives the short Korean answer to whether
  the real goal is execution-ready and which final claims remain locked.
- `01_figures/` contains final figures with source data paths recorded.
- `02_slides/` has a presentation outline or final deck synced to the report.
- `report_slide_crosswalk.md` confirms report sections, slides, and evidence
  files point to the same measured artifacts.
- `03_final_report/` points to the final polished report package.
- `../Report.md` has no unresolved result slots for metrics that were run.

Minimum artifact line:

```text
tables synced + figures synced + slides synced + final report synced
```

If this line is not met, presentation materials should be labeled draft.
