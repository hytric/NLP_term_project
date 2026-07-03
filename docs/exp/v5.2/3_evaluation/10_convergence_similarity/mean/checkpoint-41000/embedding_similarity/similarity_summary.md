# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step41000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step41000 | aligned_bible_src_eng | all | 300 | 0.922833 | 0.055394 |
| v52_mean_conv5way_step41000 | aligned_bible_src_eng | v5_target | 300 | 0.922833 | 0.055394 |
| v52_mean_conv5way_step41000 | aligned_tatoeba_src_eng | all | 300 | 0.925790 | 0.195802 |
| v52_mean_conv5way_step41000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925790 | 0.195802 |
| v52_mean_conv5way_step41000 | roundtrip_eng_pivot | all | 300 | 0.919848 | 0.029430 |
| v52_mean_conv5way_step41000 | roundtrip_eng_pivot | v5_target | 300 | 0.919848 | 0.029430 |
| v52_mean_conv5way_step41000 | roundtrip_src_eng | all | 300 | 0.920465 | 0.035367 |
| v52_mean_conv5way_step41000 | roundtrip_src_eng | v5_target | 300 | 0.920465 | 0.035367 |
| v52_mean_conv5way_step41000 | roundtrip_src_pivot | all | 300 | 0.937973 | 0.315340 |
| v52_mean_conv5way_step41000 | roundtrip_src_pivot | v5_target | 300 | 0.937973 | 0.315340 |
| v52_mean_conv5way_step41000 | same_language_bible_adjacent | all | 300 | 0.979071 | 0.748286 |
| v52_mean_conv5way_step41000 | same_language_bible_adjacent | v5_target | 300 | 0.979071 | 0.748286 |
| v52_mean_conv5way_step41000 | same_language_tatoeba_adjacent | all | 300 | 0.945937 | 0.380143 |
| v52_mean_conv5way_step41000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945937 | 0.380143 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
