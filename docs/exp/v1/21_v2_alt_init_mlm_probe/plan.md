# Step 21 Plan: V2 Alternative-Initialization MLM Probe

## Goal

Check whether the Step15/17 added-token failure is specific to the selected `fvt` initialization or persists under other plausible Step14 initialization methods after the same token-matched MLM adaptation budget.

## Inputs

- Step14 initialization checkpoints and zero-step scores
- Step15 `fvt` adapted checkpoints and original-control summaries
- Step12 v2 train text
- Step12 Mark/dev text

No `ACT` final file may be read.

## Methods

Default probe methods:

- `mean`
- `align`

`random` and `focus` are not first-priority because their Step14 zero-step losses are much worse than `fvt`, `mean`, and `align`.

## Work

1. Train each alternative init method for seeds `13,17,23` with the same 500k train-token budget used in Step15.
2. Save each adapted checkpoint under the Step21 checkpoint root.
3. Evaluate Step21 checkpoints and Step15 `fvt` checkpoints with the same Mark/dev category-loss evaluator.
4. Compare alternative methods to the Step15 `fvt` baseline on:
   - raw Mark/dev MLM loss;
   - all-token category loss;
   - base-token category loss;
   - added-token category loss;
   - original-control raw MLM loss context.

## Required Outputs

- `score_table.tsv`
- `init_probe_summary.tsv`
- `init_probe_learning_curves.tsv`
- `init_probe_category_loss.tsv`
- `init_probe_variant_summary.tsv`
- `checkpoint_selection.md`
- `v2_no_final_access_audit.tsv`
- `file_results.tsv`
- `results.md`

## Exit Criteria

The step may exit only when:

- all configured method/seed runs complete;
- all output files are listed in `file_results.tsv`;
- `score_table.tsv` has no blank or `TBD` values;
- `v2_no_final_access_audit.tsv` shows no ACT final access;
- method selection and comparison use Mark/dev only.

## Passing Probe Gate

An alternative init passes only if it improves added-token category loss without worsening base/all category loss versus the Step15 `fvt` baseline in all seeds, and its raw mean Mark/dev loss is at least no worse than the Step15 `fvt` adapted mean.

If no method passes, keep model-dependent positive claims blocked and either revisit the tokenizer/objective more substantially or downgrade the final claim.
