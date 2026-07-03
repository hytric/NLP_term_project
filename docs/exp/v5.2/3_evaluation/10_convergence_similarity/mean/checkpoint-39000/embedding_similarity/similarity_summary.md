# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step39000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step39000 | aligned_bible_src_eng | all | 300 | 0.922590 | 0.055371 |
| v52_mean_conv5way_step39000 | aligned_bible_src_eng | v5_target | 300 | 0.922590 | 0.055371 |
| v52_mean_conv5way_step39000 | aligned_tatoeba_src_eng | all | 300 | 0.925687 | 0.196221 |
| v52_mean_conv5way_step39000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925687 | 0.196221 |
| v52_mean_conv5way_step39000 | roundtrip_eng_pivot | all | 300 | 0.919648 | 0.029680 |
| v52_mean_conv5way_step39000 | roundtrip_eng_pivot | v5_target | 300 | 0.919648 | 0.029680 |
| v52_mean_conv5way_step39000 | roundtrip_src_eng | all | 300 | 0.920210 | 0.035260 |
| v52_mean_conv5way_step39000 | roundtrip_src_eng | v5_target | 300 | 0.920210 | 0.035260 |
| v52_mean_conv5way_step39000 | roundtrip_src_pivot | all | 300 | 0.937930 | 0.315384 |
| v52_mean_conv5way_step39000 | roundtrip_src_pivot | v5_target | 300 | 0.937930 | 0.315384 |
| v52_mean_conv5way_step39000 | same_language_bible_adjacent | all | 300 | 0.979047 | 0.748263 |
| v52_mean_conv5way_step39000 | same_language_bible_adjacent | v5_target | 300 | 0.979047 | 0.748263 |
| v52_mean_conv5way_step39000 | same_language_tatoeba_adjacent | all | 300 | 0.945866 | 0.380000 |
| v52_mean_conv5way_step39000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945866 | 0.380000 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
