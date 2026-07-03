# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step13000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step13000 | aligned_bible_src_eng | all | 300 | 0.903936 | -0.009045 |
| v52_family_mean_conv5way_step13000 | aligned_bible_src_eng | v5_target | 300 | 0.903936 | -0.009045 |
| v52_family_mean_conv5way_step13000 | aligned_tatoeba_src_eng | all | 300 | 0.914859 | 0.184658 |
| v52_family_mean_conv5way_step13000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.914859 | 0.184658 |
| v52_family_mean_conv5way_step13000 | roundtrip_eng_pivot | all | 300 | 0.906436 | -0.023015 |
| v52_family_mean_conv5way_step13000 | roundtrip_eng_pivot | v5_target | 300 | 0.906436 | -0.023015 |
| v52_family_mean_conv5way_step13000 | roundtrip_src_eng | all | 300 | 0.900348 | -0.030485 |
| v52_family_mean_conv5way_step13000 | roundtrip_src_eng | v5_target | 300 | 0.900348 | -0.030485 |
| v52_family_mean_conv5way_step13000 | roundtrip_src_pivot | all | 300 | 0.935976 | 0.365405 |
| v52_family_mean_conv5way_step13000 | roundtrip_src_pivot | v5_target | 300 | 0.935976 | 0.365405 |
| v52_family_mean_conv5way_step13000 | same_language_bible_adjacent | all | 300 | 0.976915 | 0.765063 |
| v52_family_mean_conv5way_step13000 | same_language_bible_adjacent | v5_target | 300 | 0.976915 | 0.765063 |
| v52_family_mean_conv5way_step13000 | same_language_tatoeba_adjacent | all | 300 | 0.943301 | 0.408294 |
| v52_family_mean_conv5way_step13000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943301 | 0.408294 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
