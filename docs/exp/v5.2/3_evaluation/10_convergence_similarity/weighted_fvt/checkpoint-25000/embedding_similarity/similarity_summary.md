# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step25000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step25000 | aligned_bible_src_eng | all | 300 | 0.922327 | 0.069704 |
| v52_weighted_fvt_conv5way_step25000 | aligned_bible_src_eng | v5_target | 300 | 0.922327 | 0.069704 |
| v52_weighted_fvt_conv5way_step25000 | aligned_tatoeba_src_eng | all | 300 | 0.924182 | 0.200946 |
| v52_weighted_fvt_conv5way_step25000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.924182 | 0.200946 |
| v52_weighted_fvt_conv5way_step25000 | roundtrip_eng_pivot | all | 300 | 0.918794 | 0.025600 |
| v52_weighted_fvt_conv5way_step25000 | roundtrip_eng_pivot | v5_target | 300 | 0.918794 | 0.025600 |
| v52_weighted_fvt_conv5way_step25000 | roundtrip_src_eng | all | 300 | 0.919253 | 0.047281 |
| v52_weighted_fvt_conv5way_step25000 | roundtrip_src_eng | v5_target | 300 | 0.919253 | 0.047281 |
| v52_weighted_fvt_conv5way_step25000 | roundtrip_src_pivot | all | 300 | 0.932915 | 0.287208 |
| v52_weighted_fvt_conv5way_step25000 | roundtrip_src_pivot | v5_target | 300 | 0.932915 | 0.287208 |
| v52_weighted_fvt_conv5way_step25000 | same_language_bible_adjacent | all | 300 | 0.978191 | 0.753070 |
| v52_weighted_fvt_conv5way_step25000 | same_language_bible_adjacent | v5_target | 300 | 0.978191 | 0.753070 |
| v52_weighted_fvt_conv5way_step25000 | same_language_tatoeba_adjacent | all | 300 | 0.943841 | 0.367443 |
| v52_weighted_fvt_conv5way_step25000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943841 | 0.367443 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
