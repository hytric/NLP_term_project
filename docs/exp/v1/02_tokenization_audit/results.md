# Step 02 Results: Baseline Tokenization Audit

Status: COMPLETED

Run id: step02_audit_20260610_224617

Completed date: 2026-06-10

Gate status: PASS

## Required Artifact Check

| Artifact | Path | Present? | Notes |
| --- | --- | --- | --- |
| score table | `score_table.tsv` | yes | 10 language rows filled |
| file results | `file_results.tsv` | yes | per-output file status recorded |
| tokenization metrics | `xlmr_baseline_tokenization_metrics.tsv` | yes | XLM-R baseline metrics |
| examples | `tokenization_examples.md` | yes | 3 examples per language |
| failure candidates | `failure_candidates.tsv` | yes | 50 candidate rows |

## Summary

Step 02 audited `xlm-roberta-base` with `use_fast=False` on the Step 01 train split only, capped at 500 rows per language. Test rows were not used.

| Metric | Value |
| --- | --- |
| languages audited | 10 |
| split used | `train` |
| max tokens_per_word | 4.854 |
| max single_char_token_pct | 74.251 |
| languages with strong bottleneck tag | 10 |

## Bottleneck Finding

The baseline tokenizer shows quantifiable fragmentation when `tokens_per_word >= 2.0` or `single_char_token_pct >= 25.0`. The strongest cases are visible in `score_table.tsv` and manually inspectable in `tokenization_examples.md`.

## Gate Evidence

Evidence:

- `score_table.tsv` has no `TBD`, blank, or unchecked fields.
- `xlmr_baseline_tokenization_metrics.tsv` has complete metrics for all 10 languages.
- `failure_candidates.tsv` contains 5 high-fragmentation examples per language.
- `tokenization_examples.md` includes human-readable before-extension token previews.

Exit criteria:

- per-language tokenization metrics are complete: pass
- at least one bottleneck type is quantified: pass
- failure candidates exist for manual inspection: pass
- `results.md` has gate status allowing next step: pass

## Failure Return

Failed gate: NOT_APPLICABLE

Observed evidence: NOT_APPLICABLE

Return-to step: NOT_APPLICABLE

Required fix: NOT_APPLICABLE
