# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step20000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step20000 | aligned_bible_src_eng | all | 300 | 0.922406 | 0.082424 |
| v52_weighted_fvt_conv5way_step20000 | aligned_bible_src_eng | v5_target | 300 | 0.922406 | 0.082424 |
| v52_weighted_fvt_conv5way_step20000 | aligned_tatoeba_src_eng | all | 300 | 0.924625 | 0.206345 |
| v52_weighted_fvt_conv5way_step20000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.924625 | 0.206345 |
| v52_weighted_fvt_conv5way_step20000 | roundtrip_eng_pivot | all | 300 | 0.919049 | 0.038570 |
| v52_weighted_fvt_conv5way_step20000 | roundtrip_eng_pivot | v5_target | 300 | 0.919049 | 0.038570 |
| v52_weighted_fvt_conv5way_step20000 | roundtrip_src_eng | all | 300 | 0.919337 | 0.059938 |
| v52_weighted_fvt_conv5way_step20000 | roundtrip_src_eng | v5_target | 300 | 0.919337 | 0.059938 |
| v52_weighted_fvt_conv5way_step20000 | roundtrip_src_pivot | all | 300 | 0.933350 | 0.290300 |
| v52_weighted_fvt_conv5way_step20000 | roundtrip_src_pivot | v5_target | 300 | 0.933350 | 0.290300 |
| v52_weighted_fvt_conv5way_step20000 | same_language_bible_adjacent | all | 300 | 0.978339 | 0.753981 |
| v52_weighted_fvt_conv5way_step20000 | same_language_bible_adjacent | v5_target | 300 | 0.978339 | 0.753981 |
| v52_weighted_fvt_conv5way_step20000 | same_language_tatoeba_adjacent | all | 300 | 0.944339 | 0.373299 |
| v52_weighted_fvt_conv5way_step20000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944339 | 0.373299 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
