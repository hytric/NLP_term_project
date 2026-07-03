# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step21000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step21000 | aligned_bible_src_eng | all | 300 | 0.921526 | 0.052713 |
| v52_mean_conv5way_step21000 | aligned_bible_src_eng | v5_target | 300 | 0.921526 | 0.052713 |
| v52_mean_conv5way_step21000 | aligned_tatoeba_src_eng | all | 300 | 0.924545 | 0.193803 |
| v52_mean_conv5way_step21000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.924545 | 0.193803 |
| v52_mean_conv5way_step21000 | roundtrip_eng_pivot | all | 300 | 0.918538 | 0.025732 |
| v52_mean_conv5way_step21000 | roundtrip_eng_pivot | v5_target | 300 | 0.918538 | 0.025732 |
| v52_mean_conv5way_step21000 | roundtrip_src_eng | all | 300 | 0.919171 | 0.032217 |
| v52_mean_conv5way_step21000 | roundtrip_src_eng | v5_target | 300 | 0.919171 | 0.032217 |
| v52_mean_conv5way_step21000 | roundtrip_src_pivot | all | 300 | 0.937600 | 0.315528 |
| v52_mean_conv5way_step21000 | roundtrip_src_pivot | v5_target | 300 | 0.937600 | 0.315528 |
| v52_mean_conv5way_step21000 | same_language_bible_adjacent | all | 300 | 0.978889 | 0.747881 |
| v52_mean_conv5way_step21000 | same_language_bible_adjacent | v5_target | 300 | 0.978889 | 0.747881 |
| v52_mean_conv5way_step21000 | same_language_tatoeba_adjacent | all | 300 | 0.945205 | 0.379217 |
| v52_mean_conv5way_step21000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945205 | 0.379217 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
