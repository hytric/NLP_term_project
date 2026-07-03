# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step21000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step21000 | aligned_bible_src_eng | all | 300 | 0.922785 | 0.078706 |
| v52_weighted_fvt_conv5way_step21000 | aligned_bible_src_eng | v5_target | 300 | 0.922785 | 0.078706 |
| v52_weighted_fvt_conv5way_step21000 | aligned_tatoeba_src_eng | all | 300 | 0.924468 | 0.203071 |
| v52_weighted_fvt_conv5way_step21000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.924468 | 0.203071 |
| v52_weighted_fvt_conv5way_step21000 | roundtrip_eng_pivot | all | 300 | 0.919746 | 0.038516 |
| v52_weighted_fvt_conv5way_step21000 | roundtrip_eng_pivot | v5_target | 300 | 0.919746 | 0.038516 |
| v52_weighted_fvt_conv5way_step21000 | roundtrip_src_eng | all | 300 | 0.919729 | 0.055767 |
| v52_weighted_fvt_conv5way_step21000 | roundtrip_src_eng | v5_target | 300 | 0.919729 | 0.055767 |
| v52_weighted_fvt_conv5way_step21000 | roundtrip_src_pivot | all | 300 | 0.933966 | 0.294022 |
| v52_weighted_fvt_conv5way_step21000 | roundtrip_src_pivot | v5_target | 300 | 0.933966 | 0.294022 |
| v52_weighted_fvt_conv5way_step21000 | same_language_bible_adjacent | all | 300 | 0.978109 | 0.751611 |
| v52_weighted_fvt_conv5way_step21000 | same_language_bible_adjacent | v5_target | 300 | 0.978109 | 0.751611 |
| v52_weighted_fvt_conv5way_step21000 | same_language_tatoeba_adjacent | all | 300 | 0.944142 | 0.369155 |
| v52_weighted_fvt_conv5way_step21000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944142 | 0.369155 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
