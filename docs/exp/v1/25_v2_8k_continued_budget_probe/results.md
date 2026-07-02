# Step 25 Results: V2 8k Continued-Budget Probe

Status: COMPLETED

Run id: step25_v2_8k_continued_budget_20260611_212536

Completed date: 2026-06-11

Artifact gate status: PASS

Probe gate status: FAIL

## Summary

Step 25 continues the Step24 8k adapted and original-control checkpoints for an additional 500k train tokens, producing approximately 1M total train tokens per run. This is a fresh-optimizer continuation probe, not a final from-scratch 1M-token control. It uses train text and Mark/dev only. ACT final was not read.

| Metric | 8k Adapted Mean | Original Mean | Ratio |
| --- | ---: | ---: | ---: |
| continued final dev loss | 4.227845 +/- 0.017924 | 2.167797 +/- 0.035483 | 1.950296 |
| estimated NLL per word | 8.670034 +/- 0.021864 | 5.461847 +/- 0.101405 | 1.587381 |
| estimated NLL per char | 1.286486 +/- 0.003244 | 0.810446 +/- 0.015047 | 1.587381 |

## Interpretation

If the probe gate passes, open a formal from-scratch 1M-token control rerun before downstream or translation final readout. If it fails, longer 8k MLM alone does not rescue the model-dependent claim.

## Failure Return

Failed gate: continued_budget_competitive_gate

Observed evidence: word_ratio=1.587381, char_ratio=1.587381

Return-to step: objective_or_data_redesign

Required fix: redesign objective/data or downgrade model-dependent claim

Runtime minutes: 17.481
