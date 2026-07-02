# Step 01 Plan: Data And Splits

## Goal

Create leakage-safe target10 data files for tokenizer training, MLM adaptation, downstream tasks, and manual samples.

## Inputs

- Step 00 `Gate status: PASS`
- target language decision from `../00_scope_and_references/scope_decisions.tsv`

## Required Work

1. Build target language inventory.
2. Build verse-level corpus table.
3. Apply default split:
    - train: all books except Mark and John
    - dev: Mark
    - test: John
4. Create tokenizer train file from train split only.
5. Create MLM train/dev files without test leakage.
6. Create downstream source tables with explicit split column.
7. Create manual sample manifest: 10 examples per language plus 10 failure candidates.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `target_languages.tsv`
- `target10_bible_verses.tsv`
- `split_stats.tsv`
- `tokenizer_train_manifest.tsv`
- `mlm_manifest.tsv`
- `downstream_manifest.tsv`
- `sample_manifest.tsv`
- `file_results.tsv`

## Score Table Contract

All counts in `score_table.tsv` must be filled. No language row may have unknown train/dev/test counts.

## Exit Criteria

- Every target language has train/dev/test counts.
- No test row appears in tokenizer train or MLM train/dev manifests.
- Sample manifest has at least 10 rows per language plus 10 failure candidates.
- `file_results.tsv` records every generated file with path, count or size, and status.
- `results.md` has `Gate status: PASS`.

## Failure Return

If leakage or missing languages are found, stay in Step 01 and rebuild the manifests. If target language decisions are wrong, return to Step 00.
