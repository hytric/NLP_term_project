# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step41000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step41000 | aligned_bible_src_eng | all | 300 | 0.922812 | 0.058552 |
| v52_weighted_fvt_conv5way_step41000 | aligned_bible_src_eng | v5_target | 300 | 0.922812 | 0.058552 |
| v52_weighted_fvt_conv5way_step41000 | aligned_tatoeba_src_eng | all | 300 | 0.926498 | 0.205968 |
| v52_weighted_fvt_conv5way_step41000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926498 | 0.205968 |
| v52_weighted_fvt_conv5way_step41000 | roundtrip_eng_pivot | all | 300 | 0.919124 | 0.012050 |
| v52_weighted_fvt_conv5way_step41000 | roundtrip_eng_pivot | v5_target | 300 | 0.919124 | 0.012050 |
| v52_weighted_fvt_conv5way_step41000 | roundtrip_src_eng | all | 300 | 0.919887 | 0.037704 |
| v52_weighted_fvt_conv5way_step41000 | roundtrip_src_eng | v5_target | 300 | 0.919887 | 0.037704 |
| v52_weighted_fvt_conv5way_step41000 | roundtrip_src_pivot | all | 300 | 0.935109 | 0.300093 |
| v52_weighted_fvt_conv5way_step41000 | roundtrip_src_pivot | v5_target | 300 | 0.935109 | 0.300093 |
| v52_weighted_fvt_conv5way_step41000 | same_language_bible_adjacent | all | 300 | 0.978734 | 0.756089 |
| v52_weighted_fvt_conv5way_step41000 | same_language_bible_adjacent | v5_target | 300 | 0.978734 | 0.756089 |
| v52_weighted_fvt_conv5way_step41000 | same_language_tatoeba_adjacent | all | 300 | 0.945240 | 0.370802 |
| v52_weighted_fvt_conv5way_step41000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945240 | 0.370802 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
