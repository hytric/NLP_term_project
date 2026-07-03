# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step29000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step29000 | aligned_bible_src_eng | all | 300 | 0.922880 | 0.055656 |
| v52_mean_conv5way_step29000 | aligned_bible_src_eng | v5_target | 300 | 0.922880 | 0.055656 |
| v52_mean_conv5way_step29000 | aligned_tatoeba_src_eng | all | 300 | 0.925711 | 0.195255 |
| v52_mean_conv5way_step29000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925711 | 0.195255 |
| v52_mean_conv5way_step29000 | roundtrip_eng_pivot | all | 300 | 0.919856 | 0.029139 |
| v52_mean_conv5way_step29000 | roundtrip_eng_pivot | v5_target | 300 | 0.919856 | 0.029139 |
| v52_mean_conv5way_step29000 | roundtrip_src_eng | all | 300 | 0.920487 | 0.035290 |
| v52_mean_conv5way_step29000 | roundtrip_src_eng | v5_target | 300 | 0.920487 | 0.035290 |
| v52_mean_conv5way_step29000 | roundtrip_src_pivot | all | 300 | 0.938037 | 0.314912 |
| v52_mean_conv5way_step29000 | roundtrip_src_pivot | v5_target | 300 | 0.938037 | 0.314912 |
| v52_mean_conv5way_step29000 | same_language_bible_adjacent | all | 300 | 0.979069 | 0.747604 |
| v52_mean_conv5way_step29000 | same_language_bible_adjacent | v5_target | 300 | 0.979069 | 0.747604 |
| v52_mean_conv5way_step29000 | same_language_tatoeba_adjacent | all | 300 | 0.946007 | 0.380095 |
| v52_mean_conv5way_step29000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.946007 | 0.380095 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
