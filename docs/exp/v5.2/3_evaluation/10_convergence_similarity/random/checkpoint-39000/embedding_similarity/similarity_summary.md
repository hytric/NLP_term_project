# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step39000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step39000 | aligned_bible_src_eng | all | 300 | 0.921698 | 0.043962 |
| v52_random_conv5way_step39000 | aligned_bible_src_eng | v5_target | 300 | 0.921698 | 0.043962 |
| v52_random_conv5way_step39000 | aligned_tatoeba_src_eng | all | 300 | 0.923072 | 0.187108 |
| v52_random_conv5way_step39000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.923072 | 0.187108 |
| v52_random_conv5way_step39000 | roundtrip_eng_pivot | all | 300 | 0.919326 | 0.020112 |
| v52_random_conv5way_step39000 | roundtrip_eng_pivot | v5_target | 300 | 0.919326 | 0.020112 |
| v52_random_conv5way_step39000 | roundtrip_src_eng | all | 300 | 0.918495 | 0.021884 |
| v52_random_conv5way_step39000 | roundtrip_src_eng | v5_target | 300 | 0.918495 | 0.021884 |
| v52_random_conv5way_step39000 | roundtrip_src_pivot | all | 300 | 0.938979 | 0.341693 |
| v52_random_conv5way_step39000 | roundtrip_src_pivot | v5_target | 300 | 0.938979 | 0.341693 |
| v52_random_conv5way_step39000 | same_language_bible_adjacent | all | 300 | 0.978015 | 0.744635 |
| v52_random_conv5way_step39000 | same_language_bible_adjacent | v5_target | 300 | 0.978015 | 0.744635 |
| v52_random_conv5way_step39000 | same_language_tatoeba_adjacent | all | 300 | 0.943779 | 0.355910 |
| v52_random_conv5way_step39000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943779 | 0.355910 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
