# v5 Final Report/PPT Package Checklist

Last updated: 2026-06-28 KST

This checklist defines what remains before the v5 deliverable can be treated as
the final report and final presentation package.

## Current Package State

| Artifact | Current file | Status |
| --- | --- | --- |
| living report draft | `../Report.md` | execution draft with measured baseline rows and pending v5 rows |
| Korean one-page summary | `one_page_summary_ko.md` | ready handout for report/PPT discussion and rehearsal |
| Korean submission file index | `submission_file_index_ko.md` | first-open file for choosing report/PPT PDFs, PPTX, rehearsal notes, and bundle handoff artifacts |
| Korean presentation readiness checklist | `presentation_readiness_checklist_ko.md` | 5-minute pre-talk claim-lock and file-opening checklist |
| standalone paper draft | `03_final_report/paper_draft.md` | paper-style draft from current evidence |
| standalone paper HTML | `03_final_report/paper_draft.html` | browser/print English paper artifact generated from `paper_draft.md` |
| standalone paper PDF | `03_final_report/paper_draft.pdf` | PDF English paper artifact generated from `paper_draft.html` |
| Korean paper-style draft | `03_final_report/paper_draft_ko.md` | Korean report body source for final report/PPT writing |
| Korean paper HTML | `03_final_report/paper_draft_ko.html` | browser/print Korean report artifact generated from `paper_draft_ko.md` |
| Korean paper PDF | `03_final_report/paper_draft_ko.pdf` | PDF Korean report artifact generated from `paper_draft_ko.html` |
| paper build spec | `03_final_report/paper_build_spec.md` | assembly checklist for the final report |
| bibliography | `03_final_report/references.bib` | BibTeX entries for cited papers and code artifacts |
| citation source map | `03_final_report/citation_source_map.md` | claim-to-reference boundary map |
| external source verification | `03_final_report/external_source_verification.md` | primary-source check for bibliography and method-lineage wording |
| slide content draft | `02_slides/ppt_content.md` | complete outline with explicit result gates and live status |
| Korean final deck source | `02_slides/final_deck_ko.md` | PPT 제작용 15-slide Korean source, execution draft |
| Korean HTML deck | `02_slides/v5_final_deck_ko.html` | browser-presentable deck generated from `final_deck_ko.md` for rehearsal and presentation |
| Korean PPTX deck | `02_slides/v5_final_deck_ko.pptx` | PowerPoint handoff deck generated from `final_deck_ko.md` |
| Korean deck PDF | `02_slides/v5_final_deck_ko.pdf` | PDF deck export generated from `v5_final_deck_ko.pptx` for review/sharing |
| Korean presenter script | `02_slides/presenter_script_ko.md` | ready for rehearsal, still execution draft |
| Korean rehearsal plan | `02_slides/rehearsal_plan_ko.md` | timing, compression, transition, and Q&A rehearsal plan for 5/8/12/15-minute talks |
| Korean defense Q&A card | `02_slides/defense_qa_ko.md` | short Korean answers for likely presentation questions |
| slide claim checklist | `02_slides/slide_claim_checklist.md` | current |
| slide completion matrix | `02_slides/slide_completion_matrix.md` | slide-level evidence and finalization gates |
| slide deck build spec | `02_slides/deck_build_spec.md` | assembly checklist for the actual PPT |
| slide asset manifest | `02_slides/slide_asset_manifest.md` | generated slide-to-asset/source map for deck assembly |
| slide citation map | `02_slides/slide_citation_map.md` | slide-level citation and local-evidence boundary map |
| report-slide crosswalk | `report_slide_crosswalk.md` | section-to-slide-to-evidence map for final synchronization |
| table source map | `00_tables/source_map.md` | current |
| metric fidelity matrix | `00_tables/table_13_metric_fidelity_matrix.md` | Glot500 metric-family retention and coverage boundary defense |
| reproduction fidelity matrix | `00_tables/table_15_glot500_reproduction_fidelity.md` | controlled 92+10 Glot500-style replay boundary and fidelity defense |
| figure manifest | `01_figures/generated/figure_manifest.tsv` | current generated figures only |
| claim ledger | `03_final_report/claim_ledger.md` | current claim boundary |
| manuscript completion matrix | `03_final_report/manuscript_completion_matrix.md` | section-level paper completion and claim gates |
| reproducibility appendix | `03_final_report/reproducibility_appendix.md` | command/path appendix for final report |
| result interpretation blocks | `03_final_report/result_interpretation_blocks.md` | outcome-conditioned report/PPT wording, including final abstract update choices and Korean final conclusion choices for report conclusion and slide 14 |
| final claim decision tree | `final_claim_decision_tree.md` | generated conclusion-selection rule from parsed v5 rows and coverage gates |
| result insertion matrix | `result_insertion_matrix.md` | current promotion and update map |
| pending result registry | `pending_result_registry.md` | explicit pending/running/blocked label map |
| current result snapshot | `current_result_snapshot.md` | generated compact handoff of measured rows and open gates |
| MLM progress ETA | `../2_training/mlm_progress_eta.md` | generated operational status for paired 10K run; not a result artifact |
| live training health audit | `../2_training/live_training_health.md` | generated operational health/no-go guard for paired 10K run; not a result artifact |
| storage readiness audit | `../2_training/storage_readiness.md` | generated disk/path/writability guard for checkpoint save, FVT start, and evaluation outputs |
| paired launcher transition audit | `../2_training/paired_launcher_transition.md` | generated random-running/FVT-waiting guard for the detached paired launcher; not a result artifact |
| result slot inventory | `result_slot_inventory.md` | generated map of report/PPT slots to replace after v5 rows arrive, including `method_comparison_claim_gate` |
| post-result update manifest | `post_result_update_manifest.md` | generated metric-by-metric command/evidence/report/PPT/claim-rule map for final result insertion, including the novelty/method claim gate |
| post-result patch plan | `post_result_patch_plan_ko.md` | generated file-by-file patch order for report/PPT updates after parsed post-checkpoint rows arrive |
| metric fidelity audit | `metric_fidelity_audit.md` | generated check that all Glot500 metric families remain required, mapped, covered, aggregated, and tabled |
| metric surface completeness audit | `metric_surface_completeness_audit.md` | generated check that source and rendered report/PPT surfaces expose every retained Glot500 metric family |
| rendered artifact freshness audit | `rendered_artifact_freshness_audit.md` | generated check that report/PPT HTML/PDF/PPTX files are not stale relative to source Markdown/intermediate artifacts |
| reproducibility audit | `reproducibility_audit.md` | generated check that roots, target set, commands, model keys, metrics, and promotion rules are reproducible |
| method comparison summary | `method_comparison_summary.md` | generated FVT-vs-random comparison table for zero-step and post-checkpoint results |
| comparison materiality audit | `comparison_materiality_audit.md` | generated practical tie/small/moderate/large bands so FVT-vs-random deltas do not become over-strong claims |
| final evidence packet audit | `final_evidence_packet_audit.md` | generated final claim-promotion packet requiring checkpoint pair, metric rows, provenance, materiality, claim gate, patch targets, and final freeze in one refreshed package |
| final assembly manifest | `final_assembly_manifest.md` | generated one-page handoff map for report/PPT final assembly status |
| final handoff runbook | `final_handoff_runbook.md` | generated phase-by-phase command path from current gates to final report/PPT freeze |
| final action dashboard | `final_action_dashboard_ko.md` | generated Korean dashboard for current state, next command, open gates, claim locks, and report/PPT update targets |
| Korean final freeze protocol | `final_freeze_protocol_ko.md` | Korean freeze/no-freeze checklist for final report/PPT submission |
| Korean final freeze evidence checklist | `final_freeze_evidence_checklist_ko.md` | Korean short evidence checklist before calling report/PPT final |
| Korean final submission handoff | `final_submission_handoff_ko.md` | Korean one-stop assembly order for report, PPT, claim locks, and post-checkpoint replacement targets |
| Korean result-delay contingency | `result_delay_contingency_ko.md` | Korean execution-draft sharing boundary if matched post-checkpoint v5 rows are delayed |
| Korean final goal acceptance rubric | `final_goal_acceptance_rubric_ko.md` | Korean acceptance criteria mapping from original user goal to evidence and final gates |
| Korean reviewer response crosswalk | `reviewer_response_crosswalk_ko.md` | Korean question-to-evidence map for execution readiness, reproduction scope, novelty, downstream coverage, and claim locks |
| Korean execution readiness review | `execution_readiness_review_ko.md` | generated short answer for whether the real goal is execution-ready and which final claims remain locked |
| feedback alignment audit | `feedback_alignment_audit.md` | generated map from `feadback.md` requirements to evidence, novelty placement, and open result gates |
| artifact reference audit | `artifact_reference_audit.md` | generated check that local report/PPT artifact references resolve to existing files |
| claim promotion matrix | `claim_promotion_matrix.md` | generated claim-to-gate matrix for deciding which report/PPT claims can be upgraded after new results |
| narrative quality audit | `narrative_quality_audit.md` | generated prose-quality audit for paper sections, slide/script coverage, draft markers, forbidden claims, and source boundaries |
| final claim freeze audit | `final_claim_freeze_audit.md` | generated guard that checks pending/disallowed claims and conclusion wording before report/PPT freeze |
| result promotion readiness audit | `result_promotion_readiness_audit.md` | generated guard that checks matched checkpoints, v5 metric/model rows, final gates, and claim locks before upgrading method claims |
| selected checkpoint manifest | `../2_training/05_checkpoint_selection/selected_checkpoint_manifest.md` | generated selected-path and 10K readiness manifest |
| post-checkpoint eval queue | `../3_evaluation/post_checkpoint_eval_queue.md` | generated runnable/waiting/measured rows for required metric/model pairs |
| post-checkpoint execution plan | `../3_evaluation/post_checkpoint_execution_plan.md` | generated guarded launch plan with runtime env, output/log targets, and promotion rules |
| post-checkpoint command consistency audit | `../3_evaluation/post_checkpoint_command_consistency.md` | generated check that report/PPT/runbook commands use the canonical guarded launch form |
| post-checkpoint recovery runbook | `../3_evaluation/post_checkpoint_eval_recovery.md` | paired/split/individual rerun procedure and final promotion rules after checkpoint readiness |
| post-checkpoint parser contract audit | `../3_evaluation/post_checkpoint_parser_contract.md` | generated check that wrapper outputs and aggregation parser inputs agree before v5 result promotion |
| post-checkpoint provenance audit | `../3_evaluation/post_checkpoint_provenance_audit.md` | generated check that aggregated rows have source files, run metadata, command logs, and unique queued v5 result destinations |
| post-checkpoint preflight audit | `../3_evaluation/post_checkpoint_preflight.md` | machine-readable Go/No-Go guard; long paired evaluation is allowed only when verdict is `post_checkpoint_preflight_ready_to_launch` |
| post-checkpoint paired runner | `../../../../scripts/run_v5_post_checkpoint_evals.sh` | guarded launcher for PPPL and available downstream v5_random/v5_fvt rows |
| checkpoint watcher | `../../../../scripts/watch_v5_mlm_handoff.sh` | optional status-only polling handoff for matched v5 checkpoints |
| roundtrip readiness audit | `../3_evaluation/07_roundtrip_alignment/blocker_audit.md` | generated evidence for Roundtrip input/runner readiness, measured baseline/reference rows, and pending v5 rows |
| table sync audit | `table_sync_audit.md` | generated check that aggregation numbers appear in report tables |
| objective completion audit | `objective_completion_audit.md` | generated strict check from the active report/PPT objective to current evidence |
| final deliverable audit | `final_deliverable_audit.md` | generated goal-to-evidence completion audit |
| final deliverable audit TSV | `final_deliverable_audit.tsv` | generated machine-readable final deliverable audit |
| release manifest | `release_manifest.md` | generated file-size and SHA-256 manifest for report/PPT handoff artifacts |
| release manifest TSV | `release_manifest.tsv` | machine-readable release manifest for final package integrity checks |
| release bundle | `release_bundle/` | compact execution-draft report/PPT handoff folder for review/sharing |
| release bundle manifest | `release_bundle/bundle_manifest.tsv` | machine-readable list of files copied into the handoff bundle |
| release bundle audit | `release_bundle_audit.md` | generated check that bundle files exist and are readable |
| release bundle audit TSV | `release_bundle_audit.tsv` | machine-readable release bundle audit |
| finalization gate status | `finalization_gate_status.md` | generated status of the remaining final-result gates |
| reporting package audit | `reporting_package_audit.md` | generated report/PPT artifact and stale-result-slot consistency audit |

## Verification Commands

| Check | Command | Current status |
| --- | --- | --- |
| Python syntax health for reproducibility/evaluation code | `python3 -m compileall preprocessing tokenization modeling scripts evaluation` | passed on 2026-06-28 KST; generated `__pycache__` directories were removed after the check |
| report/PPT package consistency | `python3 scripts/audit_v5_reporting_package.py` | ready as execution draft; final result rows still pending |
| release bundle readability | `python3 scripts/audit_v5_release_bundle.py` | ready as execution draft |
| final share/freeze smoke | `python3 scripts/audit_v5_final_submission_smoke.py` | execution draft ready; launch readiness still waits for `v5_fvt` |

## Finalization Gates

The final package is not complete until all gates below are either satisfied or
explicitly marked as blocked with claim impact.

| Gate | Required evidence | Current status |
| --- | --- | --- |
| matched MLM checkpoints | `v5_random` and `v5_fvt` model files, checkpoint selection note, and post-checkpoint preflight verdict | pending pair; `v5_random_mlm_10k` is ready, `v5_fvt_mlm_10k` is still running, so post-checkpoint evaluation remains locked until both are `ready_for_wrapper=yes` and preflight is `post_checkpoint_preflight_ready_to_launch` |
| after-MLM PPPL | aggregation rows for `v5_random` and `v5_fvt` | pending checkpoints |
| comparison materiality | `comparison_materiality_audit.md` records `tie_band`/`small`/`moderate`/`large` bands for final comparison rows | waiting for post-checkpoint rows; zero-step rows currently banded |
| downstream baseline completion | parsed NER/POS `xlmr_base` rows, plus selected external-reference rows | PPPL/Tatoeba/Bible/Taxi1500/NER/POS/Roundtrip `xlmr_base` and `glot500_base` rows parsed where local data exists |
| v5 downstream replay | parsed Tatoeba, Bible, text classification, NER, POS, and Roundtrip rows for `v5_random` and `v5_fvt` where data exists | pending checkpoints |
| blocked and pending metric accounting | v5-FVT Bible checkpoint gap and generated Roundtrip readiness audit in result tables and limitations | partial; baseline/reference and v5-random Bible/Roundtrip rows measured, v5-FVT rows pending checkpoint, Roundtrip audit says `roundtrip_inputs_ready_pending_results` |
| final tables | `00_tables/` synchronized with `09_aggregation/` | partial |
| final figures | generated from final tables and current result artifacts | partial |
| final report | `paper_draft.md` has no unresolved measured-result slot | partial |
| final slides | slide results match final report and every numeric claim has a source | partial |

## Report/PPT Content Readiness

| Requirement | Evidence file | Current status |
| --- | --- | --- |
| Glot500-style reproduction boundary is explicit | `03_final_report/paper_draft.md`, `02_slides/ppt_content.md`, `03_final_report/claim_ledger.md` | ready |
| selected 92+10 data scope is documented | `../README.md`, `../Plan.md`, `03_final_report/paper_draft.md` | ready |
| vocabulary-extension novelty is separated from corpus novelty | `03_final_report/paper_draft.md`, `03_final_report/contribution_summary.md` | ready |
| all Glot500 metric families are retained | `../3_evaluation/glot500_metric_requirements.md`, `../3_evaluation/metric_mapping.md`, `03_final_report/paper_draft.md` | ready as protocol; execution partial |
| metric-family fidelity is defensible metric by metric | `00_tables/table_13_metric_fidelity_matrix.md` | ready for current measured rows and blockers |
| metric-family fidelity has generated audit guard | `metric_fidelity_audit.md` | ready for current measured rows and blockers |
| source/rendered report/PPT surfaces expose every retained metric family | `metric_surface_completeness_audit.md` | ready for current report/PPT sources and handoff artifacts; rerun after report or deck result-section changes |
| rendered report/PPT artifacts are fresh relative to sources | `rendered_artifact_freshness_audit.md` | ready when generated HTML/PDF/PPTX mtimes are current; rerun after report or deck source changes |
| reproducibility package has generated audit guard | `reproducibility_audit.md` | ready for current command/path package and pending checkpoint handoff |
| measured baseline/reference rows are source-tracked | `../3_evaluation/09_aggregation/`, `00_tables/` | partial but current |
| measured rows and gates have a compact handoff | `current_result_snapshot.md` | ready for current measured rows |
| live training can be monitored without overclaiming | `../2_training/mlm_progress_eta.md`, `../2_training/live_training_health.md` | ready as operational status only; no method-quality claim |
| checkpoint/evaluation storage can be checked before failure | `../2_training/storage_readiness.md` | ready as operational storage/path guard |
| random-to-FVT handoff can be checked before checkpoint evaluation | `../2_training/paired_launcher_transition.md` | ready as operational transition guard while random is complete and FVT is running |
| pending report/PPT result slots are inventoried | `result_slot_inventory.md` | ready as replacement map for post-checkpoint finalization, including `method_comparison_claim_gate` for novelty wording |
| metric-by-metric post-result update order is explicit | `post_result_update_manifest.md` | ready as the shortest command/evidence/report/PPT target map after v5 rows parse, including method-comparison claim promotion |
| file-by-file post-result patch order is explicit | `post_result_patch_plan_ko.md` | ready as the concrete report/PPT edit sequence after parsed v5 rows and provenance checks |
| post-result manifest commands are wrapper-supported | `result_insertion_contract_audit.md` | ready; manifest `first_command` rows are checked against supported `../../../../scripts/run_v5_post_checkpoint_evals.sh` modes and GPU bindings |
| FVT-vs-random comparison table is centralized | `method_comparison_summary.md` | zero-step rows ready; after-MLM/downstream rows pending |
| FVT-vs-random difference size is guarded | `comparison_materiality_audit.md` | zero-step rows are `large`; post-checkpoint rows remain `not_applicable` until measured |
| final claim promotion packet is audited | `final_evidence_packet_audit.md` | ready as a waiting-checkpoint guard; measured rows stay `measured but not promotable` until packet items close together |
| final command path is generated from current gates | `final_handoff_runbook.md` | ready as waiting-checkpoint handoff |
| current next-action dashboard is generated from current gates | `final_action_dashboard_ko.md` | ready as waiting-checkpoint dashboard |
| submission/rehearsal file-opening order is explicit | `presentation_readiness_checklist_ko.md`, `submission_file_index_ko.md`, `one_page_summary_ko.md`, `release_bundle/README.md` | ready as Korean first-open handoff; still execution draft until result gates close |
| final freeze/no-freeze rules are explicit | `final_freeze_protocol_ko.md` | ready as execution-draft freeze protocol |
| final freeze evidence is summarized | `final_freeze_evidence_checklist_ko.md` | ready as five-minute evidence checklist; final-ready waits for matched v5 rows |
| final report/PPT assembly handoff is written in Korean | `final_submission_handoff_ko.md` | ready as execution draft; use with final handoff runbook after checkpoints |
| result-delay sharing boundary is explicit | `result_delay_contingency_ko.md` | ready as execution-draft contingency; final method claims still wait for matched v5 rows |
| execution readiness answer is written in Korean | `execution_readiness_review_ko.md` | ready as generated goal-readiness answer; final result gates remain pending |
| reviewer/presentation question defense is cross-linked | `reviewer_response_crosswalk_ko.md` | ready as Korean crosswalk from likely questions to evidence files, locked claims, and post-result update rules |
| report and PPT sections share the same evidence map | `report_slide_crosswalk.md` | ready for current measured rows and gates |
| local feedback requirements are directly accounted for | `feedback_alignment_audit.md` | ready as alignment map; final result rows pending |
| local artifact references resolve | `artifact_reference_audit.md` | ready; all audited report/PPT artifact references resolve |
| final claims have explicit promotion gates | `claim_promotion_matrix.md` | ready; after-MLM/downstream claims remain locked until parsed v5 rows exist |
| result promotion has a metric/model/gate cross-check | `result_promotion_readiness_audit.md` | ready as waiting-checkpoint guard; final method claims remain locked |
| final abstract and conclusion wording have generated decision rules | `final_claim_decision_tree.md`; `03_final_report/result_interpretation_blocks.md`; `post_checkpoint_outcome_matrix_ko.md` | ready as execution draft; current decision is zero-step-only pending results; abstract update blocks and Korean outcome matrix are available for final report and slide 14 |
| final claim freeze has generated audit guard | `final_claim_freeze_audit.md` | ready as execution draft; current freeze verdict should remain waiting-for-results until v5 rows parse |
| paper/PPT prose passes narrative-quality checks | `narrative_quality_audit.md` | ready as execution draft; final conclusion still waits for result gates |
| measured rows are synchronized into report tables | `table_sync_audit.md` | ready for current measured rows |
| v5 method rows are final | `../3_evaluation/09_aggregation/` | pending matched checkpoints |
| final PPT can be rehearsed without overclaiming | `02_slides/presenter_script_ko.md`, `02_slides/slide_claim_checklist.md`, `02_slides/defense_qa_ko.md` | execution-draft ready |
| final PPT has timing and compression plan | `02_slides/rehearsal_plan_ko.md` | ready for 5/8/12/15-minute rehearsal variants |
| final PPT can be assembled from locked sources | `02_slides/deck_build_spec.md`, `02_slides/slide_asset_manifest.md` | execution-draft ready |
| final PPT can be rehearsed as a deck artifact | `02_slides/v5_final_deck_ko.html`, `scripts/build_v5_slide_html.py` | ready as generated browser deck; regenerate after slide source changes |
| final PPT can be opened as PowerPoint | `02_slides/v5_final_deck_ko.pptx`, `scripts/build_v5_slide_pptx.py` | ready as generated PPTX deck; regenerate after slide source changes |
| final PPT can be reviewed as PDF | `02_slides/v5_final_deck_ko.pdf`, `scripts/build_v5_slide_pdf.sh` | ready as generated PDF deck; regenerate after slide source changes |
| final PPT citation placement has source boundaries | `02_slides/slide_citation_map.md` | ready |
| final paper can be assembled from locked sources | `03_final_report/paper_build_spec.md`, `03_final_report/manuscript_completion_matrix.md` | execution-draft ready |
| final paper can be reviewed as HTML | `03_final_report/paper_draft.html`, `03_final_report/paper_draft_ko.html`, `scripts/build_v5_report_html.py` | ready as generated browser/print artifacts; regenerate after report source changes |
| final paper can be shared as PDF | `03_final_report/paper_draft.pdf`, `03_final_report/paper_draft_ko.pdf`, `scripts/build_v5_report_pdf.sh` | ready as generated PDF artifacts; regenerate after report source changes |
| final report/PPT package has integrity manifest | `release_manifest.md`, `release_manifest.tsv`, `scripts/write_v5_release_manifest.py` | ready as generated file-size/hash manifest; regenerate after source or artifact changes |
| final report/PPT package can be bundled for review | `release_bundle/README.md`, `release_bundle/bundle_manifest.tsv`, `scripts/build_v5_release_bundle.py` | ready as compact execution-draft handoff; rebuild after source or artifact changes |
| final report/PPT release bundle is readable | `release_bundle_audit.md`, `release_bundle_audit.tsv`, `scripts/audit_v5_release_bundle.py` | ready as generated bundle QA guard |
| related work citations have claim boundaries | `03_final_report/citation_source_map.md`, `03_final_report/external_source_verification.md`, `03_final_report/references.bib` | ready |
| selected checkpoint paths are generated, not hand-copied | `../2_training/05_checkpoint_selection/selected_checkpoint_manifest.md` | ready as waiting manifest; final waits for v5 rows |
| post-checkpoint launch line is explicit | `../3_evaluation/post_checkpoint_execution_plan.md` | ready as waiting-checkpoint execution plan; final launch waits for `ready_for_wrapper=yes` and `post_checkpoint_preflight_ready_to_launch` |
| post-checkpoint command wording is guarded | `../3_evaluation/post_checkpoint_command_consistency.md` | ready when no legacy paired-wrapper commands are found |
| post-checkpoint recovery path is documented | `../3_evaluation/post_checkpoint_eval_recovery.md` | ready for staged runs, reruns, aggregation promotion, and blocked-data fallback |
| post-checkpoint parser contract is audited | `../3_evaluation/post_checkpoint_parser_contract.md` | ready; wrapper output paths and aggregation parser paths are checked before v5 rows arrive |
| post-checkpoint result provenance is audited | `../3_evaluation/post_checkpoint_provenance_audit.md` | ready as waiting-checkpoint provenance guard; aggregated rows must have source files, run metadata, and command logs before claim promotion |
| post-checkpoint Go/No-Go is machine-checkable | `../3_evaluation/post_checkpoint_preflight.md` | ready as a waiting-checkpoint preflight; verdict must become `post_checkpoint_preflight_ready_to_launch` before `run_v5_post_checkpoint_evals.sh all` |

## Claim Locks

These statements must remain locked unless new evidence changes them:

- Say `controlled 102-language Glot500-style reproduction`, not full Glot500 reproduction.
- Say `Glot500-base external reference`, not equal-budget baseline.
- Do not claim target10 downstream improvement until partial official target task membership is materialized and evaluated correctly.
- Keep `dzo_Tibt` as a visible tokenizer regression.
- Do not promote NER/POS dev F1 snapshots into final result rows.

## Update Order After New Results

1. After matched checkpoints exist, run `bash scripts/run_v5_post_checkpoint_evals.sh status`.
   This refreshes `model_matrix.tsv`, `selected_checkpoint_manifest.md`, and
   `post_checkpoint_eval_queue.tsv`.
   While waiting, `POLL_SECONDS=300 bash scripts/watch_v5_mlm_handoff.sh` may be
   used for status-only polling.
2. While waiting, confirm `../2_training/mlm_progress_eta.md`,
   `../2_training/live_training_health.md`, and
   `../2_training/paired_launcher_transition.md` show active/clean status rather
   than treating live progress as a result row.
3. Confirm `../2_training/storage_readiness.md` stays ready before checkpoint
   saves, queued FVT launch, or long evaluation output writes.
4. Prefer `SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all`
   because post-10K `v5_random` rows are already measured. Use split `pppl`
   and `downstream` modes only when staging long jobs.
5. Run or confirm `python3 scripts/refresh_v5_reporting.py --with-plots`.
6. If tokenizer, zero-step, or coverage figure sources changed, run
   `scripts/refresh_v5_reporting.py --with-plots`.
7. Confirm `selected_checkpoint_manifest.md` reports matched `ready_10k` rows
   before promoting v5 method claims.
8. Confirm `finalization_gate_status.md` before promoting any result row.
9. Confirm `final_handoff_runbook.md` for the current phase and next command.
10. Confirm `reporting_package_audit.md` has no stale result-slot/live snapshot warnings.
11. Confirm `feedback_alignment_audit.md` still maps the feedback requirements
   to evidence and explicit gates.
12. Confirm `artifact_reference_audit.md` after adding or moving any report/PPT artifact.
13. Confirm `method_comparison_summary.md` before writing FVT-vs-random claims.
14. Confirm `comparison_materiality_audit.md`; write `tie_band` as no clear
    practical separation and keep `small` deltas cautious.
15. Confirm `result_slot_inventory.md` includes `method_comparison_claim_gate`
    before changing novelty or final method wording.
16. Confirm `submission_file_index_ko.md`, `final_package_checklist.md`, and
    `00_tables/source_map.md` before sharing report/PPT artifacts or release-bundle
    handoff copies.
17. Confirm `post_result_update_manifest.md` for the metric-specific command,
    evidence, report target, slide target, and claim rule.
18. Confirm `post_result_patch_plan_ko.md` for the file-by-file report/PPT
    patch order after parsed v5 rows.
19. Confirm `../3_evaluation/post_checkpoint_execution_plan.md` for the
    exact status/all command line, runtime env, output/log locations, and
    promotion rule.
20. Confirm `../3_evaluation/post_checkpoint_command_consistency.md` before
    copying a post-checkpoint command into report/PPT handoff text.
21. Confirm `../3_evaluation/post_checkpoint_provenance_audit.md` before
    promoting any aggregated row into report/PPT result claims.
22. Confirm `claim_promotion_matrix.md` before upgrading report/PPT claims.
23. Confirm `final_claim_decision_tree.md` before choosing final conclusion wording.
24. Confirm `result_promotion_readiness_audit.md` before upgrading after-MLM
    or downstream claims.
25. Confirm `final_claim_freeze_audit.md` before freezing final conclusion wording.
26. Confirm `03_final_report/result_interpretation_blocks.md` has the
    `Final Abstract Update Choices` and `Korean Final Conclusion Choices`
    blocks matching the decision tree outcome.
27. Confirm `narrative_quality_audit.md` before freezing report/PPT prose.
28. Confirm `release_manifest.md` after rebuilding report/PPT handoff artifacts.
29. Confirm `table_sync_audit.md` after updating any result table.
30. Confirm `table_13_metric_fidelity_matrix.md` and
    `metric_surface_completeness_audit.md` if coverage, blocker status, or
    visible report/PPT metric-family wording changed.
31. Confirm `rendered_artifact_freshness_audit.md` after rebuilding or editing
    report/PPT source, HTML, PDF, PPTX, or release-bundle artifacts.
32. Confirm `table_15_glot500_reproduction_fidelity.md` if scope, corpus,
    tokenizer, initialization, metric, or claim-boundary wording changed.
33. Confirm `report_slide_crosswalk.md` still points each report section and
   slide to the right evidence artifacts.
34. Confirm `slide_asset_manifest.md` and `01_figures/generated/figure_manifest.tsv`
    when figures or slide sources changed.
35. Confirm `citation_source_map.md` and `slide_citation_map.md` if citation
    boundaries or related-work wording changed.
36. Confirm `submission_file_index_ko.md`, `one_page_summary_ko.md`, and
    `release_bundle/README.md` still point to the current report/PPT artifacts.
37. Confirm `goal_readiness.md`.
38. Run metric-specific updates below only from measured artifacts.
39. Update metric folder README and result notes.
40. Update `00_tables/`.
41. Update `Report.md`.
42. Update `03_final_report/paper_draft.md`, `claim_ledger.md`, and
    `result_interpretation_blocks.md` as needed.
43. Update `02_slides/ppt_content.md`, `presenter_script_ko.md`, and
    `slide_claim_checklist.md`.
44. Re-run stale-value search for old live snapshots.

Detailed insertion targets are listed in:

```text
result_insertion_matrix.md
```

The full completion audit is tracked in:

```text
final_deliverable_audit.md
```
