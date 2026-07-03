# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step5000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step5000 | aligned_bible_src_eng | all | 300 | 0.914144 | 0.004646 |
| v52_weighted_fvt_conv5way_step5000 | aligned_bible_src_eng | v5_target | 300 | 0.914144 | 0.004646 |
| v52_weighted_fvt_conv5way_step5000 | aligned_tatoeba_src_eng | all | 300 | 0.913746 | 0.158998 |
| v52_weighted_fvt_conv5way_step5000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.913746 | 0.158998 |
| v52_weighted_fvt_conv5way_step5000 | roundtrip_eng_pivot | all | 300 | 0.913149 | -0.027420 |
| v52_weighted_fvt_conv5way_step5000 | roundtrip_eng_pivot | v5_target | 300 | 0.913149 | -0.027420 |
| v52_weighted_fvt_conv5way_step5000 | roundtrip_src_eng | all | 300 | 0.910891 | -0.020662 |
| v52_weighted_fvt_conv5way_step5000 | roundtrip_src_eng | v5_target | 300 | 0.910891 | -0.020662 |
| v52_weighted_fvt_conv5way_step5000 | roundtrip_src_pivot | all | 300 | 0.938638 | 0.339633 |
| v52_weighted_fvt_conv5way_step5000 | roundtrip_src_pivot | v5_target | 300 | 0.938638 | 0.339633 |
| v52_weighted_fvt_conv5way_step5000 | same_language_bible_adjacent | all | 300 | 0.976699 | 0.742286 |
| v52_weighted_fvt_conv5way_step5000 | same_language_bible_adjacent | v5_target | 300 | 0.976699 | 0.742286 |
| v52_weighted_fvt_conv5way_step5000 | same_language_tatoeba_adjacent | all | 300 | 0.937379 | 0.352828 |
| v52_weighted_fvt_conv5way_step5000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.937379 | 0.352828 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
