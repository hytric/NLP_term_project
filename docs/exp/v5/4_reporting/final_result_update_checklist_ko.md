# v5 최종 결과 업데이트 체크리스트

작성 상태: execution draft, 2026-06-28 기준.

이 문서는 matched `v5_random`/`v5_fvt` checkpoint가 준비된 직후,
최종 report와 PPT에 결과를 넣을 때 보는 한국어 작업표이다. 새 metric 값을
주장으로 승격하지 않고, aggregation과 claim gate를 먼저 통과시키는 것이 목적이다.
현재 진행률과 ETA는 이 문서에 고정하지 않고 `final_action_dashboard_ko.md`와
`run_v5_post_checkpoint_evals.sh status`를 우선한다.

## 1. 실행 전 Go/No-Go

아래 명령으로 먼저 상태를 갱신한다.

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
```

평가 실행 조건:

| Gate | Go 조건 | No-Go 처리 |
| --- | --- | --- |
| model matrix | `v5_random`, `v5_fvt` 모두 `ready_for_wrapper=yes` | `waiting_model` 유지 |
| selected checkpoint manifest | 두 모델의 model file, trainer state, global step이 기록됨 | checkpoint selection pending |
| post-checkpoint queue | 실행할 metric row가 command를 가짐 | `none` command면 실행 금지 |
| post-checkpoint preflight | `post_checkpoint_preflight_ready_to_launch` | waiting/needs-update verdict면 긴 평가 실행 금지 |
| command consistency | `post_checkpoint_command_consistency_ready` | runbook/문서 명령 먼저 수정 |
| parser contract | `parser_contract_ready_*` 또는 final-ready 계열 | parser output path 먼저 수정 |
| provenance contract | `../3_evaluation/post_checkpoint_provenance_audit.md`가 ready 계열 | run_meta/source/log provenance 먼저 수정 |

위 조건이 충족되기 전에는 긴 평가를 실행하지 않는다. live step, ETA, GPU 사용률은
품질 결과가 아니라 운영 상태이다.

## 2. 평가 실행 순서

현재 큐처럼 일부 metric/model row가 이미 `measured`로 들어온 경우에는
중복 실행을 피하기 위해 `SKIP_MEASURED=1`을 붙여 전체 paired pass를 재개한다.

```bash
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
python3 scripts/refresh_v5_reporting.py --with-plots
```

의도적으로 모든 post-checkpoint row를 재측정할 때만 아래 canonical full rerun을
사용한다.

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
python3 scripts/refresh_v5_reporting.py --with-plots
```

`SKIP_MEASURED=1`은 중복 실행 방지용이지 claim 승격 조건이 아니다.

길게 나눠야 할 때만 아래 순서를 쓴다.

```bash
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh pppl
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream
python3 scripts/refresh_v5_reporting.py --with-plots
```

개별 metric 복구 명령은 `3_evaluation/post_checkpoint_eval_recovery.md`를 따른다.

## 2.5. 결과 도착 직후 10분 루틴

metric output이 새로 생기면 바로 문장을 고치지 말고 아래 순서를 고정한다.

1. `python3 scripts/refresh_v5_reporting.py --with-plots`
2. `3_evaluation/09_aggregation/metric_completion.tsv`에서 metric별 measured/missing
   상태 확인.
3. `../3_evaluation/post_checkpoint_provenance_audit.md`에서 source file,
   `run_meta.tsv`, command log가 모두 남았는지 확인.
4. `4_reporting/method_comparison_summary.md`에서 `v5_random`/`v5_fvt` 비교가
   paired row 기준으로 생성됐는지 확인.
5. `4_reporting/comparison_materiality_audit.md`에서 비교 차이가 `tie_band`,
   `small`, `moderate`, `large` 중 어디에 속하는지 확인한다. `tie_band`는
   실질적 차이 없음으로 쓰고, `small`은 cautious wording으로만 사용한다.
6. `4_reporting/final_claim_decision_tree.md`와
   `4_reporting/post_checkpoint_outcome_matrix_ko.md`가 같은 outcome family를
   가리키는지 확인.
7. downstream transfer를 말하기 전에 `post_checkpoint_outcome_matrix_ko.md`의
   `Available Downstream Majority Rule`로 measured metric family 수, FVT 우세 수,
   tie/incomplete family를 먼저 센다.
8. report는 `03_final_report/result_interpretation_blocks.md`의 outcome별 문장
   블록에서만 결론 문장을 고른다.
9. PPT는 slide 11 status/coverage, slide 12 result values, slide 14 conclusion
   순서로만 수정하고, `02_slides/slide_claim_checklist.md`를 같이 갱신한다.
10. 마지막에 `reporting_package_audit.md`, `final_claim_freeze_audit.md`,
   `final_deliverable_audit.md`, `release_bundle_audit.md`를 확인한다.

이 루틴의 목적은 숫자를 빨리 붙이는 것이 아니라, aggregation -> claim gate ->
report/PPT wording 순서를 지키는 것이다.

## 2.6. 15분 report/PPT 패치 순서

결과가 모두 parse된 직후에는 아래 순서만 따른다. 이 순서는 최종 claim이
aggregation보다 먼저 바뀌는 일을 막기 위한 편집 순서이다.

| 순서 | 파일 | 수정 내용 | 금지 사항 |
| --- | --- | --- | --- |
| 1 | `3_evaluation/09_aggregation/main_head_tail_all.tsv` | `v5_random`/`v5_fvt` paired row 존재 확인 | stdout 숫자 복사 금지 |
| 2 | `4_reporting/00_tables/table_06_pppl_partial.md` | after-MLM PPPL 행 갱신 확인 | zero-step 결과와 섞어 쓰기 금지 |
| 3 | `4_reporting/00_tables/table_07_*`-`table_14_*` | available downstream 행과 coverage note 확인 | target10 coverage 0/10을 성능 악화로 해석 금지 |
| 4 | `4_reporting/method_comparison_summary.md`, `comparison_materiality_audit.md`, `claim_promotion_matrix.md` | FVT-vs-random paired row, materiality band, promotable claim 상태 확인 | zero-step만으로 final improvement claim 작성 금지; `small`/`tie_band`를 강한 claim으로 쓰기 금지 |
| 5 | `4_reporting/post_checkpoint_outcome_matrix_ko.md` | PPPL direction과 available downstream majority/tie/incomplete count 확인 | PPPL과 downstream을 평균 내서 결론 만들기 금지 |
| 6 | `4_reporting/final_claim_decision_tree.md` | allowed outcome 하나만 선택 | live log나 단일 metric으로 outcome 선택 금지 |
| 7 | `4_reporting/03_final_report/result_interpretation_blocks.md` | 선택된 outcome의 abstract/conclusion 문장만 복사 | 새 결론 문장을 즉흥 작성 금지 |
| 8 | `4_reporting/03_final_report/paper_draft.md`, `paper_draft_ko.md` | abstract, results, discussion, conclusion 갱신 | full 511-language reproduction 표현 금지 |
| 9 | `4_reporting/02_slides/ppt_content.md` | slide 11 status -> slide 12 result values -> slide 14 conclusion 순서로 갱신 | slide 14 결론을 slide 12 result table보다 먼저 수정 금지 |
| 10 | `4_reporting/02_slides/presenter_script_ko.md` | slide 11/12/14 말문을 outcome에 맞춤 | target10 downstream improvement claim 금지 |
| 11 | `4_reporting/02_slides/slide_claim_checklist.md` | 새 숫자와 claim lock 확인 | pending claim을 unlocked로 직접 바꾸기 금지 |
| 12 | `python3 scripts/refresh_v5_reporting.py --with-plots` | figures, report/PPT, audits, release bundle 재생성 | refresh 전 수동 PDF/PPTX 공유 금지 |

최종 결론은 `final_claim_decision_tree.md`,
`post_checkpoint_outcome_matrix_ko.md`, `final_claim_freeze_audit.md`가 같은
방향을 가리킬 때만 바꾼다.

## 2.7. Metric Family Acceptance Rule

아래 조건을 metric family별 완료 조건으로 사용한다. `measured`는
`v5_random`과 `v5_fvt`가 모두 aggregation에 들어온 상태를 뜻한다.
한쪽만 있으면 final claim source가 아니라 recovery 대상이다.

| Metric family | 완료 조건 | 필수 table/source | Report/PPT 반영 조건 |
| --- | --- | --- | --- |
| PPPL | `v5_random`/`v5_fvt` 모두 `pseudoperplexity` row가 있고 target10 `10/10` coverage가 유지됨 | `main_head_tail_all.tsv`, `v5_target_subset.tsv`, `table_06_pppl_partial.md` | after-MLM intrinsic claim만 가능; downstream claim과 분리 |
| Tatoeba | 두 v5 model의 Top-10 row가 parsed되거나 명시적 blocker가 남음 | `main_head_tail_all.tsv`, `table_07_tatoeba_partial.md` | available-language retrieval claim만 가능 |
| Bible | 두 v5 model의 Top-10 row가 parsed되거나 명시적 blocker가 남음 | `main_head_tail_all.tsv`, `table_12_bible_partial.md` | target10 `0/10` coverage caveat 유지 |
| Taxi1500 | 두 v5 model의 macro-F1 row가 parsed되거나 명시적 blocker가 남음 | `main_head_tail_all.tsv`, `table_08_text_classification_partial.md` | narrow local classification claim만 가능 |
| NER | 두 v5 model의 F1 row가 parsed되거나 명시적 blocker가 남음 | `main_head_tail_all.tsv`, `table_10_ner_partial.md` | available-language tagging claim; target10-wide claim 금지 |
| POS | 두 v5 model의 F1 row가 parsed되거나 명시적 blocker가 남음 | `main_head_tail_all.tsv`, `table_11_pos_partial.md` | `TRAIN_LANGS=tur_Latn` caveat 유지 |
| Roundtrip | 두 v5 model의 accuracy row가 parsed되거나 명시적 blocker가 남음 | `main_head_tail_all.tsv`, `table_14_roundtrip_partial.md` | retained Glot500 metric-family claim; target10 `0/10` caveat 유지 |

완료 조건은 성능 향상 조건이 아니다. 성능 claim은 완료 조건을 통과한 뒤
`method_comparison_summary.md`, `comparison_materiality_audit.md`,
`claim_promotion_matrix.md`,
`final_claim_decision_tree.md`가 허용할 때만 작성한다.

## 3. 결과별 교체 위치

| 결과 | 필수 evidence | Report 교체 위치 | PPT 교체 위치 | 허용 claim |
| --- | --- | --- | --- | --- |
| selected checkpoints | `2_training/05_checkpoint_selection/selected_checkpoint_manifest.md` | training/checkpoint section, reproducibility appendix | slide 10, backup | matched comparison 시작 가능 |
| after-MLM PPPL | `09_aggregation/main_head_tail_all.tsv`, `v5_target_subset.tsv`, `table_06_pppl_partial.md` | abstract result sentence, results, analysis, conclusion | slide 11 status, slide 12 result values, slide 14 conclusion | intrinsic after-MLM FVT-vs-random claim 가능 |
| method comparison summary | `method_comparison_summary.md`, `comparison_materiality_audit.md`, `claim_promotion_matrix.md`, `final_claim_decision_tree.md` | novelty, results, discussion, conclusion | slides 9, 12, 14, presenter script | zero-step intrinsic claim 유지; final method claim은 paired PPPL/downstream 이후만 가능; `tie_band`는 no clear separation으로 작성 |
| Tatoeba retrieval | `main_head_tail_all.tsv`, `table_07_tatoeba_partial.md` | downstream results | slide 11 status, slide 12 result values | available-language retrieval claim만 가능 |
| Bible retrieval | `main_head_tail_all.tsv`, `table_12_bible_partial.md` | downstream results, limitations | slide 11 status, slide 12 result values, slide 13 caveat | target10 0/10 caveat 유지 |
| Taxi1500 | `main_head_tail_all.tsv`, `table_08_text_classification_partial.md` | downstream results | slide 11 status, slide 12 result values | local classification claim만 가능 |
| NER/POS | `main_head_tail_all.tsv`, `table_10_ner_partial.md`, `table_11_pos_partial.md` | tagging results | slide 11 status, slide 12 result values | POS `TRAIN_LANGS=tur_Latn` caveat 유지 |
| Roundtrip | `main_head_tail_all.tsv`, `table_14_roundtrip_partial.md` 또는 blocker row | downstream results, limitations | slide 11 status, slide 12 result values, slide 13 caveat | retained Glot500 metric family claim |
| final conclusion | `final_claim_decision_tree.md`, `final_claim_freeze_audit.md` | abstract, discussion, conclusion | slides 12, 14, presenter script | decision-tree outcome만 사용 |

## 4. Report/PPT 수정 규칙

- 숫자는 `3_evaluation/09_aggregation/` 또는 `00_tables/`에서만 복사한다.
- stdout, live log, partial output, 단일 모델 row만으로 report/PPT claim을 만들지 않는다.
- `Glot500-base`는 equal-budget baseline이 아니라 external reference라고 쓴다.
- full `511`-language reproduction이라고 쓰지 않는다. 표현은
  `controlled 102-language Glot500-style replay`로 고정한다.
- target10 downstream은 coverage가 없으면 개선/악화로 해석하지 않고
  `coverage-limited`로 남긴다.
- Bible과 Roundtrip은 빠뜨리지 않는다. measured, waiting, coverage-limited,
  blocked-data 중 하나로 반드시 상태를 남긴다.

## 5. 최종 Freeze 확인

결과를 넣은 뒤 아래 순서로 확인한다.

```bash
python3 scripts/refresh_v5_reporting.py --with-plots
python3 scripts/audit_v5_reporting_package.py
python3 scripts/write_v5_final_deliverable_audit.py
python3 scripts/build_v5_release_bundle.py
python3 scripts/audit_v5_release_bundle.py
```

최종 제출 가능 조건:

| File | 통과해야 하는 verdict |
| --- | --- |
| `result_promotion_readiness_audit.md` | result-ready 또는 claim-review 가능 상태 |
| `comparison_materiality_audit.md` | result-ready 또는 waiting-results 상태와 일치; final wording이 band를 따름 |
| `final_claim_decision_tree.md` | result-ready outcome 선택 |
| `final_claim_freeze_audit.md` | pending/disallowed claim lock 유지 |
| `reporting_package_audit.md` | package ready |
| `final_deliverable_audit.md` | pending result 없음 |
| `release_bundle_audit.md` | release bundle audit ready |

하나라도 pending이면 report/PPT는 execution draft로 유지한다.
