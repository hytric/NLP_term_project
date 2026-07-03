# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step29000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step29000 | aligned_bible_src_eng | all | 300 | 0.921814 | 0.043773 |
| v52_random_conv5way_step29000 | aligned_bible_src_eng | v5_target | 300 | 0.921814 | 0.043773 |
| v52_random_conv5way_step29000 | aligned_tatoeba_src_eng | all | 300 | 0.922883 | 0.186646 |
| v52_random_conv5way_step29000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922883 | 0.186646 |
| v52_random_conv5way_step29000 | roundtrip_eng_pivot | all | 300 | 0.919558 | 0.020230 |
| v52_random_conv5way_step29000 | roundtrip_eng_pivot | v5_target | 300 | 0.919558 | 0.020230 |
| v52_random_conv5way_step29000 | roundtrip_src_eng | all | 300 | 0.918613 | 0.021711 |
| v52_random_conv5way_step29000 | roundtrip_src_eng | v5_target | 300 | 0.918613 | 0.021711 |
| v52_random_conv5way_step29000 | roundtrip_src_pivot | all | 300 | 0.938884 | 0.340126 |
| v52_random_conv5way_step29000 | roundtrip_src_pivot | v5_target | 300 | 0.938884 | 0.340126 |
| v52_random_conv5way_step29000 | same_language_bible_adjacent | all | 300 | 0.977943 | 0.743774 |
| v52_random_conv5way_step29000 | same_language_bible_adjacent | v5_target | 300 | 0.977943 | 0.743774 |
| v52_random_conv5way_step29000 | same_language_tatoeba_adjacent | all | 300 | 0.943626 | 0.354922 |
| v52_random_conv5way_step29000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943626 | 0.354922 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
