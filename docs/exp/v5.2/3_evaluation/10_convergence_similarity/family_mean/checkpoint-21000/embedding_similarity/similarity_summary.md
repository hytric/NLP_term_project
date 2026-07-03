# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step21000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step21000 | aligned_bible_src_eng | all | 300 | 0.913457 | 0.031230 |
| v52_family_mean_conv5way_step21000 | aligned_bible_src_eng | v5_target | 300 | 0.913457 | 0.031230 |
| v52_family_mean_conv5way_step21000 | aligned_tatoeba_src_eng | all | 300 | 0.920733 | 0.200684 |
| v52_family_mean_conv5way_step21000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.920733 | 0.200684 |
| v52_family_mean_conv5way_step21000 | roundtrip_eng_pivot | all | 300 | 0.913236 | 0.003641 |
| v52_family_mean_conv5way_step21000 | roundtrip_eng_pivot | v5_target | 300 | 0.913236 | 0.003641 |
| v52_family_mean_conv5way_step21000 | roundtrip_src_eng | all | 300 | 0.910116 | 0.008712 |
| v52_family_mean_conv5way_step21000 | roundtrip_src_eng | v5_target | 300 | 0.910116 | 0.008712 |
| v52_family_mean_conv5way_step21000 | roundtrip_src_pivot | all | 300 | 0.939159 | 0.362748 |
| v52_family_mean_conv5way_step21000 | roundtrip_src_pivot | v5_target | 300 | 0.939159 | 0.362748 |
| v52_family_mean_conv5way_step21000 | same_language_bible_adjacent | all | 300 | 0.978131 | 0.764847 |
| v52_family_mean_conv5way_step21000 | same_language_bible_adjacent | v5_target | 300 | 0.978131 | 0.764847 |
| v52_family_mean_conv5way_step21000 | same_language_tatoeba_adjacent | all | 300 | 0.945204 | 0.403501 |
| v52_family_mean_conv5way_step21000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945204 | 0.403501 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
