# v5 Final Action Dashboard Korean

Last checked: 2026-06-28 18:08 KST

Verdict: `final_action_dashboard_ready_for_post_checkpoint_eval`

이 파일은 최종 report/PPT 제출까지 남은 행동을 한눈에 보기 위한 dashboard이다.
실험 결과표가 아니라 handoff용 운영 문서이며, 숫자 claim은 여전히
`3_evaluation/09_aggregation/`과 `4_reporting/00_tables/`에서만 승격한다.

## 지금 할 일

- 상태: `final_action_dashboard_ready_for_post_checkpoint_eval`
- 근거: queue measured=24; waiting_model=0; blocked_data=0
- 다음 명령: `bash scripts/run_v5_post_checkpoint_evals.sh status && SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all`

## Dashboard

| Category | Item | Status | Evidence | Next Action |
| --- | --- | --- | --- | --- |
| current_state | immediate_next_action | final_action_dashboard_ready_for_post_checkpoint_eval | queue measured=24; waiting_model=0; blocked_data=0 | bash scripts/run_v5_post_checkpoint_evals.sh status && SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all |
| current_state | post_checkpoint_preflight | post_checkpoint_preflight_ready_to_launch | docs/exp/v5/3_evaluation/post_checkpoint_preflight.md | long eval requires post_checkpoint_preflight_ready_to_launch |
| current_state | post_checkpoint_trigger_card | ready | docs/exp/v5/4_reporting/post_checkpoint_trigger_card_ko.md | open this one-page Go/No-Go card before launching long paired eval |
| transition_gate | launcher_process | complete_or_missing | launcher_active=False; random_running=False; fvt_running=False | none |
| transition_gate | transition_state | matched_ready | random_ready=True; random_status=ready; fvt_ready=True; fvt_status=ready; fvt_log_exists=True | none |
| transition_gate | critical_transition_log_patterns | clean | critical=0 | none |
| model_gate | v5_random | ready | model_status=ready; tokenizer_status=ready; wrapper_ready=yes; run_status=ready; progress=100.00%; remaining_steps=0; eta=2026-06-28 18:08 KST | include in paired evaluation |
| model_gate | v5_fvt | ready | model_status=ready; tokenizer_status=ready; wrapper_ready=yes; run_status=ready; progress=100.00%; remaining_steps=0; eta=2026-06-28 18:08 KST | include in paired evaluation |
| final_gate | matched MLM checkpoints | ready | v5_random_ready=True; v5_fvt_ready=True | none |
| final_gate | after-MLM PPPL | pending | measured_models=glot500_base,v5_random,xlmr_base | after checkpoint status and post-checkpoint preflight are ready, prefer SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh pppl; canonical full rerun command: WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh pppl |
| final_gate | v5 available downstream replay | pending | retrieval_tatoeba=glot500_base,v5_fvt,v5_random,xlmr_base; text_classification=glot500_base,v5_fvt,v5_random,xlmr_base; ner=glot500_base,v5_random,xlmr_base; pos=glot500_base,v5_random,xlmr_base; retrieval_bible=glot500_base,v5_fvt,v5_random,xlmr_base; roundtrip_alignment=glot500_base,v5_random,xlmr_base | after checkpoint status and post-checkpoint preflight are ready, prefer SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream or all; canonical full rerun command: WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream |
| final_gate | Bible retrieval accounting | pending | status=measured; coverage=74/102; target10=0/10; measured_models=glot500_base,v5_fvt,v5_random,xlmr_base; note= | run Bible retrieval through SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream or all after checkpoints and post-checkpoint preflight are ready |
| final_gate | Roundtrip alignment accounting | pending | status=partial; coverage=74/102; target10=0/10; measured_models=glot500_base,v5_random,xlmr_base; blocker_audit=roundtrip_inputs_ready_pending_results; note=missing_model_outputs=v5_fvt | run v5 roundtrip rows after matched checkpoints and post-checkpoint preflight are ready |
| metric_completion | pseudoperplexity | partial | measured=glot500_base,v5_random,xlmr_base; missing=v5_fvt; coverage=102/102; target10=10/10 | run post-checkpoint wrapper after both v5 models are ready and preflight is ready_to_launch |
| metric_completion | retrieval_tatoeba | measured | measured=glot500_base,v5_fvt,v5_random,xlmr_base; missing=-; coverage=63/102; target10=0/10 | none |
| metric_completion | retrieval_bible | measured | measured=glot500_base,v5_fvt,v5_random,xlmr_base; missing=-; coverage=74/102; target10=0/10 | none |
| metric_completion | text_classification | measured | measured=glot500_base,v5_fvt,v5_random,xlmr_base; missing=-; coverage=1/102; target10=0/10 | none |
| metric_completion | ner | partial | measured=glot500_base,v5_random,xlmr_base; missing=v5_fvt; coverage=78/102; target10=0/10 | run post-checkpoint wrapper after both v5 models are ready and preflight is ready_to_launch |
| metric_completion | pos | partial | measured=glot500_base,v5_random,xlmr_base; missing=v5_fvt; coverage=58/102; target10=0/10 | run post-checkpoint wrapper after both v5 models are ready and preflight is ready_to_launch |
| metric_completion | roundtrip_alignment | partial | measured=glot500_base,v5_random,xlmr_base; missing=v5_fvt; coverage=74/102; target10=0/10 | run post-checkpoint wrapper after both v5 models are ready and preflight is ready_to_launch |
| report_ppt_update_target | selected checkpoints | waiting_results | target=training/checkpoint section; slide 10; source=selected_checkpoint_manifest.md | replace only after aggregation/decision-tree evidence exists |
| report_ppt_update_target | method comparison summary | waiting_results | target=novelty/results/conclusion; slides 9, 12, 14; presenter script; source=method_comparison_summary.md + claim_promotion_matrix.md | keep zero-step claim; update final method wording only after parsed PPPL/downstream rows exist |
| report_ppt_update_target | after-MLM PPPL | waiting_results | target=abstract/results/analysis/conclusion; slides 11, 12, 14; source=09_aggregation + table_06_pppl_partial.md | replace only after aggregation/decision-tree evidence exists |
| report_ppt_update_target | retrieval rows | waiting_results | target=downstream results; slide 11 status and slide 12 result values; source=table_07_tatoeba_partial.md and table_12_bible_partial.md | replace only after aggregation/decision-tree evidence exists |
| report_ppt_update_target | classification/tagging rows | waiting_results | target=downstream/tagging results; slide 11 status and slide 12 result values; source=table_08, table_10, table_11 | replace only after aggregation/decision-tree evidence exists |
| report_ppt_update_target | roundtrip rows | waiting_results | target=limitations/downstream results; slides 11 status, 12 result values, and 13 caveat; source=table_14_roundtrip_partial.md | replace only after aggregation/decision-tree evidence exists |
| report_ppt_update_target | final conclusion | waiting_results | target=abstract/conclusion; slide 14; presenter script; source=final_claim_decision_tree.md | replace only after aggregation/decision-tree evidence exists |
| report_ppt_update_target | final evidence packet | waiting_results | target=same-refresh claim promotion packet before final report/PPT freeze; source=selected_checkpoint_manifest.md + metric tables + provenance/materiality/claim-freeze audits | leave measured rows as measured but not promotable until the packet is complete |
| report_ppt_update_target | post-result patch plan | waiting_results | target=file-by-file report/PPT patch order after parsed v5 rows; source=post_result_patch_plan_ko.md | open before editing Report.md, paper drafts, slides 11/12/14, or claim ledger |
| claim_lock | full Glot500 reproduction | locked | must remain disallowed; surface_overclaim=surface_overclaim_guard_ready | keep wording guarded until claim-promotion matrix unlocks it |
| claim_lock | FVT improves after-MLM PPPL | locked | locked until parsed PPPL rows exist; surface_overclaim=surface_overclaim_guard_ready | keep wording guarded until claim-promotion matrix unlocks it |
| claim_lock | FVT improves downstream performance | locked | locked until parsed downstream rows exist; surface_overclaim=surface_overclaim_guard_ready | keep wording guarded until claim-promotion matrix unlocks it |
| claim_lock | target10 downstream improves | locked | disallowed until partial official target task membership is materialized/evaluated correctly; surface_overclaim=surface_overclaim_guard_ready | keep wording guarded until claim-promotion matrix unlocks it |
| claim_lock | Glot500-base equal-budget baseline | locked | disallowed; use external reference; surface_overclaim=surface_overclaim_guard_ready | keep wording guarded until claim-promotion matrix unlocks it |

## Go/No-Go

- `bash scripts/run_v5_post_checkpoint_evals.sh status` 끝의 `READY_TO_LAUNCH=yes`가 최종 실행 신호이다.
- `READY_TO_LAUNCH=no`이면 `NEXT_COMMAND`에 표시된 watcher/status 명령으로 돌아간다.
- `ready_for_wrapper=yes`가 `v5_random`과 `v5_fvt` 모두에서 확인되기 전에는 긴 평가를 실행하지 않는다.
- `post_checkpoint_preflight_ready_to_launch`가 확인되기 전에는 긴 평가를 실행하지 않는다.
- 평가가 끝난 뒤에는 `python3 scripts/refresh_v5_reporting.py --with-plots`를 먼저 실행한다.
- 최종 결론은 `final_claim_decision_tree.md`와 `post_checkpoint_outcome_matrix_ko.md`가 같은 outcome을 가리킬 때만 바꾼다.
- Final Evidence Packet이 checkpoint, metric rows, provenance, materiality, claim gate, patch targets, final freeze를 같은 refresh에서 묶지 못하면 `measured but not promotable`로 남긴다.
- watcher를 오래 유지하려면 사용자 관리 shell 또는 tmux에서 실행한다. transient non-interactive launcher의 background watcher 지속성을 가정하지 않는다.
