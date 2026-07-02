# Plan: Embedding Initialization

Status: random and mean smoke complete

## Goal

Compare initialization strategies for newly added target10 subword embeddings.

## Primary Novelty

Span-aware or corpus-aware initialization may be more stable than random initialization under limited multilingual target10 data.

## Conditions

- Random: initialize new embeddings randomly.
- Mean: tokenize each new token with the old tokenizer and average old subtoken embeddings.
- Align: use character-span alignment between old and new tokenizer outputs over corpus occurrences, then aggregate old embeddings into new token embeddings.

## Planned Work

1. Implement Random initialization baseline.
2. Implement Mean initialization.
3. Verify embedding matrix and LM head resizing.
4. Run identical short adaptation jobs for each condition.
5. Compare early loss curves and validation loss.
6. Implement Align initialization if schedule allows.

## Metrics

- initial embedding norm distribution
- training loss curve
- validation MLM loss
- pseudo-perplexity if implemented
- downstream BLEU and chrF++ after NMT baseline

## Outputs

- `results.md`
- `embedding_init_metrics.tsv`
- initialized checkpoints under `data/processed/target10/initialized_models/`
- MLM smoke outputs in `../2026-06-03_05_mlm_adaptation/`

## Success Gate

This phase passes when at least Random vs Mean is compared under identical data and training settings.

## Stretch Gate

A stronger paper result requires Random vs Mean vs Align.

## Decision Rule

If Align is not better than Mean, report Mean as the practical recommendation and discuss Align as not worth the extra complexity for this corpus scale.
