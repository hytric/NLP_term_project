# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step33000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step33000 | aligned_bible_src_eng | all | 300 | 0.917038 | 0.038471 |
| v52_family_mean_conv5way_step33000 | aligned_bible_src_eng | v5_target | 300 | 0.917038 | 0.038471 |
| v52_family_mean_conv5way_step33000 | aligned_tatoeba_src_eng | all | 300 | 0.925598 | 0.215518 |
| v52_family_mean_conv5way_step33000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925598 | 0.215518 |
| v52_family_mean_conv5way_step33000 | roundtrip_eng_pivot | all | 300 | 0.915263 | 0.006201 |
| v52_family_mean_conv5way_step33000 | roundtrip_eng_pivot | v5_target | 300 | 0.915263 | 0.006201 |
| v52_family_mean_conv5way_step33000 | roundtrip_src_eng | all | 300 | 0.913663 | 0.015201 |
| v52_family_mean_conv5way_step33000 | roundtrip_src_eng | v5_target | 300 | 0.913663 | 0.015201 |
| v52_family_mean_conv5way_step33000 | roundtrip_src_pivot | all | 300 | 0.938614 | 0.350339 |
| v52_family_mean_conv5way_step33000 | roundtrip_src_pivot | v5_target | 300 | 0.938614 | 0.350339 |
| v52_family_mean_conv5way_step33000 | same_language_bible_adjacent | all | 300 | 0.978448 | 0.760430 |
| v52_family_mean_conv5way_step33000 | same_language_bible_adjacent | v5_target | 300 | 0.978448 | 0.760430 |
| v52_family_mean_conv5way_step33000 | same_language_tatoeba_adjacent | all | 300 | 0.948347 | 0.402565 |
| v52_family_mean_conv5way_step33000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.948347 | 0.402565 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
