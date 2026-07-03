# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step31000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step31000 | aligned_bible_src_eng | all | 300 | 0.922500 | 0.054943 |
| v52_mean_conv5way_step31000 | aligned_bible_src_eng | v5_target | 300 | 0.922500 | 0.054943 |
| v52_mean_conv5way_step31000 | aligned_tatoeba_src_eng | all | 300 | 0.925283 | 0.195118 |
| v52_mean_conv5way_step31000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925283 | 0.195118 |
| v52_mean_conv5way_step31000 | roundtrip_eng_pivot | all | 300 | 0.919517 | 0.028719 |
| v52_mean_conv5way_step31000 | roundtrip_eng_pivot | v5_target | 300 | 0.919517 | 0.028719 |
| v52_mean_conv5way_step31000 | roundtrip_src_eng | all | 300 | 0.920100 | 0.034639 |
| v52_mean_conv5way_step31000 | roundtrip_src_eng | v5_target | 300 | 0.920100 | 0.034639 |
| v52_mean_conv5way_step31000 | roundtrip_src_pivot | all | 300 | 0.937807 | 0.315135 |
| v52_mean_conv5way_step31000 | roundtrip_src_pivot | v5_target | 300 | 0.937807 | 0.315135 |
| v52_mean_conv5way_step31000 | same_language_bible_adjacent | all | 300 | 0.978979 | 0.747816 |
| v52_mean_conv5way_step31000 | same_language_bible_adjacent | v5_target | 300 | 0.978979 | 0.747816 |
| v52_mean_conv5way_step31000 | same_language_tatoeba_adjacent | all | 300 | 0.945603 | 0.379519 |
| v52_mean_conv5way_step31000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945603 | 0.379519 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
