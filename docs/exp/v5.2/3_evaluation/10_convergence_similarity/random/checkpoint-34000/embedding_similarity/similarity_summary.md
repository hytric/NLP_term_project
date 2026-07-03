# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step34000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step34000 | aligned_bible_src_eng | all | 300 | 0.921424 | 0.044592 |
| v52_random_conv5way_step34000 | aligned_bible_src_eng | v5_target | 300 | 0.921424 | 0.044592 |
| v52_random_conv5way_step34000 | aligned_tatoeba_src_eng | all | 300 | 0.922833 | 0.188406 |
| v52_random_conv5way_step34000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922833 | 0.188406 |
| v52_random_conv5way_step34000 | roundtrip_eng_pivot | all | 300 | 0.919054 | 0.020479 |
| v52_random_conv5way_step34000 | roundtrip_eng_pivot | v5_target | 300 | 0.919054 | 0.020479 |
| v52_random_conv5way_step34000 | roundtrip_src_eng | all | 300 | 0.918220 | 0.022513 |
| v52_random_conv5way_step34000 | roundtrip_src_eng | v5_target | 300 | 0.918220 | 0.022513 |
| v52_random_conv5way_step34000 | roundtrip_src_pivot | all | 300 | 0.938950 | 0.343184 |
| v52_random_conv5way_step34000 | roundtrip_src_pivot | v5_target | 300 | 0.938950 | 0.343184 |
| v52_random_conv5way_step34000 | same_language_bible_adjacent | all | 300 | 0.977925 | 0.744544 |
| v52_random_conv5way_step34000 | same_language_bible_adjacent | v5_target | 300 | 0.977925 | 0.744544 |
| v52_random_conv5way_step34000 | same_language_tatoeba_adjacent | all | 300 | 0.943474 | 0.355336 |
| v52_random_conv5way_step34000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943474 | 0.355336 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
