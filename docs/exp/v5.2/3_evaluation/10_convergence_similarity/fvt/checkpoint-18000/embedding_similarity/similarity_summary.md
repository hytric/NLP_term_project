# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step18000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step18000 | aligned_bible_src_eng | all | 300 | 0.919796 | 0.062463 |
| v52_fvt_conv5way_step18000 | aligned_bible_src_eng | v5_target | 300 | 0.919796 | 0.062463 |
| v52_fvt_conv5way_step18000 | aligned_tatoeba_src_eng | all | 300 | 0.925323 | 0.202389 |
| v52_fvt_conv5way_step18000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925323 | 0.202389 |
| v52_fvt_conv5way_step18000 | roundtrip_eng_pivot | all | 300 | 0.916707 | 0.023091 |
| v52_fvt_conv5way_step18000 | roundtrip_eng_pivot | v5_target | 300 | 0.916707 | 0.023091 |
| v52_fvt_conv5way_step18000 | roundtrip_src_eng | all | 300 | 0.916555 | 0.039452 |
| v52_fvt_conv5way_step18000 | roundtrip_src_eng | v5_target | 300 | 0.916555 | 0.039452 |
| v52_fvt_conv5way_step18000 | roundtrip_src_pivot | all | 300 | 0.933938 | 0.307945 |
| v52_fvt_conv5way_step18000 | roundtrip_src_pivot | v5_target | 300 | 0.933938 | 0.307945 |
| v52_fvt_conv5way_step18000 | same_language_bible_adjacent | all | 300 | 0.978597 | 0.760710 |
| v52_fvt_conv5way_step18000 | same_language_bible_adjacent | v5_target | 300 | 0.978597 | 0.760710 |
| v52_fvt_conv5way_step18000 | same_language_tatoeba_adjacent | all | 300 | 0.946096 | 0.385279 |
| v52_fvt_conv5way_step18000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.946096 | 0.385279 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
