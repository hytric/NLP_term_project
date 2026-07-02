# v5 현재 진행상황 현황판

마지막 확인: 2026-06-28 17:20 KST

이 문서는 v5 실험을 바로 이해하기 위한 한국어 현황판이다. 최종 수치표는
`3_evaluation/09_aggregation/`와 `4_reporting/00_tables/`를 기준으로
승격해야 하며, live log 숫자는 최종 claim에 직접 복사하지 않는다.

## 한 줄 요약

현재는 **matched `v5_random`/`v5_fvt` 10K checkpoints가 모두 준비된 상태**이고,
post-checkpoint downstream evaluation을 실행 중이다. 최종 framing은 v5를 본
실험으로 둔다. 이유는 v5 target10이 진짜 low-resource XLM-R-unseen target10이기
때문이다. PPPL은 Glot500 held-out test metric으로 과장하지 않고, v5에서는
train-source intrinsic diagnostic으로 명시한다. target downstream coverage는
현재 repo에서 확인 가능한 local task-list 기준 `8/10` partial이지만 기존 로컬 materialization이 tail flag를
잘못 해석해 undercount했으므로, repair 전까지 downstream은 available-language
replay로만 보고한다.

```text
READY_TO_LAUNCH=yes
MAIN_EXPERIMENT=v5
MAIN_CLAIM=genuine_low_resource_target10_intrinsic_proxy
TARGET_DOWNSTREAM_CLAIM=no
LOCAL_TARGET_TASK_MEMBERSHIP=8/10_partial
LOCAL_TARGET_DOWNSTREAM_CLAIM=pending_materialization_repair
V51_ROLE=downstream_aware_diagnostic_ablation
v5_random_ready=yes
v5_fvt_ready=yes
post_checkpoint_preflight=post_checkpoint_preflight_ready_to_launch
current_next=SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=2 bash scripts/run_v5_post_checkpoint_evals.sh downstream
```

## 지금 실제로 하고 있는 일

- `v5_fvt_mlm_10k` continued MLM training은 완료됐다.
- `v5_random`과 `v5_fvt` 모두 `ready_for_wrapper=yes`이다.
- `v5_fvt` downstream evaluation이 detached process로 실행 중이다.
- 실행 PID: `2961565`
- 실행 log:
  `/home/axt/mnt2/jongha/v5_glot50010/runs/finalization_logs/downstream_v5_fvt_20260628_171938.log`
- 현재 첫 metric은 Tatoeba retrieval이며, GPU `2`에서 실행 중이다.
- report/PPT는 execution draft로 유지하고, parsed FVT rows가 들어온 뒤 claim을 승격한다.

## 단계별 체크포인트

| 단계 | 상태 | 체크포인트 | 핵심 결과 | 다음 기준선 |
| --- | --- | --- | --- | --- |
| 0. 범위 고정 | [x] 완료 | 92 XLM-R-seen + 10 Glot500-internal target | 총 102 language-script | full 511-language reproduction이라고 쓰지 않기 |
| 1. 데이터 구성 | [x] 완료 | raw symlink 102개, missing dir 0 | main merge `92,452,251` lines, `19G` | 같은 corpus를 tokenizer/MLM/eval에 사용 |
| 2. tokenizer 확장 | [x] 완료 | Glot500-style full corpus tokenizer train | XLM-R 대비 `118,685` tokens appended; target vocab len `368,687` | tokenizer audit failure 0 유지 |
| 3. embedding init | [x] 완료 | random/mean/FVT initialized checkpoints | FVT rows `118,427`; `<mask>` diff `0.0`; LM head tied | novelty는 tokenizer가 아니라 initialization 비교로 주장 |
| 4. zero-step novelty | [x] 완료 | pre-MLM proxy evaluation | target weighted NLL: random `18.411756`, FVT `8.785518`, delta `-9.626238` | 이 결과는 intrinsic claim까지만 사용 |
| 5. matched MLM | [x] 완료 | `v5_random`/`v5_fvt` 10K checkpoint ready | 둘 다 `ready_for_wrapper=yes` | 없음 |
| 6. Glot500 metric replay | [~] 실행 중 | baseline/reference + `v5_random` rows measured; `v5_fvt` downstream running | Tatoeba/Bible/Taxi1500/NER/POS/Roundtrip FVT rows 실행 중 | 완료 후 aggregation/report/PPT refresh |
| 7. report/PPT package | [~] execution draft 준비 | report PDF, deck PPTX/PDF, release bundle 존재 | final deliverable은 pending results | parsed FVT rows 삽입 후 refresh/freeze |

## 수행 완료 체크리스트

- [x] target10을 Glot500 내부 데이터에서 다시 고름.
- [x] target10 조건을 `XLM-R != True`, `new_length >= 30000`, raw directory 존재로 고정.
- [x] 지역/문자/어족 다양성을 고려한 target10으로 범위 재정의.
- [x] v5 raw symlink root 생성: `/home/axt/mnt2/jongha/v5_glot50010/raw`.
- [x] full merge 완료: `Glot500_v5_glot50010_xlmr100.txt`.
- [x] full tokenizer training 완료.
- [x] tokenizer audit 완료.
- [x] random/mean/FVT embedding initialization 완료.
- [x] `<mask>` remap, LM-head tying, FVT row audit 완료.
- [x] main zero-step MLM proxy 완료.
- [x] `v5_random_mlm_10k` continued MLM 완료.
- [x] `v5_fvt_mlm_10k` continued MLM 완료.
- [x] matched checkpoint pair가 `ready_for_wrapper=yes`로 승격.
- [x] Glot500 held-out PPPL 정책 정리: v5 `PPPL_SPLIT=train`은 diagnostic, v5.1은 strict held-out.
- [x] PPPL 실행 가드 추가: train-source PPPL은 명시 플래그가 있어야 실행.
- [x] `v5_fvt` downstream evaluation detached launch 시작.
- [x] `v5_random` post-10K PPPL, Tatoeba, Bible, Taxi1500, NER, POS, Roundtrip rows 측정.
- [x] XLM-R baseline과 Glot500-base reference rows 측정 및 aggregation 반영.
- [x] Glot500 metric family를 모두 유지하도록 metric ledger/report surface 구성.
- [x] report/PPT execution draft 생성.
- [x] rendered artifacts 생성: report PDF/HTML, deck PPTX/PDF/HTML.
- [x] release bundle 생성 및 audit.
- [x] overclaim guard, claim promotion matrix, final evidence packet audit 구성.

## 진행 중 체크리스트

- [~] `v5_fvt` Tatoeba retrieval 실행 중.
- [ ] `v5_fvt` Bible retrieval 측정.
- [ ] `v5_fvt` Taxi1500 classification 측정.
- [ ] `v5_fvt` NER 측정.
- [ ] `v5_fvt` POS 측정.
- [ ] `v5_fvt` Roundtrip alignment 측정.
- [ ] `python3 scripts/refresh_v5_reporting.py --with-plots`로 aggregation/report/PPT 갱신.

현재 live row:

| Run | Status | Step | Progress | Wrapper ready | Evidence |
| --- | --- | ---: | ---: | --- | --- |
| `v5_random_mlm_10k` | ready | `10000/10000` | `100.00%` | yes | model artifact exists |
| `v5_fvt_mlm_10k` | ready | `10000/10000` | `100.00%` | yes | model artifact exists |

## 남은 실행 체크리스트

- [x] `bash scripts/run_v5_post_checkpoint_evals.sh status`에서 `READY_TO_LAUNCH=yes` 확인.
- [x] downstream launcher 실행:

```bash
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=2 \
  bash scripts/run_v5_post_checkpoint_evals.sh downstream
```

- [ ] downstream launcher 완료 대기.
- [ ] `python3 scripts/refresh_v5_reporting.py --with-plots`로 aggregation/report/PPT 재생성.
- [ ] `method_comparison_summary.md`, `claim_promotion_matrix.md`,
  `final_claim_decision_tree.md` 확인.
- [ ] Report/PPT의 pending result 문장을 parsed result 기반 문장으로 교체.
- [ ] `final_evidence_packet_audit.md`가 ready 계열 verdict인지 확인.
- [ ] `final_deliverable_audit.md`와 `final_submission_smoke_audit.md`로 최종 제출 후보 여부 확인.

## 핵심 결과

### 데이터와 범위

| 항목 | 값 |
| --- | ---: |
| seen/head language-scripts | 92 |
| target/tail language-scripts | 10 |
| total language-scripts | 102 |
| planned total samples | 92,452,251 |
| main merged corpus size | 19G |
| raw symlink count | 102 |
| missing raw dirs | 0 |

Selected target10:

```text
fur_Latn
krc_Cyrl
acm_Arab
dzo_Tibt
sat_Olck
mad_Latn
bam_Latn
kjb_Latn
quw_Latn
rap_Latn
```

### Novelty 결과: zero-step FVT advantage

| Group | Metric | Random | FVT | FVT - Random | Relative | 해석 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| head | weighted NLL | 12.895301 | 6.621457 | -6.273844 | -48.65% | FVT 유리 |
| target10 | weighted NLL | 18.411756 | 8.785518 | -9.626238 | -52.28% | FVT 유리 |
| all | weighted NLL | 16.511807 | 8.040183 | -8.471624 | -51.31% | FVT 유리 |

이 결과는 **embedding initialization 자체의 intrinsic evidence**이다. 최종
after-training method claim은 `v5_fvt` downstream row가 측정되어야 승격한다.
PPPL은 v5에서 train-source diagnostic으로만 쓰고, held-out test PPPL은 v5.1로
분리한다.

### 현재 metric completion

| Metric family | Coverage | Measured models | Missing |
| --- | ---: | --- | --- |
| PPPL diagnostic | 102/102 | `xlmr_base`, `glot500_base`, `v5_random` | `v5_fvt` optional diagnostic |
| Tatoeba retrieval | 63/102 | `xlmr_base`, `glot500_base`, `v5_random` | `v5_fvt` |
| Bible retrieval | 74/102 | `xlmr_base`, `glot500_base`, `v5_random` | `v5_fvt` |
| Taxi1500 classification | 1/102 | `xlmr_base`, `glot500_base`, `v5_random` | `v5_fvt` |
| NER | 78/102 | `xlmr_base`, `glot500_base`, `v5_random` | `v5_fvt` |
| POS | 58/102 | `xlmr_base`, `glot500_base`, `v5_random` | `v5_fvt` |
| Roundtrip alignment | 74/102 | `xlmr_base`, `glot500_base`, `v5_random` | `v5_fvt` |

Target10 downstream boundary:

- PPPL target10 raw-text coverage는 `10/10`이지만, 현재 row는 train-source diagnostic이다.
- 현재 repo에서 확인 가능한 Tatoeba/Bible/NER/POS task-list 기준으로는 target10 중
  `8/10`에 일부 membership이 있다:
  `fur_Latn=NER`, `rap/krc/kjb/quw/mad/dzo=Bible`, `bam=Bible,POS`.
- 기존 Tatoeba/Bible/NER/POS/Roundtrip local coverage/materialization 산출물은
  task-list flag `0`을 tail이 아니라 unavailable로 처리한 흔적이 있으므로 repair가
  필요하다.
- target-language downstream claim을 목표로 하면 현재 target10 자체를 버릴 필요는
  없지만, Bible/NER/POS tail materialization/eval을 먼저 재점검해야 한다.
- 따라서 target10 improvement claim은 PPPL과 tokenization/proxy 중심으로 둔다.
- Downstream은 available-language/head/all replay로 보고한다.

### 이미 측정된 주요 score rows

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

Glot500-base는 equal-budget baseline이 아니라 external/reference checkpoint로만 해석한다.

## 지금 막힌 이유

현재 blocker는 code failure가 아니라 **long downstream evaluation runtime**이다.

| Gate | Current | 의미 |
| --- | --- | --- |
| `v5_random_ready` | yes | random-init 10K checkpoint는 평가 가능 |
| `v5_fvt_ready` | yes | FVT 10K model artifact가 있음 |
| `post_checkpoint_preflight` | ready_to_launch | long eval 실행 가능 |
| `READY_TO_LAUNCH` | yes | downstream eval 실행 중 |

따라서 지금은 실행 중인 detached downstream job의 완료를 기다리면 된다. PPPL은
기본 `all` 모드에서 skip되며, train-source diagnostic을 원할 때만
`RUN_TRAIN_SOURCE_PPPL_DIAGNOSTIC=1`로 명시 실행한다.

## 바로 열어볼 파일

| 목적 | 파일 |
| --- | --- |
| 현재 launch gate | `4_reporting/final_action_dashboard_ko.md` |
| live training ETA | `2_training/mlm_progress_eta.md` |
| 실행 중인 job 상태 | `3_evaluation/running_status.md` |
| 언어별 데이터 구성 | `DATA_COMPOSITION_KO.md` |
| 언어 소스/coverage overlap | `LANGUAGE_SOURCE_OVERLAP_KO.md` |
| target10 downstream 재선정 audit | `TARGET10_RESELECTION_FOR_DOWNSTREAM_KO.md` |
| 언어별 상세 train/dev/test count | `0_tokenizer/00_data_scope/data_composition_by_language.md` |
| tokenizer 확장 방법 판정 | `TOKENIZER_EXTENSION_METHODS_KO.md` |
| post-checkpoint queue | `3_evaluation/post_checkpoint_eval_queue.md` |
| 최종 handoff 순서 | `4_reporting/final_handoff_runbook.md` |
| novelty 비교 | `4_reporting/method_comparison_summary.md` |
| claim 승격 조건 | `4_reporting/claim_promotion_matrix.md` |
| 최종 evidence packet | `4_reporting/final_evidence_packet_audit.md` |
| report draft | `Report.md` |
| 단계별 진행보고 | `PROGRESS_REPORT_KO.md` |
| paper/PPT package | `4_reporting/03_final_report/`, `4_reporting/02_slides/` |

## 재개 명령

먼저 status만 확인한다.

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
```

출력 끝이 아래처럼 바뀔 때만 다음 단계로 간다.

```text
READY_TO_LAUNCH=yes
```

현재 실행 중인 downstream job 확인:

```bash
ps -p 2961565 -o pid,etime,cmd
tail -f /home/axt/mnt2/jongha/v5_glot50010/runs/finalization_logs/downstream_v5_fvt_20260628_171938.log
```

마지막으로 report/PPT를 갱신한다.

```bash
python3 scripts/refresh_v5_reporting.py --with-plots
```

## 발표/보고서에 바로 쓸 현재 문장

```text
본 실험은 Glot500 전체 511개 언어의 완전 재현이 아니라, XLM-R 학습에
사용된 92개 language-script와 Glot500 내부에서 새로 선정한 10개 target
language-script로 제한한 controlled 102-language Glot500-style replay이다.
현재 데이터, tokenizer 확장, embedding initialization, zero-step novelty
evidence, v5-random 10K 결과, report/PPT execution draft는 준비되었고,
최종 method claim은 matched v5-FVT 10K checkpoint와 parsed post-checkpoint
metric rows가 들어온 뒤에만 승격한다.
```
