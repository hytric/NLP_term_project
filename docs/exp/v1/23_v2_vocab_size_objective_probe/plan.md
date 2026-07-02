# Step 23 Plan: V2 Vocab-Size Objective Probe

작성일: 2026-06-11

## Goal

Test whether the Step15/17/18/19/20 failure is partly caused by the selected 32k appended-token vocabulary being too large for the current 500k-token MLM budget.

## Hypothesis

Smaller appended vocabularies may reduce the added-token prediction burden enough to improve added-token loss without degrading base-token or all-token loss. If so, the next positive-claim path should return to Step13/14 with a smaller tokenizer instead of continuing to repair the 32k checkpoint.

## Inputs

- Step13 tokenizer candidates: 8k, 16k, and 32k.
- Step12 train text and Mark/dev text.
- Step15 32k `fvt` MLM baseline and original-control baseline.
- Step17 32k category-loss diagnosis for context.

## Work

1. Initialize the 8k and 16k tokenizer candidates with the same `fvt` method used by Step14.
2. Train each initialized checkpoint with the Step15 MLM budget: 500k train tokens, seeds 13/17/23.
3. Evaluate zero-step and final Mark/dev category loss for all/base/added tokens.
4. Compare each smaller vocabulary against the existing 32k `fvt` Step15 baseline.
5. Do not read or inspect `ACT` final.

## Exit Criteria

- All required 8k and 16k seed runs complete.
- Token budgets match within `<=1.02`.
- At least one smaller vocabulary beats 32k on raw mean final Mark/dev loss.
- At least one smaller vocabulary has seed-stable category repair:
  - added loss improves in 3/3 seeds
  - base loss is nonworse in 3/3 seeds
  - all loss is nonworse in 3/3 seeds
- `score_table.tsv`, `vocab_probe_summary.tsv`, `vocab_probe_variant_summary.tsv`, `vocab_probe_category_loss.tsv`, `checkpoint_selection.md`, `v2_no_final_access_audit.tsv`, `results.md`, and `file_results.tsv` are complete.

## Failure Return

If the probe fails:

- Keep the result as a failed tokenizer-size redesign probe.
- Return to tokenizer/objective redesign rather than downstream or translation final readout.
- Consider a changed objective schedule or external data before another model-dependent positive claim.

If the probe passes:

- Return to Step13/14 and promote the passing vocab size as the new selected tokenizer branch.
- Rerun Step15/16-style original-control and normalized-metric audits before downstream or translation final readout.
