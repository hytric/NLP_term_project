# v5 One-Page Summary Korean

Last updated: 2026-06-28

이 파일은 발표/보고서용 정적 요약이다. 현재 checkpoint 진행률, ETA, Go/No-Go는
항상 `final_action_dashboard_ko.md`와
`bash scripts/run_v5_post_checkpoint_evals.sh status` 출력을 우선한다.

이 문서는 발표와 보고서 작성 시 바로 사용할 수 있는 한 페이지 요약이다.
수치 주장은 `3_evaluation/09_aggregation/`과 `00_tables/`에 들어간 값만 사용한다.

## 발표 직전 60초 체크

발표나 보고서 공유 직전에는 이 파일만 보지 말고, 아래 다섯 파일을 같은 순서로
확인한다. 다섯 파일 중 하나라도 `waiting`, `pending`, `locked`를 보이면 최종 claim은
열지 않는다.

1. `presentation_readiness_checklist_ko.md`: 발표 5분 전 claim lock과 열 파일 순서.
2. `final_action_dashboard_ko.md`: 지금 당장 할 일과 열려 있는 gate.
3. `final_handoff_runbook.md`: checkpoint 이후 report/PPT freeze까지의 명령 순서.
4. `final_claim_decision_tree.md`: slide 14와 결론 문장을 바꿔도 되는지 여부.
5. `02_slides/rehearsal_plan_ko.md`: 발표 시간이 5/8/12/15분 중 무엇인지와
   checkpoint 상태별 마지막 20초 문장.

현재 발표에서 안전한 frame은 하나다.

```text
Glot500 전체 511-language 재학습이 아니라, 92+10 controlled subset에서
Glot500-style workflow를 재연하고, 새 vocabulary row initialization을 novelty로
검증하는 실험이다.
```

반대로 아래 네 문장은 gate가 열리기 전까지 말하지 않는다.

```text
FVT가 MLM 이후 PPPL에서 우세하다는 확정 표현.
FVT가 downstream 전체에서 우세하다는 확정 표현.
target10 downstream 성능 향상을 주장하는 표현.
Glot500-base를 같은-budget 기준선으로 부르는 표현.
```

`v5_random`과 `v5_fvt`가 모두 `ready_for_wrapper=yes`가 되고
`post_checkpoint_preflight.md`가 `post_checkpoint_preflight_ready_to_launch`를
보고하기 전에는 live training progress를 결과처럼 말하지 않는다. 그 상태에서는
“평가 전 대기”가 맞고, 실패나 누락으로 해석하지 않는다.

## 한 문장 요약

v5는 Glot500 전체 511개 언어를 다시 학습하는 실험이 아니라, XLM-R에 있던
Glot500 language-script 92개와 Glot500 내부 target10을 사용해 Glot500식
corpus merge, SentencePiece append, continued MLM, metric family를 충실히 재연하고,
새 vocabulary row initialization 방법을 novelty로 분리해 검증하는 실험이다.

## 현재 안전하게 말할 수 있는 주장

- 재연 범위는 `controlled 102-language Glot500-style replay`이다.
- corpus scope는 고정됐다: 92 seen + 10 target, merge PASS, 실제 merged lines
  `92,452,251`, missing language dirs `0`.
- main tokenizer는 XLM-R SentencePiece에 auxiliary piece를 append하는
  Glot500-style 방식이다.
- extended tokenizer는 HF token 기준 `368,687`개이고, XLM-R-base 대비
  `118,685`개 token string이 추가됐다.
- tokenizer audit은 `29/30` language에서 fertility를 개선했다. 단 `dzo_Tibt`는
  `4.223938 -> 5.552124` tokens/word로 악화되어 visible limitation으로 남긴다.
- initialization audit은 source row identity copy, `<mask>` remap, byte-row
  accounting, LM-head tying을 통과했다.
- zero-step target weighted NLL은 random `18.411756`, mean `11.953142`,
  FVT `8.785518`이다. FVT는 random 대비 `-9.626238`, mean 대비 `-3.167624`
  낮다.
- `docs/exp/v5/4_reporting/method_comparison_summary.md` 기준 FVT는 random 대비
  weighted NLL을 target `52.28%`, head `48.65%`, all zero-step row `51.31%`
  낮춘다. 이는 zero-step novelty evidence이며 after-MLM/downstream claim은 아니다.
- PPPL, Tatoeba, Bible, Taxi1500, NER, POS, Roundtrip의 XLM-R-base 및
  Glot500-base reference rows는 local data가 있는 범위에서 측정되어 aggregation에
  들어갔다. v5-random도 PPPL, Tatoeba, Bible, Taxi1500, NER, POS, Roundtrip row가
  측정됐다.
- Bible retrieval은 74개 available language-script로 materialize 되었고,
  XLM-R-base Top-10 `0.381153`, Glot500-base Top-10 `0.509356`,
  v5-random Top-10 `0.328019`가 측정됐다.
  Roundtrip alignment도 74개 available language-script에서 XLM-R accuracy
  `0.185300`, Glot500-base accuracy `0.205189`, v5-random accuracy `0.190300`이
  측정됐다. 두 metric 모두 남은 v5-FVT row는 checkpoint 이후 평가한다.

## 아직 말하면 안 되는 주장

- full 511-language Glot500 reproduction 완료.
- FVT가 after-MLM에서도 random보다 좋다는 주장.
- FVT가 downstream task에서 개선된다는 주장.
- target10 downstream improvement.
- Glot500-base를 equal-budget baseline으로 해석하는 주장.

## 핵심 수치

| 항목 | 값 |
| --- | ---: |
| merged corpus lines | 92,452,251 |
| extended HF tokens | 368,687 |
| appended token strings | 118,685 |
| tokenizer audit improved | 29/30 |
| target10 improved | 9/10 |
| zero-step target NLL random | 18.411756 |
| zero-step target NLL mean | 11.953142 |
| zero-step target NLL FVT | 8.785518 |
| FVT - random target NLL | -9.626238 |
| XLM-R target PPPL | 61.980216 |
| Glot500-base target PPPL | 15.102934 |
| v5-random target PPPL | 39.222875 |
| XLM-R Tatoeba all available Top-10 | 0.566067 |
| Glot500-base Tatoeba all available Top-10 | 0.706649 |
| v5-random Tatoeba all available Top-10 | 0.610353 |
| XLM-R Bible all available Top-10 | 0.381153 |
| Glot500-base Bible all available Top-10 | 0.509356 |
| v5-random Bible all available Top-10 | 0.328019 |
| XLM-R Taxi1500 macro-F1 | 0.592876 |
| Glot500-base Taxi1500 macro-F1 | 0.743338 |
| v5-random Taxi1500 macro-F1 | 0.702956 |
| XLM-R NER all available F1 | 0.549858 |
| Glot500-base NER all available F1 | 0.627108 |
| v5-random NER all available F1 | 0.544628 |
| XLM-R POS all available F1 | 0.481336 |
| Glot500-base POS all available F1 | 0.567542 |
| v5-random POS all available F1 | 0.481102 |
| XLM-R Roundtrip all available acc. | 0.185300 |
| Glot500-base Roundtrip all available acc. | 0.205189 |
| v5-random Roundtrip all available acc. | 0.190300 |

## 남은 final gates

1. `v5_random_mlm_10k`와 `v5_fvt_mlm_10k`의 matched 10K checkpoints. 현재
   `v5_random`은 ready이고 `v5_fvt`가 running이다.
2. v5-FVT의 after-MLM PPPL과 paired v5 comparison.
3. available-language downstream replay의 남은 v5-FVT rows:
   Tatoeba, Bible, Taxi1500, NER, POS, Roundtrip.
4. `model_matrix.tsv`, `selected_checkpoint_manifest.md`,
   `post_checkpoint_eval_queue.md`, `post_checkpoint_command_consistency.md`,
   `post_checkpoint_parser_contract.md`가 같은 readiness verdict를 가리키는지 확인.
5. measured baseline/reference rows와 v5 checkpoint-pending rows를 분리 유지.
6. `scripts/refresh_v5_reporting.py` 후 `table_sync_audit.md`와
   `reporting_package_audit.md` 통과.

현재 operational status는 `2_training/mlm_progress_eta.md`,
`2_training/live_training_health.md`, `2_training/storage_readiness.md`,
`2_training/paired_launcher_transition.md`에서 확인한다. 이 파일들이
`v5_random ready / v5_fvt running`와 storage-ready를 보여주는 것은 실행이 정상이라는
뜻이지, FVT 성능 claim이 열린다는 뜻은 아니다.

평가 전환은 live progress가 아니라 post-checkpoint command guard로 판단한다.
`post_checkpoint_command_consistency.md`와 `post_checkpoint_parser_contract.md`가
ready 계열 verdict를 유지해야 긴 paired evaluation으로 넘어간다.

## Checkpoint 이후 실행선

현재 phase와 다음 명령은 아래 generated runbook을 우선한다.

```text
docs/exp/v5/4_reporting/final_handoff_runbook.md
```

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
```

긴 작업을 나눠서 돌릴 때만 아래처럼 분할한다.

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh pppl
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream
```

이 wrapper는 `v5_random`과 `v5_fvt`가 모두 `ready_for_wrapper=yes`이고
post-checkpoint preflight가 `post_checkpoint_preflight_ready_to_launch`가 아니면
실행을 거부한다. 최종 report/PPT 수치는 wrapper output 자체가 아니라 refresh 이후
`3_evaluation/09_aggregation/`에 들어간 값에서만 승격한다.

## 발표용 닫는 문장

현재까지 확정된 결론은 setup fidelity와 zero-step novelty이다. 즉 v5는 Glot500식
실험 구조를 102-language controlled setting에서 충실히 재연했고, 새 vocabulary row
초기화가 training 전 target MLM proxy에 큰 영향을 준다는 강한 evidence를 보였다.
최종 method claim은 matched random/FVT MLM checkpoint와 downstream replay가 끝난
뒤에만 열겠다.

발표 시간이 갑자기 줄어들면 `02_slides/rehearsal_plan_ko.md`의 `5분 긴급 발표안`을
사용한다. 마지막 20초는 `READY_TO_LAUNCH=no`, `READY_TO_LAUNCH=yes`, parsed-but-not-
promotable, final-outcome-ready 중 현재 상태와 맞는 문장만 고른다.
