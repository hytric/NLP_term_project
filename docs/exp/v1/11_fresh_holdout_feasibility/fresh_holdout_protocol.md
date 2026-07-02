# Step 11 Fresh-Heldout Protocol

## Decision

No current second_try artifact provides a fresh held-out translation test set.

## Why

- Train books are already used by tokenizer training and MLM adaptation: `1CO,1JO,1PE,1TH,1TI,2CO,2JO,2PE,2TH,2TI,3JO,ACT,COL,EPH,GAL,HEB,JAM,JUD,LUK,MAT,PHI,PHM,REV,ROM,TIT`.
- Dev books are already used for selection: `MAR`.
- Test books are already burned by Step07/Branch001/Step09 feedback: `JOH`.
- No untouched target10 book remains in the current split.
- Legacy processed translation files exist outside the second_try evidence boundary and need reimport/provenance before use.

## Required Protocol For F02/F03

1. Return to `01_data_and_splits` and reserve a new final held-out book before tokenizer training and MLM adaptation, or add a new external parallel corpus under second_try with provenance.
2. Rerun tokenizer/MLM adaptation if the held-out book changes the training corpus.
3. Select method/model/pair/scoring on dev only.
4. Evaluate exactly once on the fresh final held-out set.
5. Report method-matched high-resource and target ratios in one score table.
