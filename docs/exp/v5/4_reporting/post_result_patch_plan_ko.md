# v5 Post-Result Patch Plan Korean

Last checked: 2026-06-28 18:08 KST

Verdict: `post_result_patch_plan_ready_for_execution`

이 문서는 matched v5 checkpoint와 post-checkpoint metric 결과가 들어온 뒤
보고서/PPT를 어느 파일부터 어떤 claim boundary로 고칠지 정리한다.
숫자는 aggregation table, generated result table, provenance audit를 통과한
값만 사용한다.

## Go/No-Go

- 긴 평가는 두 v5 모델이 wrapper-ready이고 post-checkpoint preflight가 ready-to-launch일 때만 실행한다.
- report/PPT 숫자는 live log, stdout, 단일 모델 row가 아니라 aggregation과 table 산출물에서만 옮긴다.
- novelty claim은 zero-step evidence와 after-MLM/downstream evidence를 분리해서 쓴다.
- partial official target task membership이 materialized/evaluated 되기 전에는
  target10-wide downstream 개선을 주장하지 않는다.
- Final Evidence Packet이 같은 refresh에서 닫히기 전에는 수치가 있어도 final claim으로 승격하지 않는다.

## Patch Table

| Phase | Order | Update Item | Status | Required Gate | Current Evidence | Patch Files | Patch Scope | Report Update | Slide Update | Claim Lock | Action When Ready |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0_go_no_go | 1 | matched_checkpoint_pair | ready_for_execution | matched MLM checkpoints | gate=ready; manifest=ready_for_status_handoff; slot=replace_now; preflight=post_checkpoint_preflight_ready_to_launch; provenance=post_checkpoint_provenance_ready_waiting_models; freeze=claim_freeze_needs_update | 2_training/05_checkpoint_selection/selected_checkpoint_manifest.md; 3_evaluation/model_matrix.tsv; 3_evaluation/post_checkpoint_eval_queue.md; 3_evaluation/post_checkpoint_preflight.md | Replace running/waiting model text only after both v5 model rows are wrapper-ready. | Training and reproducibility sections. | Slide 10 plus backup Q&A. | Checkpoint readiness unlocks evaluation only; it does not unlock method claims. | Run status/preflight, then launch paired post-checkpoint evaluation if preflight is ready-to-launch. |
| 1_intrinsic_after_mlm | 2 | after_mlm_pppl | waiting_checkpoints_or_results | after-MLM PPPL | gate=pending; manifest=ready_to_run; slot=tracked_pending; preflight=post_checkpoint_preflight_ready_to_launch; provenance=post_checkpoint_provenance_ready_waiting_models; freeze=claim_freeze_needs_update; metrics=pseudoperplexity:status=partial; measured=glot500_base,v5_random,xlmr_base; missing=v5_fvt | 4_reporting/00_tables/table_06_pppl_partial.md; Report.md; 4_reporting/03_final_report/paper_draft.md; 4_reporting/03_final_report/paper_draft_ko.md; 4_reporting/method_comparison_summary.md | Insert v5_random/v5_fvt target, head, and all PPPL rows from aggregation. | Results and analysis sections; keep zero-step and after-MLM evidence separate. | Slides 11, 12, and 14. | FVT after-MLM claim opens only from paired PPPL rows with provenance. | Patch PPPL table, rerun refresh with plots, then inspect materiality and claim-promotion audits. |
| 2_available_downstream | 3 | tatoeba_retrieval | waiting_checkpoints_or_results | v5 available downstream replay | gate=pending; manifest=measured_pair; slot=tracked_pending; preflight=post_checkpoint_preflight_ready_to_launch; provenance=post_checkpoint_provenance_ready_waiting_models; freeze=claim_freeze_needs_update; metrics=retrieval_tatoeba:status=measured; measured=glot500_base,v5_fvt,v5_random,xlmr_base; missing= | 4_reporting/00_tables/table_07_tatoeba_partial.md; Report.md; paper/deck result sections | Insert available-language Tatoeba Top-10 rows for both v5 models. | Downstream retrieval subsection. | Slides 11 and 12. | Available-language retrieval only; target10 remains coverage-limited unless task data changes. | Patch table/result prose from aggregation, then keep target10 coverage caveat. |
| 2_available_downstream | 4 | bible_retrieval | waiting_checkpoints_or_results | Bible retrieval accounting | gate=pending; manifest=measured_pair; slot=tracked_pending; preflight=post_checkpoint_preflight_ready_to_launch; provenance=post_checkpoint_provenance_ready_waiting_models; freeze=claim_freeze_needs_update; metrics=retrieval_bible:status=measured; measured=glot500_base,v5_fvt,v5_random,xlmr_base; missing= | 4_reporting/00_tables/table_12_bible_partial.md; Report.md; limitations; deck caveat slides | Insert v5 Bible rows if parsed, or retain explicit pending/blocker status. | Bible retrieval result and limitation paragraphs. | Slides 11, 12, and 13. | Available-language Bible comparison only; selected target10 Bible coverage is not implied. | Patch measured rows or blocker wording, then rerun metric-fidelity and surface audits. |
| 2_available_downstream | 5 | text_classification | waiting_checkpoints_or_results | v5 available downstream replay | gate=pending; manifest=measured_pair; slot=tracked_pending; preflight=post_checkpoint_preflight_ready_to_launch; provenance=post_checkpoint_provenance_ready_waiting_models; freeze=claim_freeze_needs_update; metrics=text_classification:status=measured; measured=glot500_base,v5_fvt,v5_random,xlmr_base; missing= | 4_reporting/00_tables/table_08_text_classification_partial.md; Report.md; paper/deck result sections | Insert local Taxi1500 macro-F1 rows for both v5 models. | Text classification result subsection with local-data boundary. | Slides 11 and 12. | Local classification comparison only; do not generalize to target10 downstream. | Patch classification rows from aggregation and keep local English-only caveat visible. |
| 2_available_downstream | 6 | ner_pos_tagging | waiting_checkpoints_or_results | v5 available downstream replay | gate=pending; manifest=ready_to_run; slot=tracked_pending; preflight=post_checkpoint_preflight_ready_to_launch; provenance=post_checkpoint_provenance_ready_waiting_models; freeze=claim_freeze_needs_update; metrics=ner:status=partial; measured=glot500_base,v5_random,xlmr_base; missing=v5_fvt \| pos:status=partial; measured=glot500_base,v5_random,xlmr_base; missing=v5_fvt | 4_reporting/00_tables/table_10_ner_partial.md; 4_reporting/00_tables/table_11_pos_partial.md; Report.md | Insert NER/POS F1 rows for both v5 models from parsed test outputs. | Tagging result subsection and POS train-language note. | Slides 11 and 12. | Tagging is available-language evidence; POS train-language caveat stays visible. | Patch tagging tables and rerun table sync plus narrative audits. |
| 2_available_downstream | 7 | roundtrip_alignment | waiting_checkpoints_or_results | Roundtrip alignment accounting | gate=pending; manifest=ready_to_run; slot=tracked_pending; preflight=post_checkpoint_preflight_ready_to_launch; provenance=post_checkpoint_provenance_ready_waiting_models; freeze=claim_freeze_needs_update; metrics=roundtrip_alignment:status=partial; measured=glot500_base,v5_random,xlmr_base; missing=v5_fvt | 4_reporting/00_tables/table_14_roundtrip_partial.md; 4_reporting/00_tables/table_09_blocked_metric_notes.md; 4_reporting/00_tables/table_13_metric_fidelity_matrix.md; Report.md | Insert parsed Roundtrip rows or retain explicit pending/blocker accounting. | Roundtrip result, metric-fidelity, and limitations. | Slides 11, 12, and 13. | No Roundtrip performance claim until both v5 rows parse with provenance. | Patch measured rows or blocker note, then rerun metric-surface and claim-freeze audits. |
| 3_claim_selection | 8 | method_comparison_claim_gate | waiting_checkpoints_or_results | after-MLM PPPL | gate=pending; manifest=ready_to_run; slot=tracked_pending; preflight=post_checkpoint_preflight_ready_to_launch; provenance=post_checkpoint_provenance_ready_waiting_models; freeze=claim_freeze_needs_update | 4_reporting/method_comparison_summary.md; 4_reporting/comparison_materiality_audit.md; 4_reporting/claim_promotion_matrix.md; 4_reporting/final_claim_decision_tree.md; 4_reporting/03_final_report/claim_ledger.md | Promote only the claim allowed by paired PPPL/downstream rows and materiality bands. | Abstract, discussion, conclusion, and claim ledger. | Slides 12 and 14 plus presenter script. | Use tie_band as no clear practical separation; keep zero-step-only outcome if after-MLM does not support FVT. | Select decision-tree outcome, patch conclusion blocks, then run final claim-freeze audit. |
| 3_claim_selection | 9 | target10_downstream_boundary | waiting_checkpoints_or_results | v5 available downstream replay | gate=pending; manifest=waiting_results; slot=tracked_coverage_limited; preflight=post_checkpoint_preflight_ready_to_launch; provenance=post_checkpoint_provenance_ready_waiting_models; freeze=claim_freeze_needs_update | Report.md; 4_reporting/03_final_report/result_interpretation_blocks.md; 4_reporting/02_slides/defense_qa_ko.md | Keep target downstream caveat unless partial official task membership is materialized and evaluated. | Limitations and conclusion. | Slides 13 and 14 plus defense Q&A. | Target10 downstream improvement is locked until tail materialization/eval is repaired. | Update caveat wording from task-list membership and materialized rows, not from intuition or live logs. |
| 4_render_freeze | 10 | final_render_and_bundle | waiting_checkpoints_or_results | final report/PPT synchronization | rendered=rendered_artifact_freshness_ready; smoke=final_submission_smoke_needs_repair; freeze=claim_freeze_needs_update | 4_reporting/03_final_report/*.md/html/pdf; 4_reporting/02_slides/final_deck_ko.md/html/pptx/pdf; 4_reporting/release_manifest.md; 4_reporting/release_bundle/ | Rebuild report, deck, figures, release manifest, and bundle after final text changes. | Final paper sources and rendered artifacts. | Final deck source, PPTX, PDF, and presenter script. | Final freeze requires rendered freshness, smoke audit, and claim-freeze agreement. | Run refresh with plots, then confirm freshness, smoke, package, and release-bundle audits. |

## Minimal Finalization Sequence

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
python3 scripts/refresh_v5_reporting.py --with-plots
```

Canonical full rerun, only when intentional remeasurement is needed:

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
```

After refresh, patch only rows whose status is `ready_for_patch`, then rerun
the same refresh command and confirm final claim-freeze, rendered freshness,
final submission smoke, reporting package, and release-bundle audits.

## Final Evidence Packet

결과가 측정되더라도 아래 packet이 같은 refresh 산출물에서 함께 닫히지 않으면
보고서와 발표에서는 `measured but not promotable`로 남긴다.

| Packet Item | Required Evidence | Report/PPT Action |
| --- | --- | --- |
| checkpoint pair | `selected_checkpoint_manifest.md`, `model_matrix.tsv`, `post_checkpoint_preflight.md` | matched 10K pair만 final result 후보로 사용 |
| metric rows | `09_aggregation/metric_completion.tsv`, `main_head_tail_all.tsv`, `v5_target_subset.tsv` | parsed row가 있는 metric만 표와 슬라이드에 삽입 |
| provenance | `post_checkpoint_provenance_audit.md`, wrapper logs, run metadata | source/log trail 없는 숫자는 본문 claim 금지 |
| materiality | `method_comparison_summary.md`, `comparison_materiality_audit.md` | tie/small/moderate/large band에 맞춰 claim 강도 선택 |
| claim gate | `claim_promotion_matrix.md`, `final_claim_decision_tree.md`, `final_claim_freeze_audit.md` | 결론/abstract/slide 14 wording을 gate outcome과 일치 |
| patch targets | this patch plan, `result_insertion_contract_audit.md`, `report_slide_crosswalk.md` | Report, paper draft, deck, script를 같은 근거로 수정 |
| final freeze | rendered freshness, final submission smoke, reporting package, release bundle audits | 최종 PDF/PPTX/bundle이 source보다 stale하지 않을 때만 제출 후보 |

Machine-readable TSV:

```text
post_result_patch_plan.tsv
```
