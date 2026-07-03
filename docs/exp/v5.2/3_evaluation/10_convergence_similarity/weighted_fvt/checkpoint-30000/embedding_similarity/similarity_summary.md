# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step30000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step30000 | aligned_bible_src_eng | all | 300 | 0.923016 | 0.075208 |
| v52_weighted_fvt_conv5way_step30000 | aligned_bible_src_eng | v5_target | 300 | 0.923016 | 0.075208 |
| v52_weighted_fvt_conv5way_step30000 | aligned_tatoeba_src_eng | all | 300 | 0.925675 | 0.208292 |
| v52_weighted_fvt_conv5way_step30000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925675 | 0.208292 |
| v52_weighted_fvt_conv5way_step30000 | roundtrip_eng_pivot | all | 300 | 0.919748 | 0.031644 |
| v52_weighted_fvt_conv5way_step30000 | roundtrip_eng_pivot | v5_target | 300 | 0.919748 | 0.031644 |
| v52_weighted_fvt_conv5way_step30000 | roundtrip_src_eng | all | 300 | 0.920041 | 0.053012 |
| v52_weighted_fvt_conv5way_step30000 | roundtrip_src_eng | v5_target | 300 | 0.920041 | 0.053012 |
| v52_weighted_fvt_conv5way_step30000 | roundtrip_src_pivot | all | 300 | 0.935214 | 0.303049 |
| v52_weighted_fvt_conv5way_step30000 | roundtrip_src_pivot | v5_target | 300 | 0.935214 | 0.303049 |
| v52_weighted_fvt_conv5way_step30000 | same_language_bible_adjacent | all | 300 | 0.978567 | 0.755748 |
| v52_weighted_fvt_conv5way_step30000 | same_language_bible_adjacent | v5_target | 300 | 0.978567 | 0.755748 |
| v52_weighted_fvt_conv5way_step30000 | same_language_tatoeba_adjacent | all | 300 | 0.944895 | 0.368466 |
| v52_weighted_fvt_conv5way_step30000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944895 | 0.368466 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
