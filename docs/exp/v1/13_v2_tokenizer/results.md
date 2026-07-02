# Step 13 Results: V2 Tokenizer

Status: COMPLETED

Run id: step13_v2_tokenizer_20260611_153357

Completed date: 2026-06-11

Artifact gate status: PASS

Claim gate status: PASS

## Summary

Step 13 trained or loaded 8k, 16k, and 32k target tokenizers from the Step 12 v2 train text only. Selection used Mark/dev tokenization metrics only. No ACT final file was read by this script.

Selected vocab size: `32000`.

Passing candidates: `3`.

## Gate Evidence

- `score_table.tsv` has no blank or `TBD` cells.
- `v2_no_final_access_audit.tsv` lists only train/dev inputs.
- XLM-R special ids are preserved for all passing candidates.
- Selected tokenizer is chosen from dev metrics only.

## Failure Return

Failed gate: NOT_APPLICABLE

Observed evidence: NOT_APPLICABLE

Return-to step: NOT_APPLICABLE

Required fix: NOT_APPLICABLE

Runtime minutes: 0.711
