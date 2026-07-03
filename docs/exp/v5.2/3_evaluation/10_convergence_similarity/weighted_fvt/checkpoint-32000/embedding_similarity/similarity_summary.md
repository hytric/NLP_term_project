# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step32000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step32000 | aligned_bible_src_eng | all | 300 | 0.921954 | 0.076286 |
| v52_weighted_fvt_conv5way_step32000 | aligned_bible_src_eng | v5_target | 300 | 0.921954 | 0.076286 |
| v52_weighted_fvt_conv5way_step32000 | aligned_tatoeba_src_eng | all | 300 | 0.924427 | 0.205145 |
| v52_weighted_fvt_conv5way_step32000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.924427 | 0.205145 |
| v52_weighted_fvt_conv5way_step32000 | roundtrip_eng_pivot | all | 300 | 0.918163 | 0.029079 |
| v52_weighted_fvt_conv5way_step32000 | roundtrip_eng_pivot | v5_target | 300 | 0.918163 | 0.029079 |
| v52_weighted_fvt_conv5way_step32000 | roundtrip_src_eng | all | 300 | 0.919009 | 0.055011 |
| v52_weighted_fvt_conv5way_step32000 | roundtrip_src_eng | v5_target | 300 | 0.919009 | 0.055011 |
| v52_weighted_fvt_conv5way_step32000 | roundtrip_src_pivot | all | 300 | 0.933932 | 0.296385 |
| v52_weighted_fvt_conv5way_step32000 | roundtrip_src_pivot | v5_target | 300 | 0.933932 | 0.296385 |
| v52_weighted_fvt_conv5way_step32000 | same_language_bible_adjacent | all | 300 | 0.978219 | 0.753961 |
| v52_weighted_fvt_conv5way_step32000 | same_language_bible_adjacent | v5_target | 300 | 0.978219 | 0.753961 |
| v52_weighted_fvt_conv5way_step32000 | same_language_tatoeba_adjacent | all | 300 | 0.944232 | 0.373150 |
| v52_weighted_fvt_conv5way_step32000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944232 | 0.373150 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
