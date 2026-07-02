# Step 05 Plan: MLM Adaptation

## Goal

Run controlled target10 MLM adaptation for initialized candidates and select gate-passing checkpoints.

## Inputs

- Step 04 `Gate status: PASS`
- initialized model checkpoints
- Step 01 MLM train/dev manifests

## Required Work

1. Evaluate original XLM-R on MLM dev as baseline.
2. Train each selected vocab/init candidate with fixed budget.
3. Run 3 seeds for init comparison where feasible.
4. Record train loss, dev loss, pseudo-perplexity if feasible, runtime, and tokens/sec.
5. Select best checkpoint by tokenizer gate + MLM dev loss.
6. Save only gate-passing candidates.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `mlm_results.tsv`
- `checkpoint_selection.md`
- `training_configs/`
- `file_results.tsv`

## Score Table Contract

Every candidate row must have train/dev loss and gate decision. If a run crashes, fill metrics with `RUN_FAILED` and explain in `results.md`; do not leave blanks.

## Exit Criteria

- Original XLM-R MLM baseline is recorded.
- Every required candidate has a completed or explicitly failed run.
- At least one adapted checkpoint improves over its zero-step loss and passes tokenization gate.
- `checkpoint_selection.md` names the selected checkpoint.
- `file_results.tsv` records every generated file with path, count or size, and status.
- `results.md` has `Gate status: PASS`.

## Failure Return

If all candidates fail to train, return to Step 04. If all candidates train but dev loss is bad, return to Step 03 or 04 depending on whether vocab size or init diagnostics look responsible.
