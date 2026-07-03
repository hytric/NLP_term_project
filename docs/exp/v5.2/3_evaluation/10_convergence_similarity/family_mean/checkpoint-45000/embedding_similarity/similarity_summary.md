# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step45000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step45000 | aligned_bible_src_eng | all | 300 | 0.917906 | 0.044556 |
| v52_family_mean_conv5way_step45000 | aligned_bible_src_eng | v5_target | 300 | 0.917906 | 0.044556 |
| v52_family_mean_conv5way_step45000 | aligned_tatoeba_src_eng | all | 300 | 0.926415 | 0.211128 |
| v52_family_mean_conv5way_step45000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926415 | 0.211128 |
| v52_family_mean_conv5way_step45000 | roundtrip_eng_pivot | all | 300 | 0.915520 | 0.007367 |
| v52_family_mean_conv5way_step45000 | roundtrip_eng_pivot | v5_target | 300 | 0.915520 | 0.007367 |
| v52_family_mean_conv5way_step45000 | roundtrip_src_eng | all | 300 | 0.914660 | 0.021687 |
| v52_family_mean_conv5way_step45000 | roundtrip_src_eng | v5_target | 300 | 0.914660 | 0.021687 |
| v52_family_mean_conv5way_step45000 | roundtrip_src_pivot | all | 300 | 0.937363 | 0.336914 |
| v52_family_mean_conv5way_step45000 | roundtrip_src_pivot | v5_target | 300 | 0.937363 | 0.336914 |
| v52_family_mean_conv5way_step45000 | same_language_bible_adjacent | all | 300 | 0.978588 | 0.760983 |
| v52_family_mean_conv5way_step45000 | same_language_bible_adjacent | v5_target | 300 | 0.978588 | 0.760983 |
| v52_family_mean_conv5way_step45000 | same_language_tatoeba_adjacent | all | 300 | 0.949581 | 0.412096 |
| v52_family_mean_conv5way_step45000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.949581 | 0.412096 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
