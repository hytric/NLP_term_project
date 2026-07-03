# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step50000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step50000 | aligned_bible_src_eng | all | 300 | 0.922117 | 0.070836 |
| v52_fvt_conv5way_step50000 | aligned_bible_src_eng | v5_target | 300 | 0.922117 | 0.070836 |
| v52_fvt_conv5way_step50000 | aligned_tatoeba_src_eng | all | 300 | 0.926709 | 0.199467 |
| v52_fvt_conv5way_step50000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926709 | 0.199467 |
| v52_fvt_conv5way_step50000 | roundtrip_eng_pivot | all | 300 | 0.919139 | 0.033689 |
| v52_fvt_conv5way_step50000 | roundtrip_eng_pivot | v5_target | 300 | 0.919139 | 0.033689 |
| v52_fvt_conv5way_step50000 | roundtrip_src_eng | all | 300 | 0.918969 | 0.048361 |
| v52_fvt_conv5way_step50000 | roundtrip_src_eng | v5_target | 300 | 0.918969 | 0.048361 |
| v52_fvt_conv5way_step50000 | roundtrip_src_pivot | all | 300 | 0.935356 | 0.313143 |
| v52_fvt_conv5way_step50000 | roundtrip_src_pivot | v5_target | 300 | 0.935356 | 0.313143 |
| v52_fvt_conv5way_step50000 | same_language_bible_adjacent | all | 300 | 0.978777 | 0.758679 |
| v52_fvt_conv5way_step50000 | same_language_bible_adjacent | v5_target | 300 | 0.978777 | 0.758679 |
| v52_fvt_conv5way_step50000 | same_language_tatoeba_adjacent | all | 300 | 0.947604 | 0.388882 |
| v52_fvt_conv5way_step50000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947604 | 0.388882 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
