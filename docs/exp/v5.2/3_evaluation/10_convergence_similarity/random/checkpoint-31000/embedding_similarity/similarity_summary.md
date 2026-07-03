# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step31000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step31000 | aligned_bible_src_eng | all | 300 | 0.921659 | 0.045417 |
| v52_random_conv5way_step31000 | aligned_bible_src_eng | v5_target | 300 | 0.921659 | 0.045417 |
| v52_random_conv5way_step31000 | aligned_tatoeba_src_eng | all | 300 | 0.922609 | 0.187038 |
| v52_random_conv5way_step31000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922609 | 0.187038 |
| v52_random_conv5way_step31000 | roundtrip_eng_pivot | all | 300 | 0.919311 | 0.021516 |
| v52_random_conv5way_step31000 | roundtrip_eng_pivot | v5_target | 300 | 0.919311 | 0.021516 |
| v52_random_conv5way_step31000 | roundtrip_src_eng | all | 300 | 0.918432 | 0.023189 |
| v52_random_conv5way_step31000 | roundtrip_src_eng | v5_target | 300 | 0.918432 | 0.023189 |
| v52_random_conv5way_step31000 | roundtrip_src_pivot | all | 300 | 0.938990 | 0.342491 |
| v52_random_conv5way_step31000 | roundtrip_src_pivot | v5_target | 300 | 0.938990 | 0.342491 |
| v52_random_conv5way_step31000 | same_language_bible_adjacent | all | 300 | 0.977948 | 0.744099 |
| v52_random_conv5way_step31000 | same_language_bible_adjacent | v5_target | 300 | 0.977948 | 0.744099 |
| v52_random_conv5way_step31000 | same_language_tatoeba_adjacent | all | 300 | 0.943414 | 0.354868 |
| v52_random_conv5way_step31000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943414 | 0.354868 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
