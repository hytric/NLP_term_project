# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step49000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step49000 | aligned_bible_src_eng | all | 300 | 0.922111 | 0.070783 |
| v52_fvt_conv5way_step49000 | aligned_bible_src_eng | v5_target | 300 | 0.922111 | 0.070783 |
| v52_fvt_conv5way_step49000 | aligned_tatoeba_src_eng | all | 300 | 0.926700 | 0.199392 |
| v52_fvt_conv5way_step49000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926700 | 0.199392 |
| v52_fvt_conv5way_step49000 | roundtrip_eng_pivot | all | 300 | 0.919133 | 0.033636 |
| v52_fvt_conv5way_step49000 | roundtrip_eng_pivot | v5_target | 300 | 0.919133 | 0.033636 |
| v52_fvt_conv5way_step49000 | roundtrip_src_eng | all | 300 | 0.918962 | 0.048290 |
| v52_fvt_conv5way_step49000 | roundtrip_src_eng | v5_target | 300 | 0.918962 | 0.048290 |
| v52_fvt_conv5way_step49000 | roundtrip_src_pivot | all | 300 | 0.935350 | 0.313113 |
| v52_fvt_conv5way_step49000 | roundtrip_src_pivot | v5_target | 300 | 0.935350 | 0.313113 |
| v52_fvt_conv5way_step49000 | same_language_bible_adjacent | all | 300 | 0.978778 | 0.758694 |
| v52_fvt_conv5way_step49000 | same_language_bible_adjacent | v5_target | 300 | 0.978778 | 0.758694 |
| v52_fvt_conv5way_step49000 | same_language_tatoeba_adjacent | all | 300 | 0.947606 | 0.388920 |
| v52_fvt_conv5way_step49000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947606 | 0.388920 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
