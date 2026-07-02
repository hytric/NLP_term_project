# Step 02 Plan: Baseline Tokenization Audit

## Goal

Measure the original XLM-R tokenizer bottleneck on target10 before any vocabulary extension.

## Inputs

- Step 01 `Gate status: PASS`
- Step 01 data manifests
- Original `xlm-roberta-base` tokenizer

## Required Work

1. Tokenize held-out-safe samples with original XLM-R.
2. Compute fertility and fragmentation metrics per language.
3. Detect `<unk>`, blank, degenerate, and character-level behavior.
4. Produce manual before-extension examples.
5. Decide whether tokenization bottleneck is strong enough to justify extension.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `xlmr_baseline_tokenization_metrics.tsv`
- `tokenization_examples.md`
- `failure_candidates.tsv`
- `file_results.tsv`

## Score Table Contract

Every metric cell must be filled for every language. If a metric does not apply, write `NOT_APPLICABLE` and explain in `results.md`.

## Exit Criteria

- Per-language tokenization metrics are complete.
- At least one bottleneck type is quantified: high tokens/word, high single-char rate, `<unk>`, blank/degenerate encoding.
- `failure_candidates.tsv` contains examples for manual inspection.
- `file_results.tsv` records every generated file with path, count or size, and status.
- `results.md` has `Gate status: PASS`.

## Failure Return

If target data is malformed, return to Step 01. If no bottleneck is found, do not skip the finding; mark the gate as `PASS_WITH_WEAK_BOTTLENECK` only if the project will shift claims toward representation adaptation.
