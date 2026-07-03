# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step7000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step7000 | aligned_bible_src_eng | all | 300 | 0.902452 | -0.044846 |
| v52_family_mean_conv5way_step7000 | aligned_bible_src_eng | v5_target | 300 | 0.902452 | -0.044846 |
| v52_family_mean_conv5way_step7000 | aligned_tatoeba_src_eng | all | 300 | 0.912878 | 0.161300 |
| v52_family_mean_conv5way_step7000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.912878 | 0.161300 |
| v52_family_mean_conv5way_step7000 | roundtrip_eng_pivot | all | 300 | 0.906903 | -0.049854 |
| v52_family_mean_conv5way_step7000 | roundtrip_eng_pivot | v5_target | 300 | 0.906903 | -0.049854 |
| v52_family_mean_conv5way_step7000 | roundtrip_src_eng | all | 300 | 0.898358 | -0.067442 |
| v52_family_mean_conv5way_step7000 | roundtrip_src_eng | v5_target | 300 | 0.898358 | -0.067442 |
| v52_family_mean_conv5way_step7000 | roundtrip_src_pivot | all | 300 | 0.939344 | 0.388456 |
| v52_family_mean_conv5way_step7000 | roundtrip_src_pivot | v5_target | 300 | 0.939344 | 0.388456 |
| v52_family_mean_conv5way_step7000 | same_language_bible_adjacent | all | 300 | 0.977064 | 0.767454 |
| v52_family_mean_conv5way_step7000 | same_language_bible_adjacent | v5_target | 300 | 0.977064 | 0.767454 |
| v52_family_mean_conv5way_step7000 | same_language_tatoeba_adjacent | all | 300 | 0.944846 | 0.415288 |
| v52_family_mean_conv5way_step7000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944846 | 0.415288 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
