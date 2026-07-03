# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step25000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step25000 | aligned_bible_src_eng | all | 300 | 0.922273 | 0.055034 |
| v52_mean_conv5way_step25000 | aligned_bible_src_eng | v5_target | 300 | 0.922273 | 0.055034 |
| v52_mean_conv5way_step25000 | aligned_tatoeba_src_eng | all | 300 | 0.924992 | 0.194760 |
| v52_mean_conv5way_step25000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.924992 | 0.194760 |
| v52_mean_conv5way_step25000 | roundtrip_eng_pivot | all | 300 | 0.919320 | 0.029162 |
| v52_mean_conv5way_step25000 | roundtrip_eng_pivot | v5_target | 300 | 0.919320 | 0.029162 |
| v52_mean_conv5way_step25000 | roundtrip_src_eng | all | 300 | 0.919860 | 0.034505 |
| v52_mean_conv5way_step25000 | roundtrip_src_eng | v5_target | 300 | 0.919860 | 0.034505 |
| v52_mean_conv5way_step25000 | roundtrip_src_pivot | all | 300 | 0.937690 | 0.314157 |
| v52_mean_conv5way_step25000 | roundtrip_src_pivot | v5_target | 300 | 0.937690 | 0.314157 |
| v52_mean_conv5way_step25000 | same_language_bible_adjacent | all | 300 | 0.978963 | 0.747845 |
| v52_mean_conv5way_step25000 | same_language_bible_adjacent | v5_target | 300 | 0.978963 | 0.747845 |
| v52_mean_conv5way_step25000 | same_language_tatoeba_adjacent | all | 300 | 0.945501 | 0.379343 |
| v52_mean_conv5way_step25000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945501 | 0.379343 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
