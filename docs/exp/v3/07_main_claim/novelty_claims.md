# Stage 07 Novelty Claims

작성일: 2026-06-13

## Safe Novelty

The safe novelty is methodological rather than positive-performance-oriented:

1. Reframes the project around Glot500-style continued pretraining from XLM-R-base instead of a standalone tokenizer-only result.
2. Uses append-only vocabulary extension to preserve all original XLM-R token ids.
3. Separates tokenizer gains from downstream claims, preventing a common overclaim.
4. Adds an explicit byte-fallback vs character-coverage tokenizer ablation.
5. Converts earlier first_try and second_try experiments into ablation/failure-analysis evidence rather than competing main experiments.

## Unsafe Novelty

Do not claim a new state of the art, a final improved XLM-R variant, or a successful Glot500 reproduction from the current evidence.
