# Step 12 Plan: V2 Split Protocol

## Goal

Create a fresh-heldout v2 split that can unblock P0 follow-ups `F02` and `F03` without reusing the burned John test set.

## Split Rule

| Role | Book | Reason |
| --- | --- | --- |
| train | all books except `MAR`, `JOH`, `ACT` | train excludes dev, burned old test, and final test |
| dev | `MAR` | retained for model/pair/scoring selection |
| burned_excluded | `JOH` | old Step07/Branch001/Step09 test feedback, not usable for new final evidence |
| final_test | `ACT` | large fresh final heldout candidate with low exact duplicate risk |

Exact normalized final-test rows duplicated in train/dev must be excluded from final scoring.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `v2_candidate_books.tsv`
- `v2_split_stats.tsv`
- `v2_split_manifest.tsv`
- `v2_final_duplicate_exclusions.tsv`
- `v2_rerun_protocol.md`
- `file_results.tsv`

Large text artifacts are allowed under `/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/`.

## Exit Criteria

- `ACT` final test has at least 8,000 clean rows total and at least 800 clean rows for every target language.
- `JOH` is excluded from train/dev/final evidence.
- tokenizer/MLM train files contain no dev/final/burned rows.
- Existing Step05/06/07/09 checkpoints and translation results are marked invalid for v2 final claims.
- No `score_table.tsv` cell is blank or `TBD`.

## Failure Return

If the final-test candidate is too small or duplicate-heavy, return to `01_data_and_splits` and choose a different final held-out book or import an external corpus with provenance.
