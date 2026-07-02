# Pairwise Candidate Selector Summary

작성일: 2026-06-04

CPU-only pairwise/listwise selector over English -> Coptic top8 retrieval candidates. No GPU was used.
The model is trained from validation candidate pairs and scores test candidates by accumulated pairwise win probability.

- Selected pairwise model by validation OOF chrF++: `logistic_regression`
- Test corpus chrF++: top1 `22.5362`, pairwise `24.7438`, oracle@8 `28.3327`
- Existing feature reranker corpus chrF++: `24.5921`
- Pairwise better/tie/worse than top1: `406/285/188`
- Pairwise oracle-rank match: `311/879`

## Test Results

| Selector | Source | Corpus BLEU | Corpus chrF++ | Sentence mean chrF++ | Gain vs top1 | Gap to oracle | Better/Tie/Worse | Oracle-rank match |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| top1_retrieval | baseline | 3.7001 | 22.5362 | 22.7410 | 0.0000 | 6.1771 | 0/879/0 | 216 |
| existing_feature_reranker | baseline_existing_train_fit | 3.5567 | 24.5921 | 24.7724 | 2.0314 | 4.1458 | 264/550/65 | 298 |
| oracle_at_8 | oracle | 5.2225 | 28.3327 | 28.9181 | 6.1771 | 0.0000 | 663/216/0 | 879 |
| logistic_regression | selected_by_validation_oof | 3.0602 | 24.7438 | 24.9134 | 2.1724 | 4.0047 | 406/285/188 | 311 |

## Reading

- Pairwise selection is a stricter test than pointwise 10B because it learns relative candidate preferences.
- If pairwise chrF++ does not beat the pointwise 10B selector, keep pointwise 10B as the current deployed CPU selector.
- If pairwise does beat pointwise 10B, use it as the preferred retrieval selector before any 10C GPU editing pilot.
- Either way, oracle@8 remains the upper bound that motivates better source-grounded reranking.
