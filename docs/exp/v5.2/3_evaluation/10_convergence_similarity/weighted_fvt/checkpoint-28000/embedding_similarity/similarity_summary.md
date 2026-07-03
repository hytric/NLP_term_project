# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step28000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step28000 | aligned_bible_src_eng | all | 300 | 0.919975 | 0.062594 |
| v52_weighted_fvt_conv5way_step28000 | aligned_bible_src_eng | v5_target | 300 | 0.919975 | 0.062594 |
| v52_weighted_fvt_conv5way_step28000 | aligned_tatoeba_src_eng | all | 300 | 0.924092 | 0.204331 |
| v52_weighted_fvt_conv5way_step28000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.924092 | 0.204331 |
| v52_weighted_fvt_conv5way_step28000 | roundtrip_eng_pivot | all | 300 | 0.916852 | 0.020600 |
| v52_weighted_fvt_conv5way_step28000 | roundtrip_eng_pivot | v5_target | 300 | 0.916852 | 0.020600 |
| v52_weighted_fvt_conv5way_step28000 | roundtrip_src_eng | all | 300 | 0.916833 | 0.039826 |
| v52_weighted_fvt_conv5way_step28000 | roundtrip_src_eng | v5_target | 300 | 0.916833 | 0.039826 |
| v52_weighted_fvt_conv5way_step28000 | roundtrip_src_pivot | all | 300 | 0.932300 | 0.295552 |
| v52_weighted_fvt_conv5way_step28000 | roundtrip_src_pivot | v5_target | 300 | 0.932300 | 0.295552 |
| v52_weighted_fvt_conv5way_step28000 | same_language_bible_adjacent | all | 300 | 0.978302 | 0.761113 |
| v52_weighted_fvt_conv5way_step28000 | same_language_bible_adjacent | v5_target | 300 | 0.978302 | 0.761113 |
| v52_weighted_fvt_conv5way_step28000 | same_language_tatoeba_adjacent | all | 300 | 0.944268 | 0.372843 |
| v52_weighted_fvt_conv5way_step28000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944268 | 0.372843 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
