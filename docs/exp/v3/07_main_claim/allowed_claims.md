# Stage 07 Allowed Claims

작성일: 2026-06-13

## Allowed

1. The third_try tokenizer is an XLM-R-base append-only vocabulary extension that preserves existing XLM-R token ids and special-token ids.
2. The selected 48k target-heavy tokenizer reduces average target10 dev tokens/word by `-29.812358%`, while Cherokee and Ojibwa remain slightly worse and the average single-character-token ratio worsens.
3. The byte-fallback auxiliary tokenizer is slightly better than the character-coverage variant in tokenizer metrics, but it is ablation-only under the current XLM-R `add_tokens` implementation.
4. FVT initialization is the best zero-step MLM initialization among the tested random, mean, fvt, align, and focus variants.
5. The fvt MLM path runs successfully across checkpoint seeds 13, 17, and 23 for both the 200-step pilot and the lower-LR replay-safe 1000-step retry.
6. Replay-safe Coptic UD POS shows a narrow pilot improvement in token accuracy across 3/3 fvt checkpoint seeds, while macro-F1 worsens slightly on average.
7. Current evidence supports a diagnostic negative interpretation: tokenizer fragmentation improved on average, but this did not become a broad target10 downstream improvement and high-resource control degraded in the proxy.

## Required Wording

Use "pilot", "proxy", "current candidate", or "diagnostic" for all model-quality claims from Stage 05/06. Do not phrase the current result as a completed full-budget Glot500 reproduction.
