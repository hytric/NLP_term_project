# Step 15 Plan: V2 MLM Control

## Goal

Run the first model-dependent v2 control after the fresh split. This step trains the selected Step 14 adapted checkpoint and an original `xlm-roberta-base` continued-pretraining control on the same v2 train text, using Mark/dev only for evaluation and checkpoint selection.

## Inputs

| Role | Path | Split Policy |
| --- | --- | --- |
| selected adapted init | `docs/exp/second_try/14_v2_embedding_init/selected_init.md` | selected on Mark/dev only |
| v2 MLM train text | `/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_tokenizer_mlm_train.txt` | train only |
| v2 MLM dev text | `/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_mlm_dev_mark.txt` | Mark/dev only |
| original control | `xlm-roberta-base` | no v2 final access |

`ACT` clean final must not be read in this step.

## Work

1. Train `adapted_extended` from the Step 14 selected checkpoint.
2. Train `original_control` from unmodified `xlm-roberta-base`.
3. Use at least three seeds for both families.
4. Use the same raw text order, batch size, max length, optimizer, learning rate, evaluation schedule, and matched train-token budget for both families.
5. Record zero-step and post-training Mark/dev MLM loss for every seed.
6. Save per-seed checkpoints and per-run configs.
7. Select checkpoints using Mark/dev only.

## Required Outputs

| File | Required Content |
| --- | --- |
| `score_table.tsv` | step gate rows with observed value, required value, status, and return target |
| `seed_summary.tsv` | every family/seed run with zero-step loss, final loss, delta, runtime, checkpoint path |
| `mlm_learning_curves.tsv` | zero-step and scheduled dev evaluations for every family/seed |
| `checkpoint_selection.md` | selected adapted checkpoint and original-control checkpoint |
| `v2_no_final_access_audit.tsv` | every input used by this step and `final_access=NO` |
| `training_configs/` | common config plus one JSON config per family/seed |
| `results.md` | artifact gate, claim gate, failure return, and next-step instruction |
| `file_results.tsv` | path, row/file count, size, checksum/status for every output |

## Exit Criteria

Artifact gate passes only if:

- all six required runs complete: 2 model families x 3 seeds.
- all six runs meet the configured train-token target within the configured tolerance.
- every required output file exists and is listed in `file_results.tsv`.
- `score_table.tsv`, `seed_summary.tsv`, and `mlm_learning_curves.tsv` contain no blank, `TBD`, or `NA_NOT_CHECKED` cells.
- `v2_no_final_access_audit.tsv` lists no `ACT` final input.

Claim gate passes only if:

- the adapted checkpoint improves over its own zero-step loss in all seeds.
- the original continued-pretraining control completes in all seeds.
- the adapted mean final Mark/dev loss is within the configured competitive margin against the original-control mean final Mark/dev loss.

Because the two families use different tokenizers, the original-control MLM loss comparison is treated as a diagnostic control, not standalone downstream proof. Downstream and translation claims still require Steps 16 and 17.

## Failure Return

| Failed Gate | Return To | Required Fix |
| --- | --- | --- |
| adapted does not improve over zero-step | `14_v2_embedding_init` or this step with longer budget | change initialization/training budget and rerun Step 15 |
| original control missing | this step | rerun missing control seed before any downstream comparison |
| adapted not competitive with original control | this step, then `14_v2_embedding_init` if repeated | increase training budget or revise the claim to a negative result |
| final data accessed | `12_v2_split_protocol` | reset contaminated run and rerun from clean train/dev inputs |
