# 04. Matched-Token MLM Control

Source:

- `docs/exp/second_try/15_v2_mlm_control`
- metric fairness check: `docs/exp/second_try/16_v2_mlm_metric_fairness`

Goal: extended-vocabulary adapted model이 단순히 좋아졌는지 보는 것이 아니라, 같은 train-token budget에서 original `xlm-roberta-base` continued-pretraining control보다 경쟁력이 있는지 확인했다.

Main finding: adapted extended model은 zero-step 대비 `3/3` seeds에서 개선되었다. 하지만 original XLM-R continued-pretraining control보다 훨씬 약했고, raw loss ratio와 normalized word/char ratio 모두 허용 기준을 통과하지 못했다.

## Setup

| Item | Value |
| --- | --- |
| Adapted model | Step14 selected `fvt` extended model |
| Control model | original `xlm-roberta-base` continued pretraining |
| Selection split | Mark/dev only |
| Final ACT access | 없음 |
| Seeds | `13`, `17`, `23` |
| Train rows | 52,124 |
| Dev rows | 6,521 |
| Train-token budget | 500,000 |
| Steps per run | 1,600 |
| Batch / eval batch | 8 / 8 |
| Token budget range | 500,008-500,407 |

## Train / Evaluation Pair

| Item | Adapted extended `fvt` | Original XLM-R control |
| --- | --- | --- |
| Starting model | Step14 selected `fvt` extended checkpoint | original `xlm-roberta-base` |
| Tokenizer | v2 extended tokenizer | original XLM-R tokenizer |
| Train data | v2 train books, `MAR/JOH/ACT` excluded | same v2 train books, `MAR/JOH/ACT` excluded |
| Train rows | 52,124 | 52,124 |
| Eval data | `MAR` dev | same `MAR` dev |
| Eval rows | 6,521 | 6,521 |
| Final holdout | `ACT`, not used | `ACT`, not used |
| Burned old test | `JOH`, excluded | `JOH`, excluded |
| Seeds | 13, 17, 23 | 13, 17, 23 |
| Train-token budget | about 500k tokens | about 500k tokens |

Book split meaning:

| Book code | Book | Role |
| --- | --- | --- |
| `MAR` | Mark | dev/evaluation only |
| `ACT` | Acts | clean final holdout, not read in this step |
| `JOH` | John | burned/excluded old test |

Interpretation: Step15 does not train on `MAR`; it trains on the v2 train books and evaluates on `MAR` dev. `ACT` final is kept untouched, and `JOH` is excluded because it was already exposed in earlier exploratory runs.

## Raw MLM Result

| Metric | Adapted extended | Original control | Ratio / note |
| --- | ---: | ---: | --- |
| Mean final dev loss | 4.946829 | 2.518008 | 1.964580 |
| Completed seeds | 3/3 | 3/3 | complete |
| Improved vs zero-step | 3/3 | n/a | improved |
| Token-budget matched | yes | yes | matched |
| Positive-claim margin | <= 1.100000 | baseline | FAIL |

Interpretation: extended model 자체는 MLM training으로 좋아졌지만, original tokenizer/model로 같은 budget을 더 학습한 control이 훨씬 더 낮은 dev loss를 얻었다. 따라서 “vocab extension이 downstream에 유리할 것”이라는 주장은 이 단계에서 아직 지지되지 않는다.

아래 표는 같은 결과를 seed별로 풀어 쓴 것이다.

## Seed별 Final Dev Loss

| Model | Seed 13 | Seed 17 | Seed 23 | Mean final dev loss |
| --- | ---: | ---: | ---: | ---: |
| adapted extended `fvt` | 4.954783 | 4.951493 | 4.934210 | 4.946829 |
| original XLM-R control | 2.542411 | 2.540437 | 2.471175 | 2.518008 |

Interpretation: `adapted extended fvt`는 세 seed 모두 비슷한 final dev loss를 보였지만, 같은 seed 조건의 original XLM-R control보다 일관되게 높았다. 즉 차이는 특정 seed 하나의 우연이 아니라 3-seed 평균에서도 유지된다.

## Normalized Fairness Check

Raw masked-token loss는 tokenizer가 다르면 직접 비교가 과도하게 불리할 수 있다. 그래서 Step16에서 word/char 단위로 loss를 재정규화했다.

| Metric | Adapted extended | Original control | Ratio | Status |
| --- | ---: | ---: | ---: | --- |
| Raw masked-token loss | 4.940636 +/- 0.015153 | 2.503305 +/- 0.015179 | 1.973645 | FAIL |
| Estimated NLL per word | 9.094015 +/- 0.027891 | 6.321168 +/- 0.038328 | 1.438660 | FAIL |
| Estimated NLL per char | 1.349398 +/- 0.004139 | 0.937954 +/- 0.005687 | 1.438660 | FAIL |

허용 기준은 `ratio <= 1.100000`이었다. 재정규화 후 ratio가 raw ratio보다 내려가긴 했지만, 여전히 기준을 크게 넘는다.

## Takeaway

Step15/16의 결론은 실패다. Extended tokenizer는 fragmentation을 줄였고, `fvt` initialization은 zero-step에서 가장 좋았으며, adapted model도 학습으로 개선되었다. 그러나 같은 train-token budget에서 original XLM-R continued-pretraining control을 따라가지 못했다. 따라서 다음 단계는 downstream 평가가 아니라, 왜 extended model의 MLM objective가 약한지 진단하는 것이다.
