# Step 25 Plan: V2 8k Continued-Budget Probe

작성일: 2026-06-11

## Goal

Test whether the selected 8k branch fails Step24 mainly because the 500k-token MLM budget is too small.

## Design

Continue both model families from their matched 500k-token checkpoints:

- adapted 8k branch from Step23
- original XLM-R continued-pretraining control from Step15

Each seed receives an additional 500k train tokens, producing approximately 1M total train tokens per run. The continuation uses fresh optimizer state for both families, so this is a budget probe rather than a final from-scratch control.

## Inputs

- Step24 `raw_control_summary.tsv`
- Step12 train text
- Step12 Mark/dev text
- Step16 normalized metric evaluator

## Exit Criteria

- All 6 continuation runs complete.
- Total train-token ratio across all runs is `<=1.020000`.
- The adapted 8k branch improves over its 500k checkpoint in `3/3` seeds.
- Word- and character-normalized adapted/original ratios are recorded.
- Probe passes only if both normalized ratios are `<=1.100000`.
- `score_table.tsv`, `continued_budget_summary.tsv`, `normalized_mlm_scores.tsv`, `checkpoint_selection.md`, `v2_no_final_access_audit.tsv`, `results.md`, and `file_results.tsv` are complete.

## Failure Return

If the probe fails:

- Budget extension alone is not enough.
- Do not run positive downstream or translation final readout.
- Either redesign objective/data beyond longer 8k MLM, or downgrade the model-dependent claim.

If the probe passes:

- Open a formal from-scratch 1M-token control rerun before downstream or translation final readout.
