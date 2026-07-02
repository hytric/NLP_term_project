# Step 10 Results: Leakage And Selection Audit

Status: COMPLETED

Run id: step10_leakage_selection_20260611_150633

Completed date: 2026-06-11

Artifact gate status: PASS

Claim gate status: FAIL

## Summary

Step 10 completed the P0 leakage and selection audit requested by Step 09 follow-up `F06`. The target10 book split itself passes the structural split checks. However, the translation success claim remains invalidated because Step 07 selected the original target pair on John/test, Branch 001 used repeated test feedback before the final LaBSE row, and the Branch 001 pass used a mixed-method high-resource comparison.

## Counts

| Item | Count |
| --- | ---: |
| audit checks | 12 |
| pass-like checks | 7 |
| warnings | 2 |
| fail/invalidating checks | 3 |
| invalidated run rows | 4 |

## Main Findings

- Split integrity: `PASS`; no duplicated `(iso, verse_id)`, no verse assigned to multiple splits, and Mark/John split rules hold.
- Exact normalized text duplicate risk: `WARN_DISCLOSED`; see `leakage_audit.tsv`.
- Step 07 original target selection: `FAIL_INVALIDATES_TRANSLATION_SELECTION`.
- Branch 001 top-tier success: `FAIL_INVALIDATES_BRANCH_SUCCESS`.
- Step 09 method-matched audit remains the current authority: selected adapted ratio below threshold.

## Failure Return

Failed gate: selection_protocol_for_translation_claim

Observed evidence: Step 07 target-pair selection used John/test; Branch 001 saw prior test feedback and used a mixed-method high-resource comparison.

Return-to step: `07_translation_benchmark` plus fresh held-out evaluation; if stronger main-model evidence is required, also return to `05_mlm_adaptation`.

Required fix: freeze method/model/pair/scoring on dev only, use method-matched high-resource and target scoring, and evaluate once on a fresh held-out set before making a top-tier translation claim.
