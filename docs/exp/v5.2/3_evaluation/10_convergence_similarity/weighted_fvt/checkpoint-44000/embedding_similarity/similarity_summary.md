# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step44000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step44000 | aligned_bible_src_eng | all | 300 | 0.923062 | 0.067164 |
| v52_weighted_fvt_conv5way_step44000 | aligned_bible_src_eng | v5_target | 300 | 0.923062 | 0.067164 |
| v52_weighted_fvt_conv5way_step44000 | aligned_tatoeba_src_eng | all | 300 | 0.926905 | 0.214154 |
| v52_weighted_fvt_conv5way_step44000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926905 | 0.214154 |
| v52_weighted_fvt_conv5way_step44000 | roundtrip_eng_pivot | all | 300 | 0.919550 | 0.019811 |
| v52_weighted_fvt_conv5way_step44000 | roundtrip_eng_pivot | v5_target | 300 | 0.919550 | 0.019811 |
| v52_weighted_fvt_conv5way_step44000 | roundtrip_src_eng | all | 300 | 0.920134 | 0.045328 |
| v52_weighted_fvt_conv5way_step44000 | roundtrip_src_eng | v5_target | 300 | 0.920134 | 0.045328 |
| v52_weighted_fvt_conv5way_step44000 | roundtrip_src_pivot | all | 300 | 0.934320 | 0.291471 |
| v52_weighted_fvt_conv5way_step44000 | roundtrip_src_pivot | v5_target | 300 | 0.934320 | 0.291471 |
| v52_weighted_fvt_conv5way_step44000 | same_language_bible_adjacent | all | 300 | 0.978603 | 0.754738 |
| v52_weighted_fvt_conv5way_step44000 | same_language_bible_adjacent | v5_target | 300 | 0.978603 | 0.754738 |
| v52_weighted_fvt_conv5way_step44000 | same_language_tatoeba_adjacent | all | 300 | 0.945162 | 0.367357 |
| v52_weighted_fvt_conv5way_step44000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945162 | 0.367357 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
