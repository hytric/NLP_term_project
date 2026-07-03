# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step12000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step12000 | aligned_bible_src_eng | all | 300 | 0.918243 | 0.055304 |
| v52_fvt_conv5way_step12000 | aligned_bible_src_eng | v5_target | 300 | 0.918243 | 0.055304 |
| v52_fvt_conv5way_step12000 | aligned_tatoeba_src_eng | all | 300 | 0.922744 | 0.192880 |
| v52_fvt_conv5way_step12000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922744 | 0.192880 |
| v52_fvt_conv5way_step12000 | roundtrip_eng_pivot | all | 300 | 0.915341 | 0.020137 |
| v52_fvt_conv5way_step12000 | roundtrip_eng_pivot | v5_target | 300 | 0.915341 | 0.020137 |
| v52_fvt_conv5way_step12000 | roundtrip_src_eng | all | 300 | 0.915015 | 0.033377 |
| v52_fvt_conv5way_step12000 | roundtrip_src_eng | v5_target | 300 | 0.915015 | 0.033377 |
| v52_fvt_conv5way_step12000 | roundtrip_src_pivot | all | 300 | 0.933540 | 0.313257 |
| v52_fvt_conv5way_step12000 | roundtrip_src_pivot | v5_target | 300 | 0.933540 | 0.313257 |
| v52_fvt_conv5way_step12000 | same_language_bible_adjacent | all | 300 | 0.978018 | 0.758473 |
| v52_fvt_conv5way_step12000 | same_language_bible_adjacent | v5_target | 300 | 0.978018 | 0.758473 |
| v52_fvt_conv5way_step12000 | same_language_tatoeba_adjacent | all | 300 | 0.945380 | 0.387688 |
| v52_fvt_conv5way_step12000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945380 | 0.387688 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
