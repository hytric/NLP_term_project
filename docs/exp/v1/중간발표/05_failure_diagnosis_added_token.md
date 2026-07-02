# 05. Failure Diagnosis: Added-Token Bottleneck

Source: `docs/exp/second_try/17_v2_added_token_failure_analysis`

Goal: Step15/16 실패가 base vocabulary 전체 붕괴 때문인지, 새로 append한 token row 예측 문제 때문인지 분리해서 확인했다.

Main finding: 실패는 base-token 전체 붕괴라기보다 added-token prediction 문제에 집중되어 있었다. Adapted model의 base-token loss는 original control의 all-token loss와 비슷한 수준이지만, added-token loss가 매우 높고 전체 loss의 대부분을 차지했다.

## Train / Evaluation Pair

Step17은 새 모델을 학습한 단계가 아니라, Step15에서 학습된 checkpoint들을 `MAR` dev에서 다시 평가한 진단 단계다.

| Item | Value |
| --- | --- |
| Source checkpoints | Step15 adapted extended and original-control checkpoints |
| Additional training in Step17 | none |
| Evaluation data | `MAR` dev |
| Dev rows | 6,521 |
| Final holdout | `ACT`, not used |
| Burned old test | `JOH`, excluded |
| Diagnostic split | masked target token이 base vocab row인지 added vocab row인지로 loss 분해 |

## Diagnostic Table

| Metric | Value |
| --- | ---: |
| Adapted base-token mean loss | 2.562618 |
| Adapted added-token mean loss | 7.267345 |
| Added/base loss ratio | 2.835906 |
| Adapted added-token target share | 50.456741% |
| Adapted added-token loss share | 74.269955% |
| Adapted all-token mean loss | 4.935611 |
| Original all-token mean loss | 2.525218 |
| Adapted/original all-token ratio | 1.954529 |

## Interpretation

Base-token behavior가 완전히 무너진 것은 아니다. Adapted model의 base-token mean loss `2.562618`은 original all-token mean loss `2.525218`와 가까운 편이다.

문제는 added-token row다. Added-token target은 전체 masked target의 약 절반(`50.456741%`)인데, loss share는 `74.269955%`까지 올라간다. 즉 새 tokenizer가 만든 target-specific token을 맞히는 부분에서 손실이 집중된다.

이 결과는 Step15의 실패를 설명한다. Vocabulary extension은 sequence fragmentation을 줄였지만, MLM head는 새로 추가된 수만 개의 class를 안정적으로 예측해야 한다. 특히 32k extension에서는 added rows가 많아서 supervision이 희소해지고, 새 class의 prediction problem이 original control보다 훨씬 어려워진다.

## Takeaway

다음 repair target은 base model 전체가 아니라 added-token learning이다. 단순히 더 학습하거나 base row까지 크게 움직이는 방식보다, added rows를 더 잘 예측하게 만들면서 base-token behavior를 보존하는 objective가 필요하다.
