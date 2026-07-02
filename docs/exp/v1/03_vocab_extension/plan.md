# Step 03 Plan: Vocabulary Extension

## Goal

Train target10 SentencePiece unigram tokenizers at 8k, 16k, and 32k, merge each into XLM-R by appending new pieces, and select valid tokenizer candidates.

## Inputs

- Step 02 `Gate status: PASS`
- Step 01 tokenizer train manifest
- Original XLM-R tokenizer

## Required Work

1. Train target10 unigram tokenizers: 8k, 16k, 32k.
2. Merge each tokenizer into original XLM-R while preserving original ids.
3. Verify special token ids are unchanged.
4. Verify encode/decode round-trip on samples.
5. Rerun tokenization audit for each extended tokenizer.
6. Compare against Step 02 baseline.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `vocab_merge_report.tsv`
- `extended_tokenization_metrics.tsv`
- `tokenization_examples.md`
- `file_results.tsv`
- tokenizer artifacts for 8k, 16k, 32k

## Score Table Contract

Every vocab size row must include added token count, overlap count, round-trip status, special-id status, and metric deltas. No `TBD` is allowed before exit.

## Exit Criteria

- All three vocab sizes are trained or an explicit failure reason is written.
- At least one extended tokenizer preserves special ids and passes round-trip checks.
- Prefer at least 10% tokens/word reduction and 10% single-char reduction without increasing `<unk>`/degenerate cases.
- `file_results.tsv` records every generated file with path, count or size, and status.
- `results.md` has `Gate status: PASS`.

## Failure Return

If merge breaks ids or round-trip, stay in Step 03. If training data is insufficient, return to Step 01. If no vocab size improves tokenization, return to Step 02 to re-evaluate the bottleneck claim.
