# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step33000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step33000 | aligned_bible_src_eng | all | 300 | 0.921445 | 0.045128 |
| v52_random_conv5way_step33000 | aligned_bible_src_eng | v5_target | 300 | 0.921445 | 0.045128 |
| v52_random_conv5way_step33000 | aligned_tatoeba_src_eng | all | 300 | 0.922676 | 0.187449 |
| v52_random_conv5way_step33000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922676 | 0.187449 |
| v52_random_conv5way_step33000 | roundtrip_eng_pivot | all | 300 | 0.919026 | 0.020612 |
| v52_random_conv5way_step33000 | roundtrip_eng_pivot | v5_target | 300 | 0.919026 | 0.020612 |
| v52_random_conv5way_step33000 | roundtrip_src_eng | all | 300 | 0.918231 | 0.022912 |
| v52_random_conv5way_step33000 | roundtrip_src_eng | v5_target | 300 | 0.918231 | 0.022912 |
| v52_random_conv5way_step33000 | roundtrip_src_pivot | all | 300 | 0.938879 | 0.342265 |
| v52_random_conv5way_step33000 | roundtrip_src_pivot | v5_target | 300 | 0.938879 | 0.342265 |
| v52_random_conv5way_step33000 | same_language_bible_adjacent | all | 300 | 0.977921 | 0.744255 |
| v52_random_conv5way_step33000 | same_language_bible_adjacent | v5_target | 300 | 0.977921 | 0.744255 |
| v52_random_conv5way_step33000 | same_language_tatoeba_adjacent | all | 300 | 0.943483 | 0.355594 |
| v52_random_conv5way_step33000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943483 | 0.355594 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
