# Step 03 Results: Vocabulary Extension

Status: COMPLETED

Run id: step03_vocab_20260610_225407

Completed date: 2026-06-10

Gate status: PASS

## Required Artifact Check

| Artifact | Path | Present? | Notes |
| --- | --- | --- | --- |
| score table | `score_table.tsv` | yes | 8k/16k/32k rows filled |
| file results | `file_results.tsv` | yes | per-output file status recorded |
| merge report | `vocab_merge_report.tsv` | yes | special id and round-trip evidence |
| tokenization metrics | `extended_tokenization_metrics.tsv` | yes | per-vocab per-language metrics |
| examples | `tokenization_examples.md` | yes | before/after previews for selected candidate |
| tokenizer artifacts | `/home/axt/mnt2/jongha/second_try/artifacts/03_vocab_extension` | yes | SPM models and saved HF tokenizers |

## Summary

Step 03 trained target10 SentencePiece unigram models at 8k, 16k, and 32k using the Step 01 train-only tokenizer corpus. Directly appending pieces inside XLM-R's SentencePiece model would move `<mask>`, so the merge used HuggingFace added tokens derived from target SPM pieces. This keeps original XLM-R ids intact while appending new target tokens after the original tokenizer vocabulary.

| Metric | Value |
| --- | --- |
| base model | `xlm-roberta-base` |
| train corpus | `/home/axt/mnt2/jongha/second_try/artifacts/01_data_and_splits/tokenizer/target10_train_all.txt` |
| selected candidate | `32000` |
| best avg tokens/word delta pct | -31.766 |
| best avg single-char delta pct | -42.365 |
| structurally valid candidates | 3 |
| full metric-pass candidates | 3 |

## Candidate Selection

Selected candidate: `32000`.

Candidates pass only if special ids are preserved, round-trip failures do not exceed the original XLM-R baseline, average tokens/word drops by at least 10%, single-character rate drops by at least 10% for languages that had baseline single-character bottlenecks, and `<unk>`/degenerate counts do not increase. Detailed candidate rows are in `score_table.tsv`.

## Gate Evidence

Evidence:

- `score_table.tsv` has no `TBD`, blank, or unchecked fields.
- `vocab_merge_report.tsv` records special ids before/after and round-trip failures.
- `extended_tokenization_metrics.tsv` compares every candidate against the Step 02 baseline.
- `file_results.tsv` records docs outputs plus large SPM/tokenizer artifact directories.

Exit criteria:

- all three vocab sizes trained or explicit failure recorded: pass
- at least one extended tokenizer preserves special ids and passes round-trip checks: pass
- at least one candidate meets tokenization reduction target: pass
- `results.md` has `Gate status: PASS`: pass

## Failure Return

Failed gate: NOT_APPLICABLE

Observed evidence: NOT_APPLICABLE

Return-to step: NOT_APPLICABLE

Required fix: NOT_APPLICABLE
