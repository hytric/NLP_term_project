# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step18000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step18000 | aligned_bible_src_eng | all | 300 | 0.908526 | 0.017835 |
| v52_family_mean_conv5way_step18000 | aligned_bible_src_eng | v5_target | 300 | 0.908526 | 0.017835 |
| v52_family_mean_conv5way_step18000 | aligned_tatoeba_src_eng | all | 300 | 0.920171 | 0.207339 |
| v52_family_mean_conv5way_step18000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.920171 | 0.207339 |
| v52_family_mean_conv5way_step18000 | roundtrip_eng_pivot | all | 300 | 0.909434 | -0.001573 |
| v52_family_mean_conv5way_step18000 | roundtrip_eng_pivot | v5_target | 300 | 0.909434 | -0.001573 |
| v52_family_mean_conv5way_step18000 | roundtrip_src_eng | all | 300 | 0.905067 | -0.003462 |
| v52_family_mean_conv5way_step18000 | roundtrip_src_eng | v5_target | 300 | 0.905067 | -0.003462 |
| v52_family_mean_conv5way_step18000 | roundtrip_src_pivot | all | 300 | 0.937254 | 0.368068 |
| v52_family_mean_conv5way_step18000 | roundtrip_src_pivot | v5_target | 300 | 0.937254 | 0.368068 |
| v52_family_mean_conv5way_step18000 | same_language_bible_adjacent | all | 300 | 0.977714 | 0.769333 |
| v52_family_mean_conv5way_step18000 | same_language_bible_adjacent | v5_target | 300 | 0.977714 | 0.769333 |
| v52_family_mean_conv5way_step18000 | same_language_tatoeba_adjacent | all | 300 | 0.945858 | 0.406675 |
| v52_family_mean_conv5way_step18000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945858 | 0.406675 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
