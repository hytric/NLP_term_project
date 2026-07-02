# v5 Main Zero-Step MLM Proxy Results

- tokenizer: `/home/axt/mnt2/jongha/v5_glot50010/tokenization/output/Glot500_extended_spm`
- manifest: `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.manifest.tsv`
- max examples/language: `5`
- max length: `96`

| Model | Group | Languages | Examples | Masked Tokens | Weighted NLL | Weighted PPPL |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| v5_fvt | all | 15 | 75 | 2256 | 8.040183 | 3103.181033 |
| v5_fvt | head | 5 | 25 | 777 | 6.621457 | 751.038819 |
| v5_fvt | v5_target | 10 | 50 | 1479 | 8.785518 | 6538.856501 |
| v5_mean | all | 15 | 75 | 2256 | 10.604370 | 40310.618084 |
| v5_mean | head | 5 | 25 | 777 | 8.037017 | 3093.372817 |
| v5_mean | v5_target | 10 | 50 | 1479 | 11.953142 | 155304.314070 |
| v5_random | all | 15 | 75 | 2256 | 16.511807 | 14824722.688186 |
| v5_random | head | 5 | 25 | 777 | 12.895301 | 398435.604683 |
| v5_random | v5_target | 10 | 50 | 1479 | 18.411756 | 99111496.403139 |
