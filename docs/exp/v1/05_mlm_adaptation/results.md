# Step 05 Results: MLM Adaptation

Status: COMPLETED

Run id: step05_mlm_20260610_230343

Completed date: 2026-06-10

Gate status: PASS

## Required Artifact Check

| Artifact | Path | Present? | Notes |
| --- | --- | --- | --- |
| score table | `score_table.tsv` | yes | baseline plus 5 candidate rows |
| file results | `file_results.tsv` | yes | docs and selected checkpoint recorded |
| MLM results | `mlm_results.tsv` | yes | train/dev losses recorded |
| checkpoint selection | `checkpoint_selection.md` | yes | selected checkpoint named |
| training configs | `training_configs/` | yes | fixed-budget configs |

## Summary

Step 05 ran a controlled fixed-budget MLM adaptation pilot on GPU fallback `cuda`. Each Step 04 passing candidate used the same training budget.

| Metric | Value |
| --- | --- |
| original XLM-R dev loss | 6.330356 |
| train rows used | 1000 |
| dev rows used | 200 |
| train steps per candidate | 20 |
| candidates run | 5 |
| improved candidates | 5 |

## Selected Checkpoint

Selected: `spm32000_fvt_seed13` at `/home/axt/mnt2/jongha/second_try/checkpoints/05_mlm_adaptation/spm32000_fvt_seed13`.

## Gate Evidence

Evidence:

- `score_table.tsv` has no `TBD`, blank, or unchecked fields.
- original XLM-R MLM baseline is recorded.
- every Step 04 candidate has a completed run.
- `checkpoint_selection.md` names the selected checkpoint when the gate passes.

Exit criteria:

- original XLM-R MLM baseline is recorded: pass
- every required candidate has a completed or explicitly failed run: pass
- at least one adapted checkpoint improves over zero-step loss and passes tokenization gate: pass
- checkpoint selection names selected checkpoint: pass
- `results.md` has `Gate status: PASS`: pass

## Failure Return

Failed gate: NOT_APPLICABLE

Observed evidence: NOT_APPLICABLE

Return-to step: NOT_APPLICABLE

Required fix: NOT_APPLICABLE
