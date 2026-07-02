# Step 10 Plan: Leakage And Selection Audit

## Goal

Run the P0 `F06_leakage_and_selection_audit` follow-up from Step 09. The purpose is to determine whether any current result depends on split leakage, verse-id oracle behavior, mixed-method comparison, or test-aware model/pair selection.

## Required Checks

1. Verify target10 split integrity:
   - no duplicated `(iso, verse_id)` rows
   - no `(iso, verse_id)` assigned to multiple splits
   - dev/test books remain Mark/John only
2. Check exact normalized text duplicates across train/dev/test and report them as potential domain leakage if present.
3. Audit Step 07 selection:
   - identify whether target pair selection used John/test
   - identify whether Branch 001 pass used a method-matched high-resource reference
4. Audit branch search:
   - count test rows observed before the final branch decision
   - mark any repeated test feedback before final success as test-adaptive model search
5. Audit Step 09:
   - confirm method-matched high-resource and target scoring
   - confirm dev-only target pair selection

## Required Outputs

- `results.md`
- `score_table.tsv`
- `leakage_audit.tsv`
- `selection_trace.md`
- `invalidated_runs.tsv`
- `file_results.tsv`

## Exit Criteria

- Every required output exists and is recorded in `file_results.tsv`.
- No `score_table.tsv` cell is blank or `TBD`.
- Any invalidated claim is explicitly named with the evidence file and return path.
- If the audit finds test-aware selection or mixed-method comparison, the current translation success claim remains blocked.

## Failure Return

If split leakage is found in Step 01 data, return to `01_data_and_splits`. If selection leakage is found in Step 07/Branch 001, return to `07_translation_benchmark` with a fresh held-out evaluation protocol.
