# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step28000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step28000 | aligned_bible_src_eng | all | 300 | 0.922434 | 0.054228 |
| v52_mean_conv5way_step28000 | aligned_bible_src_eng | v5_target | 300 | 0.922434 | 0.054228 |
| v52_mean_conv5way_step28000 | aligned_tatoeba_src_eng | all | 300 | 0.925365 | 0.194755 |
| v52_mean_conv5way_step28000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925365 | 0.194755 |
| v52_mean_conv5way_step28000 | roundtrip_eng_pivot | all | 300 | 0.919533 | 0.028688 |
| v52_mean_conv5way_step28000 | roundtrip_eng_pivot | v5_target | 300 | 0.919533 | 0.028688 |
| v52_mean_conv5way_step28000 | roundtrip_src_eng | all | 300 | 0.920041 | 0.033911 |
| v52_mean_conv5way_step28000 | roundtrip_src_eng | v5_target | 300 | 0.920041 | 0.033911 |
| v52_mean_conv5way_step28000 | roundtrip_src_pivot | all | 300 | 0.938051 | 0.316490 |
| v52_mean_conv5way_step28000 | roundtrip_src_pivot | v5_target | 300 | 0.938051 | 0.316490 |
| v52_mean_conv5way_step28000 | same_language_bible_adjacent | all | 300 | 0.979005 | 0.747841 |
| v52_mean_conv5way_step28000 | same_language_bible_adjacent | v5_target | 300 | 0.979005 | 0.747841 |
| v52_mean_conv5way_step28000 | same_language_tatoeba_adjacent | all | 300 | 0.945826 | 0.380580 |
| v52_mean_conv5way_step28000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945826 | 0.380580 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
