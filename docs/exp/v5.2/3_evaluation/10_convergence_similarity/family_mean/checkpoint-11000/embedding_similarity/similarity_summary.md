# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step11000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step11000 | aligned_bible_src_eng | all | 300 | 0.901406 | -0.037045 |
| v52_family_mean_conv5way_step11000 | aligned_bible_src_eng | v5_target | 300 | 0.901406 | -0.037045 |
| v52_family_mean_conv5way_step11000 | aligned_tatoeba_src_eng | all | 300 | 0.914732 | 0.173769 |
| v52_family_mean_conv5way_step11000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.914732 | 0.173769 |
| v52_family_mean_conv5way_step11000 | roundtrip_eng_pivot | all | 300 | 0.906211 | -0.040852 |
| v52_family_mean_conv5way_step11000 | roundtrip_eng_pivot | v5_target | 300 | 0.906211 | -0.040852 |
| v52_family_mean_conv5way_step11000 | roundtrip_src_eng | all | 300 | 0.897160 | -0.059365 |
| v52_family_mean_conv5way_step11000 | roundtrip_src_eng | v5_target | 300 | 0.897160 | -0.059365 |
| v52_family_mean_conv5way_step11000 | roundtrip_src_pivot | all | 300 | 0.935409 | 0.366455 |
| v52_family_mean_conv5way_step11000 | roundtrip_src_pivot | v5_target | 300 | 0.935409 | 0.366455 |
| v52_family_mean_conv5way_step11000 | same_language_bible_adjacent | all | 300 | 0.976452 | 0.765623 |
| v52_family_mean_conv5way_step11000 | same_language_bible_adjacent | v5_target | 300 | 0.976452 | 0.765623 |
| v52_family_mean_conv5way_step11000 | same_language_tatoeba_adjacent | all | 300 | 0.945262 | 0.416342 |
| v52_family_mean_conv5way_step11000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945262 | 0.416342 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
