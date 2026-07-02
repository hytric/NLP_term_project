# v5 Pseudoperplexity / MLM Proxy Results

- tokenizer: `/home/axt/mnt2/jongha/v5_glot50010/tokenization/output/Glot500_extended_spm`
- manifest: `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.manifest.tsv`
- max examples/language: `100`
- max length: `128`

| Model | Group | Languages | Examples | Masked Tokens | Weighted NLL | Weighted PPPL |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| v5_random | all | 102 | 10200 | 320079 | 3.002655 | 20.138927 |
| v5_random | head | 92 | 9200 | 288597 | 2.929937 | 18.726452 |
| v5_random | v5_target | 10 | 1000 | 31482 | 3.669260 | 39.222875 |
