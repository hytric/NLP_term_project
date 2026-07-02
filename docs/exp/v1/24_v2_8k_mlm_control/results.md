# Step 24 Results: V2 8k MLM Control And Normalized Audit

Status: COMPLETED

Run id: step24_v2_8k_mlm_control_20260611_211153

Completed date: 2026-06-11

Artifact gate status: PASS

Claim gate status: FAIL

## Summary

Step 24 compares the Step23 selected 8k adapted branch against the Step15 original XLM-R continued-pretraining control. It uses existing matched-budget train/dev checkpoints and re-evaluates normalized MLM diagnostics on Mark/dev only. ACT final was not read.

| Metric | 8k Adapted Mean | Original Mean | Ratio |
| --- | ---: | ---: | ---: |
| raw Step23/Step15 final dev loss | 4.541285 +/- 0.021088 | 2.518008 +/- 0.033126 | 1.803523 |
| re-evaluated raw masked-token loss | 4.534317 | 2.503305 | 1.811332 |
| estimated NLL per word | 9.304881 +/- 0.021185 | 6.321168 +/- 0.038328 | 1.472019 |
| estimated NLL per char | 1.380687 +/- 0.003144 | 0.937954 +/- 0.005687 | 1.472019 |

## Interpretation

The 8k branch is the best current adapted branch, but the positive model-dependent claim requires both normalized ratios to be within `1.100000` of the original-control baseline.

## Failure Return

Failed gate: 8k_normalized_mlm_competitive_gate

Observed evidence: word_ratio=1.472019, char_ratio=1.472019

Return-to step: 23_v2_vocab_size_objective_probe or objective_redesign

Required fix: redesign objective/data beyond smaller-vocab branch or downgrade model-dependent claim

Runtime minutes: 2.883
