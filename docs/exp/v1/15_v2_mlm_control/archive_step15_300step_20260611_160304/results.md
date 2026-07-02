# Step 15 Results: V2 MLM Control

Status: COMPLETED

Run id: step15_v2_mlm_control_20260611_160304

Completed date: 2026-06-11

Artifact gate status: PASS

Claim gate status: FAIL

## Summary

Step 15 trained the Step 14 selected adapted checkpoint and an original `xlm-roberta-base` continued-pretraining control on v2 train text. Selection and diagnostics used Mark/dev only. ACT final was not read.

| Metric | Value |
| --- | --- |
| seeds | 13,17,23 |
| train rows loaded | 52124 |
| dev rows loaded | 6521 |
| train steps per run | 300 |
| batch size | 8 |
| eval batch size | 8 |
| selected Step 14 init | fvt |
| adapted improved seeds | 3/3 |
| original-control completed seeds | 3/3 |
| adapted mean final dev loss | 5.618403 |
| original-control mean final dev loss | 3.123752 |
| adapted/original diagnostic ratio | 1.798607 |

## Gate Evidence

- `score_table.tsv` records every gate and return target.
- `seed_summary.tsv` records every family/seed result.
- `mlm_learning_curves.tsv` records zero-step and scheduled Mark/dev evaluations.
- `checkpoint_selection.md` records both selected checkpoints using Mark/dev only.
- `v2_no_final_access_audit.tsv` lists only train/dev inputs and reports no final access.

## Failure Return

Failed gate: v2_mlm_control_claim_gate

Observed evidence: adapted_improved=3/3, diagnostic_ratio=1.798607, margin=1.100000

Likely cause: adapted MLM control is not yet strong enough for a top-tier model-dependent claim

Return-to step: 15_v2_mlm_control or 14_v2_embedding_init

Required fix: increase adaptation budget, revisit initialization, or downgrade final claim before downstream/translation

Runtime minutes: 18.720
