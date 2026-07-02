# Step 21 Results: V2 Alternative-Initialization MLM Probe

Status: COMPLETED

Run id: step21_v2_alt_init_probe_20260611_194617

Completed date: 2026-06-11

Artifact gate status: PASS

Probe gate status: FAIL

## Summary

Step 21 trains alternative Step14 initialization checkpoints with the same 500k-token MLM budget as Step15 and compares them against the Step15 `fvt` adapted baseline. It uses train text and Mark/dev only. ACT final was not read.

| Metric | Value |
| --- | ---: |
| methods | mean,align |
| completed runs | 6/6 |
| passing methods | 0/2 |
| fvt raw mean final loss | 4.946829 |
| original-control raw mean final loss | 2.518008 |
| best method | align |
| best raw mean final loss | 5.086652 |
| best raw delta vs fvt | 0.139823 |
| best raw ratio vs original | 2.020110 |

## Interpretation

If probe gate passes, rerun Step15/16 style control and normalized metric audits with that initialization before downstream or translation final readout. If probe gate fails, alternative initialization did not resolve the model-dependent failure.

## Failure Return

Failed gate: alternative_init_probe_gate

Observed evidence: passing_methods=0/2; best=align; raw_delta_vs_fvt=0.139823

Return-to step: 14_v2_embedding_init or tokenizer/objective redesign

Required fix: revisit tokenizer/objective or downgrade model-dependent claim

Runtime minutes: 24.626
