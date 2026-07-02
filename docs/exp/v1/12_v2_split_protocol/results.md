# Step 12 Results: V2 Split Protocol

Status: COMPLETED

Run id: step12_v2_split_20260611_153114

Completed date: 2026-06-11

Artifact gate status: PASS

Claim gate status: PASS

## Summary

Step 12 creates a v2 split that unblocks fresh-heldout reruns. `ACT` is selected as the new final test book because it has 9,807 target10 rows and only 5 exact normalized train/dev duplicate hits. These correspond to 3 unique final rows, which are excluded from final scoring, leaving 9804 clean final rows and at least 852 clean final rows per target language.

## Decision

V2 split is ready for rerunning tokenizer, MLM adaptation, downstream proxy, and method-matched translation from scratch.

Existing v1 checkpoints and translation scores are invalid for v2 final claims.

## Failure Return

Failed gate: NOT_APPLICABLE

Observed evidence: NOT_APPLICABLE

Return-to step: NOT_APPLICABLE

Required fix: NOT_APPLICABLE
