# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step11000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step11000 | aligned_bible_src_eng | all | 300 | 0.917866 | 0.043574 |
| v52_mean_conv5way_step11000 | aligned_bible_src_eng | v5_target | 300 | 0.917866 | 0.043574 |
| v52_mean_conv5way_step11000 | aligned_tatoeba_src_eng | all | 300 | 0.920742 | 0.187061 |
| v52_mean_conv5way_step11000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.920742 | 0.187061 |
| v52_mean_conv5way_step11000 | roundtrip_eng_pivot | all | 300 | 0.916548 | 0.028026 |
| v52_mean_conv5way_step11000 | roundtrip_eng_pivot | v5_target | 300 | 0.916548 | 0.028026 |
| v52_mean_conv5way_step11000 | roundtrip_src_eng | all | 300 | 0.915434 | 0.024873 |
| v52_mean_conv5way_step11000 | roundtrip_src_eng | v5_target | 300 | 0.915434 | 0.024873 |
| v52_mean_conv5way_step11000 | roundtrip_src_pivot | all | 300 | 0.936510 | 0.311984 |
| v52_mean_conv5way_step11000 | roundtrip_src_pivot | v5_target | 300 | 0.936510 | 0.311984 |
| v52_mean_conv5way_step11000 | same_language_bible_adjacent | all | 300 | 0.978410 | 0.745880 |
| v52_mean_conv5way_step11000 | same_language_bible_adjacent | v5_target | 300 | 0.978410 | 0.745880 |
| v52_mean_conv5way_step11000 | same_language_tatoeba_adjacent | all | 300 | 0.942845 | 0.370359 |
| v52_mean_conv5way_step11000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.942845 | 0.370359 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
