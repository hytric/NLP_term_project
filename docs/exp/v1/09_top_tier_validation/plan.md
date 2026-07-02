# Step 09 Plan: Top-Tier Validation

## Goal

Convert the exploratory second_try evidence into a top-tier-paper-safe claim by removing shortcut-prone comparisons and adding method-matched validation.

## Core Review Risks

| Risk | Why It Matters | Required Check |
| --- | --- | --- |
| method mismatch | Step 07 used XLM-R high-resource reference but LaBSE target branch | recompute high-resource and target scores with the same retrieval method |
| test-aware selection | repeated branch attempts touched John test | select model/pair/scoring on dev only and report test once |
| external-model shortcut | LaBSE pass does not prove adapted XLM-R quality | separate external upper bound from adapted-encoder claim |
| proxy task weakness | retrieval proxy is not free translation | report as retrieval translation proxy only |
| weak MLM evidence | adapted MLM does not beat original XLM-R | keep MLM claim limited unless longer adaptation is run |

## Required Work

1. Evaluate method-matched translation retrieval for:
   - original XLM-R
   - selected adapted XLM-R
   - LaBSE sentence embedding upper bound
2. For each method, compute:
   - high-resource Spanish->English dev/test score
   - target10 dev-selected pair and held-out John test score
   - target/high-resource ratio using the same method
3. Set top-tier claim status:
   - `SUPPORTED` only for method-matched claims
   - `UPPER_BOUND_ONLY` for external model evidence
   - `UNSUPPORTED` for adapted-encoder translation if below threshold
4. Write additional experiment requirements for any unsupported top-tier claim.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `method_matched_translation.tsv`
- `dev_selection_grid.tsv`
- `top_tier_claim_contract.md`
- `file_results.tsv`

## Exit Criteria

- No score cell is blank or `TBD`.
- Every positive claim uses method-matched evidence.
- External model evidence is labeled separately from adapted XLM-R evidence.
- If the 80% translation target fails under method-matched evaluation, the final top-tier claim must not say translation is solved.

## Failure Return

If method-matched adapted XLM-R translation fails, return to Step 05/06/07 with stronger adaptation or stricter branch design. If external upper bound is the only pass, keep it as analysis only.
