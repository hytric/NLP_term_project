# Step 16 Results: V2 MLM Metric Fairness Audit

Status: COMPLETED

Run id: step16_v2_mlm_metric_fairness_20260611_172337

Completed date: 2026-06-11

Artifact gate status: PASS

Claim gate status: FAIL

## Summary

Step 16 evaluates every Step 15 token-matched checkpoint on Mark/dev only and reports tokenizer-normalized MLM diagnostics. ACT final was not read.

| Metric | Adapted Mean | Original Mean | Ratio |
| --- | ---: | ---: | ---: |
| raw masked-token loss | 4.940636 +/- 0.015153 | 2.503305 +/- 0.015179 | 1.973645 |
| estimated NLL per word | 9.094015 +/- 0.027891 | 6.321168 +/- 0.038328 | 1.438660 |
| estimated NLL per char | 1.349398 +/- 0.004139 | 0.937954 +/- 0.005687 | 1.438660 |

## Interpretation

Raw masked-token loss is not directly comparable across tokenizers, but the normalized diagnostics also fail the configured competitive margin of `1.100000`. Step 15's negative model-dependent conclusion remains in force.

## Failure Return

Failed gate: normalized_mlm_competitive_gate

Observed evidence: word_ratio=1.438660, char_ratio=1.438660

Return-to step: 14_v2_embedding_init or 15_v2_mlm_control

Required fix: revise initialization/objective or downgrade model-dependent claim

Runtime minutes: 4.022
