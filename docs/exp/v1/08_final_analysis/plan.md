# Step 08 Plan: Final Analysis And Report Tables

## Goal

Synthesize all completed step results into final report-ready evidence, including downstream and translation conclusions.

## Inputs

- Step 07 `Gate status: PASS`, or Step 07 `Gate status: FAIL` with a complete branch folder and return decision
- All previous step `results.md`
- All previous `score_table.tsv`
- All previous `file_results.tsv`

## Required Work

1. Verify every previous score table has no `TBD` or blank fields.
2. Build claim/evidence map.
3. Build paper tables for tokenization, vocab extension, init, MLM, downstream, and translation.
4. Write qualitative analysis from downstream predictions and translation samples.
5. Write limitations.
6. Decide final claim strength.
7. If Step 07 failed, downgrade the translation claim and preserve the retry branch as the return path.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `claim_evidence_map.md`
- `paper_tables.md`
- `qualitative_analysis.md`
- `limitations.md`
- `final_checklist.md`
- `file_results.tsv`

## Score Table Contract

Every claim row must have evidence file, evidence status, and final wording. No `TBD` is allowed before exit.

## Exit Criteria

- All previous steps have valid gate statuses.
- All previous score tables are filled.
- Final downstream claim is supported or explicitly downgraded.
- Translation 80% high-resource target is either supported by evidence or explicitly marked unsupported with a return branch.
- `final_checklist.md` confirms required artifacts exist.
- `results.md` has `Gate status: PASS` for a fully positive result or `Gate status: PASS_NEGATIVE_RESULT` for a completed negative synthesis.

## Failure Return

If a claim lacks evidence, either downgrade the claim in Step 08 or return to the step that should produce the missing evidence. Do not invent results. If the translation claim is unsupported, return to `07_translation_benchmark` via `branches/branch_001_translation_retrieval_gap` and append a new retry run id.
