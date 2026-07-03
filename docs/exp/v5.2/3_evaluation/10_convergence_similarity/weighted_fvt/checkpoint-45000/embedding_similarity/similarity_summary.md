# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step45000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step45000 | aligned_bible_src_eng | all | 300 | 0.923868 | 0.068279 |
| v52_weighted_fvt_conv5way_step45000 | aligned_bible_src_eng | v5_target | 300 | 0.923868 | 0.068279 |
| v52_weighted_fvt_conv5way_step45000 | aligned_tatoeba_src_eng | all | 300 | 0.927452 | 0.211621 |
| v52_weighted_fvt_conv5way_step45000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.927452 | 0.211621 |
| v52_weighted_fvt_conv5way_step45000 | roundtrip_eng_pivot | all | 300 | 0.919662 | 0.017456 |
| v52_weighted_fvt_conv5way_step45000 | roundtrip_eng_pivot | v5_target | 300 | 0.919662 | 0.017456 |
| v52_weighted_fvt_conv5way_step45000 | roundtrip_src_eng | all | 300 | 0.920846 | 0.046040 |
| v52_weighted_fvt_conv5way_step45000 | roundtrip_src_eng | v5_target | 300 | 0.920846 | 0.046040 |
| v52_weighted_fvt_conv5way_step45000 | roundtrip_src_pivot | all | 300 | 0.934558 | 0.294925 |
| v52_weighted_fvt_conv5way_step45000 | roundtrip_src_pivot | v5_target | 300 | 0.934558 | 0.294925 |
| v52_weighted_fvt_conv5way_step45000 | same_language_bible_adjacent | all | 300 | 0.978830 | 0.756613 |
| v52_weighted_fvt_conv5way_step45000 | same_language_bible_adjacent | v5_target | 300 | 0.978830 | 0.756613 |
| v52_weighted_fvt_conv5way_step45000 | same_language_tatoeba_adjacent | all | 300 | 0.945864 | 0.371190 |
| v52_weighted_fvt_conv5way_step45000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945864 | 0.371190 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
