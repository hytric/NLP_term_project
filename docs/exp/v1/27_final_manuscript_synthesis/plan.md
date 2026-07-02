# Step 27 Plan: Final Manuscript Synthesis

Created: 2026-06-11

## Goal

Convert the Step26 diagnostic claim contract into a paper-ready synthesis package.

This step does not add a new model experiment. It packages the current top-tier-safe claim, tables, reviewer-risk responses, and reproducibility checklist so the final write-up cannot drift back into unsupported positive wording.

## Scope

- Use only `docs/exp/second_try` evidence.
- Do not use first_try results as evidence.
- Do not read or report `ACT` final downstream or translation metrics.
- Treat Step26 as the final claim authority.
- Treat positive model, downstream, and translation claims as blocked unless a future objective/data redesign passes Step15/16-style controls.

## Required Outputs

1. `manuscript_outline.md`: title, abstract, sections, and contribution framing.
2. `paper_claims.md`: final allowed claims and exact wording rules.
3. `paper_tables.tsv`: report-ready table/figure manifest with source steps and intended claims.
4. `reviewer_risk_audit.tsv`: likely top-tier reviewer objections and evidence-backed responses.
5. `reproducibility_checklist.tsv`: artifact and audit checklist for claims, leakage, and metrics.
6. `score_table.tsv`: Step27 gates and status.
7. `v2_no_final_access_audit.tsv`: explicit no-final-access audit for this synthesis step.
8. `results.md`: short completion summary and next move.
9. `file_results.tsv`: current path, row/line count, bytes, md5, and status for every output.

## Exit Criteria

- The manuscript package states a diagnostic negative main claim.
- No table or abstract claim says the adapted model is competitive.
- No `ACT` final metric is reported.
- Reviewer risks have explicit mitigation/evidence entries.
- Every Step27 output is recorded in `file_results.tsv`.
- All TSV files have consistent column counts.

## Failure Return

If positive adapted-model, downstream, or translation language appears, return to Step26 and Step27 wording.

If a positive performance paper is still required, return to objective/data redesign and rerun Step15/16-style controls before writing a positive manuscript.
