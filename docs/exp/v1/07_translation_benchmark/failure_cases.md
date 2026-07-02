# Step 07 Failure And Exploratory Branch Cases

Gate status: `FAIL`
Branch id: `branch_001_translation_retrieval_gap`

The original adapted-encoder retrieval row failed and produced the misses below. Branch 001 later produced a strong exploratory LaBSE+CSLS row, selected on dev and evaluated on held-out John test. Step 09 supersedes this as a top-tier pass because the branch used a mixed-method high-resource comparison.

Exploratory branch row:

- run id: `branch001_sentence_embedding_20260610_234706`
- model/scoring: `sentence-transformers/LaBSE` / `csls`
- pair: `kbh->nhg`
- test chrF++: `64.434500`
- required chrF++: `49.567925`
- ratio: `1.039939`
- Step 09 method-matched LaBSE+CSLS ratio: `0.567179`

Original misses:

- b.JOH.1.1 retrieved b.JOH.1.36
- b.JOH.1.2 retrieved b.JOH.1.27
- b.JOH.1.3 retrieved b.JOH.1.51
- b.JOH.1.4 retrieved b.JOH.10.18
- b.JOH.1.5 retrieved b.JOH.1.47
- b.JOH.1.6 retrieved b.JOH.10.23
- b.JOH.1.8 retrieved b.JOH.1.47
- b.JOH.1.10 retrieved b.JOH.1.51
- b.JOH.1.11 retrieved b.JOH.11.21
- b.JOH.1.12 retrieved b.JOH.11.21
- b.JOH.1.13 retrieved b.JOH.10.38
- b.JOH.1.15 retrieved b.JOH.10.38
- b.JOH.1.16 retrieved b.JOH.1.27
- b.JOH.1.17 retrieved b.JOH.1.51
- b.JOH.1.18 retrieved b.JOH.1.48
- b.JOH.1.19 retrieved b.JOH.10.41
- b.JOH.1.20 retrieved b.JOH.10.41
- b.JOH.1.22 retrieved b.JOH.1.48
- b.JOH.1.23 retrieved b.JOH.10.41
- b.JOH.1.24 retrieved b.JOH.10.41
