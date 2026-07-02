# Branch Plan

Post-audit constraint: Step 09 supersedes the original merge criterion. A branch can only support a top-tier translation claim if the high-resource reference and target score use the same retrieval or generation method.

1. Add a trainable lightweight decoder or reranker for target verse retrieval.
2. Use train/dev splits only for tuning retrieval/reranking.
3. Re-evaluate on held-out John test verses.
4. Merge branch only if target chrF++ ratio >= 0.80 and copy/script checks pass.
5. Retry with pretrained multilingual sentence embeddings: select model/pair/scoring on dev, then evaluate that exact setting once on held-out John test.
