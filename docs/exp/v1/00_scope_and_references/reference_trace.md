# Step 00 Reference Trace

작성일: 2026-06-10

## Source Documents

| Decision Area | Source |
| --- | --- |
| Glot500-style append vocabulary extension | `../reference_summaries/2305.12182v2_glot500.md`, `../reference_summaries/glot500_extension_tutorial.md` |
| Low-resource vocab expansion gates | `../reference_summaries/2406.11477v3_low_resource_vocab_expansion.md` |
| Embedding initialization methods | `../reference_summaries/vocab_extension_tutorial.md` |
| SentencePiece unigram tokenizer | `../reference_summaries/unigram_lm.md`, `../reference_summaries/bpe_wordpiece.md` |
| Reporting and leakage discipline | `../reference_summaries/term_project_guideline.md` |
| Encoder-only downstream task design | `../downstream_tasks.md` |
| Sequential execution and failure branch rules | `../execution_rules.md`, `../step_index.md` |

## Trace Summary

- XLM-R is kept as the base model because second_try is explicitly framed as Glot500-style adaptation on `xlm-roberta-base`.
- Vocabulary extension must preserve original XLM-R token ids and append new target pieces.
- SentencePiece must be run in unigram mode.
- Vocab sizes are fixed to 8k, 16k, and 32k.
- Required embedding initialization methods are random, mean, fvt, align, and focus.
- Downstream final tasks are book/genre classification, verse retrieval/ranking, and parallel verse matching.
- Language identification is diagnostic only.
- Translation is reintroduced as Step 07 with a high-resource 80% reference target.
- Large checkpoints, manifests, logs, and branch artifacts must be stored in `/home/axt/mnt2/jongha/second_try`.
- Current GPU inventory exposes indices 0-3 only; because requested GPU 4 is unavailable, execution uses GPU 3 fallback.
