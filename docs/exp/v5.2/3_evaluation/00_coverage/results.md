# v5.2 Evaluation Coverage Results

- manifest: `/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/0_tokenizer/merge/Glot500_v52_glot5007_xlmr100.manifest.tsv`
- eval data root: `/home/axt/jongha/Glot500-py39-eval/evaluation/download_data/download`
- language rows per metric: `99`

Summary:

| Task | Has Data / Total | Target Has Data | Blocked Or Missing |
| --- | ---: | ---: | ---: |
| pseudoperplexity | 99 / 99 | 7 / 7 | 0 |
| retrieval_tatoeba | 66 / 99 | 3 / 7 | 33 |
| retrieval_bible | 74 / 99 | 0 / 7 | 25 |
| text_classification | 1 / 99 | 0 / 7 | 98 |
| ner | 81 / 99 | 3 / 7 | 18 |
| pos | 7 / 99 | 0 / 7 | 92 |
| roundtrip_alignment | 74 / 99 | 0 / 7 | 25 |

Coverage files are named `coverage_<task>.tsv`.
