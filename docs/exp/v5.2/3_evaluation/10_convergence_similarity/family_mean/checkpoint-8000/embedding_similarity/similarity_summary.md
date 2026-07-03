# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step8000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step8000 | aligned_bible_src_eng | all | 300 | 0.899489 | -0.033411 |
| v52_family_mean_conv5way_step8000 | aligned_bible_src_eng | v5_target | 300 | 0.899489 | -0.033411 |
| v52_family_mean_conv5way_step8000 | aligned_tatoeba_src_eng | all | 300 | 0.914802 | 0.175360 |
| v52_family_mean_conv5way_step8000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.914802 | 0.175360 |
| v52_family_mean_conv5way_step8000 | roundtrip_eng_pivot | all | 300 | 0.903396 | -0.043482 |
| v52_family_mean_conv5way_step8000 | roundtrip_eng_pivot | v5_target | 300 | 0.903396 | -0.043482 |
| v52_family_mean_conv5way_step8000 | roundtrip_src_eng | all | 300 | 0.895687 | -0.055079 |
| v52_family_mean_conv5way_step8000 | roundtrip_src_eng | v5_target | 300 | 0.895687 | -0.055079 |
| v52_family_mean_conv5way_step8000 | roundtrip_src_pivot | all | 300 | 0.935224 | 0.387759 |
| v52_family_mean_conv5way_step8000 | roundtrip_src_pivot | v5_target | 300 | 0.935224 | 0.387759 |
| v52_family_mean_conv5way_step8000 | same_language_bible_adjacent | all | 300 | 0.975875 | 0.769663 |
| v52_family_mean_conv5way_step8000 | same_language_bible_adjacent | v5_target | 300 | 0.975875 | 0.769663 |
| v52_family_mean_conv5way_step8000 | same_language_tatoeba_adjacent | all | 300 | 0.946201 | 0.425846 |
| v52_family_mean_conv5way_step8000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.946201 | 0.425846 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
