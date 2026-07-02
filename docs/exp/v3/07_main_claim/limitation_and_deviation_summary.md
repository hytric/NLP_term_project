# Stage 07 Limitation And Deviation Summary

작성일: 2026-06-13

## Protocol Deviations

1. Training scale is a 200-step pilot plus a lower-LR 1000-step replay-safe retry, not full continued pretraining.
2. Effective batch size is 32 sequences per optimizer step, not the Glot500-scale 384 samples per step.
3. The mixture is pre-materialized rather than sampled online with the original Glot500 sampler.
4. FVT is the only init method trained through the Stage 05 pilot/retry; other init methods are compared at zero-step only.
5. High-resource evaluation is an MLM proxy on held-out Bible control text, not a complete high-resource downstream suite.
6. Target10 supervised downstream coverage is sparse; only Coptic POS is locally confirmed and run.

## Interpretation Limits

These deviations do not invalidate the diagnostic result, but they narrow its scope. The current evidence can say that this compute-bounded candidate failed to turn tokenizer gains into broad model gains. It cannot say that every full-budget Glot500-style XLM-R vocabulary extension would fail.

## Required Final Framing

The report should present the result as:

> In a compute-bounded Glot500-style XLM-R vocabulary-extension pilot/retry, average target10 tokenization improved, but model-level evidence remained mixed or negative and high-resource control degraded. The result motivates ablations over vocab size, init, fallback, replay, and appended-token learning.
