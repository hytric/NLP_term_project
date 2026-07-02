# Plan: Pivot And Backtranslation

Status: Greek pivot gate complete; back-translation scale-up not recommended yet

## Goal

Use Greek/English pivot paths and monolingual Coptic/Syriac data to improve translation beyond direct-only training.

## Hypothesis

Because direct Coptic-Syriac data is scarce, auxiliary pivot pairs and back-translated synthetic pairs will improve chrF++ more than direct fine-tuning alone.

## Conditions

- direct-only
- direct + Greek pivot pairs
- direct + English pivot pairs
- direct + Greek/English multitask
- back-translation round 1
- back-translation round 2 if quality improves
- optional pivot-consistency filtering

## Planned Work

1. Train or use pivot translation paths.
2. Generate synthetic Coptic-Syriac pairs from monolingual Coptic.
3. Generate synthetic Syriac-Coptic pairs from monolingual Syriac.
4. Filter low-quality synthetic pairs.
5. Retrain NMT with synthetic data.
6. Compare against baseline.

## Metrics

- BLEU
- chrF++
- synthetic pair count
- synthetic length ratio
- round-by-round improvement
- qualitative adequacy and hallucination checks

## Outputs

- `synthetic_data_manifest.tsv`
- `backtranslation_results.tsv`
- `pivot_consistency.md`
- `bt_qualitative_examples.md`

## Success Gate

This phase passes when at least one synthetic-data condition is compared against a non-synthetic baseline.

## Decision Rule

If synthetic outputs are visibly poor, stop after round 1 and report back-translation failure modes rather than compounding noise.
