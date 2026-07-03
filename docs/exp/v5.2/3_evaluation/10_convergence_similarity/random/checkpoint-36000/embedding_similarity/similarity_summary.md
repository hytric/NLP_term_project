# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step36000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step36000 | aligned_bible_src_eng | all | 300 | 0.921602 | 0.043875 |
| v52_random_conv5way_step36000 | aligned_bible_src_eng | v5_target | 300 | 0.921602 | 0.043875 |
| v52_random_conv5way_step36000 | aligned_tatoeba_src_eng | all | 300 | 0.922889 | 0.187110 |
| v52_random_conv5way_step36000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922889 | 0.187110 |
| v52_random_conv5way_step36000 | roundtrip_eng_pivot | all | 300 | 0.919262 | 0.020085 |
| v52_random_conv5way_step36000 | roundtrip_eng_pivot | v5_target | 300 | 0.919262 | 0.020085 |
| v52_random_conv5way_step36000 | roundtrip_src_eng | all | 300 | 0.918396 | 0.021876 |
| v52_random_conv5way_step36000 | roundtrip_src_eng | v5_target | 300 | 0.918396 | 0.021876 |
| v52_random_conv5way_step36000 | roundtrip_src_pivot | all | 300 | 0.938918 | 0.341375 |
| v52_random_conv5way_step36000 | roundtrip_src_pivot | v5_target | 300 | 0.938918 | 0.341375 |
| v52_random_conv5way_step36000 | same_language_bible_adjacent | all | 300 | 0.977966 | 0.744175 |
| v52_random_conv5way_step36000 | same_language_bible_adjacent | v5_target | 300 | 0.977966 | 0.744175 |
| v52_random_conv5way_step36000 | same_language_tatoeba_adjacent | all | 300 | 0.943530 | 0.355129 |
| v52_random_conv5way_step36000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943530 | 0.355129 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
