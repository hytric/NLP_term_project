# Step 14 Plan: V2 Embedding Initialization

## Goal

Execute `V2_02_INIT`: initialize the Step 13 selected 32k tokenizer with all required methods and choose the initialization method using Mark/dev MLM loss only.

## Inputs

- Selected tokenizer: `docs/exp/second_try/13_v2_tokenizer/selected_tokenizer.md`
- Dev manifest: `docs/exp/second_try/12_v2_split_protocol/v2_dev_manifest.tsv`
- Base model: `xlm-roberta-base`
- Forbidden for this step: `ACT` final manifest/text and any Step07/09/Branch001 test outputs.

## Methods

- `random`
- `mean`
- `fvt`
- `align`
- `focus`

## Required Outputs

- `results.md`
- `score_table.tsv`
- `v2_embedding_init_scores.tsv`
- `v2_zero_step_mlm.tsv`
- `v2_nearest_neighbors.md`
- `v2_no_final_access_audit.tsv`
- `selected_init.md`
- `file_results.tsv`

Large initialized checkpoints go under `/home/axt/mnt2/jongha/second_try/checkpoints/14_v2_embedding_init/`.

## Exit Criteria

- Every required method loads and writes a checkpoint.
- Input embedding and LM head sizes match the Step 13 tokenizer length.
- Weight tying is preserved.
- No initialized row is NaN or zero-norm.
- Full Mark/dev zero-step MLM loss is recorded for every method.
- The selected method is chosen by Mark/dev loss only.
- No `ACT` final file is read.
- No `score_table.tsv` cell is blank or `TBD`.

## Failure Return

If any required method fails, return to Step 13 or fix the initialization method before running MLM adaptation.
