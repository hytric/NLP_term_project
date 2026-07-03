# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step25000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step25000 | aligned_bible_src_eng | all | 300 | 0.912828 | 0.026954 |
| v52_family_mean_conv5way_step25000 | aligned_bible_src_eng | v5_target | 300 | 0.912828 | 0.026954 |
| v52_family_mean_conv5way_step25000 | aligned_tatoeba_src_eng | all | 300 | 0.921121 | 0.202924 |
| v52_family_mean_conv5way_step25000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.921121 | 0.202924 |
| v52_family_mean_conv5way_step25000 | roundtrip_eng_pivot | all | 300 | 0.911069 | -0.010523 |
| v52_family_mean_conv5way_step25000 | roundtrip_eng_pivot | v5_target | 300 | 0.911069 | -0.010523 |
| v52_family_mean_conv5way_step25000 | roundtrip_src_eng | all | 300 | 0.909524 | 0.003967 |
| v52_family_mean_conv5way_step25000 | roundtrip_src_eng | v5_target | 300 | 0.909524 | 0.003967 |
| v52_family_mean_conv5way_step25000 | roundtrip_src_pivot | all | 300 | 0.937601 | 0.360623 |
| v52_family_mean_conv5way_step25000 | roundtrip_src_pivot | v5_target | 300 | 0.937601 | 0.360623 |
| v52_family_mean_conv5way_step25000 | same_language_bible_adjacent | all | 300 | 0.977931 | 0.764565 |
| v52_family_mean_conv5way_step25000 | same_language_bible_adjacent | v5_target | 300 | 0.977931 | 0.764565 |
| v52_family_mean_conv5way_step25000 | same_language_tatoeba_adjacent | all | 300 | 0.946941 | 0.411086 |
| v52_family_mean_conv5way_step25000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.946941 | 0.411086 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
