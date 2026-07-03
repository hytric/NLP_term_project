# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step6000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step6000 | aligned_bible_src_eng | all | 300 | 0.913999 | 0.016437 |
| v52_weighted_fvt_conv5way_step6000 | aligned_bible_src_eng | v5_target | 300 | 0.913999 | 0.016437 |
| v52_weighted_fvt_conv5way_step6000 | aligned_tatoeba_src_eng | all | 300 | 0.915184 | 0.159014 |
| v52_weighted_fvt_conv5way_step6000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.915184 | 0.159014 |
| v52_weighted_fvt_conv5way_step6000 | roundtrip_eng_pivot | all | 300 | 0.912863 | -0.019215 |
| v52_weighted_fvt_conv5way_step6000 | roundtrip_eng_pivot | v5_target | 300 | 0.912863 | -0.019215 |
| v52_weighted_fvt_conv5way_step6000 | roundtrip_src_eng | all | 300 | 0.910708 | -0.005509 |
| v52_weighted_fvt_conv5way_step6000 | roundtrip_src_eng | v5_target | 300 | 0.910708 | -0.005509 |
| v52_weighted_fvt_conv5way_step6000 | roundtrip_src_pivot | all | 300 | 0.932781 | 0.302208 |
| v52_weighted_fvt_conv5way_step6000 | roundtrip_src_pivot | v5_target | 300 | 0.932781 | 0.302208 |
| v52_weighted_fvt_conv5way_step6000 | same_language_bible_adjacent | all | 300 | 0.976339 | 0.745001 |
| v52_weighted_fvt_conv5way_step6000 | same_language_bible_adjacent | v5_target | 300 | 0.976339 | 0.745001 |
| v52_weighted_fvt_conv5way_step6000 | same_language_tatoeba_adjacent | all | 300 | 0.938469 | 0.356483 |
| v52_weighted_fvt_conv5way_step6000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.938469 | 0.356483 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
