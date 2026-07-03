# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step18000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step18000 | aligned_bible_src_eng | all | 300 | 0.919411 | 0.043692 |
| v52_random_conv5way_step18000 | aligned_bible_src_eng | v5_target | 300 | 0.919411 | 0.043692 |
| v52_random_conv5way_step18000 | aligned_tatoeba_src_eng | all | 300 | 0.920272 | 0.188561 |
| v52_random_conv5way_step18000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.920272 | 0.188561 |
| v52_random_conv5way_step18000 | roundtrip_eng_pivot | all | 300 | 0.917045 | 0.018236 |
| v52_random_conv5way_step18000 | roundtrip_eng_pivot | v5_target | 300 | 0.917045 | 0.018236 |
| v52_random_conv5way_step18000 | roundtrip_src_eng | all | 300 | 0.916112 | 0.021707 |
| v52_random_conv5way_step18000 | roundtrip_src_eng | v5_target | 300 | 0.916112 | 0.021707 |
| v52_random_conv5way_step18000 | roundtrip_src_pivot | all | 300 | 0.937397 | 0.341719 |
| v52_random_conv5way_step18000 | roundtrip_src_pivot | v5_target | 300 | 0.937397 | 0.341719 |
| v52_random_conv5way_step18000 | same_language_bible_adjacent | all | 300 | 0.977536 | 0.745536 |
| v52_random_conv5way_step18000 | same_language_bible_adjacent | v5_target | 300 | 0.977536 | 0.745536 |
| v52_random_conv5way_step18000 | same_language_tatoeba_adjacent | all | 300 | 0.941084 | 0.350837 |
| v52_random_conv5way_step18000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.941084 | 0.350837 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
