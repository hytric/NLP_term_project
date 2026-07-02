# v5 최종 보고서/PPT 제출 Handoff

작성 상태: execution draft, 2026-06-28 기준.

이 문서는 최종 보고서와 발표 자료를 실제로 조립할 때 열어볼 최소 파일과
claim 승격 규칙을 한 곳에 모은다. 현재 패키지는 결과 대기 상태이며,
`v5_random`/`v5_fvt` matched checkpoint와 post-checkpoint evaluation row가 생기기
전까지 final method claim은 잠금 상태이다.
발표 직전에는 이 문서보다 `presentation_readiness_checklist_ko.md`를 먼저 열고,
현재 checkpoint 진행률과 Go/No-Go는 `final_action_dashboard_ko.md`와
`bash scripts/run_v5_post_checkpoint_evals.sh status` 출력을 우선한다.

## 1. 현재 한 줄 결론

현재 안전하게 말할 수 있는 결론:

```text
v5는 Glot500-style vocabulary expansion, continued MLM setup, metric-family
accounting을 92+10 controlled subset에서 재연했고, FVT initialization은
zero-step target MLM proxy에서 random resize보다 뚜렷하게 좋은 시작점을 보였다.
```

현재 아직 말하면 안 되는 결론:

```text
FVT improves after-MLM PPPL.
FVT improves downstream performance.
target10 downstream improves.
full 511-language Glot500 reproduction is complete.
```

판정 source:

```text
final_claim_decision_tree.md
final_claim_freeze_audit.md
claim_promotion_matrix.md
final_freeze_protocol_ko.md
final_goal_acceptance_rubric_ko.md
final_result_update_checklist_ko.md
presentation_readiness_checklist_ko.md
03_final_report/result_interpretation_blocks.md의 Final Abstract Update Choices와
Korean Final Conclusion Choices
post_checkpoint_outcome_matrix_ko.md
method_comparison_summary.md
final_package_checklist.md
00_tables/source_map.md
../3_evaluation/post_checkpoint_provenance_audit.md
```

## 2. 최종 보고서 조립 순서

1. 한국어 보고서 본문은 `03_final_report/paper_draft_ko.md`를 기준으로 한다.
2. 더 긴 living report와 numeric table은 `../Report.md`와 `00_tables/`에서 가져온다.
3. reproducibility appendix는 `03_final_report/reproducibility_appendix.md`를 사용한다.
4. citation과 related-work boundary는 `03_final_report/citation_source_map.md`,
   `03_final_report/external_source_verification.md`, `03_final_report/references.bib`,
   그리고 slide 쪽 `02_slides/slide_citation_map.md`를 따른다.
5. 마지막 초록/결론 문장은 `final_claim_decision_tree.md`가 고른 outcome에 맞춰
   `03_final_report/result_interpretation_blocks.md`의
   `Final Abstract Update Choices`, `Korean Final Conclusion Choices`, 그리고
   `post_checkpoint_outcome_matrix_ko.md`에서 고른다.
6. 제출/리허설에서 처음 여는 파일 순서는 `presentation_readiness_checklist_ko.md`와
   `submission_file_index_ko.md`를 따른다.
7. 전체 package gate는 `final_package_checklist.md`, 숫자와 표의 출처는
   `00_tables/source_map.md`로 마지막에 대조한다.

현재 보고서에 이미 들어간 고정 evidence:

| Evidence | Source |
| --- | --- |
| 92+10 data scope | `../README.md`, `../Plan.md` |
| target10 selection | `../0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv` |
| merge complete | `../0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.report.json` |
| tokenizer size and audit | `00_tables/table_02_tokenizer_audit.md` |
| initialization and zero-step | `00_tables/table_03_initialization_zero_step.md` |
| metric fidelity | `00_tables/table_13_metric_fidelity_matrix.md` |
| current measured rows | `current_result_snapshot.md`, `00_tables/` |

## 3. PPT 조립 순서

1. 실제 slide source는 `02_slides/final_deck_ko.md`를 기준으로 한다.
2. 실제 PowerPoint 파일은 `02_slides/v5_final_deck_ko.pptx`로 생성한다.
3. 검토/공유용 PDF는 `02_slides/v5_final_deck_ko.pdf`로 생성한다.
4. browser rehearsal은 `02_slides/v5_final_deck_ko.html`을 사용한다.
5. 발표 발화문은 `02_slides/presenter_script_ko.md`를 기준으로 한다.
6. 발표 시간 운영은 `02_slides/rehearsal_plan_ko.md`를 기준으로 한다.
7. slide별 evidence와 asset은 `02_slides/slide_asset_manifest.md`에서 확인한다.
8. slide claim lock은 `02_slides/slide_claim_checklist.md`와
   `final_claim_freeze_audit.md`를 같이 본다.
9. 결과가 업데이트되면 slide 11의 status/coverage, slide 12의 result values,
   slide 14의 conclusion을 먼저 고친다.
10. 최종 동결 직전에는 `final_freeze_protocol_ko.md`의 freeze 금지/허용 조건을 확인한다.

현재 PPT에서 강하게 말할 수 있는 slide:

| Slide | Safe message |
| --- | --- |
| 3 | full Glot500이 아니라 controlled subset replay |
| 6 | Glot500-style SPM append, 118,685 appended tokens, `dzo_Tibt` caveat |
| 8-9 | initialization correctness and zero-step FVT advantage |
| 11 | metric-family coverage/status; v5-random diagnostic rows measured; v5-FVT rows waiting checkpoint |
| 12 | baseline/reference and v5-random diagnostic measured rows; paired FVT result values to insert after aggregation |
| 13 | target10 downstream coverage limitation and Bible/Roundtrip v5 checkpoint gaps |
| 14 | setup fidelity plus zero-step novelty, final method claims pending |

## 4. Checkpoint 이후 실행선

matched checkpoint가 준비되면 아래 순서만 따른다.

대기 중에는 아래 명령으로만 상태를 확인한다. 이 상태 확인은 final claim을
업데이트하지 않고, wrapper 실행 가능 여부만 갱신한다.

```bash
python3 scripts/refresh_v5_reporting.py
python3 scripts/write_v5_mlm_progress_eta.py
python3 scripts/audit_v5_live_training_health.py
python3 scripts/audit_v5_paired_launcher_transition.py
bash scripts/run_v5_post_checkpoint_evals.sh status
sed -n '1,80p' docs/exp/v5/2_training/mlm_progress_eta.md
sed -n '1,90p' docs/exp/v5/2_training/live_training_health.md
sed -n '1,90p' docs/exp/v5/2_training/paired_launcher_transition.md
sed -n '1,45p' docs/exp/v5/3_evaluation/running_status.md
```

평가로 넘어가는 조건은 `model_matrix.tsv`, `selected_checkpoint_manifest.md`,
`post_checkpoint_eval_queue.md`, `post_checkpoint_command_consistency.md`,
`post_checkpoint_parser_contract.md`, `post_checkpoint_provenance_audit.md`,
`post_checkpoint_preflight.md`가 모두
`v5_random`과 `v5_fvt`에 대해 `ready_for_wrapper=yes` 또는 gate-ready 상태를
가리키고, preflight verdict가 `post_checkpoint_preflight_ready_to_launch`인
것이다. 그 전까지 `waiting_model`은 실패가 아니라 정상적인 대기 상태로 둔다.

발표에서는 `../2_training/mlm_progress_eta.md`의 live progress나
`../2_training/live_training_health.md`의 health verdict, 또는
`../2_training/paired_launcher_transition.md`의 random-running/FVT-waiting
verdict를 품질 결과처럼 말하지 않는다. 이 파일들은 "지금 어느 stage에 있고
평가로 넘어가도 되는가"를 설명하는 운영 증거이고, method claim은 아래
post-checkpoint wrapper와 aggregation 이후에만 열린다.

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
python3 scripts/refresh_v5_reporting.py --with-plots
```

`GPU_RANDOM`과 `GPU_FVT`는 `CUDA_VISIBLE_DEVICES`로 직접 전달되는 물리 GPU
번호다. handoff 시점에 `nvidia-smi`로 GPU `0,1`이 비어 있는지 확인하고, 사용 중이면
같은 명령에서 빈 GPU 번호로 바꿔 실행한다.

그 다음 확인할 파일:

```text
../2_training/05_checkpoint_selection/selected_checkpoint_manifest.md
../2_training/live_training_health.md
../2_training/paired_launcher_transition.md
../3_evaluation/post_checkpoint_eval_queue.md
../3_evaluation/post_checkpoint_command_consistency.md
../3_evaluation/post_checkpoint_eval_recovery.md
../3_evaluation/post_checkpoint_parser_contract.md
../3_evaluation/09_aggregation/main_head_tail_all.tsv
../3_evaluation/09_aggregation/v5_target_subset.tsv
submission_file_index_ko.md
final_package_checklist.md
00_tables/source_map.md
finalization_gate_status.md
method_comparison_summary.md
result_slot_inventory.md
final_claim_decision_tree.md
result_promotion_readiness_audit.md
final_claim_freeze_audit.md
reporting_package_audit.md
final_result_update_checklist_ko.md
```

## 5. 결과가 들어온 뒤 교체할 위치

| New evidence | Report target | PPT target | Claim change |
| --- | --- | --- | --- |
| `v5_random`/`v5_fvt` selected checkpoint | method/training section | slide 10 | selected checkpoint pending 해제 |
| after-MLM PPPL rows | results and analysis | slide 11 status, slide 12 result values, slide 14 conclusion | FVT PPPL claim may unlock |
| `method_comparison_summary.md` refresh | novelty/results/conclusion | slides 9, 12, 14 | `method_comparison_claim_gate`에 따라 zero-step claim과 final method claim을 분리 |
| Tatoeba/Bible rows | downstream result paragraph | slide 11 status and slide 12 result values | available-language retrieval claim only |
| Taxi1500 rows | downstream result paragraph | slide 11 status and slide 12 result values | limited classification claim only |
| NER/POS rows | tagging result paragraph | slide 11 status and slide 12 result values | available-language tagging claim only |
| Roundtrip v5 rows arrive | downstream result paragraph | slide 11 status, slide 12 result values, and slide 13 caveat | add available-language Roundtrip method comparison |

더 자세한 Go/No-Go 조건, metric별 evidence, Report/PPT 교체 위치는
`final_result_update_checklist_ko.md`를 기준으로 확인한다.

## 6. 최종 동결 전 확인

최종 보고서/PPT를 freeze하기 전에는 아래 verdict를 확인한다.

```text
narrative_quality_audit.md
artifact_reference_audit.md
metric_fidelity_audit.md
reproducibility_audit.md
final_claim_freeze_audit.md
reporting_package_audit.md
final_deliverable_audit.md
release_manifest.md
release_bundle/README.md
submission_file_index_ko.md
final_package_checklist.md
00_tables/source_map.md
final_freeze_protocol_ko.md
```

허용되는 최종 상태:

- 모든 measured result는 aggregation에서 온다.
- blocked metric은 사라지지 않고 limitation row로 남는다.
- `Glot500-base`는 external reference로만 부른다.
- target10 downstream claim은 coverage가 생기기 전까지 하지 않는다.
- final abstract/conclusion은 `final_claim_decision_tree.md`와
  `final_claim_freeze_audit.md`가 허용한 문장만 사용한다.
- 한국어 보고서 초록/결론과 slide 14는
  `03_final_report/result_interpretation_blocks.md`의
  `Final Abstract Update Choices`와 `Korean Final Conclusion Choices` 중
  decision tree outcome과 일치하는 블록만 사용하고,
  `post_checkpoint_outcome_matrix_ko.md`의 outcome row와도 일치해야 한다.
- 제출/공유할 파일 묶음은 `release_manifest.md`와 `release_manifest.tsv`의
  size/hash manifest로 마지막 변경 여부를 확인한다.
- 빠른 공유용 묶음은 `release_bundle/`에 있으며, 현재 상태에서는
  `EXECUTION_DRAFT_NOT_FINAL`로만 사용한다.
