# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step10000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step10000 | aligned_bible_src_eng | all | 300 | 0.916639 | 0.052754 |
| v52_weighted_fvt_conv5way_step10000 | aligned_bible_src_eng | v5_target | 300 | 0.916639 | 0.052754 |
| v52_weighted_fvt_conv5way_step10000 | aligned_tatoeba_src_eng | all | 300 | 0.917477 | 0.177455 |
| v52_weighted_fvt_conv5way_step10000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.917477 | 0.177455 |
| v52_weighted_fvt_conv5way_step10000 | roundtrip_eng_pivot | all | 300 | 0.916207 | 0.029012 |
| v52_weighted_fvt_conv5way_step10000 | roundtrip_eng_pivot | v5_target | 300 | 0.916207 | 0.029012 |
| v52_weighted_fvt_conv5way_step10000 | roundtrip_src_eng | all | 300 | 0.913333 | 0.032152 |
| v52_weighted_fvt_conv5way_step10000 | roundtrip_src_eng | v5_target | 300 | 0.913333 | 0.032152 |
| v52_weighted_fvt_conv5way_step10000 | roundtrip_src_pivot | all | 300 | 0.931277 | 0.302106 |
| v52_weighted_fvt_conv5way_step10000 | roundtrip_src_pivot | v5_target | 300 | 0.931277 | 0.302106 |
| v52_weighted_fvt_conv5way_step10000 | same_language_bible_adjacent | all | 300 | 0.976624 | 0.752385 |
| v52_weighted_fvt_conv5way_step10000 | same_language_bible_adjacent | v5_target | 300 | 0.976624 | 0.752385 |
| v52_weighted_fvt_conv5way_step10000 | same_language_tatoeba_adjacent | all | 300 | 0.939764 | 0.362156 |
| v52_weighted_fvt_conv5way_step10000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.939764 | 0.362156 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
