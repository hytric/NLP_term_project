# Step 23 Results: V2 Vocab-Size Objective Probe

Status: COMPLETED

Run id: step23_v2_vocab_objective_probe_20260611_203226

Completed date: 2026-06-11

Artifact gate status: PASS

Probe gate status: PASS

## Summary

Step 23 initializes smaller 8k and 16k Step13 tokenizer candidates with `fvt`, trains them with the Step15 500k-token MLM budget, and evaluates Mark/dev all/base/added category losses. ACT final was not read.

| Metric | Value |
| --- | ---: |
| vocab sizes | 8000,16000 |
| completed runs | 6/6 |
| token budget ratio | 1.000450 |
| passing variants | 2/2 |
| Step15 32k raw mean final loss | 4.946829 |
| original-control raw mean final loss | 2.518008 |
| best vocab | 8000 |
| best raw mean final loss | 4.541285 |
| best raw delta vs 32k | -0.405544 |
| best raw ratio vs original | 1.803523 |

## Interpretation

If the probe gate passes, the next step is to promote the smaller tokenizer branch and rerun Step15/16 controls before any downstream or translation final readout. If the probe gate fails, smaller-vocabulary selection alone does not resolve the model-dependent failure.

## Failure Return

Failed gate: NOT_APPLICABLE

Observed evidence: passing_variants=2/2; best_vocab=8000; raw_delta_vs_32k=-0.405544

Return-to step: 15_v2_mlm_control

Required fix: rerun Step15/16 controls with selected vocab

Runtime minutes: 22.576
