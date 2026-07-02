# Step 19 Results: V2 New-Row-Only Added-Token Repair

Status: COMPLETED

Run id: step19_v2_new_row_only_repair_20260611_183952

Completed date: 2026-06-11

Artifact gate status: PASS

Repair gate status: FAIL

## Summary

Step 19 starts from each Step15 adapted checkpoint, freezes model behavior, and trains only appended vocabulary rows plus appended LM-head bias rows. Evaluation uses Mark/dev only. ACT final was not read.

| Metric | Value |
| --- | ---: |
| completed seeds | 3/3 |
| trainable audit pass seeds | 3/3 |
| added-token improved seeds | 0/3 |
| base-token nonworse seeds | 3/3 |
| all-token nonworse seeds | 0/3 |
| repaired seeds | 0/3 |
| mean added loss delta vs source | 0.240600 |
| mean base loss delta vs source | -0.048017 |
| mean all loss delta vs source | 0.097944 |
| selected seed | 13 |
| selected checkpoint | /home/axt/mnt2/jongha/second_try/checkpoints/19_v2_new_row_only_repair/new_row_only_seed13 |

## Interpretation

If repair gate passes, rerun Step15/Step16 style original-control comparisons with this repaired checkpoint family before any downstream or translation final readout. If repair gate fails, keep the result as a failed repair and try a staged or lower-learning-rate variant.

## Failure Return

Failed gate: new_row_only_repair_gate

Observed evidence: trainable_pass=3/3, added_improved=0/3, base_nonworse=3/3, all_nonworse=0/3

Return-to step: 15_v2_mlm_control or 19_v2_new_row_only_repair

Required fix: try lower learning rate, staged new-row training, or changed added-token objective

Runtime minutes: 12.240
