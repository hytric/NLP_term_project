# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step10000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step10000 | aligned_bible_src_eng | all | 300 | 0.916438 | 0.060449 |
| v52_fvt_conv5way_step10000 | aligned_bible_src_eng | v5_target | 300 | 0.916438 | 0.060449 |
| v52_fvt_conv5way_step10000 | aligned_tatoeba_src_eng | all | 300 | 0.920667 | 0.194114 |
| v52_fvt_conv5way_step10000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.920667 | 0.194114 |
| v52_fvt_conv5way_step10000 | roundtrip_eng_pivot | all | 300 | 0.913848 | 0.027153 |
| v52_fvt_conv5way_step10000 | roundtrip_eng_pivot | v5_target | 300 | 0.913848 | 0.027153 |
| v52_fvt_conv5way_step10000 | roundtrip_src_eng | all | 300 | 0.912867 | 0.037933 |
| v52_fvt_conv5way_step10000 | roundtrip_src_eng | v5_target | 300 | 0.912867 | 0.037933 |
| v52_fvt_conv5way_step10000 | roundtrip_src_pivot | all | 300 | 0.930426 | 0.309849 |
| v52_fvt_conv5way_step10000 | roundtrip_src_pivot | v5_target | 300 | 0.930426 | 0.309849 |
| v52_fvt_conv5way_step10000 | same_language_bible_adjacent | all | 300 | 0.977085 | 0.757174 |
| v52_fvt_conv5way_step10000 | same_language_bible_adjacent | v5_target | 300 | 0.977085 | 0.757174 |
| v52_fvt_conv5way_step10000 | same_language_tatoeba_adjacent | all | 300 | 0.942116 | 0.375385 |
| v52_fvt_conv5way_step10000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.942116 | 0.375385 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
