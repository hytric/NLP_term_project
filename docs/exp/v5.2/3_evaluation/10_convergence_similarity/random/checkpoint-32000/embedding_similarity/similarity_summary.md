# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step32000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step32000 | aligned_bible_src_eng | all | 300 | 0.921558 | 0.045019 |
| v52_random_conv5way_step32000 | aligned_bible_src_eng | v5_target | 300 | 0.921558 | 0.045019 |
| v52_random_conv5way_step32000 | aligned_tatoeba_src_eng | all | 300 | 0.922607 | 0.187587 |
| v52_random_conv5way_step32000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922607 | 0.187587 |
| v52_random_conv5way_step32000 | roundtrip_eng_pivot | all | 300 | 0.919230 | 0.021336 |
| v52_random_conv5way_step32000 | roundtrip_eng_pivot | v5_target | 300 | 0.919230 | 0.021336 |
| v52_random_conv5way_step32000 | roundtrip_src_eng | all | 300 | 0.918351 | 0.022932 |
| v52_random_conv5way_step32000 | roundtrip_src_eng | v5_target | 300 | 0.918351 | 0.022932 |
| v52_random_conv5way_step32000 | roundtrip_src_pivot | all | 300 | 0.938941 | 0.342076 |
| v52_random_conv5way_step32000 | roundtrip_src_pivot | v5_target | 300 | 0.938941 | 0.342076 |
| v52_random_conv5way_step32000 | same_language_bible_adjacent | all | 300 | 0.977937 | 0.744062 |
| v52_random_conv5way_step32000 | same_language_bible_adjacent | v5_target | 300 | 0.977937 | 0.744062 |
| v52_random_conv5way_step32000 | same_language_tatoeba_adjacent | all | 300 | 0.943396 | 0.355140 |
| v52_random_conv5way_step32000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943396 | 0.355140 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
