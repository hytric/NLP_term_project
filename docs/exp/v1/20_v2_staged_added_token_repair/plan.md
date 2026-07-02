# Step 20 Plan: V2 Staged Added-Token Repair Grid

## Goal

Test whether the Step19 failure was caused by too-large updates or by base-token loss pushing appended rows in the wrong direction.

This step runs added-token-only repair variants from the Step15 adapted checkpoints without reading `ACT` final data.

## Inputs

- Step15 adapted checkpoints from `15_v2_mlm_control/seed_summary.tsv`
- Step17 adapted category-loss baseline from `17_v2_added_token_failure_analysis/token_category_loss.tsv`
- v2 train text from Step12
- Mark/dev manifest from Step12

## Variants

Default variants:

1. `bias_only_added_lr1e-3`: train only appended LM-head bias rows.
2. `bias_only_added_lr1e-4`: train only appended LM-head bias rows with lower LR.
3. `new_row_added_lr1e-5`: train appended embedding/output rows plus appended LM-head bias rows with lower LR.

All variants use added-token-only masking for training (`base_mask_prob=0`, `added_mask_prob=0.30`) and standard Mark/dev evaluation masking.

## Required Outputs

- `score_table.tsv`
- `staged_repair_summary.tsv`
- `staged_category_loss.tsv`
- `staged_learning_curves.tsv`
- `trainable_parameters.tsv`
- `variant_selection.md`
- `v2_no_final_access_audit.tsv`
- `file_results.tsv`
- `results.md`

## Exit Criteria

The step may exit only when:

- all configured variants complete for all seeds;
- every output file is recorded in `file_results.tsv`;
- `score_table.tsv` has no blank or `TBD` values;
- `v2_no_final_access_audit.tsv` shows no ACT final access;
- trainable audits pass for the intended mode;
- at least one variant improves added-token loss in all seeds without worsening base-token or all-token loss in any seed.

## Failure Return

If no variant passes, do not proceed to positive downstream or translation readout. Return to `14_v2_embedding_init`, `15_v2_mlm_control`, or a stronger objective-level repair.
