# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step21000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step21000 | aligned_bible_src_eng | all | 300 | 0.920329 | 0.041307 |
| v52_random_conv5way_step21000 | aligned_bible_src_eng | v5_target | 300 | 0.920329 | 0.041307 |
| v52_random_conv5way_step21000 | aligned_tatoeba_src_eng | all | 300 | 0.921483 | 0.184710 |
| v52_random_conv5way_step21000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.921483 | 0.184710 |
| v52_random_conv5way_step21000 | roundtrip_eng_pivot | all | 300 | 0.918075 | 0.017431 |
| v52_random_conv5way_step21000 | roundtrip_eng_pivot | v5_target | 300 | 0.918075 | 0.017431 |
| v52_random_conv5way_step21000 | roundtrip_src_eng | all | 300 | 0.917074 | 0.019011 |
| v52_random_conv5way_step21000 | roundtrip_src_eng | v5_target | 300 | 0.917074 | 0.019011 |
| v52_random_conv5way_step21000 | roundtrip_src_pivot | all | 300 | 0.938145 | 0.340415 |
| v52_random_conv5way_step21000 | roundtrip_src_pivot | v5_target | 300 | 0.938145 | 0.340415 |
| v52_random_conv5way_step21000 | same_language_bible_adjacent | all | 300 | 0.977717 | 0.744653 |
| v52_random_conv5way_step21000 | same_language_bible_adjacent | v5_target | 300 | 0.977717 | 0.744653 |
| v52_random_conv5way_step21000 | same_language_tatoeba_adjacent | all | 300 | 0.942699 | 0.353961 |
| v52_random_conv5way_step21000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.942699 | 0.353961 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
