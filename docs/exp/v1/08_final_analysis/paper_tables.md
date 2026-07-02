# Step 08 Paper Tables

## Tokenization

| Source | Key result | Evidence file |
| --- | --- | --- |
| Original XLM-R | max `tokens_per_word=4.854`; max `single_char_token_pct=74.251` | `02_tokenization_audit/score_table.tsv` |
| Extended 32k tokenizer | `avg_tokens_per_word_delta_pct=-31.766`; `single_char_delta_pct=-42.365` | `03_vocab_extension/score_table.tsv` |

## Initialization And MLM

| Setup | Dev loss | Decision | Evidence file |
| --- | ---: | --- | --- |
| random zero-step | 20.809267 | weak initialization | `04_embedding_init/score_table.tsv` |
| fvt zero-step | 8.490678 | best initialization | `04_embedding_init/score_table.tsv` |
| fvt adapted 20 steps | 7.134023 | selected extended checkpoint | `05_mlm_adaptation/score_table.tsv` |
| original XLM-R | 6.330356 | original baseline remains lower | `05_mlm_adaptation/score_table.tsv` |

## Downstream Proxies

| Task | Original XLM-R | Selected adapted | Decision | Evidence file |
| --- | ---: | ---: | --- | --- |
| verse retrieval recall@1 avg | 0.021926 | 0.026222 | adapted improves | `06_downstream_tasks/score_table.tsv` |
| parallel verse matching avg | 0.569759 | 0.610759 | adapted improves | `06_downstream_tasks/score_table.tsv` |
| book/genre classification | 1.000000 | 1.000000 | trivial, not primary evidence | `06_downstream_tasks/score_table.tsv` |

## Translation Benchmark

| Setup | chrF++ | Ratio to high-resource reference | Decision | Evidence file |
| --- | ---: | ---: | --- | --- |
| high-resource Spanish->English reference | 61.959906 | 1.000000 | reference | `07_translation_benchmark/score_table.tsv` |
| best Step 07 target pair `usp->kbh` | 31.613700 | 0.510228 | fail | `07_translation_benchmark/score_table.tsv` |
| best branch measured row | 32.297328 | 0.521262 | fail | `branches/branch_001_translation_retrieval_gap/score_table.tsv` |
| Branch 001 LaBSE+CSLS `kbh->nhg` | 64.434500 | 1.039939 | exploratory only | `07_translation_benchmark/score_table.tsv` |

Required target ratio is `0.800000`. The Branch 001 row is not method-matched to its high-resource reference, so it is superseded by Step 09 for top-tier claims.

## Method-Matched Translation Audit

| Setup | High-resource test chrF++ | Target test chrF++ | Ratio | Decision | Evidence file |
| --- | ---: | ---: | ---: | --- | --- |
| original XLM-R cosine | 61.959906 | 28.979374 | 0.467712 | fail | `09_top_tier_validation/score_table.tsv` |
| selected adapted XLM-R cosine | 47.785568 | 30.488796 | 0.638034 | fail | `09_top_tier_validation/score_table.tsv` |
| LaBSE+CSLS upper bound | 100.000000 | 56.717922 | 0.567179 | fail | `09_top_tier_validation/score_table.tsv` |

No method-matched translation row reaches the `0.800000` threshold.
