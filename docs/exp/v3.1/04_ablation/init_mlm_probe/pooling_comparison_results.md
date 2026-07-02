# MLM Dev Pooling Comparison

작성일: 2026-06-19

## Judgment

CLS (`<s>`) pooling is possible, but it should be treated as an ablation rather than the main frozen semantic-similarity representation. XLM-R/RoBERTa-style MLM training does not directly train CLS as a contrastive sentence embedding, and this run shows mean pooling gives stronger retrieval-oriented metrics.

## Score Table

| Model | Mean cosine | CLS cosine | Mean margin | CLS margin | Mean R@1 | CLS R@1 | Mean MRR | CLS MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `xlmr_base` | 0.986126 | 0.985600 | -0.003000 | -0.007491 | 0.006874 | 0.002862 | 0.020418 | 0.015012 |
| `random_mlm200` | 0.993669 | 0.997086 | -0.002612 | -0.001679 | 0.005793 | 0.004721 | 0.021748 | 0.018970 |
| `mean_mlm200` | 0.996556 | 0.994511 | -0.001656 | -0.004028 | 0.005724 | 0.004709 | 0.022055 | 0.019113 |
| `fvt_mlm200` | 0.990975 | 0.993396 | -0.002530 | -0.002711 | 0.004551 | 0.003802 | 0.019034 | 0.017251 |
| `align_mlm200` | 0.990067 | 0.994633 | -0.002603 | -0.002140 | 0.004292 | 0.003535 | 0.019030 | 0.016243 |
| `focus_mlm200` | 0.984526 | 0.994485 | -0.004347 | -0.002230 | 0.004553 | 0.003790 | 0.019333 | 0.017142 |

## Reading

- CLS sometimes increases absolute cosine, but absolute cosine is already inflated and not enough for semantic alignment.
- Mean pooling is better on Recall@1 and MRR for every row in this comparison.
- For `xlmr_base`, CLS is clearly worse than mean: MRR `0.015012` vs `0.020418`.
- For `fvt_mlm200`, CLS also trails mean: MRR `0.017251` vs `0.019034`.
- Main result should keep mean pooling; CLS should be reported as a pooling ablation.
