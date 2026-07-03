# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step29000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step29000 | aligned_bible_src_eng | all | 300 | 0.914190 | 0.036425 |
| v52_family_mean_conv5way_step29000 | aligned_bible_src_eng | v5_target | 300 | 0.914190 | 0.036425 |
| v52_family_mean_conv5way_step29000 | aligned_tatoeba_src_eng | all | 300 | 0.921160 | 0.200421 |
| v52_family_mean_conv5way_step29000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.921160 | 0.200421 |
| v52_family_mean_conv5way_step29000 | roundtrip_eng_pivot | all | 300 | 0.911977 | 0.001529 |
| v52_family_mean_conv5way_step29000 | roundtrip_eng_pivot | v5_target | 300 | 0.911977 | 0.001529 |
| v52_family_mean_conv5way_step29000 | roundtrip_src_eng | all | 300 | 0.911063 | 0.014683 |
| v52_family_mean_conv5way_step29000 | roundtrip_src_eng | v5_target | 300 | 0.911063 | 0.014683 |
| v52_family_mean_conv5way_step29000 | roundtrip_src_pivot | all | 300 | 0.935346 | 0.338453 |
| v52_family_mean_conv5way_step29000 | roundtrip_src_pivot | v5_target | 300 | 0.935346 | 0.338453 |
| v52_family_mean_conv5way_step29000 | same_language_bible_adjacent | all | 300 | 0.978100 | 0.763184 |
| v52_family_mean_conv5way_step29000 | same_language_bible_adjacent | v5_target | 300 | 0.978100 | 0.763184 |
| v52_family_mean_conv5way_step29000 | same_language_tatoeba_adjacent | all | 300 | 0.946731 | 0.410582 |
| v52_family_mean_conv5way_step29000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.946731 | 0.410582 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
