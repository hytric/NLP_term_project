# Step 19 Plan: V2 New-Row-Only Added-Token Repair

## Goal

Repair the Step15 adapted checkpoints without damaging base-token behavior by training only appended vocabulary rows and optional appended LM-head bias rows.

## Inputs

- Step15 adapted checkpoints from `15_v2_mlm_control/seed_summary.tsv`
- Step17 adapted category-loss baseline from `17_v2_added_token_failure_analysis/token_category_loss.tsv`
- v2 train text from Step12
- Mark/dev manifest from Step12

No `ACT` final file may be read.

## Work

1. For each seed `13,17,23`, load the matching Step15 `adapted_extended` checkpoint.
2. Freeze all model parameters.
3. Re-enable gradients only for the tied input/output embedding matrix and LM-head bias.
4. Apply gradient hooks that zero every row `< base_vocab_size`, so only appended token rows can update.
5. Train with an added-token-focused MLM objective using v2 train text only.
6. Evaluate the source checkpoint and final checkpoint with the same Mark/dev masking protocol.
7. Audit trainable parameters and sampled base-row deltas.
8. Save per-seed checkpoints and required TSV/Markdown outputs.

## Required Outputs

- `score_table.tsv`
- `new_row_repair_summary.tsv`
- `new_row_category_loss.tsv`
- `new_row_learning_curves.tsv`
- `trainable_parameters.tsv`
- `checkpoint_selection.md`
- `v2_no_final_access_audit.tsv`
- `file_results.tsv`
- `results.md`

## Exit Criteria

The step may exit only when:

- all three seeds complete;
- `score_table.tsv` has no blank or `TBD` values;
- `file_results.tsv` records every output file and every saved checkpoint;
- `v2_no_final_access_audit.tsv` shows no ACT final access;
- trainable audit proves base rows are preserved;
- added-token loss improves in all seeds versus the source Step15 adapted checkpoint;
- base-token and all-token loss do not worsen in all seeds versus the same source checkpoint.

## Failure Return

If trainable audit fails, return to this step and fix the freeze/hook logic.

If added-token loss does not improve, return to Step14/Step15 and change initialization or objective.

If added-token loss improves but base/all loss worsens, keep this step as a failed repair and try staged training or lower learning rate before downstream/translation readout.
