# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step6000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step6000 | aligned_bible_src_eng | all | 300 | 0.911664 | 0.015752 |
| v52_mean_conv5way_step6000 | aligned_bible_src_eng | v5_target | 300 | 0.911664 | 0.015752 |
| v52_mean_conv5way_step6000 | aligned_tatoeba_src_eng | all | 300 | 0.915511 | 0.171332 |
| v52_mean_conv5way_step6000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.915511 | 0.171332 |
| v52_mean_conv5way_step6000 | roundtrip_eng_pivot | all | 300 | 0.909623 | -0.000903 |
| v52_mean_conv5way_step6000 | roundtrip_eng_pivot | v5_target | 300 | 0.909623 | -0.000903 |
| v52_mean_conv5way_step6000 | roundtrip_src_eng | all | 300 | 0.908747 | -0.004028 |
| v52_mean_conv5way_step6000 | roundtrip_src_eng | v5_target | 300 | 0.908747 | -0.004028 |
| v52_mean_conv5way_step6000 | roundtrip_src_pivot | all | 300 | 0.937463 | 0.346389 |
| v52_mean_conv5way_step6000 | roundtrip_src_pivot | v5_target | 300 | 0.937463 | 0.346389 |
| v52_mean_conv5way_step6000 | same_language_bible_adjacent | all | 300 | 0.978092 | 0.752674 |
| v52_mean_conv5way_step6000 | same_language_bible_adjacent | v5_target | 300 | 0.978092 | 0.752674 |
| v52_mean_conv5way_step6000 | same_language_tatoeba_adjacent | all | 300 | 0.939626 | 0.366951 |
| v52_mean_conv5way_step6000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.939626 | 0.366951 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
