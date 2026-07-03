# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step31000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step31000 | aligned_bible_src_eng | all | 300 | 0.921841 | 0.071393 |
| v52_fvt_conv5way_step31000 | aligned_bible_src_eng | v5_target | 300 | 0.921841 | 0.071393 |
| v52_fvt_conv5way_step31000 | aligned_tatoeba_src_eng | all | 300 | 0.926575 | 0.199418 |
| v52_fvt_conv5way_step31000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926575 | 0.199418 |
| v52_fvt_conv5way_step31000 | roundtrip_eng_pivot | all | 300 | 0.918796 | 0.034127 |
| v52_fvt_conv5way_step31000 | roundtrip_eng_pivot | v5_target | 300 | 0.918796 | 0.034127 |
| v52_fvt_conv5way_step31000 | roundtrip_src_eng | all | 300 | 0.918695 | 0.048782 |
| v52_fvt_conv5way_step31000 | roundtrip_src_eng | v5_target | 300 | 0.918695 | 0.048782 |
| v52_fvt_conv5way_step31000 | roundtrip_src_pivot | all | 300 | 0.935081 | 0.312004 |
| v52_fvt_conv5way_step31000 | roundtrip_src_pivot | v5_target | 300 | 0.935081 | 0.312004 |
| v52_fvt_conv5way_step31000 | same_language_bible_adjacent | all | 300 | 0.978730 | 0.758289 |
| v52_fvt_conv5way_step31000 | same_language_bible_adjacent | v5_target | 300 | 0.978730 | 0.758289 |
| v52_fvt_conv5way_step31000 | same_language_tatoeba_adjacent | all | 300 | 0.947415 | 0.388745 |
| v52_fvt_conv5way_step31000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947415 | 0.388745 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
