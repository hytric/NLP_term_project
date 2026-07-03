# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step32000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step32000 | aligned_bible_src_eng | all | 300 | 0.922597 | 0.056776 |
| v52_mean_conv5way_step32000 | aligned_bible_src_eng | v5_target | 300 | 0.922597 | 0.056776 |
| v52_mean_conv5way_step32000 | aligned_tatoeba_src_eng | all | 300 | 0.925247 | 0.195477 |
| v52_mean_conv5way_step32000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925247 | 0.195477 |
| v52_mean_conv5way_step32000 | roundtrip_eng_pivot | all | 300 | 0.919594 | 0.030484 |
| v52_mean_conv5way_step32000 | roundtrip_eng_pivot | v5_target | 300 | 0.919594 | 0.030484 |
| v52_mean_conv5way_step32000 | roundtrip_src_eng | all | 300 | 0.920207 | 0.036530 |
| v52_mean_conv5way_step32000 | roundtrip_src_eng | v5_target | 300 | 0.920207 | 0.036530 |
| v52_mean_conv5way_step32000 | roundtrip_src_pivot | all | 300 | 0.937926 | 0.315773 |
| v52_mean_conv5way_step32000 | roundtrip_src_pivot | v5_target | 300 | 0.937926 | 0.315773 |
| v52_mean_conv5way_step32000 | same_language_bible_adjacent | all | 300 | 0.978966 | 0.747353 |
| v52_mean_conv5way_step32000 | same_language_bible_adjacent | v5_target | 300 | 0.978966 | 0.747353 |
| v52_mean_conv5way_step32000 | same_language_tatoeba_adjacent | all | 300 | 0.945599 | 0.379807 |
| v52_mean_conv5way_step32000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945599 | 0.379807 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
