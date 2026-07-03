# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step19000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step19000 | aligned_bible_src_eng | all | 300 | 0.919497 | 0.039649 |
| v52_random_conv5way_step19000 | aligned_bible_src_eng | v5_target | 300 | 0.919497 | 0.039649 |
| v52_random_conv5way_step19000 | aligned_tatoeba_src_eng | all | 300 | 0.920104 | 0.183406 |
| v52_random_conv5way_step19000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.920104 | 0.183406 |
| v52_random_conv5way_step19000 | roundtrip_eng_pivot | all | 300 | 0.917439 | 0.017482 |
| v52_random_conv5way_step19000 | roundtrip_eng_pivot | v5_target | 300 | 0.917439 | 0.017482 |
| v52_random_conv5way_step19000 | roundtrip_src_eng | all | 300 | 0.916245 | 0.017903 |
| v52_random_conv5way_step19000 | roundtrip_src_eng | v5_target | 300 | 0.916245 | 0.017903 |
| v52_random_conv5way_step19000 | roundtrip_src_pivot | all | 300 | 0.938037 | 0.342981 |
| v52_random_conv5way_step19000 | roundtrip_src_pivot | v5_target | 300 | 0.938037 | 0.342981 |
| v52_random_conv5way_step19000 | same_language_bible_adjacent | all | 300 | 0.977529 | 0.744484 |
| v52_random_conv5way_step19000 | same_language_bible_adjacent | v5_target | 300 | 0.977529 | 0.744484 |
| v52_random_conv5way_step19000 | same_language_tatoeba_adjacent | all | 300 | 0.941590 | 0.352245 |
| v52_random_conv5way_step19000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.941590 | 0.352245 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
