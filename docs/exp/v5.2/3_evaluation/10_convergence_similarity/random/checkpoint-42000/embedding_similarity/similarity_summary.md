# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step42000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step42000 | aligned_bible_src_eng | all | 300 | 0.921844 | 0.044290 |
| v52_random_conv5way_step42000 | aligned_bible_src_eng | v5_target | 300 | 0.921844 | 0.044290 |
| v52_random_conv5way_step42000 | aligned_tatoeba_src_eng | all | 300 | 0.923075 | 0.187301 |
| v52_random_conv5way_step42000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.923075 | 0.187301 |
| v52_random_conv5way_step42000 | roundtrip_eng_pivot | all | 300 | 0.919475 | 0.020162 |
| v52_random_conv5way_step42000 | roundtrip_eng_pivot | v5_target | 300 | 0.919475 | 0.020162 |
| v52_random_conv5way_step42000 | roundtrip_src_eng | all | 300 | 0.918658 | 0.022225 |
| v52_random_conv5way_step42000 | roundtrip_src_eng | v5_target | 300 | 0.918658 | 0.022225 |
| v52_random_conv5way_step42000 | roundtrip_src_pivot | all | 300 | 0.939013 | 0.341386 |
| v52_random_conv5way_step42000 | roundtrip_src_pivot | v5_target | 300 | 0.939013 | 0.341386 |
| v52_random_conv5way_step42000 | same_language_bible_adjacent | all | 300 | 0.977960 | 0.743892 |
| v52_random_conv5way_step42000 | same_language_bible_adjacent | v5_target | 300 | 0.977960 | 0.743892 |
| v52_random_conv5way_step42000 | same_language_tatoeba_adjacent | all | 300 | 0.943727 | 0.355419 |
| v52_random_conv5way_step42000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943727 | 0.355419 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
