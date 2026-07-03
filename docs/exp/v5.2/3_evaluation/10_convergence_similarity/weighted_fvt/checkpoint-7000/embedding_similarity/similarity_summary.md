# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step7000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step7000 | aligned_bible_src_eng | all | 300 | 0.913372 | 0.010320 |
| v52_weighted_fvt_conv5way_step7000 | aligned_bible_src_eng | v5_target | 300 | 0.913372 | 0.010320 |
| v52_weighted_fvt_conv5way_step7000 | aligned_tatoeba_src_eng | all | 300 | 0.912525 | 0.155368 |
| v52_weighted_fvt_conv5way_step7000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.912525 | 0.155368 |
| v52_weighted_fvt_conv5way_step7000 | roundtrip_eng_pivot | all | 300 | 0.911474 | -0.026920 |
| v52_weighted_fvt_conv5way_step7000 | roundtrip_eng_pivot | v5_target | 300 | 0.911474 | -0.026920 |
| v52_weighted_fvt_conv5way_step7000 | roundtrip_src_eng | all | 300 | 0.910064 | -0.011993 |
| v52_weighted_fvt_conv5way_step7000 | roundtrip_src_eng | v5_target | 300 | 0.910064 | -0.011993 |
| v52_weighted_fvt_conv5way_step7000 | roundtrip_src_pivot | all | 300 | 0.931958 | 0.302677 |
| v52_weighted_fvt_conv5way_step7000 | roundtrip_src_pivot | v5_target | 300 | 0.931958 | 0.302677 |
| v52_weighted_fvt_conv5way_step7000 | same_language_bible_adjacent | all | 300 | 0.976623 | 0.751950 |
| v52_weighted_fvt_conv5way_step7000 | same_language_bible_adjacent | v5_target | 300 | 0.976623 | 0.751950 |
| v52_weighted_fvt_conv5way_step7000 | same_language_tatoeba_adjacent | all | 300 | 0.937157 | 0.362228 |
| v52_weighted_fvt_conv5way_step7000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.937157 | 0.362228 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
