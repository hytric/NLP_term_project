# Stage 07 Blocked Claims

작성일: 2026-06-13

## Blocked

1. "The final model improves target10 downstream performance over XLM-R-base."

Blocked because target10 downstream seed stability is `NOT_RUN`, only Coptic has a local supervised task, and frozen proxy evidence is mixed.

2. "The model improves Coptic and Syriac downstream performance."

Blocked because Coptic POS is weakly positive but Syriac has no fresh supervised downstream run in the current encoder-only protocol.

3. "High-resource replay prevents high-resource degradation."

Blocked because the replay-safe high-resource control MLM proxy still worsens by `+0.675539` mean loss and `0/4` control languages pass the no-large-collapse threshold.

4. "Tokenizer fragmentation reduction is sufficient for downstream gains."

Blocked because target10 MLM proxy is worse than XLM-R-base on average and downstream/proxy evidence is mixed.

5. "Byte fallback should replace the main tokenizer."

Blocked because byte fallback is only measured as a tokenizer ablation here; SentencePiece BYTE pieces are not faithfully activated by the current append-only XLM-R `add_tokens` mechanism.

6. "The experiment fully follows Glot500 training scale."

Blocked because Stage 05 is a compute-bounded 200-step pilot plus 1000-step replay-safe retry with effective batch 32 and a materialized mixture, not a full-budget Glot500 continued-pretraining run.
