# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step10000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step10000 | aligned_bible_src_eng | all | 300 | 0.917086 | 0.032586 |
| v52_mean_conv5way_step10000 | aligned_bible_src_eng | v5_target | 300 | 0.917086 | 0.032586 |
| v52_mean_conv5way_step10000 | aligned_tatoeba_src_eng | all | 300 | 0.920596 | 0.180831 |
| v52_mean_conv5way_step10000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.920596 | 0.180831 |
| v52_mean_conv5way_step10000 | roundtrip_eng_pivot | all | 300 | 0.915088 | 0.016017 |
| v52_mean_conv5way_step10000 | roundtrip_eng_pivot | v5_target | 300 | 0.915088 | 0.016017 |
| v52_mean_conv5way_step10000 | roundtrip_src_eng | all | 300 | 0.914607 | 0.015402 |
| v52_mean_conv5way_step10000 | roundtrip_src_eng | v5_target | 300 | 0.914607 | 0.015402 |
| v52_mean_conv5way_step10000 | roundtrip_src_pivot | all | 300 | 0.935700 | 0.318658 |
| v52_mean_conv5way_step10000 | roundtrip_src_pivot | v5_target | 300 | 0.935700 | 0.318658 |
| v52_mean_conv5way_step10000 | same_language_bible_adjacent | all | 300 | 0.978149 | 0.747088 |
| v52_mean_conv5way_step10000 | same_language_bible_adjacent | v5_target | 300 | 0.978149 | 0.747088 |
| v52_mean_conv5way_step10000 | same_language_tatoeba_adjacent | all | 300 | 0.943177 | 0.374465 |
| v52_mean_conv5way_step10000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943177 | 0.374465 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
