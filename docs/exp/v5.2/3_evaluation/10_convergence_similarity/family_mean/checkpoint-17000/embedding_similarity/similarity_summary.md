# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step17000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step17000 | aligned_bible_src_eng | all | 300 | 0.906520 | 0.001091 |
| v52_family_mean_conv5way_step17000 | aligned_bible_src_eng | v5_target | 300 | 0.906520 | 0.001091 |
| v52_family_mean_conv5way_step17000 | aligned_tatoeba_src_eng | all | 300 | 0.919984 | 0.199951 |
| v52_family_mean_conv5way_step17000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.919984 | 0.199951 |
| v52_family_mean_conv5way_step17000 | roundtrip_eng_pivot | all | 300 | 0.906529 | -0.022673 |
| v52_family_mean_conv5way_step17000 | roundtrip_eng_pivot | v5_target | 300 | 0.906529 | -0.022673 |
| v52_family_mean_conv5way_step17000 | roundtrip_src_eng | all | 300 | 0.903014 | -0.021780 |
| v52_family_mean_conv5way_step17000 | roundtrip_src_eng | v5_target | 300 | 0.903014 | -0.021780 |
| v52_family_mean_conv5way_step17000 | roundtrip_src_pivot | all | 300 | 0.937088 | 0.373396 |
| v52_family_mean_conv5way_step17000 | roundtrip_src_pivot | v5_target | 300 | 0.937088 | 0.373396 |
| v52_family_mean_conv5way_step17000 | same_language_bible_adjacent | all | 300 | 0.977900 | 0.771560 |
| v52_family_mean_conv5way_step17000 | same_language_bible_adjacent | v5_target | 300 | 0.977900 | 0.771560 |
| v52_family_mean_conv5way_step17000 | same_language_tatoeba_adjacent | all | 300 | 0.946905 | 0.411548 |
| v52_family_mean_conv5way_step17000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.946905 | 0.411548 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
