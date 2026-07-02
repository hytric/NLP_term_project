# Plan: Tokenization Audit

Status: initial baseline audit complete

## Goal

Quantify how badly existing multilingual tokenizers fragment the 10-language low-resource pilot set, with Coptic/Syriac retained as the main downstream translation case.

## Hypothesis

Existing Glot500/XLM-R/NLLB tokenizers tokenize several target10 languages into overly short, character-level, or unknown-token units. A joint target10 unigram tokenizer should reduce fragmentation.

## Tokenizers To Compare

- XLM-R tokenizer
- Glot500-m tokenizer
- NLLB tokenizer
- newly trained joint target10 SentencePiece unigram tokenizer

## Planned Work

1. Build a tokenizer audit script.
2. Run audit on held-out-safe target10 samples.
3. Save tokenized examples for manual inspection.
4. Compute fragmentation metrics.
5. Produce a paper-ready table.

## Metrics

- average characters per sentence
- average tokens per sentence
- character/token fertility
- percentage of single-character tokens
- percentage of target-script characters covered by meaningful subwords
- sequence length reduction after new tokenizer
- examples of severe overfragmentation

## Outputs

- `tokenization_audit.py`
- `tokenization_metrics.tsv`
- `tokenization_examples.md`
- `fig_token_length_distribution.png`

## Success Gate

This phase passes when the project can answer:

- Which target10 languages fragment most severely?
- Which baseline tokenizer is worst?
- How much does a new tokenizer reduce sequence length?

## Decision Rule

If tokenization is not badly fragmented, the project should shift novelty away from vocabulary extension and toward data/pivot training. If fragmentation is severe, continue to vocabulary extension.
