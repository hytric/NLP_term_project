# v5 Pseudoperplexity / MLM Proxy Results

- tokenizer: `xlm-roberta-base`
- manifest: `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.manifest.tsv`
- max examples/language: `100`
- max length: `128`

| Model | Group | Languages | Examples | Masked Tokens | Weighted NLL | Weighted PPPL |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| xlmr_base | all | 102 | 10200 | 357679 | 2.301211 | 9.986271 |
| xlmr_base | head | 92 | 9200 | 321220 | 2.094002 | 8.117338 |
| xlmr_base | v5_target | 10 | 1000 | 36459 | 4.126815 | 61.980216 |
