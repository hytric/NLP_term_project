# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step45000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step45000 | aligned_bible_src_eng | all | 300 | 0.922842 | 0.054702 |
| v52_mean_conv5way_step45000 | aligned_bible_src_eng | v5_target | 300 | 0.922842 | 0.054702 |
| v52_mean_conv5way_step45000 | aligned_tatoeba_src_eng | all | 300 | 0.925862 | 0.196240 |
| v52_mean_conv5way_step45000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925862 | 0.196240 |
| v52_mean_conv5way_step45000 | roundtrip_eng_pivot | all | 300 | 0.919876 | 0.028763 |
| v52_mean_conv5way_step45000 | roundtrip_eng_pivot | v5_target | 300 | 0.919876 | 0.028763 |
| v52_mean_conv5way_step45000 | roundtrip_src_eng | all | 300 | 0.920458 | 0.034602 |
| v52_mean_conv5way_step45000 | roundtrip_src_eng | v5_target | 300 | 0.920458 | 0.034602 |
| v52_mean_conv5way_step45000 | roundtrip_src_pivot | all | 300 | 0.938067 | 0.315621 |
| v52_mean_conv5way_step45000 | roundtrip_src_pivot | v5_target | 300 | 0.938067 | 0.315621 |
| v52_mean_conv5way_step45000 | same_language_bible_adjacent | all | 300 | 0.979097 | 0.748324 |
| v52_mean_conv5way_step45000 | same_language_bible_adjacent | v5_target | 300 | 0.979097 | 0.748324 |
| v52_mean_conv5way_step45000 | same_language_tatoeba_adjacent | all | 300 | 0.945999 | 0.379729 |
| v52_mean_conv5way_step45000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945999 | 0.379729 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
