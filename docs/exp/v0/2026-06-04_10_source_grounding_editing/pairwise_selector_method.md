# Pairwise Candidate Selector Method

작성일: 2026-06-04

## Purpose

This 10B follow-up checks whether relative candidate preferences improve over the pointwise candidate decision selector.

## Compute

- CPU-only.
- No GPU was used.
- No checkpoint was saved.

## Inputs

- Validation candidates: `docs/exp/2026-06-03_06_nmt_baselines/retrieval_topk_oracle_eng_to_cop_char345_k8/validation_top8_candidates.tsv`
- Test candidates: `docs/exp/2026-06-03_06_nmt_baselines/retrieval_topk_oracle_eng_to_cop_char345_k8/test_top8_candidates.tsv`
- Existing selector comparison: `docs/exp/2026-06-03_06_nmt_baselines/retrieval_topk_feature_reranker_eng_to_cop_char345_k8/test_selected.tsv`

## Command

```bash
python3 scripts/evaluate_retrieval_topk_pairwise_feature_selector.py \
  --validation-candidates docs/exp/2026-06-03_06_nmt_baselines/retrieval_topk_oracle_eng_to_cop_char345_k8/validation_top8_candidates.tsv \
  --test-candidates docs/exp/2026-06-03_06_nmt_baselines/retrieval_topk_oracle_eng_to_cop_char345_k8/test_top8_candidates.tsv \
  --existing-selected docs/exp/2026-06-03_06_nmt_baselines/retrieval_topk_feature_reranker_eng_to_cop_char345_k8/test_selected.tsv \
  --output-dir docs/exp/2026-06-04_10_source_grounding_editing \
  --models logistic_regression
```

## Method

For each validation verse, the selector builds all candidate pairs from the top8 retrieval pool. If candidate A has higher sentence-level chrF++ than candidate B, the feature-difference vector `features(A) - features(B)` receives label 1; the reverse vector receives label 0.

At test time, each candidate competes against the other candidates in its top8 pool. The selector accumulates pairwise win probabilities and chooses the candidate with the highest total score.

## Features

The feature set uses only inference-time metadata:

- candidate rank and retrieval score
- score gap and ratio relative to rank 1
- source/matched-source/candidate length ratios
- source vs matched-source word Jaccard
- source vs matched-source character 3/4/5-gram Jaccard

The Coptic reference is only used to create validation pair labels, not at test time.

## Result

| Selector | Corpus chrF++ |
| --- | ---: |
| Top1 retrieval | 22.5362 |
| Existing feature reranker | 24.5921 |
| Pointwise 10B selector | 24.6862 |
| Pairwise logistic selector | 24.7438 |
| Oracle@8 | 28.3327 |

Interpretation:

- Pairwise selection is the current best CPU retrieval selector.
- The gain over pointwise 10B is small, so the claim should remain cautious.
- Oracle@8 still leaves substantial headroom for source-grounded reranking or retrieval editing.
