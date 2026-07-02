# Step 09 Results: Top-Tier Validation

Status: COMPLETED

Run id: step09_top_tier_20260611_144919

Completed date: 2026-06-11

Artifact gate status: PASS

Claim gate status: FAIL

## Summary

Step 09 recomputed translation retrieval with method-matched high-resource and target scores. The main question is whether the selected adapted XLM-R encoder, not an external sentence embedding model, reaches 80% of a same-method Spanish->English reference.

## Key Results

| Method | Role | High test chrF++ | Target test chrF++ | Ratio | Status |
| --- | --- | ---: | ---: | ---: | --- |
| original_xlmr_cosine | baseline | 61.959906 | 28.979374 | 0.467712 | FAIL |
| selected_adapted_xlmr_cosine | main_model | 47.785568 | 30.488796 | 0.638034 | FAIL |
| labse_csls_upper_bound | external_upper_bound | 100.000000 | 56.717922 | 0.567179 | FAIL |

## Claim Decision

Main adapted-encoder translation claim: `UNSUPPORTED_FOR_MAIN_MODEL`.

External LaBSE upper bound: `FAIL`.

Required follow-up experiments are listed in `required_followups.tsv` and `required_followups.md`.

## Gate Evidence

- `score_table.tsv` has no blank or `TBD` fields.
- Every ratio uses the same retrieval method for high-resource and target scores.
- Target pair selection uses dev only; John test is used for selected settings.

## Failure Return

Failed gate: method_matched_translation_80_percent

Observed evidence: selected_adapted_xlmr_cosine ratio=0.638034 < 0.800000; labse_csls_upper_bound ratio=0.567179 < 0.800000

Return-to step: 05_mlm_adaptation / 06_downstream_tasks / 07_translation_benchmark

Required fix: run stronger adaptation controls, dev-only branch selection, and a fresh held-out translation retrieval/generation benchmark before making a top-tier translation claim
