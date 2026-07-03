# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step39000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step39000 | aligned_bible_src_eng | all | 300 | 0.923280 | 0.064027 |
| v52_weighted_fvt_conv5way_step39000 | aligned_bible_src_eng | v5_target | 300 | 0.923280 | 0.064027 |
| v52_weighted_fvt_conv5way_step39000 | aligned_tatoeba_src_eng | all | 300 | 0.926257 | 0.207004 |
| v52_weighted_fvt_conv5way_step39000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926257 | 0.207004 |
| v52_weighted_fvt_conv5way_step39000 | roundtrip_eng_pivot | all | 300 | 0.919889 | 0.020049 |
| v52_weighted_fvt_conv5way_step39000 | roundtrip_eng_pivot | v5_target | 300 | 0.919889 | 0.020049 |
| v52_weighted_fvt_conv5way_step39000 | roundtrip_src_eng | all | 300 | 0.920378 | 0.042814 |
| v52_weighted_fvt_conv5way_step39000 | roundtrip_src_eng | v5_target | 300 | 0.920378 | 0.042814 |
| v52_weighted_fvt_conv5way_step39000 | roundtrip_src_pivot | all | 300 | 0.934284 | 0.290755 |
| v52_weighted_fvt_conv5way_step39000 | roundtrip_src_pivot | v5_target | 300 | 0.934284 | 0.290755 |
| v52_weighted_fvt_conv5way_step39000 | same_language_bible_adjacent | all | 300 | 0.978673 | 0.755055 |
| v52_weighted_fvt_conv5way_step39000 | same_language_bible_adjacent | v5_target | 300 | 0.978673 | 0.755055 |
| v52_weighted_fvt_conv5way_step39000 | same_language_tatoeba_adjacent | all | 300 | 0.944631 | 0.367086 |
| v52_weighted_fvt_conv5way_step39000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944631 | 0.367086 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
