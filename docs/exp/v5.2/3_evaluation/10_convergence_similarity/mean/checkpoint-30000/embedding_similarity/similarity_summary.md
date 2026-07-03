# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step30000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step30000 | aligned_bible_src_eng | all | 300 | 0.922600 | 0.054462 |
| v52_mean_conv5way_step30000 | aligned_bible_src_eng | v5_target | 300 | 0.922600 | 0.054462 |
| v52_mean_conv5way_step30000 | aligned_tatoeba_src_eng | all | 300 | 0.925442 | 0.195137 |
| v52_mean_conv5way_step30000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925442 | 0.195137 |
| v52_mean_conv5way_step30000 | roundtrip_eng_pivot | all | 300 | 0.919672 | 0.028536 |
| v52_mean_conv5way_step30000 | roundtrip_eng_pivot | v5_target | 300 | 0.919672 | 0.028536 |
| v52_mean_conv5way_step30000 | roundtrip_src_eng | all | 300 | 0.920198 | 0.034043 |
| v52_mean_conv5way_step30000 | roundtrip_src_eng | v5_target | 300 | 0.920198 | 0.034043 |
| v52_mean_conv5way_step30000 | roundtrip_src_pivot | all | 300 | 0.938081 | 0.316284 |
| v52_mean_conv5way_step30000 | roundtrip_src_pivot | v5_target | 300 | 0.938081 | 0.316284 |
| v52_mean_conv5way_step30000 | same_language_bible_adjacent | all | 300 | 0.979057 | 0.748032 |
| v52_mean_conv5way_step30000 | same_language_bible_adjacent | v5_target | 300 | 0.979057 | 0.748032 |
| v52_mean_conv5way_step30000 | same_language_tatoeba_adjacent | all | 300 | 0.945748 | 0.379492 |
| v52_mean_conv5way_step30000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945748 | 0.379492 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
