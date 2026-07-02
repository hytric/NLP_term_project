# v5 최종 목표 수락 루브릭

작성 상태: execution draft, 2026-06-28 기준.

이 문서는 사용자의 원래 목표를 최종 report/PPT 제출 기준으로 다시 풀어 쓴
한국어 acceptance rubric이다. 자동 판정은 `objective_completion_audit.md`와
`final_deliverable_audit.md`가 담당하고, 이 문서는 사람이 최종 제출 직전에
빠르게 확인하는 기준표이다.

## 1. 최종 목표별 수락 기준

| 사용자 목표 | 수락 기준 | 현재 증거 | 현재 상태 | 최종 gate |
| --- | --- | --- | --- | --- |
| Glot500을 충실히 재연 | full 511-language가 아니라 92+10 controlled subset에서 Glot500-style corpus merge, SPM append, continued MLM, metric-family replay를 수행 | `goal_readiness.md`, `table_15_glot500_reproduction_fidelity.md`, merge report | setup/protocol ready | matched v5 rows까지 aggregation에 들어가야 end-to-end |
| XLM-R seen 92개 + 선택 target10만 사용 | target10 manifest와 merge report가 92 seen, 10 target, missing dirs 0을 증명 | `0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv`, merge report | proven | scope 변경 없음 |
| novelty 확보 | corpus novelty가 아니라 appended vocabulary row initialization 비교로 novelty를 고정 | `table_03_initialization_zero_step.md`, FVT init report, `method_comparison_summary.md`, `comparison_materiality_audit.md` | zero-step novelty ready | after-MLM PPPL과 downstream은 checkpoint 이후, final wording은 materiality band를 따름 |
| downstream task도 Glot500에 충실 | PPPL, Tatoeba, Bible, Taxi1500, NER, POS, Roundtrip family를 모두 유지하고 measured/waiting/coverage-limited를 분리 | `metric_fidelity_audit.md`, `table_13_metric_fidelity_matrix.md`, `metric_completion.tsv` | protocol ready, v5-random diagnostic rows measured, v5-FVT rows pending | paired `v5_random`/`v5_fvt` post-checkpoint rows |
| 완전한 논문 형식 report | abstract, introduction, related work, data, method, results, analysis, limitations, conclusion, reproducibility, references가 존재하고 claim lock을 따름 | `paper_draft.md`, `paper_draft_ko.md`, `manuscript_completion_matrix.md` | execution draft ready | final decision tree가 non-pending outcome 선택 |
| PPT 발표 내용 작성 | 15-slide deck, presenter script, rehearsal plan, Q&A, claim checklist가 report와 동기화됨 | `final_deck_ko.md`, `v5_final_deck_ko.pptx`, `presenter_script_ko.md`, `slide_completion_matrix.md` | execution draft ready | slides 11/12/14가 final v5 rows로 갱신 |
| 결과 claim 안전성 | 모든 숫자는 aggregation 또는 `00_tables/`에서 오고, live log/stdout/single-model row는 final claim source가 아니며, high-risk overclaim과 tiny-delta overclaim은 guard 문맥 없이 남지 않음 | `reporting_package_audit.md`, `surface_overclaim_audit.md`, `comparison_materiality_audit.md`, `final_result_update_checklist_ko.md`, `source_map.md` | guard ready | final freeze 직전 guard 재실행 |
| Final Evidence Packet | 결과 row가 있더라도 checkpoint pair, metric rows, provenance, materiality, claim gate, patch targets, final freeze가 같은 refresh에서 함께 닫혀야 final claim으로 승격 | `post_result_patch_plan_ko.md`, `post_checkpoint_outcome_matrix_ko.md`, `result_insertion_contract_audit.md`, `final_action_dashboard_ko.md` | packet rule ready | packet incomplete이면 `measured but not promotable` |

## 2. 현재 최종 판정

현재 허용되는 말:

```text
v5는 Glot500-style workflow를 92+10 controlled subset에서 재연하는 실행 draft를
완성했고, vocabulary extension 이후 FVT initialization이 zero-step target MLM proxy에서
random resize보다 강한 intrinsic advantage를 보인다는 점까지는 증명했다.
```

아직 금지되는 말:

```text
final report/PPT is complete.
FVT improves after-MLM PPPL.
FVT improves downstream performance.
target10 downstream improves.
full 511-language Glot500 reproduction is complete.
```

## 3. 최종 Complete 판정 조건

아래가 모두 current artifact로 증명될 때만 active goal을 complete로 볼 수 있다.

| Gate | Required evidence |
| --- | --- |
| matched checkpoints | `v5_random`과 `v5_fvt` 모두 `ready_for_wrapper=yes`, selected checkpoint manifest에 model file/global step 기록, post-checkpoint preflight가 `post_checkpoint_preflight_ready_to_launch` |
| PPPL | `v5_random`과 `v5_fvt` PPPL row가 `09_aggregation/`에 parsed |
| downstream | available-language v5 rows가 parsed되거나 명시적 blocker/coverage-limited 상태로 남음 |
| materiality | `comparison_materiality_audit.md`가 final comparison row의 `tie_band`/`small`/`moderate`/`large` band를 기록하고 report/PPT wording이 이를 따름 |
| claim decision | `final_claim_decision_tree.md`가 waiting이 아닌 outcome을 선택 |
| report sync | `paper_draft.md`, `paper_draft_ko.md`, `Report.md`가 aggregation/table 값으로 갱신 |
| slide sync | slides 11/12/14, presenter script, Q&A가 같은 outcome을 말함 |
| source hygiene | `reporting_package_audit.md`의 stale/live/source hygiene guard가 ready |
| overclaim hygiene | `surface_overclaim_audit.md`가 `surface_overclaim_guard_ready`이고 unguarded high-risk claim이 0 |
| release package | `release_bundle_audit.md`가 ready이고 bundle status가 `FINAL_CANDIDATE` 또는 `FINAL_CANDIDATE_WITH_CAVEATS`로 표시됨 |
| outcome rule | `post_checkpoint_outcome_matrix_ko.md`가 metric별 방향, tie rule, incomplete evaluation 처리, slide 교체 규칙을 포함 |
| Final Evidence Packet | checkpoint pair, metric rows, provenance, materiality, claim gate, patch targets, final freeze가 같은 refresh 산출물에서 닫힘. 하나라도 빠지면 측정값은 `measured but not promotable`로 남김 |

## 4. 다음 실행선

두 모델이 모두 wrapper-ready이고 post-checkpoint preflight가 ready-to-launch가 된 뒤에만 아래를 실행한다.
긴 evaluation의 직접 실행 신호는 `bash scripts/run_v5_post_checkpoint_evals.sh status`
끝의 `READY_TO_LAUNCH=yes`이다. `READY_TO_LAUNCH=no`이면 두 번째 명령으로
넘어가지 않고 출력된 `NEXT_COMMAND`로 돌아간다.

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
# Continue only when the status output says READY_TO_LAUNCH=yes.
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
python3 scripts/refresh_v5_reporting.py --with-plots
```

그 다음 아래 파일을 보고 최종 결론을 고른다.

```text
final_claim_decision_tree.md
result_promotion_readiness_audit.md
comparison_materiality_audit.md
final_claim_freeze_audit.md
objective_completion_audit.md
final_deliverable_audit.md
```

결론 판정은 `post_checkpoint_outcome_matrix_ko.md`의 metric 방향을 따른다.
PPPL은 낮을수록 좋고, retrieval/F1/accuracy 계열은 높을수록 좋다. 한쪽 row만
있거나 parser/coverage 조건이 맞지 않으면 최종 method claim으로 승격하지 않고
`incomplete evaluation`으로 남긴다. `comparison_materiality_audit.md`에서
`tie_band`인 비교는 raw sign이 있더라도 no clear practical separation으로 쓰고,
`small` band는 cautious wording으로만 쓴다.

## 5. 심사자 5분 체크리스트

이 표는 최종 report/PPT를 처음 보는 심사자나 발표 질문자가 5분 안에 확인할
가능성이 높은 항목을 기준으로 만든다. 각 항목은 "그럴듯한 주장"이 아니라
현재 열 수 있는 evidence와 claim lock으로 방어되어야 한다.

| 심사 질문 | 바로 보여줄 답 | 열 evidence | 통과 기준 | 아직 잠긴 부분 |
| --- | --- | --- | --- | --- |
| 재연 범위가 정확한가? | full 511-language가 아니라 92+10 controlled Glot500-style replay이다. | `table_15_glot500_reproduction_fidelity.md`, `goal_readiness.md` | scope 축소와 retained workflow가 동시에 보인다. | full Glot500 reproduction claim |
| novelty가 명확한가? | target10 선택이 아니라 appended vocabulary row initialization 비교가 novelty이다. | `table_03_initialization_zero_step.md`, `method_comparison_summary.md`, `comparison_materiality_audit.md` | random/mean/FVT 비교, zero-step delta, materiality band가 보인다. | after-MLM/downstream superiority claim |
| Glot500 metric을 빼먹지 않았나? | PPPL, Tatoeba, Bible, Taxi1500, NER, POS, Roundtrip을 모두 retained surface로 유지했다. | `metric_fidelity_audit.md`, `table_13_metric_fidelity_matrix.md` | measured, waiting, coverage-limited row가 분리되어 있다. | target10 downstream improvement |
| 결과 claim이 안전한가? | 숫자는 aggregation/`00_tables/`에서만 승격하고 live log와 tiny delta는 강한 결과 claim이 아니다. | `reporting_package_audit.md`, `surface_overclaim_audit.md`, `comparison_materiality_audit.md` | stale/live/overclaim guard가 ready이고 `tie_band`/`small` wording rule이 보인다. | parsed v5 rows 전 method improvement |
| 최종 제출물이 열리는가? | report PDF, PPTX/PDF, 발표 대본, Q&A, release bundle이 존재한다. | `submission_file_index_ko.md`, `release_bundle/README.md`, `release_bundle_audit.md` | 필요한 파일이 존재하고 bundle은 현재 상태를 `EXECUTION_DRAFT_NOT_FINAL`로 표시한다. | final candidate label |
| 결과 이후 업데이트 경로가 분명한가? | status -> guarded all -> refresh -> patch plan -> decision tree 순서만 따른다. | `final_handoff_runbook.md`, `final_result_update_checklist_ko.md`, `post_result_patch_plan_ko.md` | slide 11/12/14와 report 결론 교체 위치가 파일 단위로 명시되어 있다. | checkpoints ready 전 long eval |
| 결과 해석 rule이 재현 가능한가? | PPPL/retrieval/F1/accuracy 방향, tie/incomplete 처리, materiality band를 outcome matrix와 audit이 고정한다. | `post_checkpoint_outcome_matrix_ko.md`, `comparison_materiality_audit.md` | 결과를 본 뒤 임의로 결론 문장을 만들지 않는다. | parsed v5 rows 전 outcome 선택 |
| Final Evidence Packet이 닫혔나? | 숫자 row만으로 final claim을 열지 않고, checkpoint/provenance/materiality/claim/freeze packet이 같은 refresh에서 닫혀야 한다. | `post_result_patch_plan_ko.md`, `result_insertion_contract_audit.md`, `final_action_dashboard_ko.md` | packet incomplete이면 `measured but not promotable`로 남긴다. | packet 닫히기 전 final claim |

심사자에게 가장 안전한 요약:

```text
현재 패키지는 setup/protocol/report/PPT는 발표 가능한 execution draft이고,
method-result conclusion은 matched v5 checkpoints와 parsed metric rows 이후에만
열리는 구조입니다. 따라서 지금의 강한 주장은 controlled Glot500-style replay와
FVT zero-step initialization advantage까지입니다.
```
