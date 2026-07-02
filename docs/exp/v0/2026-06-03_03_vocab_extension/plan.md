# Plan: Vocabulary Extension

Status: target10 tokenizer trained and merged

## Goal

Train and validate a joint 10-language low-resource subword vocabulary, then merge genuinely new tokens into a Glot500-compatible tokenizer.

## Hypothesis

Joint 10-language vocabulary extension reduces sequence length and single-character fragmentation without excessively increasing vocabulary size.

## Conditions

- No extension baseline
- per-script or per-language extension, if needed
- joint 10-language extension
- optional: joint extension with Greek/English anchor text

## Planned Work

1. Train SentencePiece unigram tokenizer on target corpus.
2. Try vocab sizes such as 8K, 16K, and 32K if data allows.
3. Merge new tokens with Glot500 tokenizer.
4. Count genuinely new tokens.
5. Re-run tokenization audit after merge.
6. Save tokenizer artifacts with exact command lines.

## Metrics

- new token count
- overlap with original vocabulary
- average tokens per sentence
- single-character token ratio
- target-script token coverage
- tokenizer model size

## Outputs

- `train_tokenizer.sh`
- `merge_vocab.md`
- `tokenizer_config.json`
- `vocab_extension_metrics.tsv`
- `extended_tokenizer/`

## Success Gate

This phase passes when:

- an extended tokenizer can encode/decode all target10 languages
- tokenization metrics improve over Glot500 baseline
- tokenizer artifacts and commands are reproducible

## Decision Rule

Use the smallest vocabulary size that gives strong fragmentation reduction. If per-language or per-script variants are not clearly better than joint target10 extension, use joint extension for later experiments.
