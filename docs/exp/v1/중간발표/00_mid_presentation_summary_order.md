# 00. 중간 발표용 요약 순서

작성일: 2026-06-12

이 문서는 중간 발표에서 읽을 순서를 정리한 요약본이다. 세부 근거는 `01`부터 `08`까지의 문서에 있고, 이 파일은 발표 흐름, 현재까지 한 일, 앞으로 할 일을 한 번에 말하기 위한 앞문서다.

## 발표 전체 메시지

> XLM-R는 target10 low-resource/unsupported-script 언어에서 tokenization fragmentation이 크다. Vocabulary extension은 이 fragmentation을 줄였고, embedding initialization에서는 `fvt`가 가장 안정적이었다. 하지만 matched-token MLM control에서는 extended-vocabulary adapted model이 original XLM-R continued-pretraining control을 이기지 못했다. 실패는 appended-token prediction에 집중되어 있으며, 다음 단계는 appended-token supervision과 base-token preservation을 함께 넣는 objective를 검증하는 것이다.

## 발표 순서

```text
1. 문제 제기: XLM-R tokenizer가 target10에서 왜 병목인가
2. Baseline audit: 실제 fragmentation 수치 확인
3. Vocabulary extension: 8k / 16k / 32k tokenizer 비교
4. Before-after 예시: token count가 어떻게 줄었는지 시각화
5. Embedding initialization: random / mean / fvt / align / focus 비교
6. Matched-token MLM control: model-level positive claim 실패
7. Failure diagnosis: added-token bottleneck 확인
8. Repair probes: 단순 처방들이 왜 부족했는지 정리
9. Smaller vocab probe: 8k가 낫지만 충분하지 않음
10. Longer budget probe: 더 오래 학습해도 gap이 닫히지 않음
11. 다음 계획: teacher-guided appended-token objective + base KL/replay
```

## 1. 문제 제기

목적:

- multilingual pretrained model이라도 모든 언어를 같은 품질로 tokenize하지 못한다는 점을 보여준다.
- low-resource script, diacritic-heavy Latin orthography, unsupported script에서 tokenizer mismatch가 sequence length와 representation burden을 키운다는 문제를 제기한다.

발표용 문장:

> 이 연구의 출발점은 model architecture가 아니라 tokenizer mismatch입니다. XLM-R는 target10 언어를 `<unk>` 없이 표현할 수는 있지만, 많은 경우 단어를 character-level에 가깝게 쪼개서 sequence length와 prediction burden을 키웁니다.

## 2. Baseline Tokenization Audit

Source: `docs/exp/second_try/중간발표/01_xlmr_baseline_tokenization_audit.md`

수행상황:

- Step02 완료.
- XLM-R baseline tokenizer로 target10을 tokenize했다.
- 모든 언어가 `tokens_per_word >= 2.0` 기준에서 bottleneck에 걸렸다.
- 가장 강한 예시는 Syriac이다.

핵심 수치:

| Example | Value |
| --- | ---: |
| `syr` tokens/word | `4.854` |
| `syr` single-char token % | `74.251%` |
| `ake` tokens/word | `3.311` |
| `bsn` tokens/word | `3.520` |
| `kbh` tokens/word | `3.564` |

발표용 문장:

> Baseline audit 결과, 모든 target10 언어가 평균 2 tokens/word 이상으로 쪼개졌습니다. 특히 Syriac은 평균 4.854 tokens/word이고 single-character token 비율이 74%를 넘어서, 거의 character-level tokenization에 가깝습니다.

Takeaway:

- `<unk>`가 없다는 것은 충분하지 않다.
- 문제는 unknown coverage가 아니라 fragmentation이다.
- 이 결과가 vocabulary extension의 직접 동기다.

## 3. Vocabulary Extension

Source: `docs/exp/second_try/중간발표/02_vocab_extension_8k_16k_32k.md`

수행상황:

- Step03에서 target-language SentencePiece unigram tokenizer를 `8k`, `16k`, `32k`로 학습했다.
- XLM-R original id를 보존하기 위해 target SPM piece를 `added_tokens`로 append했다.
- 세 후보 모두 structural gate를 통과했다.
- tokenizer-only metric에서는 `32k`가 가장 좋았다.

핵심 수치:

| Vocab | Avg tokens/word delta | Single-char delta |
| ---: | ---: | ---: |
| 8k | `-19.581%` | `-39.693%` |
| 16k | `-26.353%` | `-41.349%` |
| 32k | `-31.766%` | `-42.365%` |

발표용 문장:

> Vocabulary extension은 tokenizer-level에서는 성공적입니다. 8k, 16k, 32k 모두 XLM-R special id를 보존했고, 평균 tokens/word와 single-character token 비율을 줄였습니다. 이 중 32k가 tokenizer-only 기준 best candidate였습니다.

Takeaway:

- tokenizer-level positive claim은 supported.
- 하지만 tokenizer metric이 곧 model performance를 뜻하지는 않는다.
- 새 token row가 많아질수록 model-side prediction burden이 생길 수 있다.

## 4. Before-After Tokenization Example

발표에 쓸 예시:

- Syriac `b.MAT.1.1`
  - baseline token count: `47`
  - extended token count: `10`
- Barasana-Eduria `b.MAT.1.1`
  - baseline token count: `120`
  - extended token count: `59`
- Camsa `b.MAT.1.1`
  - baseline token count: `37`
  - extended token count: `19`

발표용 문장:

> 수치만 보면 추상적일 수 있어서 실제 verse를 보면 차이가 더 뚜렷합니다. Syriac 예시에서는 XLM-R가 거의 모든 문자를 따로 쪼개지만, extended tokenizer는 단어 또는 긴 subword 단위로 묶습니다.

Takeaway:

- visual slide에서는 baseline token preview와 extended token preview를 좌우 비교한다.
- 이 부분이 발표에서 가장 직관적인 tokenizer evidence다.

## 5. Embedding Initialization

Source: `docs/exp/second_try/중간발표/03_embedding_initialization_methods.md`

수행상황:

- Step04에서 selected `32k` tokenizer 기준 embedding initialization을 비교했다.
- Step14에서 v2 selected `32k` tokenizer 기준으로 같은 비교를 재현했다.
- 비교한 방법은 `random`, `mean`, `fvt`, `align`, `focus`다.
- zero-step MLM loss 기준 `fvt`가 best였다.

방법 출처:

- Method family는 vocabulary-extension initialization tutorial에서 가져왔다.
- 정리 문서: `docs/exp/second_try/reference_summaries/vocab_extension_tutorial.md`.
- 원본 PDF: `docs/exp/second_try/feedback/vocab_extension_tutorial.pdf`.
- 실제 계산 방식은 이 레포의 Step04/Step14 구현 기준이며, `align`과 `focus`는 full external implementation이 아니라 lightweight proxy다.

Method 요약:

| Method | 의미 |
| --- | --- |
| `random` | 새 row를 random initialized vector 그대로 둠 |
| `mean` | 기존 XLM-R embedding 전체 평균을 새 row에 복사 |
| `fvt` | 새 token을 기존 XLM-R tokenizer로 다시 쪼개고 subtoken embedding 평균 사용 |
| `align` | 문자/span alignment 기반으로 기존 token embedding 평균 사용 |
| `focus` | `fvt`, `align`, global mean을 섞은 proxy method |

핵심 수치:

| Method | Step04 zero-step dev loss | Step14 v2 zero-step dev loss |
| --- | ---: | ---: |
| `random` | `20.809267` | `18.015601` |
| `mean` | `12.437534` | `11.257934` |
| `fvt` | `8.490678` | `8.681328` |
| `align` | `9.039471` | `9.065176` |
| `focus` | `15.581055` | `16.083522` |

발표용 문장:

> 새 token row를 random으로 두면 모델이 새 vocabulary를 거의 모르는 상태에서 시작합니다. `fvt`는 새 token을 기존 XLM-R subtoken 조합으로 되돌려 보고 그 embedding 평균을 쓰기 때문에, 새 token을 기존 의미 공간에 가장 자연스럽게 붙입니다.

Takeaway:

- initialization은 zero-step MLM readiness에 큰 영향을 준다.
- 현재 selected initialization은 `fvt`다.
- `align`은 close second지만 `fvt`를 넘지는 못했다.
- `random`과 단순 `mean`은 baseline으로만 의미가 있다.

## 6. Matched-Token MLM Control

Source: `docs/exp/second_try/중간발표/04_matched_token_mlm_control.md`

수행상황:

- Step15에서 `fvt` initialized extended model을 MLM adaptation했다.
- original `xlm-roberta-base` continued-pretraining control도 같은 train-token budget으로 돌렸다.
- Step16에서 raw-token loss가 tokenizer 차이 때문에 생기는 착시인지 word/char normalized metric으로 다시 확인했다.

학습/평가 쌍:

| Stage | Train data | Eval data | Model pair |
| --- | --- | --- | --- |
| Step15 MLM control | v2 train books, `MAR/JOH/ACT` 제외, 52,124 rows | `MAR` dev, 6,521 rows | adapted extended `fvt` vs original XLM-R control |
| Step16 normalized audit | 추가 학습 없음, Step15 checkpoint만 평가 | `MAR` dev, 6,521 rows | Step15의 6개 checkpoint 재평가 |

데이터 역할:

| Book code | Book | 역할 |
| --- | --- | --- |
| `MAR` | Mark | dev/evaluation only |
| `ACT` | Acts | clean final holdout, 여기서는 읽지 않음 |
| `JOH` | John | burned/excluded old test |

핵심 수치:

| Metric | Adapted extended | Original control | Ratio / status |
| --- | ---: | ---: | --- |
| Mean final dev loss | `4.946829` | `2.518008` | `1.964580` FAIL |
| Estimated NLL per word ratio | n/a | n/a | `1.438660` FAIL |
| Estimated NLL per char ratio | n/a | n/a | `1.438660` FAIL |

Seed별 final dev loss:

| Model | Seed 13 | Seed 17 | Seed 23 | Mean final dev loss |
| --- | ---: | ---: | ---: | ---: |
| adapted extended `fvt` | `4.954783` | `4.951493` | `4.934210` | `4.946829` |
| original XLM-R control | `2.542411` | `2.540437` | `2.471175` | `2.518008` |

발표용 문장:

> Extended model은 zero-step 대비 좋아졌지만, 같은 token budget으로 original XLM-R를 계속 학습한 control보다 훨씬 약했습니다. 따라서 tokenizer-level 성공을 model-level 성공으로 바로 말할 수 없습니다.

Takeaway:

- model-level positive claim은 여기서 막혔다.
- 다음 질문은 "왜 실패했는가"다.

## 7. Failure Diagnosis

Source: `docs/exp/second_try/중간발표/05_failure_diagnosis_added_token.md`

수행상황:

- Step17에서 MLM loss를 base-token target과 added-token target으로 나눠 봤다.
- 실패가 base vocabulary 전체 붕괴라기보다 appended-token prediction 문제에 집중됨을 확인했다.
- Step17은 새로 학습한 실험이 아니라 Step15 checkpoint를 `MAR` dev에서 다시 평가한 진단이다.

핵심 수치:

| Metric | Value |
| --- | ---: |
| Adapted base-token mean loss | `2.562618` |
| Adapted added-token mean loss | `7.267345` |
| Added/base loss ratio | `2.835906` |
| Added-token target share | `50.456741%` |
| Added-token loss share | `74.269955%` |

발표용 문장:

> Base-token behavior가 완전히 무너진 것은 아닙니다. 문제는 새로 append한 token을 맞히는 부분에 집중되어 있습니다. Added tokens는 masked target의 약 절반인데, loss의 74% 이상을 차지합니다.

Takeaway:

- repair target은 전체 model이 아니라 appended-token learning이다.
- 단순히 vocabulary를 붙이는 것만으로는 LM head의 새 class prediction 문제가 해결되지 않는다.

## 8. Repair Probes

Source: `docs/exp/second_try/중간발표/06_repair_probes.md`

수행상황:

- Step18: added-token weighted objective.
- Step19: new-row-only repair.
- Step20: staged/lower-rate repair.
- Step21: alternative initialization `mean`, `align`.
- passing variant는 없었다.

핵심 요약:

| Probe | Main evidence | Result |
| --- | --- | --- |
| Added-token weighting | added loss improves, all loss worsens | FAIL |
| New-row-only | base preserved, added does not improve | FAIL |
| Staged/lower-rate | best variant improves too weakly | FAIL |
| Alternative init | `align` still worse than `fvt` | FAIL |

발표용 문장:

> Repair probes는 useful diagnostic information을 줬지만, top-tier positive model claim을 열 gate는 통과하지 못했습니다. Added-token만 세게 밀면 전체 loss가 망가지고, base를 보존하면 added-token이 충분히 좋아지지 않았습니다.

Takeaway:

- 단일 처방으로는 부족하다.
- added-token supervision 강화와 base-token preservation을 같이 설계해야 한다.

## 9. Smaller Vocab Probe

Source: `docs/exp/second_try/중간발표/07_smaller_vocab_probe.md`

수행상황:

- Step23에서 `8k`, `16k` smaller vocab branch를 테스트했다.
- 8k가 32k보다 raw MLM loss는 낮았다.
- 하지만 original control 대비 gap은 여전히 컸고, Step24 normalized check도 실패했다.

핵심 수치:

| Model / vocab | Mean final raw dev loss | Vs original control |
| --- | ---: | ---: |
| Adapted 32k | `4.946829` | `1.964580` |
| Adapted 16k | `4.798048` | `1.905494` |
| Adapted 8k | `4.541285` | `1.803523` |
| Original control | `2.518008` | baseline |

Vocab size별 차이:

| Comparison | Loss difference | Relative change |
| --- | ---: | ---: |
| 16k vs 32k | `-0.148781` | `-3.008%` |
| 8k vs 32k | `-0.405544` | `-8.198%` |
| 8k vs 16k | `-0.256763` | `-5.351%` |

발표용 문장:

> 8k는 32k보다 낫습니다. 즉 added row가 너무 많은 것은 실제로 부담입니다. 하지만 8k도 original control을 따라잡지는 못해서, vocab size만 줄이는 것은 충분한 해결책이 아닙니다.

Takeaway:

- smaller vocab은 좋은 방향이지만 solution은 아니다.
- model-side objective mismatch가 계속 남아 있다.

## 10. Longer Budget Probe And Next Steps

Source: `docs/exp/second_try/중간발표/08_longer_budget_and_next_steps.md`

수행상황:

- Step25에서 8k adapted model과 original control을 약 1M train-token budget까지 이어서 학습했다.
- adapted 8k도 좋아졌지만 original control이 더 잘 좋아졌다.
- gap은 닫히지 않았다.

핵심 수치:

| Metric | Adapted 8k continued | Original control continued | Ratio |
| --- | ---: | ---: | ---: |
| Final dev loss | `4.227845` | `2.167797` | `1.950296` |
| Estimated NLL per word ratio | n/a | n/a | `1.587381` |
| Estimated NLL per char ratio | n/a | n/a | `1.587381` |

발표용 문장:

> 더 오래 학습하면 adapted 8k loss는 내려갑니다. 하지만 original control도 더 빠르게 좋아지기 때문에 상대 gap은 닫히지 않았습니다. 단순한 budget 증가는 현재 실패를 해결하지 못합니다.

Takeaway:

- longer training alone is not enough.
- 다음 실험은 objective redesign이어야 한다.

## 11. 현재까지 한 것

완료:

1. target10 corpus와 split 정리.
2. XLM-R baseline tokenization bottleneck 확인.
3. target-language vocabulary extension 구현.
4. `8k`, `16k`, `32k` tokenizer 후보 비교.
5. tokenizer-only 기준 `32k` 후보 선택.
6. 새 token embedding initialization 방법 5개 비교.
7. zero-step MLM 기준 `fvt` initialization 선택.
8. matched-token MLM control 수행.
9. word/char normalized metric audit 수행.
10. added-token bottleneck 진단.
11. repair probes, smaller vocab probe, longer budget probe 수행.

현재 말할 수 있는 claim:

- XLM-R tokenizer는 target10에서 fragmentation bottleneck을 보인다.
- Vocabulary extension은 평균 tokenization fragmentation을 줄인다.
- 새 token embedding initialization은 중요하며, 현재 비교에서는 `fvt`가 가장 좋다.
- 그러나 clean MLM control에서 extended-vocabulary adapted model은 original continued-pretraining control보다 competitive하지 않다.
- 실패는 appended-token prediction에 집중된다.

말하면 안 되는 claim:

- extended-vocabulary model이 original XLM-R보다 좋아졌다는 claim.
- 8k branch가 model adaptation 문제를 해결했다는 claim.
- longer budget으로 gap이 닫혔다는 claim.
- downstream/translation positive claim.

## 12. 앞으로 할 예정

다음 실험 목표:

1. Original XLM-R subtoken decomposition을 teacher signal로 사용한다.
2. Appended token row와 span prediction을 teacher-guided objective로 학습한다.
3. Added-token mask/loss pressure를 curriculum으로 점진적으로 키운다.
4. Base-token behavior는 KL 또는 replay loss로 보존한다.
5. Step15/16-style original control과 normalized word/char gate를 다시 통과해야 positive claim을 연다.

우선순위:

| Priority | Experiment | 목적 |
| --- | --- | --- |
| P0 | teacher-guided appended-token initialization | `fvt`보다 강한 새 row supervision 검증 |
| P0 | curriculum added-token MLM + base KL/replay | added loss 개선과 base 보존을 동시에 달성 |
| P0 | non-final data redesign | Bible-only signal이 부족할 때 rare added token coverage 보강 |
| P1 | pruned vocab + distillation | tail appended row 부담을 줄이는 branch |

발표용 문장:

> 다음 실험은 단순히 더 오래 학습하는 것이 아니라, appended token을 original XLM-R subtoken teacher로 지도하고, base-token behavior는 KL 또는 replay로 보존하는 방향입니다. 이 방법도 original-control gate를 통과하기 전까지는 positive performance claim으로 말하지 않습니다.

## 마지막 슬라이드 문장

> 중간 결론은 보수적으로 잡겠습니다. Tokenizer extension은 target10 fragmentation을 실제로 줄였지만, 현재 objective에서는 extended-vocabulary model이 original continued-pretraining control을 이기지 못했습니다. 실패 원인은 appended-token prediction이며, 다음 단계는 teacher-guided appended-token learning과 base-token preservation을 함께 검증하는 것입니다.
