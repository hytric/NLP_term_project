# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step9000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step9000 | aligned_bible_src_eng | all | 300 | 0.914952 | 0.054778 |
| v52_weighted_fvt_conv5way_step9000 | aligned_bible_src_eng | v5_target | 300 | 0.914952 | 0.054778 |
| v52_weighted_fvt_conv5way_step9000 | aligned_tatoeba_src_eng | all | 300 | 0.913488 | 0.171807 |
| v52_weighted_fvt_conv5way_step9000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.913488 | 0.171807 |
| v52_weighted_fvt_conv5way_step9000 | roundtrip_eng_pivot | all | 300 | 0.913555 | 0.024721 |
| v52_weighted_fvt_conv5way_step9000 | roundtrip_eng_pivot | v5_target | 300 | 0.913555 | 0.024721 |
| v52_weighted_fvt_conv5way_step9000 | roundtrip_src_eng | all | 300 | 0.911723 | 0.034044 |
| v52_weighted_fvt_conv5way_step9000 | roundtrip_src_eng | v5_target | 300 | 0.911723 | 0.034044 |
| v52_weighted_fvt_conv5way_step9000 | roundtrip_src_pivot | all | 300 | 0.930155 | 0.291311 |
| v52_weighted_fvt_conv5way_step9000 | roundtrip_src_pivot | v5_target | 300 | 0.930155 | 0.291311 |
| v52_weighted_fvt_conv5way_step9000 | same_language_bible_adjacent | all | 300 | 0.977108 | 0.756903 |
| v52_weighted_fvt_conv5way_step9000 | same_language_bible_adjacent | v5_target | 300 | 0.977108 | 0.756903 |
| v52_weighted_fvt_conv5way_step9000 | same_language_tatoeba_adjacent | all | 300 | 0.937508 | 0.362580 |
| v52_weighted_fvt_conv5way_step9000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.937508 | 0.362580 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
