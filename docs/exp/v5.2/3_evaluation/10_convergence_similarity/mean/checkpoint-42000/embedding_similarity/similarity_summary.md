# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step42000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step42000 | aligned_bible_src_eng | all | 300 | 0.922794 | 0.055429 |
| v52_mean_conv5way_step42000 | aligned_bible_src_eng | v5_target | 300 | 0.922794 | 0.055429 |
| v52_mean_conv5way_step42000 | aligned_tatoeba_src_eng | all | 300 | 0.925728 | 0.196248 |
| v52_mean_conv5way_step42000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925728 | 0.196248 |
| v52_mean_conv5way_step42000 | roundtrip_eng_pivot | all | 300 | 0.919821 | 0.029357 |
| v52_mean_conv5way_step42000 | roundtrip_eng_pivot | v5_target | 300 | 0.919821 | 0.029357 |
| v52_mean_conv5way_step42000 | roundtrip_src_eng | all | 300 | 0.920418 | 0.035247 |
| v52_mean_conv5way_step42000 | roundtrip_src_eng | v5_target | 300 | 0.920418 | 0.035247 |
| v52_mean_conv5way_step42000 | roundtrip_src_pivot | all | 300 | 0.937914 | 0.314533 |
| v52_mean_conv5way_step42000 | roundtrip_src_pivot | v5_target | 300 | 0.937914 | 0.314533 |
| v52_mean_conv5way_step42000 | same_language_bible_adjacent | all | 300 | 0.979037 | 0.747823 |
| v52_mean_conv5way_step42000 | same_language_bible_adjacent | v5_target | 300 | 0.979037 | 0.747823 |
| v52_mean_conv5way_step42000 | same_language_tatoeba_adjacent | all | 300 | 0.945839 | 0.379438 |
| v52_mean_conv5way_step42000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945839 | 0.379438 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
