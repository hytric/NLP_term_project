# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step29000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step29000 | aligned_bible_src_eng | all | 300 | 0.921941 | 0.071125 |
| v52_fvt_conv5way_step29000 | aligned_bible_src_eng | v5_target | 300 | 0.921941 | 0.071125 |
| v52_fvt_conv5way_step29000 | aligned_tatoeba_src_eng | all | 300 | 0.926609 | 0.199650 |
| v52_fvt_conv5way_step29000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926609 | 0.199650 |
| v52_fvt_conv5way_step29000 | roundtrip_eng_pivot | all | 300 | 0.918948 | 0.033879 |
| v52_fvt_conv5way_step29000 | roundtrip_eng_pivot | v5_target | 300 | 0.918948 | 0.033879 |
| v52_fvt_conv5way_step29000 | roundtrip_src_eng | all | 300 | 0.918802 | 0.048567 |
| v52_fvt_conv5way_step29000 | roundtrip_src_eng | v5_target | 300 | 0.918802 | 0.048567 |
| v52_fvt_conv5way_step29000 | roundtrip_src_pivot | all | 300 | 0.935230 | 0.312099 |
| v52_fvt_conv5way_step29000 | roundtrip_src_pivot | v5_target | 300 | 0.935230 | 0.312099 |
| v52_fvt_conv5way_step29000 | same_language_bible_adjacent | all | 300 | 0.978756 | 0.758491 |
| v52_fvt_conv5way_step29000 | same_language_bible_adjacent | v5_target | 300 | 0.978756 | 0.758491 |
| v52_fvt_conv5way_step29000 | same_language_tatoeba_adjacent | all | 300 | 0.947427 | 0.388242 |
| v52_fvt_conv5way_step29000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947427 | 0.388242 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
