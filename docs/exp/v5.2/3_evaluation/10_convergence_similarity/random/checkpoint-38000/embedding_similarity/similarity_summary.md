# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step38000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step38000 | aligned_bible_src_eng | all | 300 | 0.921831 | 0.044701 |
| v52_random_conv5way_step38000 | aligned_bible_src_eng | v5_target | 300 | 0.921831 | 0.044701 |
| v52_random_conv5way_step38000 | aligned_tatoeba_src_eng | all | 300 | 0.923109 | 0.187950 |
| v52_random_conv5way_step38000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.923109 | 0.187950 |
| v52_random_conv5way_step38000 | roundtrip_eng_pivot | all | 300 | 0.919463 | 0.020750 |
| v52_random_conv5way_step38000 | roundtrip_eng_pivot | v5_target | 300 | 0.919463 | 0.020750 |
| v52_random_conv5way_step38000 | roundtrip_src_eng | all | 300 | 0.918641 | 0.022723 |
| v52_random_conv5way_step38000 | roundtrip_src_eng | v5_target | 300 | 0.918641 | 0.022723 |
| v52_random_conv5way_step38000 | roundtrip_src_pivot | all | 300 | 0.939027 | 0.341672 |
| v52_random_conv5way_step38000 | roundtrip_src_pivot | v5_target | 300 | 0.939027 | 0.341672 |
| v52_random_conv5way_step38000 | same_language_bible_adjacent | all | 300 | 0.978015 | 0.744463 |
| v52_random_conv5way_step38000 | same_language_bible_adjacent | v5_target | 300 | 0.978015 | 0.744463 |
| v52_random_conv5way_step38000 | same_language_tatoeba_adjacent | all | 300 | 0.943661 | 0.355125 |
| v52_random_conv5way_step38000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943661 | 0.355125 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
