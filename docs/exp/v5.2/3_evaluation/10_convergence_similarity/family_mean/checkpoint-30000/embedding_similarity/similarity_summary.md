# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step30000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step30000 | aligned_bible_src_eng | all | 300 | 0.915550 | 0.036782 |
| v52_family_mean_conv5way_step30000 | aligned_bible_src_eng | v5_target | 300 | 0.915550 | 0.036782 |
| v52_family_mean_conv5way_step30000 | aligned_tatoeba_src_eng | all | 300 | 0.923487 | 0.208179 |
| v52_family_mean_conv5way_step30000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.923487 | 0.208179 |
| v52_family_mean_conv5way_step30000 | roundtrip_eng_pivot | all | 300 | 0.913605 | 0.002033 |
| v52_family_mean_conv5way_step30000 | roundtrip_eng_pivot | v5_target | 300 | 0.913605 | 0.002033 |
| v52_family_mean_conv5way_step30000 | roundtrip_src_eng | all | 300 | 0.912237 | 0.013396 |
| v52_family_mean_conv5way_step30000 | roundtrip_src_eng | v5_target | 300 | 0.912237 | 0.013396 |
| v52_family_mean_conv5way_step30000 | roundtrip_src_pivot | all | 300 | 0.937515 | 0.349893 |
| v52_family_mean_conv5way_step30000 | roundtrip_src_pivot | v5_target | 300 | 0.937515 | 0.349893 |
| v52_family_mean_conv5way_step30000 | same_language_bible_adjacent | all | 300 | 0.978103 | 0.760115 |
| v52_family_mean_conv5way_step30000 | same_language_bible_adjacent | v5_target | 300 | 0.978103 | 0.760115 |
| v52_family_mean_conv5way_step30000 | same_language_tatoeba_adjacent | all | 300 | 0.947549 | 0.407226 |
| v52_family_mean_conv5way_step30000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947549 | 0.407226 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
