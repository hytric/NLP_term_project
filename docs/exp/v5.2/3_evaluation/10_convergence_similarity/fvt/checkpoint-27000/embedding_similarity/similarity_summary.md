# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step27000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step27000 | aligned_bible_src_eng | all | 300 | 0.922297 | 0.073073 |
| v52_fvt_conv5way_step27000 | aligned_bible_src_eng | v5_target | 300 | 0.922297 | 0.073073 |
| v52_fvt_conv5way_step27000 | aligned_tatoeba_src_eng | all | 300 | 0.926626 | 0.199130 |
| v52_fvt_conv5way_step27000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926626 | 0.199130 |
| v52_fvt_conv5way_step27000 | roundtrip_eng_pivot | all | 300 | 0.919411 | 0.036672 |
| v52_fvt_conv5way_step27000 | roundtrip_eng_pivot | v5_target | 300 | 0.919411 | 0.036672 |
| v52_fvt_conv5way_step27000 | roundtrip_src_eng | all | 300 | 0.919174 | 0.050728 |
| v52_fvt_conv5way_step27000 | roundtrip_src_eng | v5_target | 300 | 0.919174 | 0.050728 |
| v52_fvt_conv5way_step27000 | roundtrip_src_pivot | all | 300 | 0.935168 | 0.310249 |
| v52_fvt_conv5way_step27000 | roundtrip_src_pivot | v5_target | 300 | 0.935168 | 0.310249 |
| v52_fvt_conv5way_step27000 | same_language_bible_adjacent | all | 300 | 0.978702 | 0.757533 |
| v52_fvt_conv5way_step27000 | same_language_bible_adjacent | v5_target | 300 | 0.978702 | 0.757533 |
| v52_fvt_conv5way_step27000 | same_language_tatoeba_adjacent | all | 300 | 0.947478 | 0.388599 |
| v52_fvt_conv5way_step27000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947478 | 0.388599 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
