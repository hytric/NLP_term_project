# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step34000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step34000 | aligned_bible_src_eng | all | 300 | 0.922080 | 0.073454 |
| v52_fvt_conv5way_step34000 | aligned_bible_src_eng | v5_target | 300 | 0.922080 | 0.073454 |
| v52_fvt_conv5way_step34000 | aligned_tatoeba_src_eng | all | 300 | 0.926649 | 0.200361 |
| v52_fvt_conv5way_step34000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926649 | 0.200361 |
| v52_fvt_conv5way_step34000 | roundtrip_eng_pivot | all | 300 | 0.919091 | 0.036023 |
| v52_fvt_conv5way_step34000 | roundtrip_eng_pivot | v5_target | 300 | 0.919091 | 0.036023 |
| v52_fvt_conv5way_step34000 | roundtrip_src_eng | all | 300 | 0.918948 | 0.051040 |
| v52_fvt_conv5way_step34000 | roundtrip_src_eng | v5_target | 300 | 0.918948 | 0.051040 |
| v52_fvt_conv5way_step34000 | roundtrip_src_pivot | all | 300 | 0.935387 | 0.314467 |
| v52_fvt_conv5way_step34000 | roundtrip_src_pivot | v5_target | 300 | 0.935387 | 0.314467 |
| v52_fvt_conv5way_step34000 | same_language_bible_adjacent | all | 300 | 0.978691 | 0.757932 |
| v52_fvt_conv5way_step34000 | same_language_bible_adjacent | v5_target | 300 | 0.978691 | 0.757932 |
| v52_fvt_conv5way_step34000 | same_language_tatoeba_adjacent | all | 300 | 0.947473 | 0.389301 |
| v52_fvt_conv5way_step34000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947473 | 0.389301 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
