# v5 Pseudoperplexity / MLM Proxy Results

- tokenizer: `xlm-roberta-large`
- manifest: `/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/0_tokenizer/merge/Glot500_v52_glot5007_xlmr100.manifest.tsv`
- max examples/language: `20`
- max length: `128`

| Model | Group | Languages | Examples | Masked Tokens | Weighted NLL | Weighted PPPL |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| xlmr_large | all | 99 | 1980 | 69569 | 1.832242 | 6.247878 |
| xlmr_large | head | 92 | 1840 | 63011 | 1.590555 | 4.906473 |
| xlmr_large | v5_target | 7 | 140 | 6558 | 4.154431 | 63.715695 |
