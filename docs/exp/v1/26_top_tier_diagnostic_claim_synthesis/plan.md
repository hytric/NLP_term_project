# Step 26 Plan: Top-Tier Diagnostic Claim Synthesis

Created: 2026-06-11

## Goal

Lock the final top-tier claim that is actually supported by the current `second_try` evidence.

The intended outcome is not a positive adapted-model claim. Steps 15, 16, 24, and 25 block that. The intended outcome is a diagnostic/negative claim that explains what works, what fails, why the failure is not a shortcut, and what experiment would be required to reopen a positive claim.

## Scope

- Use only files under `docs/exp/second_try`.
- Do not use first_try evidence.
- Do not train a model in this step.
- Do not read or inspect the `ACT` final held-out set.
- Treat Step 22 as the shortcut authority and Step 25 as the latest model-dependent control evidence.

## Required Checks

1. Convert supported evidence into allowed final claim wording.
2. Convert failed gates into explicitly blocked claim wording.
3. Verify that Step23 smaller-vocab `PASS` is not worded as original-control competitiveness.
4. Verify that Step24 and Step25 failures block positive downstream and translation final readout.
5. Define the exact P0 experiments required if a future positive claim is pursued.
6. Record every Step26 output in `file_results.tsv`.

## Exit Criteria

- `final_claim_contract.md` defines the paper's allowed main claim.
- `evidence_table.tsv` maps every allowed claim to a source and numeric evidence.
- `unsupported_claims.tsv` lists every blocked positive claim and its failed gate.
- `paper_framing.md` provides title, abstract, contribution, and table/figure guidance.
- `next_positive_experiments.tsv` gives the return path if positive claims are pursued later.
- `score_table.tsv` has no blank, `TBD`, or `NA_NOT_CHECKED` cells.
- `file_results.tsv` records current path, size, md5, and status for every Step26 output.

## Failure Return

If a blocked positive claim appears in final wording, return to this step and rewrite the claim contract.

If a positive model-dependent claim is still required, return to `objective_or_data_redesign`, then rerun Step15/16-style original-control and normalized audits before downstream or translation final readout.

If any Step26 output references final `ACT` evaluation metrics, return to `12_v2_split_protocol` and repeat the no-final audit before continuing.
