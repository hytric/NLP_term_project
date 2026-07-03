# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step19000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step19000 | aligned_bible_src_eng | all | 300 | 0.920960 | 0.070911 |
| v52_weighted_fvt_conv5way_step19000 | aligned_bible_src_eng | v5_target | 300 | 0.920960 | 0.070911 |
| v52_weighted_fvt_conv5way_step19000 | aligned_tatoeba_src_eng | all | 300 | 0.923083 | 0.199188 |
| v52_weighted_fvt_conv5way_step19000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.923083 | 0.199188 |
| v52_weighted_fvt_conv5way_step19000 | roundtrip_eng_pivot | all | 300 | 0.918166 | 0.029398 |
| v52_weighted_fvt_conv5way_step19000 | roundtrip_eng_pivot | v5_target | 300 | 0.918166 | 0.029398 |
| v52_weighted_fvt_conv5way_step19000 | roundtrip_src_eng | all | 300 | 0.917871 | 0.048452 |
| v52_weighted_fvt_conv5way_step19000 | roundtrip_src_eng | v5_target | 300 | 0.917871 | 0.048452 |
| v52_weighted_fvt_conv5way_step19000 | roundtrip_src_pivot | all | 300 | 0.931915 | 0.281589 |
| v52_weighted_fvt_conv5way_step19000 | roundtrip_src_pivot | v5_target | 300 | 0.931915 | 0.281589 |
| v52_weighted_fvt_conv5way_step19000 | same_language_bible_adjacent | all | 300 | 0.977904 | 0.753231 |
| v52_weighted_fvt_conv5way_step19000 | same_language_bible_adjacent | v5_target | 300 | 0.977904 | 0.753231 |
| v52_weighted_fvt_conv5way_step19000 | same_language_tatoeba_adjacent | all | 300 | 0.943925 | 0.370101 |
| v52_weighted_fvt_conv5way_step19000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943925 | 0.370101 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
