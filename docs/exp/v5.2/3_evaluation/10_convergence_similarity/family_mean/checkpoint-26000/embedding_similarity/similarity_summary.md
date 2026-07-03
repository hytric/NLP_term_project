# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step26000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step26000 | aligned_bible_src_eng | all | 300 | 0.910371 | 0.021758 |
| v52_family_mean_conv5way_step26000 | aligned_bible_src_eng | v5_target | 300 | 0.910371 | 0.021758 |
| v52_family_mean_conv5way_step26000 | aligned_tatoeba_src_eng | all | 300 | 0.920018 | 0.204650 |
| v52_family_mean_conv5way_step26000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.920018 | 0.204650 |
| v52_family_mean_conv5way_step26000 | roundtrip_eng_pivot | all | 300 | 0.908936 | -0.011731 |
| v52_family_mean_conv5way_step26000 | roundtrip_eng_pivot | v5_target | 300 | 0.908936 | -0.011731 |
| v52_family_mean_conv5way_step26000 | roundtrip_src_eng | all | 300 | 0.906893 | -0.001229 |
| v52_family_mean_conv5way_step26000 | roundtrip_src_eng | v5_target | 300 | 0.906893 | -0.001229 |
| v52_family_mean_conv5way_step26000 | roundtrip_src_pivot | all | 300 | 0.936136 | 0.356867 |
| v52_family_mean_conv5way_step26000 | roundtrip_src_pivot | v5_target | 300 | 0.936136 | 0.356867 |
| v52_family_mean_conv5way_step26000 | same_language_bible_adjacent | all | 300 | 0.977747 | 0.766990 |
| v52_family_mean_conv5way_step26000 | same_language_bible_adjacent | v5_target | 300 | 0.977747 | 0.766990 |
| v52_family_mean_conv5way_step26000 | same_language_tatoeba_adjacent | all | 300 | 0.945743 | 0.412750 |
| v52_family_mean_conv5way_step26000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945743 | 0.412750 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
