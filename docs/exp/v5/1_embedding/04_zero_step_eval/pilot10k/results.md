# v5 Zero-Step MLM Proxy Results

- tokenizer: `/home/axt/mnt2/jongha/v5_glot50010/tokenization/pilot10k_output/Glot500_extended_spm`
- manifest: `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100_pilot10k.manifest.tsv`
- max examples/language: `5`
- max length: `96`

| Model | Group | Languages | Examples | Masked Tokens | Weighted NLL | Weighted PPPL |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| v5_fvt | all | 15 | 75 | 2664 | 5.845506 | 345.677582 |
| v5_fvt | head | 5 | 25 | 899 | 3.573436 | 35.638850 |
| v5_fvt | v5_target | 10 | 50 | 1765 | 7.002782 | 1099.688124 |
| v5_mean | all | 15 | 75 | 2664 | 8.044169 | 3115.575309 |
| v5_mean | head | 5 | 25 | 899 | 3.367013 | 28.991806 |
| v5_mean | v5_target | 10 | 50 | 1765 | 10.426471 | 33741.072977 |
| v5_random | all | 15 | 75 | 2664 | 12.348813 | 230686.067210 |
| v5_random | head | 5 | 25 | 899 | 4.294692 | 73.309609 |
| v5_random | v5_target | 10 | 50 | 1765 | 16.451167 | 13952471.416749 |
