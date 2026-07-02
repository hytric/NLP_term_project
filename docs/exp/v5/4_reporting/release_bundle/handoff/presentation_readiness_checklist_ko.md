# v5 발표 직전 체크리스트

작성 상태: execution draft, 2026-06-28 기준.

이 파일은 발표 직전 5분 동안 보는 한국어 체크리스트이다. 보고서/PPT의
최종 숫자 source가 아니라, 어떤 파일을 열고 어떤 주장을 잠글지 정리하는
handoff 문서이다. 현재 checkpoint 진행률과 Go/No-Go는 항상
`final_action_dashboard_ko.md`와
`bash scripts/run_v5_post_checkpoint_evals.sh status` 출력을 우선한다.

## 1. 먼저 열 파일

| 순서 | 파일 | 확인할 것 |
| --- | --- | --- |
| 1 | `final_action_dashboard_ko.md` | 현재 상태, 다음 명령, 열린 gate |
| 2 | `one_page_summary_ko.md` | 안전한 한 문장 요약과 금지 claim |
| 3 | `02_slides/rehearsal_plan_ko.md` | 5/8/12/15분 발표 운영과 checkpoint 상태별 마지막 20초 |
| 4 | `02_slides/v5_final_deck_ko.pptx` | 실제 발표 deck |
| 5 | `02_slides/presenter_script_ko.md` | slide별 말문 |
| 6 | `02_slides/defense_qa_ko.md` | 질문 방어 문장 |
| 7 | `final_claim_decision_tree.md` | slide 14 결론을 바꿔도 되는지 |
| 8 | `post_checkpoint_trigger_card_ko.md` | checkpoint 이후 평가 실행 Go/No-Go |

## 2. 발표 가능 상태 판정

| 상태 | 말해도 되는 것 | 말하면 안 되는 것 |
| --- | --- | --- |
| `READY_TO_LAUNCH=no` | setup fidelity, tokenizer 결과, zero-step FVT novelty, baseline/reference rows, 남은 gate | after-MLM FVT 우세, downstream FVT 우세, target10 downstream improvement |
| `READY_TO_LAUNCH=yes` but metrics not parsed | 평가 실행 준비 완료 | 아직 숫자 결과나 결론 변경 |
| v5 rows parsed and refreshed | `final_claim_decision_tree.md`가 허용한 outcome | decision tree 밖의 즉흥 결론 |

## 3. 안전한 핵심 문장

```text
v5는 full 511-language Glot500 재학습이 아니라, 92 seen + 10 Glot500-internal
target으로 제한한 controlled Glot500-style replay이다. 현재 확정 claim은
data/tokenizer/initialization/zero-step novelty이며, after-MLM과 downstream
method claim은 matched checkpoint와 parsed metric row 이후에만 연다.
```

## 4. 반드시 잠글 claim

- `full 511-language Glot500 reproduction`이라고 말하지 않는다.
- `Glot500-base`를 equal-budget baseline이라고 말하지 않는다.
- FVT가 after-MLM PPPL에서 좋다고 말하려면 `v5_random`/`v5_fvt` PPPL rows가
  aggregation에 있어야 한다.
- FVT가 downstream에서 좋다고 말하려면 available downstream rows와
  `claim_promotion_matrix.md`가 unlock 상태여야 한다.
- target10 downstream improvement는 target10 downstream coverage가 0/10이면
  말하지 않는다.
- live training step, ETA, GPU 사용률은 결과가 아니라 운영 상태이다.

## 5. 30초 Q&A 답변

**왜 Glot500 완전 재현이 아닌가?**

계산 가능성과 실험 통제를 위해 92 seen + 10 target으로 범위를 고정했다. 대신
Glot500-style tokenizer expansion, continued MLM, metric family, head/tail/all
reporting 구조는 유지했다.

**novelty가 무엇인가?**

새 corpus가 아니라 vocabulary extension 이후 appended embedding row를 어떻게
초기화할지 비교한 것이다. FVT는 새 token surface를 기존 tokenizer로 분해해
source subtoken embedding 평균으로 초기화한다.

**downstream은 충분한가?**

Glot500 metric family는 모두 유지한다. 다만 target10 downstream local coverage는
현재 대부분 0/10이므로, downstream은 available-language/head/all 기준으로 보고하고
target10은 PPPL과 tokenizer/zero-step 중심으로 해석한다.

**지금 결과를 최종 결론으로 말할 수 있나?**

현재 `READY_TO_LAUNCH=no`이면 아니다. zero-step novelty와 setup fidelity는 말할 수
있지만 after-MLM/downstream method claim은 checkpoint와 aggregation 이후에만 말한다.

## 6. 결과가 들어온 뒤 교체 순서

1. `bash scripts/run_v5_post_checkpoint_evals.sh status`
2. `SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all`
3. `python3 scripts/refresh_v5_reporting.py --with-plots`
4. `method_comparison_summary.md`, `comparison_materiality_audit.md`,
   `claim_promotion_matrix.md`, `final_claim_decision_tree.md` 확인
5. `post_result_patch_plan_ko.md`에서 `ready_for_patch` row만 수정
6. slide 11 status/coverage, slide 12 result values, slide 14 conclusion 순서로 갱신
7. `reporting_package_audit.md`, `final_claim_freeze_audit.md`,
   `final_deliverable_audit.md`, `release_bundle_audit.md` 확인

## 7. 마지막 한 줄

```text
Checkpoint readiness unlocks evaluation; parsed aggregation rows unlock claims.
```

시간이 5분 이하로 줄면 `02_slides/rehearsal_plan_ko.md`의 `5분 긴급 발표안`만 따른다.
그 경우 slide 11/12의 수치를 많이 읽지 말고, scope, tokenizer, initialization audit,
zero-step novelty, locked final claim만 남긴다.
