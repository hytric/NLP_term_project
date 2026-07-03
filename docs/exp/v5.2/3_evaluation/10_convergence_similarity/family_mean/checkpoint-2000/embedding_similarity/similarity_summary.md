# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step2000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step2000 | aligned_bible_src_eng | all | 300 | 0.892062 | -0.077845 |
| v52_family_mean_conv5way_step2000 | aligned_bible_src_eng | v5_target | 300 | 0.892062 | -0.077845 |
| v52_family_mean_conv5way_step2000 | aligned_tatoeba_src_eng | all | 300 | 0.900125 | 0.130867 |
| v52_family_mean_conv5way_step2000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.900125 | 0.130867 |
| v52_family_mean_conv5way_step2000 | roundtrip_eng_pivot | all | 300 | 0.899298 | -0.079086 |
| v52_family_mean_conv5way_step2000 | roundtrip_eng_pivot | v5_target | 300 | 0.899298 | -0.079086 |
| v52_family_mean_conv5way_step2000 | roundtrip_src_eng | all | 300 | 0.887179 | -0.103106 |
| v52_family_mean_conv5way_step2000 | roundtrip_src_eng | v5_target | 300 | 0.887179 | -0.103106 |
| v52_family_mean_conv5way_step2000 | roundtrip_src_pivot | all | 300 | 0.934836 | 0.402006 |
| v52_family_mean_conv5way_step2000 | roundtrip_src_pivot | v5_target | 300 | 0.934836 | 0.402006 |
| v52_family_mean_conv5way_step2000 | same_language_bible_adjacent | all | 300 | 0.974660 | 0.768480 |
| v52_family_mean_conv5way_step2000 | same_language_bible_adjacent | v5_target | 300 | 0.974660 | 0.768480 |
| v52_family_mean_conv5way_step2000 | same_language_tatoeba_adjacent | all | 300 | 0.936664 | 0.393229 |
| v52_family_mean_conv5way_step2000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.936664 | 0.393229 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
