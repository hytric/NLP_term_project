# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step38000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step38000 | aligned_bible_src_eng | all | 300 | 0.913524 | 0.025957 |
| v52_family_mean_conv5way_step38000 | aligned_bible_src_eng | v5_target | 300 | 0.913524 | 0.025957 |
| v52_family_mean_conv5way_step38000 | aligned_tatoeba_src_eng | all | 300 | 0.922975 | 0.203479 |
| v52_family_mean_conv5way_step38000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922975 | 0.203479 |
| v52_family_mean_conv5way_step38000 | roundtrip_eng_pivot | all | 300 | 0.910663 | -0.014164 |
| v52_family_mean_conv5way_step38000 | roundtrip_eng_pivot | v5_target | 300 | 0.910663 | -0.014164 |
| v52_family_mean_conv5way_step38000 | roundtrip_src_eng | all | 300 | 0.910241 | 0.002592 |
| v52_family_mean_conv5way_step38000 | roundtrip_src_eng | v5_target | 300 | 0.910241 | 0.002592 |
| v52_family_mean_conv5way_step38000 | roundtrip_src_pivot | all | 300 | 0.936724 | 0.347329 |
| v52_family_mean_conv5way_step38000 | roundtrip_src_pivot | v5_target | 300 | 0.936724 | 0.347329 |
| v52_family_mean_conv5way_step38000 | same_language_bible_adjacent | all | 300 | 0.978357 | 0.765224 |
| v52_family_mean_conv5way_step38000 | same_language_bible_adjacent | v5_target | 300 | 0.978357 | 0.765224 |
| v52_family_mean_conv5way_step38000 | same_language_tatoeba_adjacent | all | 300 | 0.947981 | 0.412826 |
| v52_family_mean_conv5way_step38000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947981 | 0.412826 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
