# v5 한국어 논문형 보고서 초안

작성 상태: execution draft, 2026-06-28 refresh 기준

이 문서는 최종 발표와 보고서 작성을 위한 한국어 논문형 원고 초안이다. 숫자와
claim은 현재 측정된 artifact만 반영하며, after-MLM 및 downstream 결과는 matched
`v5_random`/`v5_fvt` checkpoint와 aggregation row가 생기기 전까지 조건부로 둔다.
현재 checkpoint 진행률과 post-checkpoint Go/No-Go는 이 정적 원고 header가 아니라
`../final_action_dashboard_ko.md`와
`bash scripts/run_v5_post_checkpoint_evals.sh status` 출력을 우선한다.

관련 gate:

- claim boundary: `claim_ledger.md`
- method comparison: `../method_comparison_summary.md`
- post-result patch plan: `../post_result_patch_plan_ko.md`
- final claim rule: `../final_claim_decision_tree.md`
- outcome matrix: `../post_checkpoint_outcome_matrix_ko.md`
- final claim freeze audit: `../final_claim_freeze_audit.md`
- final package audit: `../reporting_package_audit.md`

## 초록

본 연구는 Glot500의 multilingual vocabulary expansion 및 continued MLM
pretraining 흐름을 통제된 102개 language-script 설정에서 재연하고, vocabulary
extension 이후 새 embedding row를 어떻게 초기화할지 비교한다. 실험 데이터는
XLM-R seen Glot500 language-script 92개와 Glot500 내부 raw corpus에서 선택한
target language-script 10개로 구성된다. target10은 모두 XLM-R seen language가
아니며, 30,000 sentence 이상 조건과 raw directory 존재 조건을 만족한다.

핵심 novelty는 새로운 corpus나 task가 아니라, 확장된 vocabulary row의
initialization이다. Glot500-style random resize baseline과 비교하여,
source-token decomposition 기반 FVT 초기화가 zero-step MLM proxy에서 더 좋은
초기 상태를 만드는지 확인한다. 현재까지 full tokenizer, initialization audit,
zero-step evaluation은 완료되었고, FVT는 v5 target group weighted NLL에서 random
대비 9.626238 낮은 값을 보였다. 다만 after-MLM PPPL과 downstream transfer claim은
matched checkpoint 및 downstream parsing 완료 후에만 승격한다.

## 1. 서론

다국어 사전학습 모델은 수백 개 언어를 지원하지만, 실제 성능은 tokenizer coverage,
script, corpus size, related language support에 크게 좌우된다. Glot500은 더 많은
language-script corpus와 vocabulary expansion, continued pretraining을 통해
이 문제를 다룬다. 본 프로젝트는 전체 511개 언어의 full reproduction을 목표로
하지 않고, 계산 가능한 subset에서 Glot500의 핵심 실험 구조를 충실히 재연한다.

본 실험의 질문은 다음과 같다.

1. Glot500-style tokenizer expansion과 continued MLM을 92+10 subset에서 재연할 수
   있는가?
2. vocabulary extension 이후 새 token embedding row를 random으로 둘 때와
   source-token decomposition으로 초기화할 때 zero-step 및 after-MLM behavior가
   달라지는가?
3. MLM proxy의 차이가 Glot500 downstream metric replay에서도 관찰되는가?

### 1.1 기여 요약

본 보고서의 기여는 세 가지로 정리한다.

첫째, Glot500의 full-scale claim을 과장하지 않고, 92개 XLM-R-seen language-script와
10개 Glot500-internal target language-script로 구성된 controlled replay package를
구축한다. 이 package는 corpus merge, SentencePiece append tokenizer, continued MLM,
metric-family coverage, claim freeze audit를 함께 묶어 재연 범위를 artifact 단위로
검증한다.

둘째, vocabulary extension 이후 새 embedding row initialization을 독립된 방법론 축으로
분리한다. source-token decomposition 기반 FVT는 source row identity, `<mask>` remap,
byte row accounting, LM-head tying을 보존하면서 zero-step target MLM proxy에서 random
resize보다 낮은 weighted NLL을 보인다.

셋째, Glot500 downstream task family를 생략하지 않고 local coverage와 blocker를
명시한다. 따라서 최종 claim은 PPPL, retrieval, classification, tagging, Roundtrip
alignment가 aggregation에 들어온 뒤에만 승격되며, target10 downstream coverage가 없는
metric은 limitation으로 남긴다.

## 2. 재연 범위와 방법론 위치

본 실험은 full Glot500 reproduction이 아니라 controlled subset reproduction이다.
따라서 허용되는 표현은 다음과 같다.

- 허용: Glot500-style pipeline을 102-language subset에서 재연했다.
- 불가: Glot500 511-language experiment를 완벽히 재현했다.

tokenization 측면에서 V4/V5는 Glot500-style이다. auxiliary SentencePiece model을
학습하고, XLM-R SPM에 없는 piece를 기존 SPM 뒤에 append한다. 반면 V3는 기존
tokenizer에 새 token을 추가하는 Yamaguchi-style vocabulary expansion ablation에
가깝다. 이 구분 덕분에 reproduction axis와 novelty axis가 분리된다. reproduction은
Glot500-style tokenizer/continued MLM이고, novelty는 appended row initialization이다.

### 2.1 Glot500과 본 연구의 관계

Glot500은 language-script coverage를 넓히고, tokenizer vocabulary를 확장한 뒤,
continued pretraining과 downstream evaluation으로 low-resource multilingual model의
효과를 검증한다. 본 연구는 이 전체 규모를 다시 학습하지 않는다. 대신 Glot500의 핵심
실험 논리를 보존한다. 즉, corpus scope를 고정하고, SentencePiece 기반 vocabulary
expansion을 수행하고, continued MLM으로 representation을 갱신하고, Glot500에서 사용한
metric family를 유지한다.

따라서 v5의 contribution은 "더 큰 Glot500"이 아니라, Glot500-style pipeline을 작고
검증 가능한 subset으로 재연하면서 vocabulary expansion 이후 initialization이라는
새 질문을 붙이고, 두 방법론 축을 분리해 분석하는 데 있다. 재연 fidelity의 세부
구분은 다음 표에 고정한다.

```text
docs/exp/v5/4_reporting/00_tables/table_15_glot500_reproduction_fidelity.md
```

전체 실험 흐름을 요약한 overview figure는 다음 파일에 둔다.

```text
docs/exp/v5/4_reporting/01_figures/generated/figure_01_experiment_pipeline.png
```

요약하면 v5는 experimental logic 수준에서는 충실하다. Glot500-internal data,
SentencePiece append, continued MLM, metric-family accounting, head/tail/all-style
reporting을 유지한다. 다만 full 511-language scale과 original compute budget은
의도적으로 재연하지 않는다.

### 2.2 Yamaguchi-style Vocabulary Expansion과의 관계

Yamaguchi 계열 방법은 적은 target-language text로 vocabulary를 확장하고, 추가된 token
embedding을 어떻게 초기화할지 다룬다는 점에서 본 연구의 novelty axis와 연결된다. 다만
v5 tokenizer 자체는 V3식 `add_tokens()` route가 아니라 Glot500-style SPM append route를
사용한다. 따라서 Yamaguchi-style은 v5의 tokenizer reproduction method가 아니라,
새 vocabulary row initialization을 비교하는 motivation과 ablation framing에 가깝다.

이 구분은 보고서와 발표에서 중요하다. tokenizer method를 Yamaguchi method라고 부르면
Glot500 재연성이 흐려지고, 반대로 initialization novelty를 Glot500 reproduction만으로
설명하면 본 연구의 방법론적 기여가 약해진다.

## 3. 데이터

head group은 XLM-R seen Glot500 language-script 중 local raw directory가 존재하는
92개이다. target group은 Glot500 raw 안에 있으면서 XLM-R seen이 아니고,
new length가 30,000 이상인 후보 중 지역, 문자, 어족 다양성을 고려해 고른 10개이다.

target10:

- `fur_Latn`: Friulian, Europe, Latin
- `krc_Cyrl`: Karachay-Balkar, North Caucasus, Cyrillic
- `acm_Arab`: Mesopotamian Arabic, West Asia, Arabic
- `dzo_Tibt`: Dzongkha, Himalaya, Tibetan
- `sat_Olck`: Santali, South Asia, Ol Chiki
- `mad_Latn`: Madurese, Southeast Asia, Latin
- `bam_Latn`: Bambara, West Africa, Latin
- `kjb_Latn`: Q'anjob'al, Mesoamerica, Latin
- `quw_Latn`: Tena Lowland Quichua, Andean South America, Latin
- `rap_Latn`: Rapanui, Polynesia, Latin

main merge는 92,452,251 lines로 완료되었고, missing language directory는 0개였다.
이 값은 `../../0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.report.json`과
`../../0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.manifest.tsv`에서 확인한다.

## 4. 방법

### 4.1 Tokenizer Expansion

full corpus에서 Glot500-style auxiliary SentencePiece tokenizer를 학습한 뒤,
XLM-R-base tokenizer에 없는 pieces를 append했다. 최종 tokenizer는 368,687 HF tokens를
가지며, XLM-R 대비 118,685 token strings가 추가되었다. `<mask>` id는 source
250001에서 target 368686으로 이동했으므로, embedding 복사는 id prefix가 아니라 token
identity 기준으로 수행해야 한다.

main tokenizer audit은 20개 head language와 10개 target language에서 failure 0으로
통과했다. audited 30개 언어 중 29개는 tokens/word가 감소했다. target10에서는 9개
언어가 개선되었고, `dzo_Tibt`는 여전히 regression case로 남았다. 이 regression은
보고서에서 failure를 숨기지 않고 score calibration 및 newly appended Tibetan piece의
영향으로 분석한다.

### 4.2 Embedding Initialization

비교 대상은 다음과 같다.

| Method | Description | Role |
| --- | --- | --- |
| `random` | Hugging Face resize 기본 random row | Glot500-style baseline |
| `mean` | source/global mean 기반 초기화 | simple ablation |
| `fvt` | target token surface를 source tokenizer로 분해하고 source embedding 평균 사용 | main novelty |
| `align` | script/character-aware fallback | exploratory ablation |

main checkpoint initialization audit에서 `v5_fvt`는 118,427개 새 row를
source-token decomposition으로 초기화했고, 256 byte rows와 2 lexical fallback rows는
global mean을 사용했다. source identity rows 250,002개가 보존되었고, `<mask>` remap
max absolute difference는 0.0이며, LM head tying도 true로 확인되었다.

### 4.3 Continued MLM

continued MLM은 동일한 corpus, tokenizer, seed, schedule, checkpoint rule로
`v5_random`과 `v5_fvt`를 paired comparison한다. 이 단계의 핵심은 long training 후
성능만 보는 것이 아니라, zero-step, early-step, selected checkpoint를 분리해서
initialization effect가 언제 살아 있는지 확인하는 것이다.

현재 상태에서는 paired 10K MLM run이 진행 중이며, matched checkpoint가 준비되기 전에는
after-MLM claim을 승격하지 않는다.

### 4.4 Evaluation

Glot500에서 측정한 metric family는 v5에서도 모두 required로 둔다.

| Metric family | Required | Current interpretation |
| --- | --- | --- |
| Pseudoperplexity / MLM proxy | yes | target10까지 raw-text 평가 가능 |
| Tatoeba retrieval | yes | available-language replay, target10 coverage limited |
| Bible retrieval | yes | available-language replay, target10 coverage limited |
| Text classification | yes | local English split 중심 |
| NER | yes | available-language replay |
| POS | yes | available-language replay |
| Roundtrip alignment | yes | XLM-R/Glot500-base/v5-random 측정 완료, FVT checkpoint 대기 |

coverage가 없는 언어는 제외하지 않고, measured, excluded, blocked reason을 기록한다.
따라서 downstream claim은 target10 전체에 대한 직접 claim이 아니라
available-language/head/all replay로 해석해야 한다.

## 5. 현재 결과

### 5.1 Setup Fidelity

scope, merge, tokenizer, initialization 단계는 main experiment 기준으로 준비되었다.
핵심 값은 다음과 같다.

| Item | Value |
| --- | ---: |
| seen language-scripts | 92 |
| target language-scripts | 10 |
| merged corpus lines | 92,452,251 |
| missing language dirs | 0 |
| final tokenizer size | 368,687 |
| appended token strings | 118,685 |

### 5.2 Tokenizer Result

main tokenizer audit은 failure 0으로 통과했다. audited target10 중 9개는 fertility가
개선되었고, `dzo_Tibt`는 regression으로 남았다. 이 결과는 tokenizer expansion의
전체 방향은 긍정적이지만, script-specific calibration 문제가 있을 수 있음을 보여준다.
정량적으로는 audited 30개 언어 중 29개가 개선되었고(29/30), target10에서는 9개가
개선되었다(9/10). `dzo_Tibt`는 `4.223938 -> 5.552124` tokens/word로 악화되어
visible limitation으로 유지한다.

### 5.3 Zero-Step Initialization Result

zero-step MLM proxy에서 FVT는 random resize보다 명확히 좋은 초기 상태를 보였다. mean
initialization ablation의 target weighted NLL은 11.953142로, random보다는 좋지만 FVT에는
미치지 못했다.

| Split | random weighted NLL | FVT weighted NLL | Delta | Relative |
| --- | ---: | ---: | ---: | ---: |
| head sample | 12.895301 | 6.621457 | -6.273844 | -48.65% |
| v5 target | 18.411756 | 8.785518 | -9.626238 | -52.28% |
| all | 16.511807 | 8.040183 | -8.471624 | -51.31% |

이 결과는 final downstream claim이 아니라 intrinsic initialization evidence이다.
after-MLM PPPL과 downstream row가 준비되면 이 효과가 유지되는지, 줄어드는지, 또는
task별로 달라지는지 확인한다.

### 5.4 Baseline and External Reference Rows

현재 final result table에 넣을 수 있는 measured row는 XLM-R-base baseline과
Glot500-base external reference이다. Glot500-base는 같은 budget으로 재학습한 baseline이
아니므로, equal-budget comparison이 아니라 reference scale로 해석한다.

| Metric | XLM-R-base | Glot500-base | Interpretation |
| --- | ---: | ---: | --- |
| target PPPL | 61.980216 | 15.102934 | target raw-text intrinsic reference |
| Tatoeba all Top-10 | 0.566067 | 0.706649 | available-language retrieval reference; v5-random 0.610353 measured |
| Bible all Top-10 | 0.381153 | 0.509356 | available-language Bible retrieval reference; v5-random 0.328019 measured |
| Taxi1500 macro-F1 | 0.592876 | 0.743338 | local text-classification reference; v5-random 0.702956 measured |
| NER all F1 | 0.549858 | 0.627108 | available-language tagging reference; v5-random 0.544628 measured |
| POS all F1 | 0.481336 | 0.567542 | available-language tagging reference with local train-language caveat; v5-random 0.481102 measured |
| Roundtrip accuracy | 0.185300 | 0.205189 | available-language alignment reference; v5-random 0.190300 measured |

추가로 `v5_random` after-MLM PPPL은 측정 완료됐다. weighted PPPL은 target10
`39.222875`, head `18.726452`, all `20.138927`이다. 이 값은 random-initialized
checkpoint의 measured row이며, 아직 FVT와의 method comparison claim은 아니다.
`v5_random` Tatoeba retrieval도 measured row가 생겼다. Top-10 accuracy는 head
`0.700285`, all available `0.610353`이다. target10 coverage는 여전히 `0/10`이므로
available-language downstream row로만 해석한다.
`v5_random` Taxi1500도 measured row가 생겼다. macro-F1은 `0.702956`, accuracy는
`0.747748`이다. local English-only classification row이므로 target10 downstream
claim으로 쓰지 않는다.
`v5_random` Roundtrip accuracy도 available 74-language setting에서 `0.190300`으로
측정됐지만, FVT downstream row가 없으므로 downstream method claim은 여전히 잠겨 있다.
`v5_random` Bible Top-10도 같은 available 74-language setting에서 `0.328019`로
측정됐다. 다만 FVT Bible row가 없으므로 이것도 method win claim으로 쓰지 않는다.
`v5_random` NER all F1은 `0.544628`, head F1은 `0.608020`이며, POS all F1은
`0.481102`, head F1은 `0.587430`이다. POS는 baseline/reference와 동일하게
`TRAIN_LANGS=tur_Latn` 조건에서 해석한다.

중간 해석은 분명하다. `v5_random`은 method win이 아니라 diagnostic lower-bound row이다.
target10 PPPL에서는 XLM-R보다 좋아졌지만 Glot500-base reference에는 아직 못 미치고,
head/all PPPL에서는 두 reference보다 나쁘다. Downstream은 metric별로 섞인다. Tatoeba와
Taxi1500에서는 XLM-R보다 높지만 Glot500-base에는 못 미치고, Bible retrieval에서는 두
reference보다 낮으며, POS head에서는 두 reference보다 높고, Roundtrip에서는 XLM-R과
Glot500-base 사이에 있다. 따라서 이 결과는 실험 설계를 약하게 만드는 것이 아니라,
matched `v5_fvt`가 왜 결정적인 test인지 보여준다.

이 표에서 아직 빠진 핵심 row는 `v5_fvt`의 after-MLM PPPL 및 available downstream
결과이다. 이 row는 selected 10K checkpoint가 생긴 뒤
`scripts/run_v5_post_checkpoint_evals.sh` wrapper로만 채운다.

### 5.5 Current Finalization Gates

현재 결론 동결 상태는 `../final_claim_freeze_audit.md`가 관리한다. 현 단계에서
허용되는 결론은 setup fidelity와 zero-step novelty까지이다. after-MLM PPPL 개선,
downstream improvement, target10 downstream improvement는 모두 locked claim이다.

이 구조는 보수적이지만 발표 방어에는 유리하다. live training log나 중간 dev score가
좋아 보여도, aggregation에 들어간 measured row가 아니면 final report/PPT claim으로
승격하지 않는다.

## 6. 논의

현재까지 가장 강한 기여는 “Glot500-style vocabulary expansion에서 새 row를 random으로
두지 않아도 된다”는 실험적 근거이다. FVT는 target token을 기존 XLM-R tokenizer로
분해한 뒤 source embedding 평균을 사용하므로, low-resource corpus만으로도 더 안정적인
초기 embedding을 제공할 수 있다.

다만 tokenizer 자체가 모든 언어에서 균일하게 이득을 주지는 않는다. `dzo_Tibt`는
byte fallback이나 `<unk>` 문제가 아니라 새 Tibetan pieces의 segmentation score
calibration 문제로 보인다. 이 failure case는 오히려 발표에서 설득력 있는 분석 포인트가
된다. 좋은 실험은 성공만 있는 실험이 아니라, 어떤 조건에서 깨지는지도 보여준다.

## 7. Limitations

- v5는 511-language full reproduction이 아니라 102-language controlled subset이다.
- PPPL은 target10 coverage 10/10이지만 retained downstream task coverage는 target10 0/10이므로 target10 downstream transfer를 직접
  주장하지 않는다.
- Roundtrip alignment는 available-language 기준 XLM-R/Glot500-base/v5-random row를
  측정했지만, target10 coverage는 0/10이고 FVT method row는 checkpoint 이후에만 확정한다.
- after-MLM 및 downstream novelty claim은 matched `v5_random`/`v5_fvt` checkpoint와
  parsed aggregation row 이후에만 확정한다.

## 8. 결론 초안

현재 안전한 결론은 다음과 같다.

> v5는 Glot500-style tokenizer expansion, continued MLM 준비, evaluation family
> accounting을 92+10 controlled subset에서 충실히 재연하는 구조를 갖췄다. 또한
> vocabulary extension 이후 source-token decomposition 기반 FVT initialization은
> zero-step MLM proxy에서 random resize보다 큰 이점을 보였다. 최종 after-MLM 및
> downstream transfer 결론은 matched checkpoint와 available-language metric replay
> 완료 후 결정한다.

### 8.1 결과별 최종 결론 선택 규칙

checkpoint 이후 초록과 결론은 새로 즉흥 작성하지 않고,
`../post_checkpoint_outcome_matrix_ko.md`와 `../final_claim_decision_tree.md`가
허용한 outcome만 사용한다.

| Outcome | 조건 | 최종 report/PPT 문장 방향 |
| --- | --- | --- |
| bounded positive | FVT가 after-MLM PPPL과 available downstream 다수에서 우세 | target10 coverage caveat를 단 제한적 positive claim |
| intrinsic positive, downstream mixed | FVT가 PPPL에서는 우세하지만 downstream은 섞임 | intrinsic adaptation 개선 claim, downstream은 coverage-dependent |
| early-only diagnostic | zero-step은 우세하지만 after-MLM에서 우위가 사라짐 | final superiority가 아니라 early adaptation diagnostic |
| negative final comparison | PPPL/downstream에서 random이 같거나 우세 | controlled negative result와 추가 objective 필요성 |
| incomplete evaluation | matched row 또는 parser output이 완결되지 않음 | execution draft 결론 유지, final method claim 잠금 |

최종 문장 승격 조건은 세 가지이다. 첫째, `3_evaluation/09_aggregation/`에
`v5_random`과 `v5_fvt` row가 모두 있어야 한다. 둘째,
`result_promotion_readiness_audit.md`가 결과 승격 가능 상태여야 한다. 셋째,
`final_claim_freeze_audit.md`가 pending/disallowed claim을 다시 잠근 상태여야 한다.
하나라도 충족되지 않으면 위 안전 결론을 유지한다.

## 9. 재현성 요약

실행 경로와 문서 source of truth:

- top-level plan: `../../Plan.md`
- living report: `../../Report.md`
- selected data manifest:
  `../../0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv`
- main merge report:
  `../../0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.report.json`
- metric mapping: `../../3_evaluation/metric_mapping.md`
- aggregation folder: `../../3_evaluation/09_aggregation/`
- post-checkpoint runner: `../../../../scripts/run_v5_post_checkpoint_evals.sh`
- reporting refresh: `../../../../scripts/refresh_v5_reporting.py`

최종 결과 반영 순서:

1. matched `v5_random` and `v5_fvt` checkpoints를 확인한다.
2. `../../3_evaluation/post_checkpoint_eval_queue.md`에서 runnable metric rows를 확인한다.
3. `../../3_evaluation/post_checkpoint_execution_plan.md`에서 launch env, output/log 위치,
   promotion rule을 확인한다.
4. `post_checkpoint_preflight.md`가 `post_checkpoint_preflight_ready_to_launch`를
   보고한 뒤 guarded post-checkpoint runner로 PPPL 및 available downstream rows를 실행한다.
5. reporting refresh를 실행한다.
6. `../post_result_patch_plan_ko.md`에서 `ready_for_patch` 행만 보고서와 PPT 수정 대상으로 삼는다.
7. `../final_claim_decision_tree.md`가 허용하는 conclusion wording만 보고서와 PPT에 반영한다.

checkpoint가 준비된 뒤 실제 handoff 명령:

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
python3 scripts/refresh_v5_reporting.py --with-plots
```

## 10. 참고문헌

본 한국어 원고의 citation boundary는 `citation_source_map.md`와
`external_source_verification.md`를 따른다. 인용은 배경과 방법론 계보를 설명하기
위한 것이며, v5의 수치 결과는 항상 local artifact와 aggregation table에서만 온다.

- Ayyoob ImaniGooghari et al. 2023. *Glot500: Scaling Multilingual Corpora and
  Language Models to 500 Languages*. ACL 2023.
  `https://aclanthology.org/2023.acl-long.61/`,
  DOI `10.18653/v1/2023.acl-long.61`.
  본 연구에서는 Glot500-style corpus/tokenizer/continued-MLM/evaluation 흐름의
  reproduction target으로 인용한다. v5가 511-language full scale을 재학습했다는
  근거로 사용하지 않는다.
- Glot500 official code. `https://github.com/cisnlp/Glot500`.
  inherited tokenizer/evaluation script lineage를 설명하는 code reference이다.
  local v5 재현성 근거는 `reproducibility_appendix.md`, `source_map.md`, 그리고
  generated audit files에 둔다.
- Atsuki Yamaguchi, Aline Villavicencio, Nikolaos Aletras. 2026.
  *How Can We Effectively Expand the Vocabulary of LLMs with 0.01GB of Target
  Language Text?* Computational Linguistics 52(1):295-330.
  `https://aclanthology.org/2026.cl-1.9/`,
  DOI `10.1162/coli.a.581`.
  본 연구에서는 low-resource vocabulary expansion과 new-row initialization 문제의
  inspiration/contrast로 인용한다. v5 main tokenizer는 Yamaguchi-style add-token
  route가 아니라 Glot500-style SentencePiece append route이다.
- Low-resource continued vocabulary expansion official code.
  `https://github.com/gucci-j/lowres-cve`.
  관련 구현 계보와 terminology bridge로만 사용한다. 실행된 v5 pipeline의 근거는
  local scripts와 generated artifacts이다.
