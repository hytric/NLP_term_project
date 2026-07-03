# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step24000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step24000 | aligned_bible_src_eng | all | 300 | 0.922745 | 0.076582 |
| v52_weighted_fvt_conv5way_step24000 | aligned_bible_src_eng | v5_target | 300 | 0.922745 | 0.076582 |
| v52_weighted_fvt_conv5way_step24000 | aligned_tatoeba_src_eng | all | 300 | 0.924948 | 0.204764 |
| v52_weighted_fvt_conv5way_step24000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.924948 | 0.204764 |
| v52_weighted_fvt_conv5way_step24000 | roundtrip_eng_pivot | all | 300 | 0.919867 | 0.034172 |
| v52_weighted_fvt_conv5way_step24000 | roundtrip_eng_pivot | v5_target | 300 | 0.919867 | 0.034172 |
| v52_weighted_fvt_conv5way_step24000 | roundtrip_src_eng | all | 300 | 0.919722 | 0.054500 |
| v52_weighted_fvt_conv5way_step24000 | roundtrip_src_eng | v5_target | 300 | 0.919722 | 0.054500 |
| v52_weighted_fvt_conv5way_step24000 | roundtrip_src_pivot | all | 300 | 0.933426 | 0.291358 |
| v52_weighted_fvt_conv5way_step24000 | roundtrip_src_pivot | v5_target | 300 | 0.933426 | 0.291358 |
| v52_weighted_fvt_conv5way_step24000 | same_language_bible_adjacent | all | 300 | 0.978175 | 0.754506 |
| v52_weighted_fvt_conv5way_step24000 | same_language_bible_adjacent | v5_target | 300 | 0.978175 | 0.754506 |
| v52_weighted_fvt_conv5way_step24000 | same_language_tatoeba_adjacent | all | 300 | 0.944727 | 0.374019 |
| v52_weighted_fvt_conv5way_step24000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944727 | 0.374019 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
