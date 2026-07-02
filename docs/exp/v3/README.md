# Third Try

작성일: 2026-06-12

## Core Direction

피드백과 사용자 scope 확인 후 `third_try`의 방향은 두 문장으로 고정한다.

1. Main experiment는 target10 low-resource 전체를 대상으로 high-resource replay/control data를 함께 사용해 실제 downstream 성능 개선 모델을 만드는 것이다.
2. 지금까지 수행한 실험 중 final model 조건을 만족하지 않는 결과는 ablation/failure analysis로 배치한다.

## Documents

| File | Purpose |
| --- | --- |
| `idea.md` | third_try의 핵심 claim, main/extension/ablation 분리 |
| `scope_lock_20260612.md` | 사용자 확인으로 고정된 target10, high-resource replay, seed/init 범위 |
| `plan.md` | target10 성능 개선 모델 실행 순서 |
| `ablation_study.md` | first_try/second_try 결과와 byte-vs-char fallback 비교를 ablation으로 재배치하는 기준 |
| `step_index.md` | stage별 task 순서, dependency, exit gate |
| `execution_rules.md` | 반복 실행, failure return, artifact 저장, main/ablation 경계 규칙 |
| `iteration_log.md` | run id별 반복 요약과 다음 행동 기록 |
| `decision_log.md` | 고정 결정, Stage 00 해결사항, 이후 남은 결정 |
| `task_board.tsv` | stage별 현재 상태와 next action |
| `status_report_20260613.md` | 2026-06-13 기준 진행상황, 생성 데이터, 다음 실행 계획 |
| `final_pre_start_report_20260613.md` | Stage 05 continued-MLM 시작 전 최종 go/no-go 보고 |
| `final_diagnostic_report_20260613.md` | Stage 05/06/07/08 이후 positive/diagnostic claim 최종 검토 |
| `final_goal_20260613.md` | third_try의 최종 목표, 성공/실패 판정 기준, 현재 결론 |
| `final_goal_completion_audit_20260613.md` | 최종 목표 요구사항별 PASS/FAIL 감사 |
| `final_goal_completion_audit_20260613.tsv` | 감사표 원본 |
| `positive_route_survey_methodology_20260618.md` | broad target10 positive claim으로 재진입하기 위한 survey 및 방법론 |
| `10_embedding_alignment_downstream/plan.md` | cross-lingual semantic embedding alignment, 2D map, embedding-based downstream 실험 계획 |
| `05_mlm/results.md` | Stage 05 smoke and fvt 3-seed pilot 결과 |
| `06_eval/results.md` | Stage 06 MLM/frozen proxy 및 Coptic POS pilot 결과 |
| `07_main_claim/results.md` | positive claim 차단 근거와 diagnostic negative claim synthesis |
| `08_ablation/results.md` | first_try/second_try를 ablation/failure analysis로 재배치한 패키지 |
| `00_scope/` - `09_extension_case/` | stage별 plan/results/score/file result 작업 폴더 |
| `branches/` | gate failure 후 제한적 branch 탐구 기록 |
| `_templates/` | results, score table, file results, iteration summary 템플릿 |
| `feedback/vocab_extension_tutorial.pdf` | vocabulary extension 및 initialization feedback source |

## Reading Order

1. `idea.md`
2. `scope_lock_20260612.md`
3. `plan.md`
4. `step_index.md`
5. `execution_rules.md`
6. `status_report_20260613.md`
7. `final_pre_start_report_20260613.md`
8. `05_mlm/results.md`
9. `06_eval/results.md`
10. `07_main_claim/results.md`
11. `08_ablation/results.md`
12. `final_diagnostic_report_20260613.md`
13. `final_goal_20260613.md`
14. `final_goal_completion_audit_20260613.md`
15. `positive_route_survey_methodology_20260618.md`
16. `10_embedding_alignment_downstream/plan.md`
17. `ablation_study.md`
18. `docs/survey/2305.12182v2.pdf`
19. `docs/survey/GLOT500_extension.pdf`
20. `feedback/vocab_extension_tutorial.pdf`

## Current Status

2026-06-13 replay-safe retry와 최종 감사 작성 후 기준:

- Stage 00 scope/data inventory는 완료 상태로 둔다.
- Stage 01 data manifest는 완료 상태로 둔다.
- Stage 02 baseline은 tokenization + deterministic MLM baseline까지 완료했고, exact PPPL/downstream baseline은 pending이다.
- Stage 03 tokenizer는 `PASS_DEVIATION_AND_FALLBACK_ABLATION_DOCUMENTED`로 닫았고, target-heavy 48k tokenizer를 provisional main candidate로 둔다. Byte fallback vs character coverage 비교도 ablation으로 측정했다.
- Stage 04 initialization은 완료했고, fvt checkpoint를 첫 Stage 05 pilot 시작점으로 둔다.
- Stage 05 continued-MLM은 smoke test, `fvt` 3-seed 200-step pilot, lower-LR replay-safe 1000-step 3-seed retry를 완료했다. Replay-safe retry는 200-step보다 dev MLM loss가 낮지만 full Glot500 training-budget reproduction은 아니다.
- Stage 06은 deterministic MLM proxy, frozen Bible proxy, Coptic UD POS pilot/replay-safe eval, high-resource Bible-control MLM proxy, target10 downstream availability audit을 완료했다. Replay-safe Coptic POS token accuracy는 3/3 seed에서 XLM-R-base보다 높지만, high-resource control proxy는 여전히 0/4 언어에서 no-collapse threshold를 통과하지 못했다. Target10 전체 supervised coverage가 sparse하므로 positive final claim은 계속 금지된다.
- Stage 07은 `PASS_NEGATIVE_MAIN_READY`로 닫았다. 현재 evidence는 positive target10 downstream claim이 아니라 diagnostic negative claim을 지지한다.
- Stage 08은 `PASS_ABLATION_PACKAGE_READY`로 닫았다. `first_try`와 `second_try`는 main claim이 아니라 vocab size, init, fallback, replay, repair, downstream proxy failure analysis로 배치한다.
- Final goal audit verdict는 `DIAGNOSTIC_NEGATIVE_REPORT_READY`다. Positive model claim으로는 `NO_GO`다.

## One-Line Contract

`third_try`는 target10 low-resource 언어 전체를 main으로 두고, high-resource replay/control data를 동시에 사용해 실제 downstream 성능 개선 모델을 만드는 것을 목표로 한다. Coptic/Syriac는 extension이 아니라 main evidence이며, 기존 실험은 ablation/failure analysis로 재배치한다.
