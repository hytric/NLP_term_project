# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step39000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step39000 | aligned_bible_src_eng | all | 300 | 0.914877 | 0.034572 |
| v52_family_mean_conv5way_step39000 | aligned_bible_src_eng | v5_target | 300 | 0.914877 | 0.034572 |
| v52_family_mean_conv5way_step39000 | aligned_tatoeba_src_eng | all | 300 | 0.923704 | 0.205712 |
| v52_family_mean_conv5way_step39000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.923704 | 0.205712 |
| v52_family_mean_conv5way_step39000 | roundtrip_eng_pivot | all | 300 | 0.912703 | -0.003678 |
| v52_family_mean_conv5way_step39000 | roundtrip_eng_pivot | v5_target | 300 | 0.912703 | -0.003678 |
| v52_family_mean_conv5way_step39000 | roundtrip_src_eng | all | 300 | 0.911604 | 0.011777 |
| v52_family_mean_conv5way_step39000 | roundtrip_src_eng | v5_target | 300 | 0.911604 | 0.011777 |
| v52_family_mean_conv5way_step39000 | roundtrip_src_pivot | all | 300 | 0.937130 | 0.342502 |
| v52_family_mean_conv5way_step39000 | roundtrip_src_pivot | v5_target | 300 | 0.937130 | 0.342502 |
| v52_family_mean_conv5way_step39000 | same_language_bible_adjacent | all | 300 | 0.978347 | 0.763504 |
| v52_family_mean_conv5way_step39000 | same_language_bible_adjacent | v5_target | 300 | 0.978347 | 0.763504 |
| v52_family_mean_conv5way_step39000 | same_language_tatoeba_adjacent | all | 300 | 0.948091 | 0.412153 |
| v52_family_mean_conv5way_step39000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.948091 | 0.412153 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
