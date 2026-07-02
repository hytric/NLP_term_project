# Stage 08 Report Placement

작성일: 2026-06-13

## Main Body

Place these in the main method/result narrative:

1. XLM-R-base starting point and id-preserving append-only vocabulary extension.
2. High-resource replay + target10 mixture design.
3. Stage03 main tokenizer tokenization metrics.
4. Stage04 fvt initialization selection.
5. Stage05/06 current-candidate model evidence.
6. Stage07 diagnostic negative claim.

## Ablation Section

Place these in the ablation section:

1. Vocab-size grid and second_try smaller-vocab probes.
2. Random/mean/fvt/align/focus initialization comparison.
3. Byte fallback vs character coverage.
4. High-resource replay/control versus target-only or original-control evidence.
5. Added-token failure and repair probes.
6. Frozen Bible proxy, retrieval, and translation diagnostics.

## Appendix

Place these in the appendix:

1. first_try translation and pivot details.
2. second_try repair branch tables.
3. Shortcut/leakage audits.
4. Sample tokenization and generation outputs.
5. Full file manifests and command logs.

## Wording Boundary

All first_try and second_try entries must be introduced as "ablation", "diagnostic", "prototype", or "failure analysis". They must not be described as the final target10 model.
