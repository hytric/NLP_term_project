# Step 17 Plan: V2 Added-Token Failure Analysis

## Goal

Diagnose why the v2 adapted checkpoint fails the original-control MLM gate. This step decomposes Step 15 MLM loss into base-token and added-token losses under the adapted tokenizer, and reports language/script-level added-token usage.

## Inputs

| Role | Path | Split Policy |
| --- | --- | --- |
| Step 15 seed summary | `docs/exp/second_try/15_v2_mlm_control/seed_summary.tsv` | checkpoint metadata only |
| v2 Mark/dev manifest | `docs/exp/second_try/12_v2_split_protocol/v2_dev_manifest.tsv` | dev only |
| base tokenizer | `xlm-roberta-base` | metadata only |

`ACT` clean final must not be read in this step.

## Work

1. Evaluate every Step 15 final checkpoint on the same Mark/dev manifest.
2. For adapted checkpoints, split masked-token losses into original XLM-R token rows and added-token rows.
3. Report language/script-level added-token usage and loss.
4. Report the highest-loss added tokens across adapted seeds.
5. Decide whether the next repair should focus on added-token initialization/objective or on broader encoder degradation.

## Required Outputs

| File | Required Content |
| --- | --- |
| `score_table.tsv` | artifact and diagnostic gates |
| `token_category_loss.tsv` | all/base/added token loss by model family and seed |
| `language_token_breakdown.tsv` | per-language token counts, added-token usage, and category loss |
| `new_token_loss_samples.tsv` | highest-loss and most frequent added tokens under adapted checkpoints |
| `v2_no_final_access_audit.tsv` | input access audit with `final_access=NO` |
| `results.md` | interpretation and next repair target |
| `file_results.tsv` | path/count/size/checksum evidence |

## Exit Criteria

Artifact gate passes if every Step 15 checkpoint is evaluated and no final data is read.

Diagnostic gate passes if the step identifies whether added-token loss is materially higher than base-token loss. This is not a positive model claim; it only determines the next repair path.

