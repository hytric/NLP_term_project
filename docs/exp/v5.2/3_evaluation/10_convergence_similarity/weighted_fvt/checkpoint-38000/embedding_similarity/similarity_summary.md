# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step38000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step38000 | aligned_bible_src_eng | all | 300 | 0.922864 | 0.061554 |
| v52_weighted_fvt_conv5way_step38000 | aligned_bible_src_eng | v5_target | 300 | 0.922864 | 0.061554 |
| v52_weighted_fvt_conv5way_step38000 | aligned_tatoeba_src_eng | all | 300 | 0.926072 | 0.206540 |
| v52_weighted_fvt_conv5way_step38000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926072 | 0.206540 |
| v52_weighted_fvt_conv5way_step38000 | roundtrip_eng_pivot | all | 300 | 0.919295 | 0.015447 |
| v52_weighted_fvt_conv5way_step38000 | roundtrip_eng_pivot | v5_target | 300 | 0.919295 | 0.015447 |
| v52_weighted_fvt_conv5way_step38000 | roundtrip_src_eng | all | 300 | 0.919929 | 0.039420 |
| v52_weighted_fvt_conv5way_step38000 | roundtrip_src_eng | v5_target | 300 | 0.919929 | 0.039420 |
| v52_weighted_fvt_conv5way_step38000 | roundtrip_src_pivot | all | 300 | 0.934152 | 0.289102 |
| v52_weighted_fvt_conv5way_step38000 | roundtrip_src_pivot | v5_target | 300 | 0.934152 | 0.289102 |
| v52_weighted_fvt_conv5way_step38000 | same_language_bible_adjacent | all | 300 | 0.978692 | 0.755433 |
| v52_weighted_fvt_conv5way_step38000 | same_language_bible_adjacent | v5_target | 300 | 0.978692 | 0.755433 |
| v52_weighted_fvt_conv5way_step38000 | same_language_tatoeba_adjacent | all | 300 | 0.944629 | 0.366892 |
| v52_weighted_fvt_conv5way_step38000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944629 | 0.366892 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
