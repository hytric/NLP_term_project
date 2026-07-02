# Step 11 Plan: Fresh-Heldout Feasibility

## Goal

Determine whether the current second_try artifacts contain a clean fresh held-out evaluation set for the P0 method-matched translation follow-ups `F02` and `F03`.

## Required Checks

1. Identify books used by current train/dev/test split.
2. Mark books touched by tokenizer training and MLM adaptation.
3. Mark books touched by dev selection and John/test feedback.
4. Search second_try artifacts for non-Bible or non-current-split parallel evaluation data.
5. Decide whether F02/F03 can run now without redefining the top-tier held-out requirement.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `data_availability.tsv`
- `fresh_holdout_protocol.md`
- `file_results.tsv`

## Exit Criteria

- All candidate data sources are labeled `USABLE_NOW`, `REQUIRES_RERUN`, `OUT_OF_SCOPE`, or `NOT_FOUND`.
- If no fresh held-out set exists, the return path must identify the earliest step to rerun.
- No `score_table.tsv` cell is blank or `TBD`.

## Failure Return

If no fresh held-out set exists in the current artifacts, return to `01_data_and_splits` to reserve a new held-out book before tokenizer/MLM adaptation, or add a new external corpus with provenance under second_try before evaluation.
