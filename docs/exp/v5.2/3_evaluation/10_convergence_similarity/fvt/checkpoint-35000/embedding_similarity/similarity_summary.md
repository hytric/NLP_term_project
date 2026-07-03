# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step35000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step35000 | aligned_bible_src_eng | all | 300 | 0.922055 | 0.073412 |
| v52_fvt_conv5way_step35000 | aligned_bible_src_eng | v5_target | 300 | 0.922055 | 0.073412 |
| v52_fvt_conv5way_step35000 | aligned_tatoeba_src_eng | all | 300 | 0.926433 | 0.199672 |
| v52_fvt_conv5way_step35000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926433 | 0.199672 |
| v52_fvt_conv5way_step35000 | roundtrip_eng_pivot | all | 300 | 0.919085 | 0.036320 |
| v52_fvt_conv5way_step35000 | roundtrip_eng_pivot | v5_target | 300 | 0.919085 | 0.036320 |
| v52_fvt_conv5way_step35000 | roundtrip_src_eng | all | 300 | 0.918930 | 0.050923 |
| v52_fvt_conv5way_step35000 | roundtrip_src_eng | v5_target | 300 | 0.918930 | 0.050923 |
| v52_fvt_conv5way_step35000 | roundtrip_src_pivot | all | 300 | 0.935315 | 0.313735 |
| v52_fvt_conv5way_step35000 | roundtrip_src_pivot | v5_target | 300 | 0.935315 | 0.313735 |
| v52_fvt_conv5way_step35000 | same_language_bible_adjacent | all | 300 | 0.978670 | 0.757712 |
| v52_fvt_conv5way_step35000 | same_language_bible_adjacent | v5_target | 300 | 0.978670 | 0.757712 |
| v52_fvt_conv5way_step35000 | same_language_tatoeba_adjacent | all | 300 | 0.947283 | 0.388629 |
| v52_fvt_conv5way_step35000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947283 | 0.388629 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
