# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step9000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step9000 | aligned_bible_src_eng | all | 300 | 0.899789 | -0.040443 |
| v52_family_mean_conv5way_step9000 | aligned_bible_src_eng | v5_target | 300 | 0.899789 | -0.040443 |
| v52_family_mean_conv5way_step9000 | aligned_tatoeba_src_eng | all | 300 | 0.912959 | 0.169723 |
| v52_family_mean_conv5way_step9000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.912959 | 0.169723 |
| v52_family_mean_conv5way_step9000 | roundtrip_eng_pivot | all | 300 | 0.902028 | -0.054851 |
| v52_family_mean_conv5way_step9000 | roundtrip_eng_pivot | v5_target | 300 | 0.902028 | -0.054851 |
| v52_family_mean_conv5way_step9000 | roundtrip_src_eng | all | 300 | 0.896018 | -0.062181 |
| v52_family_mean_conv5way_step9000 | roundtrip_src_eng | v5_target | 300 | 0.896018 | -0.062181 |
| v52_family_mean_conv5way_step9000 | roundtrip_src_pivot | all | 300 | 0.936668 | 0.386656 |
| v52_family_mean_conv5way_step9000 | roundtrip_src_pivot | v5_target | 300 | 0.936668 | 0.386656 |
| v52_family_mean_conv5way_step9000 | same_language_bible_adjacent | all | 300 | 0.977382 | 0.775617 |
| v52_family_mean_conv5way_step9000 | same_language_bible_adjacent | v5_target | 300 | 0.977382 | 0.775617 |
| v52_family_mean_conv5way_step9000 | same_language_tatoeba_adjacent | all | 300 | 0.943973 | 0.415220 |
| v52_family_mean_conv5way_step9000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943973 | 0.415220 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
