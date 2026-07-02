# Step 01 Results: Data And Splits

Status: COMPLETED

Run id: step01_data_20260610_224337

Completed date: 2026-06-10

Gate status: PASS

## Required Artifact Check

| Artifact | Path | Present? | Notes |
| --- | --- | --- | --- |
| score table | `score_table.tsv` | yes | 10 language rows filled; no TBD values |
| file results | `file_results.tsv` | yes | per-output file status recorded |
| target languages | `target_languages.tsv` | yes | 10 target languages |
| verse table | `target10_bible_verses.tsv` | yes | 76972 verse rows |
| split stats | `split_stats.tsv` | yes | train/dev/test counts per language |
| tokenizer manifest | `tokenizer_train_manifest.tsv` | yes | train-only tokenizer data |
| MLM manifest | `mlm_manifest.tsv` | yes | train/dev only; test excluded |
| downstream manifest | `downstream_manifest.tsv` | yes | train/dev/test source table path |
| sample manifest | `sample_manifest.tsv` | yes | 110 rows including 10 failure candidates |

## Summary

Step 01 rebuilt target10 data from raw Bible XML files only. Outputs in this docs folder are the authoritative small TSV evidence. Larger train/dev/source files were written under `/home/axt/mnt2/jongha/second_try/artifacts/01_data_and_splits`.

Totals:

| Metric | Value |
| --- | --- |
| target languages | 10 |
| total verse rows | 76972 |
| train rows | 61931 |
| dev rows | 6521 |
| test rows | 8520 |
| shared verse overlap across all 10 | 4892 |

## Leakage Check

| Check | Result |
| --- | --- |
| tokenizer train uses train split only | PASS |
| MLM train uses train split only | PASS |
| MLM dev uses dev split only | PASS |
| test split excluded from tokenizer and MLM manifests | PASS |
| every language has non-zero train/dev/test rows | PASS |

## Gate Evidence

Evidence:

- `score_table.tsv` has no `TBD`, blank, or unchecked fields.
- `file_results.tsv` records all generated docs and large artifact files with row/line count, bytes, md5, and status.
- `target10_bible_verses.tsv` includes explicit `split`, `book`, `chapter`, and `verse_id`.
- `tokenizer_train_manifest.tsv` and `mlm_manifest.tsv` report `test_rows_included=0`.
- `sample_manifest.tsv` has 10 regular train samples per language plus 1 long-train failure candidate per language.

Exit criteria:

- every target language has train/dev/test counts: pass
- no test row appears in tokenizer train or MLM train/dev manifests: pass
- sample manifest has at least 10 rows per language plus 10 failure candidates: pass
- `results.md` has `Gate status: PASS`: pass

## Failure Return

Failed gate: NOT_APPLICABLE

Observed evidence: NOT_APPLICABLE

Return-to step: NOT_APPLICABLE

Required fix: NOT_APPLICABLE
