# Step 20 Results: V2 Staged Added-Token Repair Grid

Status: COMPLETED

Run id: step20_v2_staged_added_repair_20260611_190908

Completed date: 2026-06-11

Artifact gate status: PASS

Repair gate status: FAIL

## Summary

Step 20 tests added-token-only repair variants from the Step15 adapted checkpoints. It uses train text and Mark/dev only. ACT final was not read.

| Metric | Value |
| --- | ---: |
| configured variants | 3 |
| completed variant/seed runs | 9/9 |
| passing variants | 0/3 |
| trainable audit failures | 0 |
| selected variant | new_row_added_lr1e-5 |
| selected mean added delta | -0.004565 |
| selected mean base delta | -0.029149 |
| selected mean all delta | -0.016669 |

## Interpretation

If repair gate passes, rerun Step15/Step16 style original-control comparisons with the selected variant family before downstream or translation final readout. If repair gate fails, added-token repair remains unresolved and model-dependent positive claims remain blocked.

## Failure Return

Failed gate: staged_added_token_repair_gate

Observed evidence: passing_variants=0/3; selected_mean_added_delta=-0.004565

Return-to step: 14_v2_embedding_init or 15_v2_mlm_control

Required fix: revisit initialization, token objective, or explicitly downgrade model-dependent claim

Runtime minutes: 25.338
