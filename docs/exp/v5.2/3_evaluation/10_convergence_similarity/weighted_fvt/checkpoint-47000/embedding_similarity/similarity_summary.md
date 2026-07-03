# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step47000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step47000 | aligned_bible_src_eng | all | 300 | 0.922667 | 0.065354 |
| v52_weighted_fvt_conv5way_step47000 | aligned_bible_src_eng | v5_target | 300 | 0.922667 | 0.065354 |
| v52_weighted_fvt_conv5way_step47000 | aligned_tatoeba_src_eng | all | 300 | 0.926462 | 0.209171 |
| v52_weighted_fvt_conv5way_step47000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926462 | 0.209171 |
| v52_weighted_fvt_conv5way_step47000 | roundtrip_eng_pivot | all | 300 | 0.919072 | 0.018546 |
| v52_weighted_fvt_conv5way_step47000 | roundtrip_eng_pivot | v5_target | 300 | 0.919072 | 0.018546 |
| v52_weighted_fvt_conv5way_step47000 | roundtrip_src_eng | all | 300 | 0.919628 | 0.043676 |
| v52_weighted_fvt_conv5way_step47000 | roundtrip_src_eng | v5_target | 300 | 0.919628 | 0.043676 |
| v52_weighted_fvt_conv5way_step47000 | roundtrip_src_pivot | all | 300 | 0.934264 | 0.295439 |
| v52_weighted_fvt_conv5way_step47000 | roundtrip_src_pivot | v5_target | 300 | 0.934264 | 0.295439 |
| v52_weighted_fvt_conv5way_step47000 | same_language_bible_adjacent | all | 300 | 0.978661 | 0.757158 |
| v52_weighted_fvt_conv5way_step47000 | same_language_bible_adjacent | v5_target | 300 | 0.978661 | 0.757158 |
| v52_weighted_fvt_conv5way_step47000 | same_language_tatoeba_adjacent | all | 300 | 0.945158 | 0.370547 |
| v52_weighted_fvt_conv5way_step47000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945158 | 0.370547 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
