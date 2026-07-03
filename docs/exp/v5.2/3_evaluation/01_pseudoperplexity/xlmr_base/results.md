# v5 Pseudoperplexity / MLM Proxy Results

- tokenizer: `xlm-roberta-base`
- manifest: `/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/0_tokenizer/merge/Glot500_v52_glot5007_xlmr100.manifest.tsv`
- max examples/language: `20`
- max length: `128`

| Model | Group | Languages | Examples | Masked Tokens | Weighted NLL | Weighted PPPL |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| xlmr_base | all | 99 | 1980 | 69569 | 2.321768 | 10.193684 |
| xlmr_base | head | 92 | 1840 | 63011 | 2.085967 | 8.052377 |
| xlmr_base | v5_target | 7 | 140 | 6558 | 4.587406 | 98.239305 |
