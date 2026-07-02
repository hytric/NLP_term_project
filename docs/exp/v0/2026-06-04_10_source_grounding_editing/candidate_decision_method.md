# Candidate Decision Selector Method

작성일: 2026-06-04

## Purpose

10B tests whether a lightweight source-candidate selector can choose better Coptic retrieval candidates before any new GPU retrieval-editing run.

## Compute

- CPU-only.
- No GPU was used.
- No model checkpoint was saved.

## Inputs

- Validation candidates: `docs/exp/2026-06-03_06_nmt_baselines/retrieval_topk_oracle_eng_to_cop_char345_k8/validation_top8_candidates.tsv`
- Test candidates: `docs/exp/2026-06-03_06_nmt_baselines/retrieval_topk_oracle_eng_to_cop_char345_k8/test_top8_candidates.tsv`
- Existing selector comparison: `docs/exp/2026-06-03_06_nmt_baselines/retrieval_topk_feature_reranker_eng_to_cop_char345_k8/test_selected.tsv`

## Model Selection

Candidate regressors:

- Ridge regression
- Random forest
- Extra trees
- Gradient boosting

Selection rule:

- Use 5-fold `GroupKFold` on validation IDs.
- Fit candidate-level regressors to validation candidate chrF++ labels.
- Select the model with the best out-of-fold validation corpus chrF++ after choosing one candidate per verse.
- Fit the selected model on all validation top8 candidates.
- Evaluate once on test top8 candidates.

Selected model:

- `gradient_boosting`

## Features

The selector uses only source/candidate metadata available at inference time:

- candidate rank
- retrieval score
- retrieval score gap/ratio against rank 1
- source and matched-source length features
- Coptic candidate length features
- source vs matched-source word Jaccard
- source vs matched-source character 3/4/5-gram Jaccard

It does not use the Coptic reference at test time.

## Outputs

- `candidate_decision_model_cv.tsv`
- `candidate_decision_results.tsv`
- `candidate_decision_test_selected.tsv`
- `candidate_decision_feature_importances.tsv`
- `candidate_decision_summary.md`
- `candidate_decision_errors.md`

## Main Result

On the English -> Coptic test set:

| Selector | Corpus chrF++ |
| --- | ---: |
| Top1 retrieval | 22.5362 |
| Existing feature reranker | 24.5921 |
| 10B gradient-boosting selector | 24.6862 |
| Oracle@8 | 28.3327 |

Interpretation:

- 10B slightly improves over the existing feature reranker.
- The improvement is small, so the safe claim is candidate-selection viability, not solved source-grounded translation.
- The oracle@8 gap remains large enough to justify a stronger pairwise/listwise selector before a GPU retrieval-editing pilot.
