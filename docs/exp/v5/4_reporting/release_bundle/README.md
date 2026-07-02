# v5 Report/PPT Release Bundle

Last built: 2026-06-28 18:08 KST

Verdict: `release_bundle_ready`

Status: `EXECUTION_DRAFT_NOT_FINAL`

This bundle collects the current report/PPT handoff artifacts for review.
It does not mean final v5 method results are complete. Final after-MLM
and downstream claims remain locked until matched `v5_random` and
`v5_fvt` checkpoints, post-checkpoint preflight, and parsed runner outputs are ready.

Primary files:

- `reports/paper_draft_ko.pdf`: Korean paper-style report.
- `reports/paper_draft.pdf`: English paper-style report.
- `reports/paper_draft_ko.html`: browser-readable Korean report.
- `reports/paper_draft.html`: browser-readable English report.
- `reports/result_interpretation_blocks.md`: template-only final abstract/conclusion outcome blocks.
- `reports/manuscript_completion_matrix.md`: report section-level completion gates.
- `reports/paper_build_spec.md`: final paper assembly and rebuild checklist.
- `reports/references.bib`: BibTeX references for cited papers and code artifacts.
- `reports/citation_source_map.md`: paper claim-to-citation boundary map.
- `reports/external_source_verification.md`: primary-source verification for Glot500/Yamaguchi lineage wording.
- `slides/v5_final_deck_ko.pptx`: PowerPoint deck.
- `slides/v5_final_deck_ko.pdf`: review/share deck PDF.
- `slides/presenter_script_ko.md`: Korean presenter script.
- `slides/defense_qa_ko.md`: Korean presentation Q&A card.
- `slides/rehearsal_plan_ko.md`: timing and compression plan.
- `slides/slide_claim_checklist.md`: slide-level claim locks.
- `slides/slide_completion_matrix.md`: slide-level evidence and finalization gates.
- `slides/deck_build_spec.md`: PPT assembly and rebuild checklist.
- `slides/slide_asset_manifest.md`: slide-to-asset/source map.
- `slides/slide_citation_map.md`: slide-level citation and local-evidence boundary map.
- `handoff/presentation_readiness_checklist_ko.md`: five-minute pre-talk claim-lock and file-opening checklist.
- `handoff/submission_file_index_ko.md`: which report/PPT files to open for submission and rehearsal.
- `handoff/reviewer_response_crosswalk_ko.md`: likely reviewer questions mapped to answers, evidence, and claim locks.
- `handoff/final_submission_handoff_ko.md`: what to update after checkpoints and preflight.
- `handoff/objective_requirement_trace_ko.md`: active-goal readiness answers for execution, reproduction, novelty, downstream, and final report/PPT.
- `handoff/objective_completion_audit.md`: strict requirement-by-requirement active-goal completion audit.
- `handoff/goal_readiness.md`: top-level execution-readiness verdict for the v5 archive.
- `handoff/goal_readiness.tsv`: machine-readable top-level execution-readiness rows.
- `handoff/folder_readme_audit.md`: README and next-step coverage across the experiment tree.
- `handoff/final_goal_acceptance_rubric_ko.md`: Korean acceptance criteria for the original objective.
- `handoff/final_result_update_checklist_ko.md`: Korean Go/No-Go and result insertion checklist.
- `handoff/post_checkpoint_trigger_card_ko.md`: one-page Go/No-Go card before long paired eval.
- `handoff/post_checkpoint_outcome_matrix_ko.md`: Korean conclusion matrix after post-checkpoint results.
- `handoff/post_result_patch_plan_ko.md`: file-by-file report/PPT patch plan after parsed post-checkpoint results.
- `handoff/final_freeze_evidence_checklist_ko.md`: five-minute final-freeze evidence checklist.
- `final_claim_decision_tree.md`: generated allowed conclusion state from parsed results and gates.
- `claim_promotion_matrix.md`: claim-to-gate upgrade matrix for report/PPT wording.
- `handoff/final_action_dashboard_ko.md`: current state, next command, open gates, and report/PPT update targets.
- `handoff/final_assembly_manifest.md`: final report/PPT assembly map, including presentation handoff status.
- `handoff/result_delay_contingency_ko.md`: execution-draft sharing boundary if post-checkpoint v5 rows are delayed.
- `handoff/post_checkpoint_execution_plan.md`: exact guarded launch plan.
- `handoff/post_checkpoint_eval_recovery.md`: split/rerun recovery protocol and single-model claim-source guard.
- `scripts/run_v5_ready_to_final_package.sh`: one-shot guarded launcher for ready-to-final-package execution.
- `audits/training_loss_snapshot.md`: Trainer-log loss snapshot for live paired MLM progress; not a final metric claim.
- `audits/post_checkpoint_provenance_audit.md`: verifies source files, run metadata, command logs, and queued v5 result destinations.
- `handoff/result_insertion_matrix.md`: raw-output to report/PPT promotion and non-promotion rules.
- `handoff/result_slot_inventory.md`: exact report/PPT slots that wait for parsed results.
- `handoff/pending_result_registry.md`: explicit pending/running/blocked status labels.
- `handoff/report_slide_crosswalk.md`: report-section to slide/evidence synchronization map.
- `handoff/final_package_checklist.md`: final report/PPT package checklist.
- `handoff/source_map.md`: table, figure, claim, and handoff source map.
- `audits/final_submission_smoke_audit.md`: one-page share/freeze sanity check.
- `tables/table_01_data_scope.md`: data scope and target10 selection evidence.
- `tables/table_02_tokenizer_audit.md`: tokenizer expansion/fertility evidence.
- `tables/table_03_initialization_zero_step.md`: initialization and zero-step evidence.
- `tables/table_04_evaluation_coverage.md`: local/head/target10 coverage accounting.
- `tables/table_05_training_status.md`: live MLM/checkpoint readiness accounting.
- `tables/table_06_pppl_partial.md` through `tables/table_12_bible_partial.md`: partial baseline/reference metric tables.
- `tables/table_13_metric_fidelity_matrix.md`: Glot500 metric-family retention and caveat matrix.
- `tables/table_14_roundtrip_partial.md`: Roundtrip baseline/reference rows and target10 coverage caveat.
- `tables/table_15_glot500_reproduction_fidelity.md`: controlled-subset replay fidelity defense.
- `figures/figure_plan.md`: figure set, source files, and refresh rules.
- `figures/captions.md`: report/PPT figure captions.
- `figures/figure_manifest.tsv`: machine-readable figure manifest.
- `figures/figure_01_experiment_pipeline.png`: overview of the controlled replay and initialization novelty flow.
- `figures/figure_02_tokenizer_fertility_delta.png`: tokenizer fertility delta visual evidence.
- `figures/figure_03_zero_step_initialization.png`: zero-step initialization visual evidence.
- `figures/figure_05_evaluation_coverage.png`: metric coverage visual evidence.
- `handoff/metric_execution_ledger.md`: one-page measured/waiting/coverage ledger for every retained metric family.
- `audits/metric_surface_completeness_audit.md`: checks source and rendered report/PPT surfaces mention every retained metric family.
- `audits/rendered_artifact_freshness_audit.md`: checks report/PPT HTML/PDF/PPTX artifacts are fresh relative to source edits.
- `audits/deliverable_openability_audit.md`: checks original report/PPT PDF/PPTX/HTML artifacts are structurally openable.
- `handoff/release_manifest.md`: source artifact sizes and hashes.
- `audits/method_comparison_summary.md`: novelty method comparison and decision-tree input summary.
- `audits/comparison_materiality_audit.md`: practical tie/small/moderate/large bands for FVT-vs-random wording.
- `audits/result_insertion_contract_audit.md`: metric insertion paths plus post-result wrapper command support.
- `audits/claim_source_contract_audit.md`: final numeric-claim source and patch-target contract.

Bundle contents:

| Bundle Path | Status | Bytes | Source | Role |
| --- | --- | ---: | --- | --- |
| `reports/paper_draft.pdf` | copied | 127722 | `4_reporting/03_final_report/paper_draft.pdf` | English paper-style report PDF |
| `reports/paper_draft_ko.pdf` | copied | 210539 | `4_reporting/03_final_report/paper_draft_ko.pdf` | Korean paper-style report PDF |
| `reports/paper_draft.html` | copied | 42091 | `4_reporting/03_final_report/paper_draft.html` | English browser-readable report |
| `reports/paper_draft_ko.html` | copied | 30967 | `4_reporting/03_final_report/paper_draft_ko.html` | Korean browser-readable report |
| `reports/paper_draft.md` | copied | 31375 | `4_reporting/03_final_report/paper_draft.md` | English report source |
| `reports/paper_draft_ko.md` | copied | 23944 | `4_reporting/03_final_report/paper_draft_ko.md` | Korean report source |
| `reports/contribution_summary.md` | copied | 5087 | `4_reporting/03_final_report/contribution_summary.md` | Current contribution and novelty claim summary |
| `reports/result_interpretation_blocks.md` | copied | 20266 | `4_reporting/03_final_report/result_interpretation_blocks.md` | Outcome-conditioned final abstract/conclusion blocks |
| `reports/manuscript_completion_matrix.md` | copied | 7460 | `4_reporting/03_final_report/manuscript_completion_matrix.md` | Section-level manuscript completion and claim gates |
| `reports/paper_build_spec.md` | copied | 11019 | `4_reporting/03_final_report/paper_build_spec.md` | Paper assembly and rebuild specification |
| `reports/references.bib` | copied | 1845 | `4_reporting/03_final_report/references.bib` | BibTeX references for report/PPT citations |
| `reports/citation_source_map.md` | copied | 3133 | `4_reporting/03_final_report/citation_source_map.md` | Paper claim-to-citation boundary map |
| `reports/external_source_verification.md` | copied | 4216 | `4_reporting/03_final_report/external_source_verification.md` | Primary-source verification for bibliography and method-lineage wording |
| `slides/v5_final_deck_ko.pptx` | copied | 30236 | `4_reporting/02_slides/v5_final_deck_ko.pptx` | PowerPoint deck |
| `slides/v5_final_deck_ko.pdf` | copied | 80525 | `4_reporting/02_slides/v5_final_deck_ko.pdf` | PDF deck export |
| `slides/v5_final_deck_ko.html` | copied | 16259 | `4_reporting/02_slides/v5_final_deck_ko.html` | Browser rehearsal deck |
| `slides/final_deck_ko.md` | copied | 9241 | `4_reporting/02_slides/final_deck_ko.md` | Korean slide source |
| `slides/presenter_script_ko.md` | copied | 18148 | `4_reporting/02_slides/presenter_script_ko.md` | Korean presenter script |
| `slides/rehearsal_plan_ko.md` | copied | 10075 | `4_reporting/02_slides/rehearsal_plan_ko.md` | Korean rehearsal timing plan |
| `slides/slide_claim_checklist.md` | copied | 3310 | `4_reporting/02_slides/slide_claim_checklist.md` | Slide claim lock checklist |
| `slides/slide_completion_matrix.md` | copied | 5878 | `4_reporting/02_slides/slide_completion_matrix.md` | Slide-level completion and finalization gates |
| `slides/deck_build_spec.md` | copied | 8801 | `4_reporting/02_slides/deck_build_spec.md` | Deck assembly and rebuild specification |
| `slides/slide_asset_manifest.md` | copied | 7318 | `4_reporting/02_slides/slide_asset_manifest.md` | Slide-to-asset/source manifest |
| `slides/slide_asset_manifest.tsv` | copied | 6465 | `4_reporting/02_slides/slide_asset_manifest.tsv` | Machine-readable slide asset manifest |
| `slides/slide_citation_map.md` | copied | 3993 | `4_reporting/02_slides/slide_citation_map.md` | Slide-to-citation and slide-to-local-evidence map |
| `slides/defense_qa_ko.md` | copied | 13909 | `4_reporting/02_slides/defense_qa_ko.md` | Korean presentation Q&A card |
| `slides/defense_qa.md` | copied | 11637 | `4_reporting/02_slides/defense_qa.md` | English presentation Q&A |
| `slides/novelty_defense_matrix_ko.md` | copied | 8651 | `4_reporting/02_slides/novelty_defense_matrix_ko.md` | Korean novelty/reproduction Q&A defense matrix |
| `handoff/one_page_summary_ko.md` | copied | 9170 | `4_reporting/one_page_summary_ko.md` | Korean one-page summary |
| `handoff/presentation_readiness_checklist_ko.md` | copied | 4904 | `4_reporting/presentation_readiness_checklist_ko.md` | Korean five-minute pre-talk readiness checklist |
| `handoff/submission_file_index_ko.md` | copied | 5632 | `4_reporting/submission_file_index_ko.md` | Korean submission and presentation file index |
| `handoff/reviewer_response_crosswalk_ko.md` | copied | 7985 | `4_reporting/reviewer_response_crosswalk_ko.md` | Korean reviewer/presentation question-to-evidence crosswalk |
| `handoff/final_submission_handoff_ko.md` | copied | 11043 | `4_reporting/final_submission_handoff_ko.md` | Final assembly handoff |
| `handoff/objective_requirement_trace_ko.md` | copied | 9528 | `4_reporting/objective_requirement_trace_ko.md` | Korean active-goal requirement readiness trace |
| `handoff/objective_requirement_trace_ko.tsv` | copied | 7883 | `4_reporting/objective_requirement_trace_ko.tsv` | Machine-readable active-goal requirement trace |
| `handoff/objective_completion_audit.md` | copied | 10369 | `4_reporting/objective_completion_audit.md` | Strict active-goal completion audit |
| `handoff/objective_completion_audit.tsv` | copied | 9098 | `4_reporting/objective_completion_audit.tsv` | Machine-readable active-goal completion audit |
| `handoff/goal_readiness.md` | copied | 5628 | `goal_readiness.md` | Top-level v5 execution readiness audit |
| `handoff/goal_readiness.tsv` | copied | 3269 | `goal_readiness.tsv` | Machine-readable top-level v5 execution readiness audit |
| `handoff/folder_readme_audit.md` | copied | 19870 | `folder_readme_audit.md` | Per-folder README and next-step audit |
| `handoff/folder_readme_audit.tsv` | copied | 17876 | `folder_readme_audit.tsv` | Machine-readable per-folder README audit |
| `handoff/final_goal_acceptance_rubric_ko.md` | copied | 10819 | `4_reporting/final_goal_acceptance_rubric_ko.md` | Korean final goal acceptance rubric |
| `handoff/final_result_update_checklist_ko.md` | copied | 13268 | `4_reporting/final_result_update_checklist_ko.md` | Korean post-result update checklist |
| `handoff/post_checkpoint_trigger_card_ko.md` | copied | 5288 | `4_reporting/post_checkpoint_trigger_card_ko.md` | One-page post-checkpoint Go/No-Go trigger card |
| `handoff/post_checkpoint_outcome_matrix_ko.md` | copied | 11938 | `4_reporting/post_checkpoint_outcome_matrix_ko.md` | Korean post-checkpoint outcome matrix |
| `handoff/post_result_patch_plan_ko.md` | copied | 11971 | `4_reporting/post_result_patch_plan_ko.md` | Korean file-by-file post-result report/PPT patch plan |
| `handoff/post_result_patch_plan.tsv` | copied | 8463 | `4_reporting/post_result_patch_plan.tsv` | Machine-readable post-result report/PPT patch plan |
| `handoff/final_freeze_protocol_ko.md` | copied | 9817 | `4_reporting/final_freeze_protocol_ko.md` | Freeze/no-freeze protocol |
| `handoff/final_freeze_evidence_checklist_ko.md` | copied | 4643 | `4_reporting/final_freeze_evidence_checklist_ko.md` | Korean final freeze evidence checklist |
| `handoff/final_handoff_runbook.md` | copied | 7420 | `4_reporting/final_handoff_runbook.md` | Dynamic post-checkpoint runbook |
| `handoff/final_action_dashboard_ko.md` | copied | 10092 | `4_reporting/final_action_dashboard_ko.md` | Korean final next-action dashboard |
| `handoff/final_action_dashboard_ko.tsv` | copied | 7790 | `4_reporting/final_action_dashboard_ko.tsv` | Machine-readable final next-action dashboard |
| `handoff/final_assembly_manifest.md` | copied | 3934 | `4_reporting/final_assembly_manifest.md` | Final report/PPT assembly manifest |
| `handoff/final_assembly_manifest.tsv` | copied | 3004 | `4_reporting/final_assembly_manifest.tsv` | Machine-readable final assembly manifest |
| `handoff/result_delay_contingency_ko.md` | copied | 5752 | `4_reporting/result_delay_contingency_ko.md` | Korean execution-draft result-delay contingency |
| `final_claim_decision_tree.md` | copied | 2867 | `4_reporting/final_claim_decision_tree.md` | Generated final conclusion decision tree |
| `final_claim_decision_tree.tsv` | copied | 2559 | `4_reporting/final_claim_decision_tree.tsv` | Machine-readable final conclusion decision tree |
| `claim_promotion_matrix.md` | copied | 4416 | `4_reporting/claim_promotion_matrix.md` | Claim-to-gate promotion matrix |
| `claim_promotion_matrix.tsv` | copied | 3459 | `4_reporting/claim_promotion_matrix.tsv` | Machine-readable claim promotion matrix |
| `handoff/post_checkpoint_execution_plan.md` | copied | 7837 | `3_evaluation/post_checkpoint_execution_plan.md` | Concrete post-checkpoint launch plan |
| `handoff/post_checkpoint_eval_recovery.md` | copied | 7628 | `3_evaluation/post_checkpoint_eval_recovery.md` | Post-checkpoint split/rerun recovery protocol |
| `handoff/metric_mapping.md` | copied | 6380 | `3_evaluation/metric_mapping.md` | Glot500 metric-to-wrapper/evaluator mapping |
| `handoff/glot500_metric_requirements.md` | copied | 4173 | `3_evaluation/glot500_metric_requirements.md` | Retained Glot500 metric-family requirements |
| `audits/training_loss_snapshot.md` | copied | 2019 | `2_training/training_loss_snapshot.md` | Trainer-log loss snapshot for live paired MLM progress |
| `audits/training_loss_snapshot.tsv` | copied | 31183 | `2_training/training_loss_snapshot.tsv` | Machine-readable Trainer-log loss rows |
| `audits/post_checkpoint_provenance_audit.md` | copied | 13960 | `3_evaluation/post_checkpoint_provenance_audit.md` | Post-checkpoint source/run_meta/log provenance audit |
| `audits/post_checkpoint_provenance_audit.tsv` | copied | 12357 | `3_evaluation/post_checkpoint_provenance_audit.tsv` | Machine-readable post-checkpoint provenance audit |
| `handoff/result_insertion_matrix.md` | copied | 11586 | `4_reporting/result_insertion_matrix.md` | Raw-output to report/PPT promotion rule matrix |
| `handoff/result_slot_inventory.md` | copied | 15072 | `4_reporting/result_slot_inventory.md` | Report/PPT pending-result slot inventory |
| `handoff/result_slot_inventory.tsv` | copied | 16018 | `4_reporting/result_slot_inventory.tsv` | Machine-readable report/PPT result slot inventory |
| `handoff/pending_result_registry.md` | copied | 5725 | `4_reporting/pending_result_registry.md` | Explicit pending/running/blocked label registry |
| `handoff/post_result_update_manifest.md` | copied | 6050 | `4_reporting/post_result_update_manifest.md` | Metric-by-metric report/PPT update manifest |
| `handoff/report_slide_crosswalk.md` | copied | 6146 | `4_reporting/report_slide_crosswalk.md` | Report-section to slide/evidence crosswalk |
| `handoff/final_package_checklist.md` | copied | 33120 | `4_reporting/final_package_checklist.md` | Final package checklist |
| `handoff/source_map.md` | copied | 26469 | `4_reporting/00_tables/source_map.md` | Report/PPT source map |
| `tables/table_01_data_scope.md` | copied | 1415 | `4_reporting/00_tables/table_01_data_scope.md` | Data scope and target10 selection table |
| `tables/table_02_tokenizer_audit.md` | copied | 1381 | `4_reporting/00_tables/table_02_tokenizer_audit.md` | Tokenizer audit and fertility summary table |
| `tables/table_03_initialization_zero_step.md` | copied | 1259 | `4_reporting/00_tables/table_03_initialization_zero_step.md` | Initialization and zero-step comparison table |
| `tables/table_04_evaluation_coverage.md` | copied | 1940 | `4_reporting/00_tables/table_04_evaluation_coverage.md` | Evaluation coverage table |
| `tables/table_04_evaluation_coverage.tsv` | copied | 1093 | `4_reporting/00_tables/table_04_evaluation_coverage.tsv` | Machine-readable evaluation coverage table |
| `tables/table_05_training_status.md` | copied | 1627 | `4_reporting/00_tables/table_05_training_status.md` | Live MLM training and checkpoint readiness table |
| `tables/table_06_pppl_partial.md` | copied | 1765 | `4_reporting/00_tables/table_06_pppl_partial.md` | Partial PPPL baseline/reference results table |
| `tables/table_07_tatoeba_partial.md` | copied | 1724 | `4_reporting/00_tables/table_07_tatoeba_partial.md` | Partial Tatoeba baseline/reference results table |
| `tables/table_08_text_classification_partial.md` | copied | 1291 | `4_reporting/00_tables/table_08_text_classification_partial.md` | Partial text classification baseline/reference results table |
| `tables/table_09_blocked_metric_notes.md` | copied | 2201 | `4_reporting/00_tables/table_09_blocked_metric_notes.md` | Blocked and coverage-limited metric note table |
| `tables/table_10_ner_partial.md` | copied | 1717 | `4_reporting/00_tables/table_10_ner_partial.md` | Partial NER baseline/reference results table |
| `tables/table_11_pos_partial.md` | copied | 1376 | `4_reporting/00_tables/table_11_pos_partial.md` | Partial POS baseline/reference results table |
| `tables/table_12_bible_partial.md` | copied | 2438 | `4_reporting/00_tables/table_12_bible_partial.md` | Partial Bible retrieval baseline/reference results table |
| `tables/table_13_metric_fidelity_matrix.md` | copied | 4271 | `4_reporting/00_tables/table_13_metric_fidelity_matrix.md` | Glot500 metric-family fidelity matrix |
| `tables/table_14_roundtrip_partial.md` | copied | 2442 | `4_reporting/00_tables/table_14_roundtrip_partial.md` | Roundtrip baseline/reference partial results table |
| `tables/table_15_glot500_reproduction_fidelity.md` | copied | 3887 | `4_reporting/00_tables/table_15_glot500_reproduction_fidelity.md` | Glot500 controlled-subset reproduction fidelity matrix |
| `figures/figure_plan.md` | copied | 2876 | `4_reporting/01_figures/figure_plan.md` | Planned report/PPT figure set and refresh rules |
| `figures/captions.md` | copied | 1923 | `4_reporting/01_figures/generated/captions.md` | Generated figure captions |
| `figures/figure_manifest.tsv` | copied | 1782 | `4_reporting/01_figures/generated/figure_manifest.tsv` | Machine-readable figure manifest |
| `figures/figure_01_experiment_pipeline.png` | copied | 192288 | `4_reporting/01_figures/generated/figure_01_experiment_pipeline.png` | Experiment pipeline overview figure |
| `figures/figure_01_experiment_pipeline.svg` | copied | 80712 | `4_reporting/01_figures/generated/figure_01_experiment_pipeline.svg` | Experiment pipeline overview figure source |
| `figures/figure_02_tokenizer_fertility_delta.png` | copied | 138768 | `4_reporting/01_figures/generated/figure_02_tokenizer_fertility_delta.png` | Tokenizer fertility delta figure |
| `figures/figure_02_tokenizer_fertility_delta.svg` | copied | 57339 | `4_reporting/01_figures/generated/figure_02_tokenizer_fertility_delta.svg` | Tokenizer fertility delta figure source |
| `figures/figure_03_zero_step_initialization.png` | copied | 62392 | `4_reporting/01_figures/generated/figure_03_zero_step_initialization.png` | Zero-step initialization comparison figure |
| `figures/figure_03_zero_step_initialization.svg` | copied | 32541 | `4_reporting/01_figures/generated/figure_03_zero_step_initialization.svg` | Zero-step initialization comparison figure source |
| `figures/figure_05_evaluation_coverage.png` | copied | 60816 | `4_reporting/01_figures/generated/figure_05_evaluation_coverage.png` | Evaluation coverage figure |
| `figures/figure_05_evaluation_coverage.svg` | copied | 33757 | `4_reporting/01_figures/generated/figure_05_evaluation_coverage.svg` | Evaluation coverage figure source |
| `handoff/metric_execution_ledger.md` | copied | 3709 | `4_reporting/metric_execution_ledger.md` | Retained Glot500 metric execution state ledger |
| `handoff/metric_execution_ledger.tsv` | copied | 2598 | `4_reporting/metric_execution_ledger.tsv` | Machine-readable retained metric execution ledger |
| `audits/metric_surface_completeness_audit.md` | copied | 4039 | `4_reporting/metric_surface_completeness_audit.md` | Source/rendered report/PPT visible metric-family completeness audit |
| `audits/metric_surface_completeness_audit.tsv` | copied | 2802 | `4_reporting/metric_surface_completeness_audit.tsv` | Machine-readable metric surface completeness audit |
| `audits/rendered_artifact_freshness_audit.md` | copied | 2506 | `4_reporting/rendered_artifact_freshness_audit.md` | Rendered report/PPT artifact freshness audit |
| `audits/rendered_artifact_freshness_audit.tsv` | copied | 1723 | `4_reporting/rendered_artifact_freshness_audit.tsv` | Machine-readable rendered artifact freshness audit |
| `audits/deliverable_openability_audit.md` | copied | 1684 | `4_reporting/deliverable_openability_audit.md` | Original report/PPT openability audit |
| `audits/deliverable_openability_audit.tsv` | copied | 1133 | `4_reporting/deliverable_openability_audit.tsv` | Machine-readable original report/PPT openability audit |
| `handoff/release_manifest.md` | copied | 16554 | `4_reporting/release_manifest.md` | File-size and hash manifest |
| `handoff/release_manifest.tsv` | copied | 22426 | `4_reporting/release_manifest.tsv` | Machine-readable release manifest |
| `audits/method_comparison_summary.md` | copied | 3819 | `4_reporting/method_comparison_summary.md` | Method comparison and decision-tree input summary |
| `audits/method_comparison_summary.tsv` | copied | 5636 | `4_reporting/method_comparison_summary.tsv` | Machine-readable method comparison summary |
| `audits/comparison_materiality_audit.md` | copied | 3986 | `4_reporting/comparison_materiality_audit.md` | Practical materiality bands for method comparison rows |
| `audits/comparison_materiality_audit.tsv` | copied | 3753 | `4_reporting/comparison_materiality_audit.tsv` | Machine-readable comparison materiality audit |
| `audits/result_insertion_contract_audit.md` | copied | 2506 | `4_reporting/result_insertion_contract_audit.md` | Post-result report/PPT insertion and command-support contract audit |
| `audits/result_insertion_contract_audit.tsv` | copied | 1405 | `4_reporting/result_insertion_contract_audit.tsv` | Machine-readable result insertion contract audit |
| `audits/claim_source_contract_audit.md` | copied | 7828 | `4_reporting/claim_source_contract_audit.md` | Report/PPT final numeric-claim source contract audit |
| `audits/claim_source_contract_audit.tsv` | copied | 6817 | `4_reporting/claim_source_contract_audit.tsv` | Machine-readable claim-source contract audit |
| `audits/reporting_package_audit.md` | copied | 41398 | `4_reporting/reporting_package_audit.md` | Package audit |
| `audits/final_deliverable_audit.md` | copied | 7989 | `4_reporting/final_deliverable_audit.md` | Goal deliverable audit |
| `audits/final_submission_smoke_audit.md` | copied | 2873 | `4_reporting/final_submission_smoke_audit.md` | Final share/freeze smoke audit |
| `audits/final_submission_smoke_audit.tsv` | copied | 1903 | `4_reporting/final_submission_smoke_audit.tsv` | Machine-readable final share/freeze smoke audit |
| `audits/execution_readiness_review_ko.md` | copied | 6033 | `4_reporting/execution_readiness_review_ko.md` | Korean readiness review |
| `audits/final_claim_freeze_audit.md` | copied | 2612 | `4_reporting/final_claim_freeze_audit.md` | Claim freeze audit |
| `audits/final_evidence_packet_audit.md` | copied | 3547 | `4_reporting/final_evidence_packet_audit.md` | Final evidence packet claim-promotion audit |
| `audits/final_evidence_packet_audit.tsv` | copied | 2736 | `4_reporting/final_evidence_packet_audit.tsv` | Machine-readable final evidence packet claim-promotion audit |
| `audits/result_promotion_readiness_audit.md` | copied | 3080 | `4_reporting/result_promotion_readiness_audit.md` | Result-promotion readiness audit |
| `audits/metric_fidelity_audit.md` | copied | 2996 | `4_reporting/metric_fidelity_audit.md` | Glot500 metric fidelity audit |
| `audits/slide_rendering_audit.md` | copied | 1035 | `4_reporting/slide_rendering_audit.md` | Slide rendering and Markdown table leakage audit |
| `audits/slide_rendering_audit.tsv` | copied | 444 | `4_reporting/slide_rendering_audit.tsv` | Machine-readable slide rendering audit |
| `audits/surface_overclaim_audit.md` | copied | 3895 | `4_reporting/surface_overclaim_audit.md` | Report/PPT overclaim surface audit |
| `audits/refresh_sequence_sync_audit.md` | copied | 1624 | `4_reporting/refresh_sequence_sync_audit.md` | Refresh sequence sync audit |
| `audits/post_checkpoint_command_consistency.md` | copied | 3390 | `3_evaluation/post_checkpoint_command_consistency.md` | Canonical post-checkpoint command audit |
| `audits/post_checkpoint_preflight.md` | copied | 2814 | `3_evaluation/post_checkpoint_preflight.md` | Machine-readable post-checkpoint Go/No-Go preflight audit |
| `audits/post_checkpoint_preflight.tsv` | copied | 1941 | `3_evaluation/post_checkpoint_preflight.tsv` | Machine-readable post-checkpoint preflight rows |
| `scripts/run_v5_ready_to_final_package.sh` | copied | 2876 | `../../../scripts/run_v5_ready_to_final_package.sh` | One-shot ready-to-final-package guarded launcher |
| `audits/checkpoint_selection_contract_audit.md` | copied | 1384 | `2_training/05_checkpoint_selection/checkpoint_selection_contract_audit.md` | Fixed 10K checkpoint selection contract audit |
| `audits/live_training_health.md` | copied | 1681 | `2_training/live_training_health.md` | Live MLM training health audit |
| `audits/storage_readiness.md` | copied | 2999 | `2_training/storage_readiness.md` | Storage/output readiness audit |
| `audits/paired_launcher_transition.md` | copied | 1642 | `2_training/paired_launcher_transition.md` | Random-to-FVT paired launcher transition audit |

Next execution gate:

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_ready_to_final_package.sh
```

Use the one-shot launcher when you want evaluation, refresh, and
final evidence-packet checks in one guarded pass. For intentional
full remeasurement, use the canonical wrapper directly:

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
python3 scripts/refresh_v5_reporting.py --with-plots
```

Only run the long evaluation command after both v5 model rows are
`ready_for_wrapper=yes` and `post_checkpoint_preflight.md` says
`post_checkpoint_preflight_ready_to_launch`.
