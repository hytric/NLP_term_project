# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step38000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step38000 | aligned_bible_src_eng | all | 300 | 0.922312 | 0.073012 |
| v52_fvt_conv5way_step38000 | aligned_bible_src_eng | v5_target | 300 | 0.922312 | 0.073012 |
| v52_fvt_conv5way_step38000 | aligned_tatoeba_src_eng | all | 300 | 0.926759 | 0.200143 |
| v52_fvt_conv5way_step38000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926759 | 0.200143 |
| v52_fvt_conv5way_step38000 | roundtrip_eng_pivot | all | 300 | 0.919302 | 0.035840 |
| v52_fvt_conv5way_step38000 | roundtrip_eng_pivot | v5_target | 300 | 0.919302 | 0.035840 |
| v52_fvt_conv5way_step38000 | roundtrip_src_eng | all | 300 | 0.919194 | 0.050497 |
| v52_fvt_conv5way_step38000 | roundtrip_src_eng | v5_target | 300 | 0.919194 | 0.050497 |
| v52_fvt_conv5way_step38000 | roundtrip_src_pivot | all | 300 | 0.935357 | 0.312195 |
| v52_fvt_conv5way_step38000 | roundtrip_src_pivot | v5_target | 300 | 0.935357 | 0.312195 |
| v52_fvt_conv5way_step38000 | same_language_bible_adjacent | all | 300 | 0.978739 | 0.757779 |
| v52_fvt_conv5way_step38000 | same_language_bible_adjacent | v5_target | 300 | 0.978739 | 0.757779 |
| v52_fvt_conv5way_step38000 | same_language_tatoeba_adjacent | all | 300 | 0.947545 | 0.388535 |
| v52_fvt_conv5way_step38000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947545 | 0.388535 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
