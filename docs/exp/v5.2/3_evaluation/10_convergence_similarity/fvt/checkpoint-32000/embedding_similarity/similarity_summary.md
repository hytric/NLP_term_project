# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step32000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step32000 | aligned_bible_src_eng | all | 300 | 0.922074 | 0.073007 |
| v52_fvt_conv5way_step32000 | aligned_bible_src_eng | v5_target | 300 | 0.922074 | 0.073007 |
| v52_fvt_conv5way_step32000 | aligned_tatoeba_src_eng | all | 300 | 0.926525 | 0.199589 |
| v52_fvt_conv5way_step32000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926525 | 0.199589 |
| v52_fvt_conv5way_step32000 | roundtrip_eng_pivot | all | 300 | 0.919064 | 0.035897 |
| v52_fvt_conv5way_step32000 | roundtrip_eng_pivot | v5_target | 300 | 0.919064 | 0.035897 |
| v52_fvt_conv5way_step32000 | roundtrip_src_eng | all | 300 | 0.918951 | 0.050647 |
| v52_fvt_conv5way_step32000 | roundtrip_src_eng | v5_target | 300 | 0.918951 | 0.050647 |
| v52_fvt_conv5way_step32000 | roundtrip_src_pivot | all | 300 | 0.935319 | 0.313182 |
| v52_fvt_conv5way_step32000 | roundtrip_src_pivot | v5_target | 300 | 0.935319 | 0.313182 |
| v52_fvt_conv5way_step32000 | same_language_bible_adjacent | all | 300 | 0.978737 | 0.758101 |
| v52_fvt_conv5way_step32000 | same_language_bible_adjacent | v5_target | 300 | 0.978737 | 0.758101 |
| v52_fvt_conv5way_step32000 | same_language_tatoeba_adjacent | all | 300 | 0.947381 | 0.389134 |
| v52_fvt_conv5way_step32000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947381 | 0.389134 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
