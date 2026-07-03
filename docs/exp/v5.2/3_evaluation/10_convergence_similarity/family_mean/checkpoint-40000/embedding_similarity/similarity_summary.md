# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step40000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step40000 | aligned_bible_src_eng | all | 300 | 0.914057 | 0.036597 |
| v52_family_mean_conv5way_step40000 | aligned_bible_src_eng | v5_target | 300 | 0.914057 | 0.036597 |
| v52_family_mean_conv5way_step40000 | aligned_tatoeba_src_eng | all | 300 | 0.923867 | 0.208806 |
| v52_family_mean_conv5way_step40000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.923867 | 0.208806 |
| v52_family_mean_conv5way_step40000 | roundtrip_eng_pivot | all | 300 | 0.911608 | -0.001320 |
| v52_family_mean_conv5way_step40000 | roundtrip_eng_pivot | v5_target | 300 | 0.911608 | -0.001320 |
| v52_family_mean_conv5way_step40000 | roundtrip_src_eng | all | 300 | 0.910843 | 0.014584 |
| v52_family_mean_conv5way_step40000 | roundtrip_src_eng | v5_target | 300 | 0.910843 | 0.014584 |
| v52_family_mean_conv5way_step40000 | roundtrip_src_pivot | all | 300 | 0.935577 | 0.340491 |
| v52_family_mean_conv5way_step40000 | roundtrip_src_pivot | v5_target | 300 | 0.935577 | 0.340491 |
| v52_family_mean_conv5way_step40000 | same_language_bible_adjacent | all | 300 | 0.978296 | 0.766604 |
| v52_family_mean_conv5way_step40000 | same_language_bible_adjacent | v5_target | 300 | 0.978296 | 0.766604 |
| v52_family_mean_conv5way_step40000 | same_language_tatoeba_adjacent | all | 300 | 0.947586 | 0.413198 |
| v52_family_mean_conv5way_step40000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947586 | 0.413198 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
