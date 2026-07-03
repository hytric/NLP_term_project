# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step28000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step28000 | aligned_bible_src_eng | all | 300 | 0.911676 | 0.022278 |
| v52_family_mean_conv5way_step28000 | aligned_bible_src_eng | v5_target | 300 | 0.911676 | 0.022278 |
| v52_family_mean_conv5way_step28000 | aligned_tatoeba_src_eng | all | 300 | 0.919018 | 0.194893 |
| v52_family_mean_conv5way_step28000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.919018 | 0.194893 |
| v52_family_mean_conv5way_step28000 | roundtrip_eng_pivot | all | 300 | 0.909469 | -0.014882 |
| v52_family_mean_conv5way_step28000 | roundtrip_eng_pivot | v5_target | 300 | 0.909469 | -0.014882 |
| v52_family_mean_conv5way_step28000 | roundtrip_src_eng | all | 300 | 0.908230 | -0.001501 |
| v52_family_mean_conv5way_step28000 | roundtrip_src_eng | v5_target | 300 | 0.908230 | -0.001501 |
| v52_family_mean_conv5way_step28000 | roundtrip_src_pivot | all | 300 | 0.936020 | 0.345198 |
| v52_family_mean_conv5way_step28000 | roundtrip_src_pivot | v5_target | 300 | 0.936020 | 0.345198 |
| v52_family_mean_conv5way_step28000 | same_language_bible_adjacent | all | 300 | 0.977699 | 0.761230 |
| v52_family_mean_conv5way_step28000 | same_language_bible_adjacent | v5_target | 300 | 0.977699 | 0.761230 |
| v52_family_mean_conv5way_step28000 | same_language_tatoeba_adjacent | all | 300 | 0.945130 | 0.404157 |
| v52_family_mean_conv5way_step28000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945130 | 0.404157 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
