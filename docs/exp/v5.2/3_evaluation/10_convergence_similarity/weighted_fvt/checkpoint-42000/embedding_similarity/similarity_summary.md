# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step42000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step42000 | aligned_bible_src_eng | all | 300 | 0.921330 | 0.060573 |
| v52_weighted_fvt_conv5way_step42000 | aligned_bible_src_eng | v5_target | 300 | 0.921330 | 0.060573 |
| v52_weighted_fvt_conv5way_step42000 | aligned_tatoeba_src_eng | all | 300 | 0.925608 | 0.207265 |
| v52_weighted_fvt_conv5way_step42000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925608 | 0.207265 |
| v52_weighted_fvt_conv5way_step42000 | roundtrip_eng_pivot | all | 300 | 0.917546 | 0.011855 |
| v52_weighted_fvt_conv5way_step42000 | roundtrip_eng_pivot | v5_target | 300 | 0.917546 | 0.011855 |
| v52_weighted_fvt_conv5way_step42000 | roundtrip_src_eng | all | 300 | 0.918365 | 0.039032 |
| v52_weighted_fvt_conv5way_step42000 | roundtrip_src_eng | v5_target | 300 | 0.918365 | 0.039032 |
| v52_weighted_fvt_conv5way_step42000 | roundtrip_src_pivot | all | 300 | 0.933458 | 0.294471 |
| v52_weighted_fvt_conv5way_step42000 | roundtrip_src_pivot | v5_target | 300 | 0.933458 | 0.294471 |
| v52_weighted_fvt_conv5way_step42000 | same_language_bible_adjacent | all | 300 | 0.978404 | 0.756974 |
| v52_weighted_fvt_conv5way_step42000 | same_language_bible_adjacent | v5_target | 300 | 0.978404 | 0.756974 |
| v52_weighted_fvt_conv5way_step42000 | same_language_tatoeba_adjacent | all | 300 | 0.944788 | 0.371349 |
| v52_weighted_fvt_conv5way_step42000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944788 | 0.371349 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
