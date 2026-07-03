# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step24000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step24000 | aligned_bible_src_eng | all | 300 | 0.921994 | 0.053394 |
| v52_mean_conv5way_step24000 | aligned_bible_src_eng | v5_target | 300 | 0.921994 | 0.053394 |
| v52_mean_conv5way_step24000 | aligned_tatoeba_src_eng | all | 300 | 0.924909 | 0.193870 |
| v52_mean_conv5way_step24000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.924909 | 0.193870 |
| v52_mean_conv5way_step24000 | roundtrip_eng_pivot | all | 300 | 0.919088 | 0.027792 |
| v52_mean_conv5way_step24000 | roundtrip_eng_pivot | v5_target | 300 | 0.919088 | 0.027792 |
| v52_mean_conv5way_step24000 | roundtrip_src_eng | all | 300 | 0.919597 | 0.033065 |
| v52_mean_conv5way_step24000 | roundtrip_src_eng | v5_target | 300 | 0.919597 | 0.033065 |
| v52_mean_conv5way_step24000 | roundtrip_src_pivot | all | 300 | 0.937550 | 0.314855 |
| v52_mean_conv5way_step24000 | roundtrip_src_pivot | v5_target | 300 | 0.937550 | 0.314855 |
| v52_mean_conv5way_step24000 | same_language_bible_adjacent | all | 300 | 0.978933 | 0.748298 |
| v52_mean_conv5way_step24000 | same_language_bible_adjacent | v5_target | 300 | 0.978933 | 0.748298 |
| v52_mean_conv5way_step24000 | same_language_tatoeba_adjacent | all | 300 | 0.945503 | 0.379901 |
| v52_mean_conv5way_step24000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945503 | 0.379901 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
