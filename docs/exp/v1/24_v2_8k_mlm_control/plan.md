# Step 24 Plan: V2 8k MLM Control And Normalized Audit

작성일: 2026-06-11

## Goal

Evaluate whether the Step23 selected 8k vocabulary branch is competitive with the original XLM-R continued-pretraining control under the Step15/16 control protocol.

## Inputs

- Step23 8k adapted checkpoints for seeds 13, 17, and 23.
- Step15 original-control checkpoints for seeds 13, 17, and 23.
- Step12 Mark/dev text only.
- Step23 and Step15 train-token summaries.

## Work

1. Build a formal 8k-vs-original raw control table from existing matched-budget runs.
2. Re-evaluate all six checkpoints on Mark/dev with the Step16 normalized MLM diagnostic.
3. Compare raw masked-token loss, estimated NLL per word, and estimated NLL per character.
4. Select the best 8k checkpoint on Mark/dev only.
5. Do not read or inspect `ACT` final.

## Exit Criteria

- All 3 Step23 8k adapted checkpoints and all 3 Step15 original-control checkpoints exist.
- Train-token budget ratio is `<=1.020000`.
- Raw adapted/original ratio is recorded.
- Word- and character-normalized adapted/original ratios are recorded.
- Positive model-dependent claim gate passes only if both normalized ratios are `<=1.100000`.
- `score_table.tsv`, `raw_control_summary.tsv`, `normalized_mlm_scores.tsv`, `checkpoint_selection.md`, `v2_no_final_access_audit.tsv`, `results.md`, and `file_results.tsv` are complete.

## Failure Return

If the claim gate fails:

- Do not run positive downstream or translation final readout.
- Either redesign objective/data beyond the 8k branch, or downgrade the model-dependent claim.

If the claim gate passes:

- Proceed to v2 downstream hard-negative evaluation and method-matched translation, with `ACT` final read exactly once after all decisions are frozen.
