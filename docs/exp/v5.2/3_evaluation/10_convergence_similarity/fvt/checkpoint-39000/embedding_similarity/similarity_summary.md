# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step39000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step39000 | aligned_bible_src_eng | all | 300 | 0.922194 | 0.072178 |
| v52_fvt_conv5way_step39000 | aligned_bible_src_eng | v5_target | 300 | 0.922194 | 0.072178 |
| v52_fvt_conv5way_step39000 | aligned_tatoeba_src_eng | all | 300 | 0.926723 | 0.199577 |
| v52_fvt_conv5way_step39000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926723 | 0.199577 |
| v52_fvt_conv5way_step39000 | roundtrip_eng_pivot | all | 300 | 0.919225 | 0.035367 |
| v52_fvt_conv5way_step39000 | roundtrip_eng_pivot | v5_target | 300 | 0.919225 | 0.035367 |
| v52_fvt_conv5way_step39000 | roundtrip_src_eng | all | 300 | 0.919066 | 0.049816 |
| v52_fvt_conv5way_step39000 | roundtrip_src_eng | v5_target | 300 | 0.919066 | 0.049816 |
| v52_fvt_conv5way_step39000 | roundtrip_src_pivot | all | 300 | 0.935324 | 0.311876 |
| v52_fvt_conv5way_step39000 | roundtrip_src_pivot | v5_target | 300 | 0.935324 | 0.311876 |
| v52_fvt_conv5way_step39000 | same_language_bible_adjacent | all | 300 | 0.978776 | 0.758192 |
| v52_fvt_conv5way_step39000 | same_language_bible_adjacent | v5_target | 300 | 0.978776 | 0.758192 |
| v52_fvt_conv5way_step39000 | same_language_tatoeba_adjacent | all | 300 | 0.947586 | 0.388740 |
| v52_fvt_conv5way_step39000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947586 | 0.388740 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
