# Step 17 Results: V2 Added-Token Failure Analysis

Status: COMPLETED

Run id: step17_v2_added_token_failure_20260611_173758

Completed date: 2026-06-11

Artifact gate status: PASS

Diagnostic gate status: PASS

## Summary

Step 17 decomposes Step 15 Mark/dev MLM loss into original-XLM-R base-token rows and appended-token rows. ACT final was not read.

| Metric | Value |
| --- | ---: |
| adapted base-token mean loss | 2.562618 |
| adapted added-token mean loss | 7.267345 |
| added/base loss ratio | 2.835906 |
| adapted added-token share | 50.456741% |
| adapted added-token loss share | 74.269955% |
| adapted all-token mean loss | 4.935611 |
| original all-token mean loss | 2.525218 |
| adapted/original all-token ratio | 1.954529 |

## Interpretation

Next repair target: `added-token learning/init/objective`.

If the diagnostic gate passes, the adapted failure is concentrated in added-token prediction and the next method revision should prioritize added-token-specific objectives, frequency-aware initialization, or staged/frozen-base training. If it fails, the repair should focus on broader encoder degradation or the experimental claim should be downgraded.

## Failure Return

Failed gate: NOT_APPLICABLE

Observed evidence: added/base ratio `2.835906`; adapted/original ratio `1.954529`

Return-to step: `14_v2_embedding_init` / `15_v2_mlm_control`

Required fix: revise initialization/objective before positive model-dependent claims.

Runtime minutes: 4.368
