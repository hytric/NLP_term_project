# v5 Pseudoperplexity / MLM Proxy Results

- tokenizer: `cis-lmu/glot500-base`
- manifest: `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.manifest.tsv`
- max examples/language: `100`
- max length: `128`

| Model | Group | Languages | Examples | Masked Tokens | Weighted NLL | Weighted PPPL |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| glot500_base | all | 102 | 10200 | 339064 | 2.364654 | 10.640353 |
| glot500_base | head | 92 | 9200 | 303545 | 2.323671 | 10.213100 |
| glot500_base | v5_target | 10 | 1000 | 35519 | 2.714889 | 15.102934 |
