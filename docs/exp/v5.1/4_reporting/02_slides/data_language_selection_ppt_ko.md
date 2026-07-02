# 데이터 및 언어 선택 발표 내용

이 섹션은 v5.1 발표에서 데이터 구성과 target10 선정 이유를 설명하기 위한
PPT 원고다. 숫자는 현재 local audit 기준이며, v5.1은 최종 low-resource claim이
아니라 downstream-aware diagnostic/ablation line으로 설명한다.

## Slide A. 데이터 설계의 핵심

Title:

```text
Glot500-style 재현을 위해 102개 language-script를 고정하고 train/dev/test를 먼저 분리
```

On-slide bullets:

- 전체 universe: `102` language-script
- Head: XLM-R 학습에 포함된 `92`개 언어
- Target10: XLM-R 학습에 포함되지 않은 `10`개 언어
- 각 언어에서 dev/test를 먼저 제외하고, MLM은 train-only corpus만 사용
- PPPL은 train이 아니라 held-out `test` split에서 측정

Speaker note:

```text
이번 실험에서 가장 먼저 고친 부분은 데이터 분리입니다. 이전에는 raw train source에서
PPPL을 보는 diagnostic이 섞일 수 있었기 때문에, Glot500 방식에 맞춰 언어별로
dev 1000문장, test 1000문장을 먼저 빼고 tokenizer와 continued MLM에는 train만
넣었습니다. 따라서 학습 데이터와 평가 데이터가 분리됩니다.
```

## Slide B. 왜 target10을 다시 골랐나

Title:

```text
Target10은 raw corpus만 있으면 충분하지 않고, downstream task coverage도 필요
```

On-slide bullets:

- PPPL은 raw text만 있으면 모든 target10에서 가능
- Retrieval/NER/Roundtrip은 별도 task data가 있어야 평가 가능
- raw-only 언어만 고르면 downstream target-side claim이 막힘
- v5.1은 downstream coverage를 고려한 diagnostic target10
- 단, downstream-covered target은 일부 mid/high-resource로 이동하므로 final low-resource claim은 제한

Speaker note:

```text
처음에는 Glot500 raw corpus 안에 있는 XLM-R-unseen 언어를 고르면 충분해 보였습니다.
하지만 downstream task는 raw text와 별개입니다. 예를 들어 Bible retrieval이나 NER는
해당 언어의 task split이 실제로 있어야 합니다. 그래서 v5.1에서는 target10을 다시
고를 때 raw corpus뿐 아니라 Tatoeba, Bible, NER, Roundtrip overlap을 같이 봤습니다.
이 선택 덕분에 downstream 분석은 가능해졌지만, 일부 언어가 더 큰 corpus를 가진
mid/high-resource 쪽으로 이동한다는 limitation도 함께 명시합니다.
```

## Slide C. 언어 선택 기준

Title:

```text
선정 기준: XLM-R-unseen + raw corpus + task overlap + 지역/문자 다양성
```

On-slide bullets:

- `XLM-R training language = no`
- Glot500 raw directory 존재
- `new_length >= 30,000`
- PPPL 가능한 held-out raw split 확보
- Tatoeba/Bible/NER/Roundtrip 중 가능한 downstream overlap 우선
- South Asia, Southeast Asia, Southeast Europe, Caucasus/West Asia, Himalaya 포함
- Gujarati, Bengali, Cyrillic, Latin, Tibetan, Ol Chiki 등 script diversity 확보

Speaker note:

```text
언어 선택은 단순히 데이터가 많은 순서가 아니라, 실험 목적에 맞는 조건을 통과한
후보에서 골랐습니다. 모두 XLM-R 학습 언어가 아니어야 하고, Glot500 raw corpus가
있어야 하며, 최소 3만 문장 이상의 원천 데이터가 있어야 합니다. 그 다음에는
downstream overlap을 우선했고, 마지막으로 특정 지역이나 Latin script에만 쏠리지
않도록 지역과 문자 체계를 분산했습니다.
```

## Slide D. 최종 Target10

Title:

```text
Selected Target10: XLM-R-unseen 10개 language-script
```

On-slide table:

| Language-script | Language | Region | Script | Main downstream coverage |
| --- | --- | --- | --- | --- |
| `guj_Gujr` | Gujarati | South Asia | Gujarati | Bible, Roundtrip, NER |
| `asm_Beng` | Assamese | South Asia | Bengali | Bible, Roundtrip, NER |
| `srp_Cyrl` | Serbian | Southeast Europe | Cyrillic | Bible, Roundtrip, NER |
| `sun_Latn` | Sundanese | Southeast Asia | Latin | Bible, Roundtrip, NER |
| `zsm_Latn` | Standard Malay | Southeast Asia | Latin | Tatoeba, Bible, Roundtrip |
| `aze_Latn` | Azerbaijani | Caucasus/West Asia | Latin | Tatoeba, NER |
| `fil_Latn` | Filipino | Southeast Asia | Latin | Bible, Roundtrip |
| `bos_Latn` | Bosnian | Southeast Europe | Latin | Tatoeba, NER |
| `dzo_Tibt` | Dzongkha | Himalaya | Tibetan | PPPL-only script anchor |
| `sat_Olck` | Santali | South Asia | Ol Chiki | PPPL-only script anchor |

Speaker note:

```text
최종 target10은 downstream coverage가 있는 8개 언어와 script diversity anchor 2개로
구성했습니다. Gujarati, Assamese, Serbian Cyrillic, Sundanese는 Bible/Roundtrip/NER를
같이 볼 수 있고, Malay는 Tatoeba/Bible/Roundtrip을 볼 수 있습니다. Dzongkha와
Santali는 downstream coverage는 없지만 Tibetan script와 Ol Chiki script를 포함해
tokenizer 확장과 PPPL 관점의 문자 다양성을 보완합니다.
```

## Slide E. Raw Corpus / MLM / PPPL 데이터 양

Title:

```text
학습과 평가는 분리: MLM은 train-only, PPPL은 held-out test
```

On-slide table:

| Data scope | Coverage | Train | Dev | Test | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Raw corpus strict split | 102 = 92 head + 10 target | 1,169,231,705 | 100,850 | 100,851 | 1,169,433,406 |
| MLM strict 5% train sample | 102 = 92 head + 10 target | 8,130,401 | 0 | 0 | 8,130,401 |
| PPPL held-out set | 102 = 92 head + 10 target | 0 | 100,850 | 100,851 | 201,701 |

Speaker note:

```text
전체 raw split은 약 11.69억 example입니다. 여기서 실제 continued MLM에는 strict
5% sample인 813만 line만 사용했습니다. 중요한 점은 PPPL 후보 dev/test가 따로
분리되어 있다는 것입니다. 최종 PPPL은 test 100,851개 example 기준으로 보고해야
하고, MLM train corpus에서 나온 값은 final metric이 아니라 diagnostic으로만 둡니다.
```

## Slide F. Downstream task별 실제 데이터 양

Title:

```text
Downstream은 task data가 있는 언어에서만 claim 가능
```

On-slide table:

| Task | Coverage | Target10 | Train | Dev | Test | Total | Metric |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Tatoeba retrieval | 66 / 102 | 3 / 10 | 0 | 0 | 57,479 | 57,479 | Top-10 Acc. |
| Bible retrieval | 80 / 102 | 6 / 10 | 0 | 0 | 622,393 | 622,393 | Top-10 Acc. |
| NER | 84 / 102 | 6 / 10 | 894,300 | 405,300 | 405,300 | 1,704,900 | F1 |
| Roundtrip alignment | 80 / 102 | 6 / 10 | 0 | 0 | 40,000 | 40,000 | Accuracy |
| POS | 9 / 102 local count | 0 / 10 | 66,894 | 9,673 | 12,851 | 89,418 | F1 |
| Taxi1500 | 1 / 102 | 0 / 10 | 860 | 106 | 111 | 1,077 | Macro-F1 |

Speaker note:

```text
Downstream claim은 모든 metric에서 같은 강도로 할 수 없습니다. Target10 기준으로
Tatoeba는 3개, Bible과 Roundtrip은 6개, NER도 6개 언어에서 가능합니다. 반면 POS와
Taxi1500은 target10 coverage가 없기 때문에 Glot500-style replay로는 남기되,
target-side novelty evidence로 쓰지 않습니다.
```

## Slide G. Head / Target10 / All을 왜 나누는가

Title:

```text
Head, Target10, All을 분리해야 성능 해석이 흔들리지 않음
```

On-slide bullets:

- `head`: XLM-R 학습에 포함된 92개 언어 중 해당 task data가 있는 subset
- `target10`: XLM-R-unseen 10개 언어 중 해당 task data가 있는 subset
- `all`: v5.1의 102개 universe에서 data가 있는 전체 subset
- 같은 metric이라도 target coverage가 다르므로 평균을 섞어 해석하지 않음
- Novelty claim은 `v51_random` vs `v51_fvt`의 target10 결과를 중심으로 판단

Speaker note:

```text
Glot500류 실험에서 평균 하나만 제시하면 어떤 언어에서 좋아진 것인지 알기 어렵습니다.
특히 이번 실험은 head 92개와 XLM-R-unseen target10의 역할이 다릅니다. 그래서 모든
결과는 head, target10, all로 분리해서 보고합니다. target10 coverage가 없는 POS와
Taxi1500은 target10 평균에 넣지 않습니다.
```

## Slide H. 이 데이터 선택으로 가능한 주장

Title:

```text
가능한 주장과 불가능한 주장을 분리
```

On-slide table:

| Claim | Status | Reason |
| --- | --- | --- |
| Held-out PPPL 비교 | 가능하도록 설계됨 | 102개 언어 모두 dev/test split 존재 |
| Random vs FVT initializer 비교 | 가능하도록 설계됨 | 같은 corpus/tokenizer/schedule의 matched pair |
| Target10 downstream 일부 비교 | 제한적으로 가능 | Tatoeba 3개, Bible/NER/Roundtrip 6개 target coverage |
| Full target10 downstream claim | 불가 | POS/Taxi1500 target coverage 0, 일부 task도 10/10 아님 |
| Strict low-resource final claim | v5.1 단독으로는 제한 | downstream-aware target 중 일부가 mid/high-resource |

Speaker note:

```text
이 데이터 선택의 장점은 claim boundary가 명확하다는 점입니다. PPPL은 102개 모두에서
held-out test로 측정할 수 있고, Random과 FVT는 같은 조건의 matched pair로 비교할 수
있습니다. 다만 downstream은 task data가 있는 target subset에서만 말해야 합니다.
그래서 v5.1은 좋은 diagnostic line이지만, strict low-resource final claim은 v5와
함께 구분해서 설명합니다.
```

## One-minute Summary Script

```text
데이터 구성은 102개 language-script를 기준으로 잡았습니다. 이 중 92개는 XLM-R
학습에 포함된 head 언어이고, 10개는 XLM-R-unseen target 언어입니다. 모든 언어에서
먼저 dev/test를 분리했고, tokenizer와 MLM은 train-only corpus로만 진행했습니다.
따라서 PPPL은 held-out test에서 계산할 수 있습니다.

Target10은 단순히 raw corpus가 있는 언어가 아니라, downstream task까지 볼 수 있는
언어를 중심으로 다시 선정했습니다. 기준은 XLM-R-unseen, Glot500 raw 존재,
new_length 3만 이상, downstream overlap, 그리고 지역/문자 다양성입니다.

최종 target10은 Gujarati, Assamese, Serbian Cyrillic, Sundanese, Standard Malay,
Azerbaijani, Filipino, Bosnian, Dzongkha, Santali입니다. 이 중 8개는 적어도 하나의
downstream task coverage가 있고, Dzongkha와 Santali는 Tibetan/Ol Chiki script
diversity anchor 역할을 합니다.

결과 해석에서는 head, target10, all을 분리합니다. 특히 POS와 Taxi1500은 target10
coverage가 없기 때문에 target novelty evidence로 쓰지 않고, Tatoeba, Bible, NER,
Roundtrip만 target-side downstream claim에 사용합니다.
```

## Source Files

| Need | Source |
| --- | --- |
| target10 manifest | `docs/exp/v5.1/0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv` |
| strict language split | `docs/exp/v5.1/0_tokenizer/00_data_scope/strict_data_composition_by_language.md` |
| coverage summary | `docs/exp/v5.1/3_evaluation/00_coverage/coverage_summary.tsv` |
| dataset size table | `docs/exp/v5.1/4_reporting/00_tables/table_07_dataset_sizes.md` |
