# v5 결과 지연 대응 Handoff

작성 상태: execution draft.

이 문서는 matched `v5_random`/`v5_fvt` post-checkpoint 결과가 발표 또는 보고서
공유 시점까지 도착하지 않았을 때의 임시 대응선을 정리한다. 목표를 낮추는 문서가
아니다. 최종 목표는 여전히 paired 10K checkpoint, post-checkpoint PPPL,
available downstream replay, final report/PPT freeze까지 완료하는 것이다.

## 한 줄 판정

결과가 지연되면 **final result paper**가 아니라 **execution-draft report/PPT**로
공유한다. 이때 강한 주장은 `controlled 92+10 Glot500-style replay`와
`zero-step FVT initialization advantage`까지만 허용한다.

## 공유 가능/금지 Matrix

| 영역 | 공유 가능 | 금지 | 근거 파일 |
| --- | --- | --- | --- |
| 재연 범위 | 92 seen + 10 target controlled subset에서 Glot500-style pipeline을 재연했다 | full 511-language Glot500 reproduction | `00_tables/table_15_glot500_reproduction_fidelity.md`, `goal_readiness.md` |
| 데이터 | target10은 Glot500 내부 raw, XLM-R unseen, 30K 이상, 지역/문자 다양성 기준으로 골랐다 | target selection 자체가 main novelty | `00_tables/table_01_data_scope.md`, `../0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv` |
| tokenizer | Glot500-style SPM append와 audit를 완료했고, `dzo_Tibt` regression은 limitation으로 공개한다 | every target improved | `00_tables/table_02_tokenizer_audit.md`, `03_final_report/claim_ledger.md` |
| initialization novelty | FVT/source-token decomposition initialization이 zero-step target MLM proxy에서 random보다 좋은 시작점을 보였다 | after-MLM/downstream superiority claim | `00_tables/table_03_initialization_zero_step.md`, `method_comparison_summary.md` |
| continued MLM | `v5_random`은 ready, `v5_fvt`는 running 또는 pending 상태라고 운영 상태를 말한다 | live step/ETA를 model-quality result로 말하기 | `../2_training/mlm_progress_eta.md`, `../2_training/live_training_health.md` |
| Glot500 metrics | PPPL, Tatoeba, Bible, Taxi1500, NER, POS, Roundtrip을 모두 retained metric family로 유지했다 | v5 method rows가 이미 완료됐다고 말하기 | `metric_fidelity_audit.md`, `metric_execution_ledger.md` |
| downstream | available-language downstream replay protocol과 baseline/reference rows를 보고한다 | target10 downstream improvement | `00_tables/table_04_evaluation_coverage.md`, `00_tables/table_13_metric_fidelity_matrix.md` |
| final conclusion | final method conclusion is pending matched checkpoint and parsed v5 rows | final report/PPT complete | `final_claim_decision_tree.md`, `final_goal_acceptance_rubric_ko.md` |

## 발표에서 쓸 안전 문장

```text
현재 이 자료는 final result paper가 아니라 execution draft입니다. 데이터 구성,
Glot500-style tokenizer expansion, initialization audit, zero-step novelty,
그리고 Glot500 metric-family replay protocol은 준비되어 있습니다. 다만
`v5_fvt` matched checkpoint와 post-checkpoint metric rows가 아직 들어오지 않았기
때문에 after-MLM PPPL 및 downstream superiority claim은 잠가두었습니다.
```

## 보고서/PPT 표시 규칙

| 위치 | 결과 지연 시 표시 |
| --- | --- |
| report abstract | `execution draft`와 `final method claims pending matched checkpoint` 문장을 유지 |
| report results | zero-step 결과와 baseline/reference rows만 수치 claim으로 사용 |
| report conclusion | `final_claim_decision_tree.md`의 zero-step-only/pending outcome 유지 |
| slide 10 | live training status는 operational state로만 표시 |
| slide 11 | metric-family status와 coverage를 표시하고 v5 rows는 waiting으로 둠 |
| slide 12 | baseline/reference와 zero-step novelty만 표시; after-MLM v5 rows는 `waiting checkpoint` |
| slide 14 | final method conclusion pending 문장 유지 |
| Q&A | `reviewer_response_crosswalk_ko.md`와 `defense_qa_ko.md`의 locked-claim 답변 사용 |

## 제출/공유 전 체크

결과가 아직 없다면 아래 조건이 모두 `ready`일 때만 execution draft로 공유한다.

| Check | Required evidence |
| --- | --- |
| artifact freshness | `rendered_artifact_freshness_audit.md` |
| overclaim guard | `surface_overclaim_audit.md` |
| stale live/result slot guard | `reporting_package_audit.md` |
| release bundle | `release_bundle_audit.md` |
| final smoke | `final_submission_smoke_audit.md` with `execution_draft_ready` verdict |
| claim freeze | `final_claim_freeze_audit.md` with waiting-for-results verdict |

## 결과가 뒤늦게 도착하면

아래 순서로만 final candidate로 승격한다.

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
# Continue only when the status output says READY_TO_LAUNCH=yes.
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
python3 scripts/refresh_v5_reporting.py --with-plots
```

`READY_TO_LAUNCH=no`이면 평가를 시작하지 않고 `NEXT_COMMAND`에 표시된
watcher/status 명령으로 돌아간다.

의도적으로 모든 post-checkpoint row를 재측정할 때만
`WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all`
을 사용한다.

그 다음 `final_result_update_checklist_ko.md`,
`post_result_patch_plan_ko.md`, `comparison_materiality_audit.md`,
`final_claim_decision_tree.md`, `final_claim_freeze_audit.md` 순서로 확인한다.

## 결론

결과 지연 대응은 실패 선언이 아니다. 이 프로젝트는 이미 재연 scope, tokenizer,
initialization, metric-family protocol, report/PPT handoff가 잘 정리되어 있다.
다만 final method claim은 paired v5 rows 이후에만 열리는 구조로 유지한다.
