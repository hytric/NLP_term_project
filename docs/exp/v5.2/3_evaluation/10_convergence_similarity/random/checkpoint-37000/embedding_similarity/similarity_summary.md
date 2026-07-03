# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step37000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step37000 | aligned_bible_src_eng | all | 300 | 0.921450 | 0.043772 |
| v52_random_conv5way_step37000 | aligned_bible_src_eng | v5_target | 300 | 0.921450 | 0.043772 |
| v52_random_conv5way_step37000 | aligned_tatoeba_src_eng | all | 300 | 0.922837 | 0.187758 |
| v52_random_conv5way_step37000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922837 | 0.187758 |
| v52_random_conv5way_step37000 | roundtrip_eng_pivot | all | 300 | 0.919108 | 0.019810 |
| v52_random_conv5way_step37000 | roundtrip_eng_pivot | v5_target | 300 | 0.919108 | 0.019810 |
| v52_random_conv5way_step37000 | roundtrip_src_eng | all | 300 | 0.918235 | 0.021654 |
| v52_random_conv5way_step37000 | roundtrip_src_eng | v5_target | 300 | 0.918235 | 0.021654 |
| v52_random_conv5way_step37000 | roundtrip_src_pivot | all | 300 | 0.938880 | 0.342373 |
| v52_random_conv5way_step37000 | roundtrip_src_pivot | v5_target | 300 | 0.938880 | 0.342373 |
| v52_random_conv5way_step37000 | same_language_bible_adjacent | all | 300 | 0.977968 | 0.744980 |
| v52_random_conv5way_step37000 | same_language_bible_adjacent | v5_target | 300 | 0.977968 | 0.744980 |
| v52_random_conv5way_step37000 | same_language_tatoeba_adjacent | all | 300 | 0.943528 | 0.355551 |
| v52_random_conv5way_step37000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943528 | 0.355551 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
