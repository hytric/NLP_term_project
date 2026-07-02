# Task 6. Text Classification

작성일: 2026-06-19

## Task 정의

Text Classification은 sentence/document-level meaning이 언어 간에 transfer되는지 평가한다.

Glot500은 Taxi1500-style multilingual text classification을 사용한다. v3.1에는 아직 target10 전체에 대한 Taxi1500-style label이 없으므로, 현재 evidence는 Coptic-Syriac pair-classification proxy다.

## 데이터/설정

현재 proxy:

- task: Coptic-Syriac sentence pair가 같은 Bible `item_id`를 공유하는지 분류
- directions: `cop -> syr`, `syr -> cop`
- encoder: frozen
- classifier: logistic regression
- best features: `abs(e_src - e_tgt) + e_src * e_tgt + cosine`
- positive: same `item_id`
- negative: shifted negative 및 hard negative pairs

## 결과

| Direction | Baseline macro F1 | Candidate mean macro F1 | Delta | Baseline AUROC | Candidate mean AUROC | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `cop -> syr` | `0.6894` | `0.7247` | `+0.0352` | `0.8026` | `0.8603` | `+0.0577` |
| `syr -> cop` | `0.7198` | `0.7916` | `+0.0718` | `0.7960` | `0.8841` | `+0.0880` |

## 해석

현재 v3.1 result set에서 가장 강한 downstream-style signal이다. Shallow classifier가 XLM-R-base embedding보다 adapted embedding에서 더 강한 Coptic-Syriac same-verse signal을 뽑아낸다.

Raw cosine만으로는 결과가 불안정하다. Positive result는 classifier가 pairwise difference/product structure를 사용할 때 나타난다.

## 주장 가능 범위

가능:

> Adapted frozen embeddings는 Coptic-Syriac pair-classification proxy를 개선한다.

불가능:

> 이것을 full Taxi1500-style text classification 또는 target10-wide downstream transfer라고 주장할 수 없다.

## 산출물

| Artifact | 용도 |
| --- | --- |
| `../../02_embedding_downstream/results.md` | main pair-classification result |
| `../../02_embedding_downstream/pair_classification_results.tsv` | raw result rows |
| `../../02_embedding_downstream/pair_classification_delta_summary.tsv` | baseline-candidate deltas |
