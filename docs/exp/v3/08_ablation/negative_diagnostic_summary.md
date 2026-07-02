# Stage 08 Negative Diagnostic Summary

작성일: 2026-06-13

## Diagnostic Chain

The current evidence supports the following failure chain:

1. Append-only vocabulary extension is structurally valid and reduces average target10 fragmentation.
2. Better fragmentation does not guarantee lower MLM loss for the extended model.
3. Appended-token learning is a major failure mode: second_try shows added-token loss dominates adapted-model loss, and third_try replay-safe target10 MLM proxy remains worse than XLM-R-base on average.
4. High-resource replay is necessary in the design, but the current replay mixture does not yet prevent high-resource control degradation; the lower-LR 1000-step retry reduces the delta but still fails `0/4` control languages.
5. Coptic POS token accuracy shows a weak supervised gain, but macro F1 is negative and this is not broad enough to support target10 downstream success, especially with Syriac still proxy-only.
6. Byte fallback slightly improves tokenizer metrics, but the current append-only XLM-R tokenizer cannot directly execute SentencePiece byte fallback behavior.

## Main Explanation

The most likely explanation is not that tokenizer extension is useless. It is that the current extension creates many new prediction targets whose embeddings and MLM head rows are not learned well enough under the available budget and replay schedule. Vocab size, initialization, fallback behavior, and replay ratio all affect this pressure, but none of the current branches clears the positive model-quality gates.

## Reusable Negative Claim

> Vocabulary extension reduced target10 tokenization fragmentation, and a replay-safe retry improved the short pilot, but the current compute-bounded XLM-R append-only continued-pretraining candidate still did not convert that tokenizer gain into broad target10 model gains. The failure concentrates around appended-token learning, replay/control degradation, and sparse downstream coverage.
