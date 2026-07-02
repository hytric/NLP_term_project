# Step 18 Plan: V2 Added-Token-Focused Repair

## Goal

Test whether the Step 17 failure mode can be repaired by changing the training objective rather than only extending the same MLM budget. This step trains the Step 14 selected adapted checkpoint with an added-token-focused MLM objective and compares the result against Step 15/17 regular adapted baselines.

## Inputs

| Role | Path | Split Policy |
| --- | --- | --- |
| selected Step 14 init | `docs/exp/second_try/14_v2_embedding_init/selected_init.md` | selected on Mark/dev only |
| v2 train text | `/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_tokenizer_mlm_train.txt` | train only |
| v2 Mark/dev manifest | `docs/exp/second_try/12_v2_split_protocol/v2_dev_manifest.tsv` | dev only |
| Step 17 category baseline | `docs/exp/second_try/17_v2_added_token_failure_analysis/token_category_loss.tsv` | dev diagnostic metadata |

`ACT` clean final must not be read in this step.

## Repair Objective

- base-token mask probability: `0.15`
- added-token mask probability: `0.30`
- base-token loss weight: `1.0`
- added-token loss weight: `3.0`
- target train-token budget: `500000`
- seeds: `13,17,23`

Evaluation remains unweighted standard MLM on Mark/dev so that results are comparable to Steps 15-17.

## Required Outputs

| File | Required Content |
| --- | --- |
| `score_table.tsv` | artifact and repair gates |
| `repair_summary.tsv` | per-seed training result and comparison against Step 17 baseline |
| `repair_category_loss.tsv` | all/base/added dev loss after repair |
| `repair_learning_curves.tsv` | zero and final dev category loss |
| `checkpoint_selection.md` | selected repaired checkpoint |
| `v2_no_final_access_audit.tsv` | input access audit with `final_access=NO` |
| `file_results.tsv` | path/count/size/checksum evidence |
| `results.md` | interpretation and next return path |

## Exit Criteria

Artifact gate passes if all three repaired seeds finish, checkpoints are saved, and no ACT final file is read.

Repair gate passes if added-token mean loss improves over the Step 17 regular adapted baseline in all three seeds without increasing all-token dev loss. This is still not a final positive model claim; it only allows a rerun of Step 15 control with the repaired method.

