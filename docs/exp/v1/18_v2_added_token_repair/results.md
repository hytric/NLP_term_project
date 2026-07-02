# Step 18 Results: V2 Added-Token-Focused Repair

Status: COMPLETED

Run id: step18_v2_added_token_repair_20260611_175200

Completed date: 2026-06-11

Artifact gate status: PASS

Repair gate status: FAIL

## Summary

Step 18 trains the Step 14 selected adapted checkpoint with an added-token-focused MLM objective. Evaluation uses the standard unweighted Mark/dev MLM diagnostic. ACT final was not read.

| Metric | Value |
| --- | ---: |
| completed seeds | 3/3 |
| added-token improved seeds | 3/3 |
| all-token nonworse seeds | 0/3 |
| repaired seeds | 0/3 |
| mean added loss delta vs Step17 | -0.508373 |
| mean all loss delta vs Step17 | 0.122137 |
| selected seed | 23 |
| selected checkpoint | /home/axt/mnt2/jongha/second_try/checkpoints/18_v2_added_token_repair/added_weighted_seed23 |

## Interpretation

If repair gate passes, rerun Step 15-style original-control comparison with the repaired checkpoint family. If repair gate fails, this weighted objective is insufficient and the next repair should change initialization or use a staged/frozen-base objective.

## Failure Return

Failed gate: added_token_repair_gate

Observed evidence: improved_added=3/3, nonworse_all=0/3

Return-to step: 14_v2_embedding_init or 18_v2_added_token_repair

Required fix: try frequency-aware initialization, staged training, or stronger added-token objective

Runtime minutes: 25.772
