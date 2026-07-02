# v5 Evaluation Coverage Results

- manifest: `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.manifest.tsv`
- eval data root: `evaluation/download_data/download`
- language rows per metric: `102`

Summary:

| Task | Has Data / Total | Target Has Data | Blocked Or Missing |
| --- | ---: | ---: | ---: |
| pseudoperplexity | 102 / 102 | 10 / 10 | 0 |
| retrieval_tatoeba | 63 / 102 | 0 / 10 | 39 |
| retrieval_bible | 74 / 102 | 0 / 10 | 28 |
| text_classification | 1 / 102 | 0 / 10 | 101 |
| ner | 78 / 102 | 0 / 10 | 24 |
| pos | 58 / 102 | 0 / 10 | 44 |
| roundtrip_alignment | 74 / 102 | 0 / 10 | 28 |

Coverage files are named `coverage_<task>.tsv`.
