# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step37000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step37000 | aligned_bible_src_eng | all | 300 | 0.922595 | 0.069331 |
| v52_weighted_fvt_conv5way_step37000 | aligned_bible_src_eng | v5_target | 300 | 0.922595 | 0.069331 |
| v52_weighted_fvt_conv5way_step37000 | aligned_tatoeba_src_eng | all | 300 | 0.926214 | 0.210304 |
| v52_weighted_fvt_conv5way_step37000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926214 | 0.210304 |
| v52_weighted_fvt_conv5way_step37000 | roundtrip_eng_pivot | all | 300 | 0.918820 | 0.022736 |
| v52_weighted_fvt_conv5way_step37000 | roundtrip_eng_pivot | v5_target | 300 | 0.918820 | 0.022736 |
| v52_weighted_fvt_conv5way_step37000 | roundtrip_src_eng | all | 300 | 0.919665 | 0.047360 |
| v52_weighted_fvt_conv5way_step37000 | roundtrip_src_eng | v5_target | 300 | 0.919665 | 0.047360 |
| v52_weighted_fvt_conv5way_step37000 | roundtrip_src_pivot | all | 300 | 0.934490 | 0.297481 |
| v52_weighted_fvt_conv5way_step37000 | roundtrip_src_pivot | v5_target | 300 | 0.934490 | 0.297481 |
| v52_weighted_fvt_conv5way_step37000 | same_language_bible_adjacent | all | 300 | 0.978819 | 0.758749 |
| v52_weighted_fvt_conv5way_step37000 | same_language_bible_adjacent | v5_target | 300 | 0.978819 | 0.758749 |
| v52_weighted_fvt_conv5way_step37000 | same_language_tatoeba_adjacent | all | 300 | 0.945139 | 0.372203 |
| v52_weighted_fvt_conv5way_step37000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945139 | 0.372203 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
