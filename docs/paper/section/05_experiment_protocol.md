# 05 Experiment Protocol Draft

## 목적

무엇을 어떻게 평가하는지 정의한다. 결과값을 보기 전에 metric family, score direction, coverage rule을 먼저 고정했다는 인상을 줘야 한다.

## Main Comparison

50K-step convergence run에서 나온 다섯 method를 비교한다.

- `random`
- `mean`
- `FVT`
- `weighted FVT`
- `family-aware mean`

모든 method는 같은 tokenizer, corpus, MLM objective, training budget, evaluation protocol을 사용한다. 따라서 차이는 새 vocabulary row initialization에서 온다.

## Evaluation Metrics

| Metric | Score | Direction | 이유 |
| --- | --- | --- | --- |
| Pseudoperplexity | weighted PPPL | lower better | MLM intrinsic fit을 본다. |
| Tatoeba retrieval | Acc10 | higher better | sentence alignment/retrieval 능력을 본다. |
| Bible retrieval | Acc10 | higher better | multilingual parallel data retrieval을 본다. |
| Text classification | macro-F1 | higher better | classification transfer를 본다. |
| NER | F1 | higher better | token-level entity labeling을 본다. |
| POS | F1 | higher better | morphosyntactic sequence labeling을 본다. |
| Roundtrip alignment | accuracy | higher better | lexical alignment consistency를 본다. |

## Reporting Groups

- `tail`: target7 또는 target coverage가 있는 unseen language group.
- `head`: XLM-R-seen/high-resource replay group.
- `all`: available evaluated languages 전체.

Coverage가 없는 group은 `NA`로 둔다. `0`은 실패 점수가 아니라 실제 score이므로 coverage 없음과 혼동하면 안 된다.

## Step-4000 Diagnostic

Step-4000 table은 다음 용도로만 쓴다.

- 50K five-way run을 왜 돌렸는지 설명하는 초기 신호.
- FVT가 early checkpoint에서 강한 signal을 보였다는 보조 근거.
- final convergence claim의 직접 근거는 아님.

## Final Table Plan

최종 표는 method columns와 group rows를 모두 포함한다.

| Metric | Group | Random | Mean | FVT | Weighted FVT | Family-aware mean | Coverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PPPL | tail/head/all | TBD | TBD | TBD | TBD | TBD | language count |
| Tatoeba | tail/head/all | TBD | TBD | TBD | TBD | TBD | language count |
| Bible | tail/head/all | TBD | TBD | TBD | TBD | TBD | language count |
| Text classification | tail/head/all | TBD | TBD | TBD | TBD | TBD | language count |
| NER | tail/head/all | TBD | TBD | TBD | TBD | TBD | language count |
| POS | tail/head/all | TBD | TBD | TBD | TBD | TBD | language count |
| Roundtrip | tail/head/all | TBD | TBD | TBD | TBD | TBD | language count |

