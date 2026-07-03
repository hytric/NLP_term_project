# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step11000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step11000 | aligned_bible_src_eng | all | 300 | 0.920536 | 0.065039 |
| v52_fvt_conv5way_step11000 | aligned_bible_src_eng | v5_target | 300 | 0.920536 | 0.065039 |
| v52_fvt_conv5way_step11000 | aligned_tatoeba_src_eng | all | 300 | 0.922827 | 0.186599 |
| v52_fvt_conv5way_step11000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922827 | 0.186599 |
| v52_fvt_conv5way_step11000 | roundtrip_eng_pivot | all | 300 | 0.917928 | 0.030506 |
| v52_fvt_conv5way_step11000 | roundtrip_eng_pivot | v5_target | 300 | 0.917928 | 0.030506 |
| v52_fvt_conv5way_step11000 | roundtrip_src_eng | all | 300 | 0.917331 | 0.043112 |
| v52_fvt_conv5way_step11000 | roundtrip_src_eng | v5_target | 300 | 0.917331 | 0.043112 |
| v52_fvt_conv5way_step11000 | roundtrip_src_pivot | all | 300 | 0.935673 | 0.314876 |
| v52_fvt_conv5way_step11000 | roundtrip_src_pivot | v5_target | 300 | 0.935673 | 0.314876 |
| v52_fvt_conv5way_step11000 | same_language_bible_adjacent | all | 300 | 0.978496 | 0.754627 |
| v52_fvt_conv5way_step11000 | same_language_bible_adjacent | v5_target | 300 | 0.978496 | 0.754627 |
| v52_fvt_conv5way_step11000 | same_language_tatoeba_adjacent | all | 300 | 0.945651 | 0.382576 |
| v52_fvt_conv5way_step11000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945651 | 0.382576 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
