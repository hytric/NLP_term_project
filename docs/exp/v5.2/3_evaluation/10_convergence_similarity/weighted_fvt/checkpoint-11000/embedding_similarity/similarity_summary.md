# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step11000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step11000 | aligned_bible_src_eng | all | 300 | 0.918424 | 0.061323 |
| v52_weighted_fvt_conv5way_step11000 | aligned_bible_src_eng | v5_target | 300 | 0.918424 | 0.061323 |
| v52_weighted_fvt_conv5way_step11000 | aligned_tatoeba_src_eng | all | 300 | 0.918070 | 0.177614 |
| v52_weighted_fvt_conv5way_step11000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.918070 | 0.177614 |
| v52_weighted_fvt_conv5way_step11000 | roundtrip_eng_pivot | all | 300 | 0.917088 | 0.029328 |
| v52_weighted_fvt_conv5way_step11000 | roundtrip_eng_pivot | v5_target | 300 | 0.917088 | 0.029328 |
| v52_weighted_fvt_conv5way_step11000 | roundtrip_src_eng | all | 300 | 0.915146 | 0.041008 |
| v52_weighted_fvt_conv5way_step11000 | roundtrip_src_eng | v5_target | 300 | 0.915146 | 0.041008 |
| v52_weighted_fvt_conv5way_step11000 | roundtrip_src_pivot | all | 300 | 0.932295 | 0.291911 |
| v52_weighted_fvt_conv5way_step11000 | roundtrip_src_pivot | v5_target | 300 | 0.932295 | 0.291911 |
| v52_weighted_fvt_conv5way_step11000 | same_language_bible_adjacent | all | 300 | 0.977460 | 0.753665 |
| v52_weighted_fvt_conv5way_step11000 | same_language_bible_adjacent | v5_target | 300 | 0.977460 | 0.753665 |
| v52_weighted_fvt_conv5way_step11000 | same_language_tatoeba_adjacent | all | 300 | 0.941344 | 0.368101 |
| v52_weighted_fvt_conv5way_step11000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.941344 | 0.368101 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
