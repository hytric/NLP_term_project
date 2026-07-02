# v5.1 Evaluation Coverage Results

- manifest: `docs/exp/v5.1/0_tokenizer/merge/Glot500_v51_glot50010_xlmr100_strict_5pct.manifest.tsv`
- eval data root: `/home/axt/mnt2/jongha/v5_1_glot50010/eval_data_download`
- language rows per metric: `102`

Summary:

| Task | Has Data / Total | Target Has Data | Blocked Or Missing |
| --- | ---: | ---: | ---: |
| pseudoperplexity | 102 / 102 | 10 / 10 | 0 |
| retrieval_tatoeba | 66 / 102 | 3 / 10 | 36 |
| retrieval_bible | 80 / 102 | 6 / 10 | 22 |
| text_classification | 1 / 102 | 0 / 10 | 101 |
| ner | 84 / 102 | 6 / 10 | 18 |
| pos | 58 / 102 | 0 / 10 | 44 |
| roundtrip_alignment | 80 / 102 | 6 / 10 | 22 |

Coverage files are named `coverage_<task>.tsv`.
