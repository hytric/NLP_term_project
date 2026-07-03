# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step37000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step37000 | aligned_bible_src_eng | all | 300 | 0.915141 | 0.036398 |
| v52_family_mean_conv5way_step37000 | aligned_bible_src_eng | v5_target | 300 | 0.915141 | 0.036398 |
| v52_family_mean_conv5way_step37000 | aligned_tatoeba_src_eng | all | 300 | 0.924379 | 0.207299 |
| v52_family_mean_conv5way_step37000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.924379 | 0.207299 |
| v52_family_mean_conv5way_step37000 | roundtrip_eng_pivot | all | 300 | 0.912933 | -0.001678 |
| v52_family_mean_conv5way_step37000 | roundtrip_eng_pivot | v5_target | 300 | 0.912933 | -0.001678 |
| v52_family_mean_conv5way_step37000 | roundtrip_src_eng | all | 300 | 0.911953 | 0.013979 |
| v52_family_mean_conv5way_step37000 | roundtrip_src_eng | v5_target | 300 | 0.911953 | 0.013979 |
| v52_family_mean_conv5way_step37000 | roundtrip_src_pivot | all | 300 | 0.935881 | 0.336878 |
| v52_family_mean_conv5way_step37000 | roundtrip_src_pivot | v5_target | 300 | 0.935881 | 0.336878 |
| v52_family_mean_conv5way_step37000 | same_language_bible_adjacent | all | 300 | 0.978262 | 0.765270 |
| v52_family_mean_conv5way_step37000 | same_language_bible_adjacent | v5_target | 300 | 0.978262 | 0.765270 |
| v52_family_mean_conv5way_step37000 | same_language_tatoeba_adjacent | all | 300 | 0.948795 | 0.414444 |
| v52_family_mean_conv5way_step37000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.948795 | 0.414444 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
