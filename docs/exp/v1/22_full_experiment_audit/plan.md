# Step 22 Plan: Full Experiment Shortcut And Next-Experiment Audit

작성일: 2026-06-11

## Goal

Audit the complete second_try evidence through Step 27 and decide whether any surviving result is shortcut-driven. Also define which additional experiments are mandatory before a positive top-tier model claim.

## Scope

- Inputs are existing second_try documents and audit tables only.
- Do not train models in this step.
- Do not inspect or tune on the `ACT` final set.
- V1 evidence may be reviewed only to mark it exploratory or invalidated.
- V2 evidence is authoritative for any future final claim.

## Required Checks

1. Check every `score_table.tsv` for blanks, `TBD`, and `NA_NOT_CHECKED`.
2. Check every `file_results.tsv` path, byte count, and md5 for current files.
3. Check every `v2_no_final_access_audit.tsv` row for `final_access=NO` and passing status.
4. Check Steps 13-27 run scripts and synthesis outputs for `ACT`/final-test path reads.
5. Review Step09 and Step10 shortcut findings for v1 translation.
6. Review Steps 15-27 model-dependent, claim-synthesis, and manuscript-synthesis gates.
7. Write a required-next-experiment matrix with explicit gates and return steps.

## Exit Criteria

- `score_table.tsv` has no blank or unchecked cells.
- `shortcut_matrix.tsv` states whether each suspected shortcut is active, invalidated, or absent.
- `next_experiments.tsv` separates mandatory positive-claim experiments from optional paper-strengthening experiments.
- `results.md` states whether the current evidence can support a positive top-tier claim.
- `file_results.tsv` records every Step 22 output.

## Failure Return

If this audit finds stale artifacts, missing outputs, or final-set access:

- Return to the earliest affected step.
- Regenerate that step's outputs.
- Recompute `file_results.tsv`.
- Rerun this Step 22 audit before any final synthesis.

If this audit finds no active shortcut but the model-dependent claim remains unsupported:

- Either open a tokenizer/objective redesign step before downstream or translation final readout.
- Or downgrade the paper to a negative/diagnostic top-tier claim and proceed to final synthesis with unsupported claims removed.
