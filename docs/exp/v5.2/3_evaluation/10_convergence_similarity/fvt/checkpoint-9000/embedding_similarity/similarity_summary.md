# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step9000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step9000 | aligned_bible_src_eng | all | 300 | 0.917150 | 0.060860 |
| v52_fvt_conv5way_step9000 | aligned_bible_src_eng | v5_target | 300 | 0.917150 | 0.060860 |
| v52_fvt_conv5way_step9000 | aligned_tatoeba_src_eng | all | 300 | 0.918678 | 0.183405 |
| v52_fvt_conv5way_step9000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.918678 | 0.183405 |
| v52_fvt_conv5way_step9000 | roundtrip_eng_pivot | all | 300 | 0.915152 | 0.033210 |
| v52_fvt_conv5way_step9000 | roundtrip_eng_pivot | v5_target | 300 | 0.915152 | 0.033210 |
| v52_fvt_conv5way_step9000 | roundtrip_src_eng | all | 300 | 0.913700 | 0.037926 |
| v52_fvt_conv5way_step9000 | roundtrip_src_eng | v5_target | 300 | 0.913700 | 0.037926 |
| v52_fvt_conv5way_step9000 | roundtrip_src_pivot | all | 300 | 0.931974 | 0.303809 |
| v52_fvt_conv5way_step9000 | roundtrip_src_pivot | v5_target | 300 | 0.931974 | 0.303809 |
| v52_fvt_conv5way_step9000 | same_language_bible_adjacent | all | 300 | 0.977429 | 0.755183 |
| v52_fvt_conv5way_step9000 | same_language_bible_adjacent | v5_target | 300 | 0.977429 | 0.755183 |
| v52_fvt_conv5way_step9000 | same_language_tatoeba_adjacent | all | 300 | 0.942223 | 0.375108 |
| v52_fvt_conv5way_step9000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.942223 | 0.375108 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
