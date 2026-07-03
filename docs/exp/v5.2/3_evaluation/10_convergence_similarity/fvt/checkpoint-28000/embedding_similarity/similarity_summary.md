# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step28000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step28000 | aligned_bible_src_eng | all | 300 | 0.921940 | 0.072092 |
| v52_fvt_conv5way_step28000 | aligned_bible_src_eng | v5_target | 300 | 0.921940 | 0.072092 |
| v52_fvt_conv5way_step28000 | aligned_tatoeba_src_eng | all | 300 | 0.926601 | 0.199368 |
| v52_fvt_conv5way_step28000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926601 | 0.199368 |
| v52_fvt_conv5way_step28000 | roundtrip_eng_pivot | all | 300 | 0.918984 | 0.035076 |
| v52_fvt_conv5way_step28000 | roundtrip_eng_pivot | v5_target | 300 | 0.918984 | 0.035076 |
| v52_fvt_conv5way_step28000 | roundtrip_src_eng | all | 300 | 0.918814 | 0.049648 |
| v52_fvt_conv5way_step28000 | roundtrip_src_eng | v5_target | 300 | 0.918814 | 0.049648 |
| v52_fvt_conv5way_step28000 | roundtrip_src_pivot | all | 300 | 0.935137 | 0.311042 |
| v52_fvt_conv5way_step28000 | roundtrip_src_pivot | v5_target | 300 | 0.935137 | 0.311042 |
| v52_fvt_conv5way_step28000 | same_language_bible_adjacent | all | 300 | 0.978714 | 0.758112 |
| v52_fvt_conv5way_step28000 | same_language_bible_adjacent | v5_target | 300 | 0.978714 | 0.758112 |
| v52_fvt_conv5way_step28000 | same_language_tatoeba_adjacent | all | 300 | 0.947512 | 0.389355 |
| v52_fvt_conv5way_step28000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947512 | 0.389355 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
