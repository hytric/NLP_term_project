# Step 12 V2 Rerun Protocol

Run id: `step12_v2_split_20260611_153114`

## Locked V2 Split

| Role | Book | Rows |
| --- | --- | ---: |
| train | all except `MAR`, `JOH`, `ACT` | 52124 |
| dev | `MAR` | 6521 |
| burned_excluded | `JOH` | 8520 |
| final_test_clean | `ACT` minus exact train/dev text duplicates | 9804 |

Exact duplicate final rows excluded from scoring: `3`.

Minimum clean final rows per target language: `852`.

## Required Rerun

1. Rerun tokenizer training and merge using only `v2_tokenizer_mlm_train.txt`.
2. Rerun embedding initialization and MLM adaptation from the base model under the v2 split.
3. Rerun downstream proxy tasks, using Mark/dev for selection and ACT/final only once if final reporting is required.
4. Rerun method-matched translation with dev-only model/pair/scoring selection.
5. Report ACT final test once, after all settings are frozen.

Detailed stage gates are in `v2_execution_matrix.tsv`.

## Invalid For V2 Final Claims

- Step 05 checkpoint `spm32000_fvt_seed13`
- Step 06 downstream proxy scores
- Step 07 translation rows
- Branch 001 translation rows
- Step 09 method-matched rows

These artifacts remain useful as exploratory evidence but cannot support the v2 top-tier final claim because their training, selection, or evaluation touched the old split.
