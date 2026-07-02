# Candidate Decision Selector Summary

작성일: 2026-06-04

10B CPU-only selector over English -> Coptic top8 retrieval candidates. No GPU was used.
Models were selected by group cross-validation on the validation split, then fitted on all validation candidates and evaluated on the test split.

- Selected model by validation OOF chrF++: `gradient_boosting`
- Test corpus chrF++: top1 `22.5362`, selected 10B `24.6862`, existing feature reranker `24.5921`, oracle@8 `28.3327`
- Sentence-level gain over top1 for 10B: `2.1258`
- Sentence-level remaining oracle gap for 10B: `4.0513`
- 10B better/tie/worse than top1: `375/330/174`
- 10B oracle-rank match: `298/879`

## Test Results

| Selector | Source | Corpus BLEU | Corpus chrF++ | Sentence mean chrF++ | Gain vs top1 | Gap to oracle | Better/Tie/Worse | Oracle-rank match |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| top1_retrieval | baseline | 3.7001 | 22.5362 | 22.7410 | 0.0000 | 6.1771 | 0/879/0 | 216 |
| existing_feature_reranker | baseline_existing_train_fit | 3.5567 | 24.5921 | 24.7724 | 2.0314 | 4.1458 | 264/550/65 | 298 |
| oracle_at_8 | oracle | 5.2225 | 28.3327 | 28.9181 | 6.1771 | 0.0000 | 663/216/0 | 879 |
| ridge | model_full_validation_fit | 3.1923 | 24.6279 | 24.7976 | 2.0566 | 4.1205 | 365/354/160 | 301 |
| random_forest | model_full_validation_fit | 3.4370 | 24.4931 | 24.6690 | 1.9280 | 4.2492 | 377/309/193 | 281 |
| extra_trees | model_full_validation_fit | 3.4193 | 24.4662 | 24.6405 | 1.8995 | 4.2777 | 371/328/180 | 284 |
| gradient_boosting | selected_by_validation_oof | 3.4576 | 24.6862 | 24.8668 | 2.1258 | 4.0513 | 375/330/174 | 298 |

## Reading

- 10B confirms that candidate selection has useful signal, and the validation-selected gradient-boosting model slightly improves over the existing feature reranker on test corpus chrF++.
- The improvement over the existing feature reranker is small, so this should be framed as diagnostic evidence for candidate-selection viability rather than a large modeling gain.
- The remaining oracle gap justifies future pairwise/listwise source-grounded reranking before a GPU retrieval-editing pilot.
- If 10C is run, use 10B decisions as controls and report exact-copy/wrong-retrieval sensitivity, not only chrF++.
