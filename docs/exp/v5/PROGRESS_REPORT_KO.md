# v5 단계별 진행 보고

작성 시각: 2026-06-28 17:20 KST

이 문서는 발표와 최종 report/PPT 작성자가 바로 읽을 수 있도록, 현재까지
무엇을 했고 무엇이 남았는지를 단계별 체크포인트와 핵심 결과 중심으로 정리한다.
실험은 좋은 방향으로 정돈되어 있고, 현재 남은 핵심 병목은 코드 문제가 아니라
`v5_fvt` downstream evaluation runtime이다.

## 1. 현재 결론

- [x] 데이터, tokenizer, embedding initialization, zero-step novelty evidence는 준비됐다.
- [x] `v5_random` 10K MLM과 post-checkpoint metric rows는 준비됐다.
- [x] `v5_fvt` 10K MLM checkpoint도 준비됐다.
- [x] `READY_TO_LAUNCH=yes` preflight가 열렸다.
- [x] v5 PPPL 정책을 수정했다: `PPPL_SPLIT=train`은 train-source diagnostic이며
  held-out test PPPL은 v5.1 strict correction line이다.
- [x] Report/PPT execution draft, PDF/PPTX, release bundle은 생성되어 있다.
- [~] `v5_fvt` downstream evaluation이 실행 중이다.
- [ ] parsed `v5_fvt` downstream rows가 아직 없어 final FVT-vs-random after-MLM/downstream claim은 잠겨 있다.

현재 launch gate:

```text
READY_TO_LAUNCH=yes
v5_random_ready=yes
v5_fvt_ready=yes
post_checkpoint_preflight=post_checkpoint_preflight_ready_to_launch
```

현재 training row:

| Run | Status | Step | Progress | ETA | Wrapper |
| --- | --- | ---: | ---: | --- | --- |
| `v5_random_mlm_10k` | ready | `10000/10000` | `100.00%` | done | yes |
| `v5_fvt_mlm_10k` | ready | `10000/10000` | `100.00%` | done | yes |

현재 downstream 실행 상태:

- [x] detached PID: `2961565`
- [x] log:
  `/home/axt/mnt2/jongha/v5_glot50010/runs/finalization_logs/downstream_v5_fvt_20260628_171938.log`
- [x] GPU: `2`
- [~] current first metric: `retrieval_tatoeba`

## 2. 단계별 체크포인트

| 단계 | 상태 | 완료 기준 | 현재 evidence | 남은 일 |
| --- | --- | --- | --- | --- |
| Scope freeze | [x] 완료 | 92 seen + 10 target 확정 | `README.md`, `0_tokenizer/dataset_processing.md` | 없음 |
| Data materialization | [x] 완료 | raw symlink 102개, missing 0 | `/home/axt/mnt2/jongha/v5_glot50010/raw` | 없음 |
| Corpus merge | [x] 완료 | 102-language corpus 생성 | `92,452,251` lines, `19G` | 없음 |
| Tokenizer expansion | [x] 완료 | Glot500-style XLM-R tokenizer 확장 | appended tokens `118,685`; vocab len `368,687` | 없음 |
| Tokenizer audit | [x] 완료 | head/target audit 통과 | failure 0 | 없음 |
| Embedding init | [x] 완료 | random/mean/FVT checkpoint 생성 | FVT rows `118,427`; `<mask>` diff `0.0` | 없음 |
| Zero-step proxy | [x] 완료 | pre-MLM random/FVT 비교 | target NLL delta `-9.626238` | final method claim으로 과승격 금지 |
| Matched MLM random | [x] 완료 | `v5_random` 10K checkpoint | `ready_for_wrapper=yes` | 없음 |
| Matched MLM FVT | [x] 완료 | `v5_fvt` 10K checkpoint | `ready_for_wrapper=yes` | 없음 |
| Post-checkpoint eval | [~] 실행 중 | Glot500 metric family row 측정 | XLM-R, Glot500-base, v5-random measured; v5-FVT downstream running | v5-FVT rows 완료 대기 |
| Report/PPT | [~] draft 준비 | report/PPT rendered artifacts | PDF/PPTX/release bundle exist | FVT 결과 삽입 후 freeze |

## 3. 수행한 작업 체크리스트

- [x] v5 폴더를 새 실험 라인으로 정리.
- [x] Glot500 내부에서 target10 재선정.
- [x] 10개 target 언어를 3만 문장 이상, XLM-R 미학습, raw directory 존재 조건으로 제한.
- [x] 지역/문자 다양성을 고려해 target10 구성.
- [x] 92 seen + 10 target의 controlled 102-language scope 확정.
- [x] full corpus merge 완료.
- [x] SentencePiece tokenizer 확장 완료.
- [x] tokenizer fertility/audit 완료.
- [x] random/mean/FVT embedding initialization 구현 및 산출물 생성.
- [x] source row copy, `<mask>` remap, LM-head tying audit 완료.
- [x] zero-step MLM proxy로 FVT 초기화 이점 확인.
- [x] paired MLM launcher로 `v5_random` 후 `v5_fvt` 순서 학습 시작.
- [x] `v5_random` 10K 학습 완료.
- [x] `v5_fvt` 10K 학습 완료.
- [x] `v5_random`/`v5_fvt` matched checkpoint pair ready 확인.
- [x] Glot500 PPPL held-out 원칙 확인 및 v5/v5.1 정책 분리.
- [x] PPPL 실행 가드 추가: train-source PPPL은 명시적으로 diagnostic이라고 선언해야 실행.
- [x] `v5_fvt` downstream evaluation detached launch.
- [x] baseline/reference와 `v5_random` post-checkpoint rows aggregation 반영.
- [x] Glot500 metric family를 모두 문서와 table/report/PPT surface에 유지.
- [x] report draft, Korean paper draft, PPT content, presenter script, defense Q&A 구성.
- [x] rendered report PDF/HTML과 deck PPTX/PDF/HTML 생성.
- [x] release bundle 생성 및 audit 완료.
- [x] overclaim guard와 claim promotion matrix 구성.
- [x] live status를 `CURRENT_STATUS_KO.md`에 정리.

## 4. 핵심 결과 요약

### 4.1 데이터 범위

| 항목 | 값 |
| --- | ---: |
| seen/head language-scripts | 92 |
| target/tail language-scripts | 10 |
| total language-scripts | 102 |
| total planned samples | 92,452,251 |
| merged corpus size | 19G |
| raw symlink count | 102 |
| missing raw dirs | 0 |

Target10:

```text
fur_Latn, krc_Cyrl, acm_Arab, dzo_Tibt, sat_Olck,
mad_Latn, bam_Latn, kjb_Latn, quw_Latn, rap_Latn
```

### 4.2 Tokenizer/embedding

| 항목 | 결과 |
| --- | --- |
| tokenizer method | Glot500-style SPM protobuf extension |
| tokenizer expansion | XLM-R 대비 `118,685` token append |
| final vocab len | `368,687` |
| FVT initialized rows | `118,427` |
| FVT fallback rows | `2` |
| `<mask>` remap diff | `0.0` |
| LM-head tied | true |

### 4.3 Novelty: zero-step FVT advantage

| Group | Random NLL | FVT NLL | Delta | Relative |
| --- | ---: | ---: | ---: | ---: |
| head | 12.895301 | 6.621457 | -6.273844 | -48.65% |
| target10 | 18.411756 | 8.785518 | -9.626238 | -52.28% |
| all | 16.511807 | 8.040183 | -8.471624 | -51.31% |

해석:

- [x] FVT/source-token decomposition initialization은 zero-step proxy에서 random보다 강하게 유리하다.
- [ ] 그러나 final after-training claim은 아직 아니다.
- [ ] final claim은 `v5_fvt` downstream rows가 들어와야 한다.
- [ ] PPPL held-out test claim은 v5가 아니라 v5.1 strict correction line에서만 가능하다.

## 5. Glot500 metric replay 상태

| Metric family | Coverage | Measured | Waiting |
| --- | ---: | --- | --- |
| PPPL diagnostic | 102/102 | XLM-R, Glot500-base, v5-random | v5-FVT optional diagnostic |
| Tatoeba retrieval | 63/102 | XLM-R, Glot500-base, v5-random | v5-FVT |
| Bible retrieval | 74/102 | XLM-R, Glot500-base, v5-random | v5-FVT |
| Taxi1500 classification | 1/102 | XLM-R, Glot500-base, v5-random | v5-FVT |
| NER | 78/102 | XLM-R, Glot500-base, v5-random | v5-FVT |
| POS | 58/102 | XLM-R, Glot500-base, v5-random | v5-FVT |
| Roundtrip alignment | 74/102 | XLM-R, Glot500-base, v5-random | v5-FVT |

Target10 downstream caveat:

- [x] PPPL은 target10 raw-text `10/10` coverage지만 현재 row는 train-source diagnostic.
- [ ] Tatoeba/Bible/Taxi1500/NER/POS/Roundtrip은 현재 target10 direct coverage `0/10`.
- [ ] target-language downstream claim을 하려면 target10을 downstream-aware로
  재선정해야 한다. 후보 audit은 `TARGET10_RESELECTION_FOR_DOWNSTREAM_KO.md`에 있다.
- [x] 따라서 downstream은 target10 improvement claim이 아니라 available-language/head/all replay로 보고한다.

## 6. 이미 확보한 주요 measured rows

| Metric | Group | XLM-R | Glot500-base | v5-random | v5-FVT |
| --- | --- | ---: | ---: | ---: | --- |
| PPPL | target10 | 61.980216 | 15.102934 | 39.222875 | waiting |
| PPPL | head | 8.117338 | 10.213100 | 18.726452 | waiting |
| PPPL | all | 9.986271 | 10.640353 | 20.138927 | waiting |
| Tatoeba Top-10 | all | 0.566067 | 0.706649 | 0.610353 | waiting |
| Bible Top-10 | all | 0.381153 | 0.509356 | 0.328019 | waiting |
| Taxi1500 macro-F1 | all | 0.592876 | 0.743338 | 0.702956 | waiting |
| NER F1 | all | 0.549858 | 0.627108 | 0.544628 | waiting |
| POS F1 | all | 0.481336 | 0.567542 | 0.481102 | waiting |
| Roundtrip accuracy | all | 0.185300 | 0.205189 | 0.190300 | waiting |

주의:

- Glot500-base는 equal-budget baseline이 아니라 external/reference checkpoint이다.
- v5-random rows는 FVT 비교 전 diagnostic/control row이다.
- final novelty claim은 v5-random vs v5-FVT matched rows 이후에만 가능하다.

## 7. Report/PPT 상태

| Artifact | 상태 | 위치 |
| --- | --- | --- |
| main report plan/draft | [x] execution draft | `Report.md` |
| paper draft | [x] execution draft | `4_reporting/03_final_report/paper_draft.md` |
| Korean paper draft | [x] execution draft | `4_reporting/03_final_report/paper_draft_ko.md` |
| report PDFs | [x] generated | `4_reporting/03_final_report/*.pdf` |
| PPT content | [x] execution draft | `4_reporting/02_slides/final_deck_ko.md` |
| PPTX/PDF deck | [x] generated | `4_reporting/02_slides/v5_final_deck_ko.*` |
| presenter script | [x] draft | `4_reporting/02_slides/presenter_script_ko.md` |
| release bundle | [x] ready as draft | `4_reporting/release_bundle/` |
| final deliverable | [ ] pending | waits for v5-FVT rows and claim freeze |

Current finalization verdicts:

```text
final_deliverable=final_deliverable_pending_results
final_submission_smoke=final_submission_smoke_execution_draft_ready
release_bundle=release_bundle_audit_ready
```

## 8. 다음에 해야 할 일

1. 계속 기다린다. 지금은 `v5_fvt`가 아직 `ready_for_wrapper=no`이므로 long eval을 실행하지 않는다.
1. 실행 중인 downstream job을 확인한다.

```bash
ps -p 2961565 -o pid,etime,cmd
tail -f /home/axt/mnt2/jongha/v5_glot50010/runs/finalization_logs/downstream_v5_fvt_20260628_171938.log
```

2. 필요하면 status를 확인한다.

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
```

3. PPPL train-source diagnostic은 원할 때만 명시 실행한다.

```text
RUN_TRAIN_SOURCE_PPPL_DIAGNOSTIC=1
```

4. downstream 결과가 들어오면 report/PPT를 갱신한다.

```bash
python3 scripts/refresh_v5_reporting.py --with-plots
```

5. v5.1 strict correction line에서는 held-out split을 먼저 만든 뒤 PPPL을 실행한다.

```bash
PPPL_SPLIT=test PPPL_EVAL_ROLE=heldout_test bash scripts/run_v5_eval_metric.sh pppl v5_fvt 1
```

6. 다음 파일을 확인한 뒤 final claim을 고정한다.

```text
4_reporting/method_comparison_summary.md
4_reporting/claim_promotion_matrix.md
4_reporting/final_claim_decision_tree.md
4_reporting/final_evidence_packet_audit.md
4_reporting/final_deliverable_audit.md
```

## 9. 발표용 현재 문장

```text
현재 v5는 Glot500 전체 511개 언어의 완전 재현이 아니라, XLM-R 학습에
사용된 92개 언어와 Glot500 내부 target10을 합친 controlled 102-language
Glot500-style replay로 정리되어 있다. 데이터 구성, tokenizer 확장,
embedding initialization, zero-step novelty evidence, v5-random 10K 결과,
그리고 report/PPT execution draft는 준비되었다. 현재 matched v5-FVT checkpoint는
준비됐고 downstream evaluation이 실행 중이다. 최종 novelty claim은 parsed
post-checkpoint downstream metrics가 도착한 뒤에만 승격한다. PPPL held-out test
claim은 v5.1 strict correction line으로 분리한다.
```

## 10. 관련 문서

| 목적 | 파일 |
| --- | --- |
| 실시간 현황판 | `CURRENT_STATUS_KO.md` |
| 언어별 데이터 구성 요약 | `DATA_COMPOSITION_KO.md` |
| 언어 소스/coverage overlap | `LANGUAGE_SOURCE_OVERLAP_KO.md` |
| target10 downstream 재선정 audit | `TARGET10_RESELECTION_FOR_DOWNSTREAM_KO.md` |
| 언어별 상세 count 표 | `0_tokenizer/00_data_scope/data_composition_by_language.md` |
| tokenizer 확장 방법 판정 | `TOKENIZER_EXTENSION_METHODS_KO.md` |
| PPPL held-out 정책 | `MLM_HELDOUT_POLICY_KO.md` |
| 전체 구조 | `README.md` |
| 실험 계획 | `Plan.md` |
| report 계획/초안 | `Report.md` |
| launch gate | `4_reporting/final_action_dashboard_ko.md` |
| handoff runbook | `4_reporting/final_handoff_runbook.md` |
| novelty comparison | `4_reporting/method_comparison_summary.md` |
| final claim gate | `4_reporting/claim_promotion_matrix.md` |
| report/PPT final audit | `4_reporting/final_deliverable_audit.md` |
