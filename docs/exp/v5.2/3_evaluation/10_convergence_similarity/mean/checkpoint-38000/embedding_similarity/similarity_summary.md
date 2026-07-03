# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step38000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step38000 | aligned_bible_src_eng | all | 300 | 0.922625 | 0.055491 |
| v52_mean_conv5way_step38000 | aligned_bible_src_eng | v5_target | 300 | 0.922625 | 0.055491 |
| v52_mean_conv5way_step38000 | aligned_tatoeba_src_eng | all | 300 | 0.925704 | 0.196653 |
| v52_mean_conv5way_step38000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925704 | 0.196653 |
| v52_mean_conv5way_step38000 | roundtrip_eng_pivot | all | 300 | 0.919648 | 0.029499 |
| v52_mean_conv5way_step38000 | roundtrip_eng_pivot | v5_target | 300 | 0.919648 | 0.029499 |
| v52_mean_conv5way_step38000 | roundtrip_src_eng | all | 300 | 0.920264 | 0.035480 |
| v52_mean_conv5way_step38000 | roundtrip_src_eng | v5_target | 300 | 0.920264 | 0.035480 |
| v52_mean_conv5way_step38000 | roundtrip_src_pivot | all | 300 | 0.937881 | 0.315001 |
| v52_mean_conv5way_step38000 | roundtrip_src_pivot | v5_target | 300 | 0.937881 | 0.315001 |
| v52_mean_conv5way_step38000 | same_language_bible_adjacent | all | 300 | 0.979034 | 0.748156 |
| v52_mean_conv5way_step38000 | same_language_bible_adjacent | v5_target | 300 | 0.979034 | 0.748156 |
| v52_mean_conv5way_step38000 | same_language_tatoeba_adjacent | all | 300 | 0.945829 | 0.379926 |
| v52_mean_conv5way_step38000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945829 | 0.379926 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
