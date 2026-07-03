# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step32000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step32000 | aligned_bible_src_eng | all | 300 | 0.915611 | 0.031484 |
| v52_family_mean_conv5way_step32000 | aligned_bible_src_eng | v5_target | 300 | 0.915611 | 0.031484 |
| v52_family_mean_conv5way_step32000 | aligned_tatoeba_src_eng | all | 300 | 0.922731 | 0.206112 |
| v52_family_mean_conv5way_step32000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922731 | 0.206112 |
| v52_family_mean_conv5way_step32000 | roundtrip_eng_pivot | all | 300 | 0.913623 | -0.003009 |
| v52_family_mean_conv5way_step32000 | roundtrip_eng_pivot | v5_target | 300 | 0.913623 | -0.003009 |
| v52_family_mean_conv5way_step32000 | roundtrip_src_eng | all | 300 | 0.912387 | 0.008607 |
| v52_family_mean_conv5way_step32000 | roundtrip_src_eng | v5_target | 300 | 0.912387 | 0.008607 |
| v52_family_mean_conv5way_step32000 | roundtrip_src_pivot | all | 300 | 0.937932 | 0.346247 |
| v52_family_mean_conv5way_step32000 | roundtrip_src_pivot | v5_target | 300 | 0.937932 | 0.346247 |
| v52_family_mean_conv5way_step32000 | same_language_bible_adjacent | all | 300 | 0.978308 | 0.759836 |
| v52_family_mean_conv5way_step32000 | same_language_bible_adjacent | v5_target | 300 | 0.978308 | 0.759836 |
| v52_family_mean_conv5way_step32000 | same_language_tatoeba_adjacent | all | 300 | 0.947473 | 0.405645 |
| v52_family_mean_conv5way_step32000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947473 | 0.405645 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
