# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step44000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step44000 | aligned_bible_src_eng | all | 300 | 0.922083 | 0.071038 |
| v52_fvt_conv5way_step44000 | aligned_bible_src_eng | v5_target | 300 | 0.922083 | 0.071038 |
| v52_fvt_conv5way_step44000 | aligned_tatoeba_src_eng | all | 300 | 0.926691 | 0.199921 |
| v52_fvt_conv5way_step44000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926691 | 0.199921 |
| v52_fvt_conv5way_step44000 | roundtrip_eng_pivot | all | 300 | 0.919151 | 0.034254 |
| v52_fvt_conv5way_step44000 | roundtrip_eng_pivot | v5_target | 300 | 0.919151 | 0.034254 |
| v52_fvt_conv5way_step44000 | roundtrip_src_eng | all | 300 | 0.918931 | 0.048547 |
| v52_fvt_conv5way_step44000 | roundtrip_src_eng | v5_target | 300 | 0.918931 | 0.048547 |
| v52_fvt_conv5way_step44000 | roundtrip_src_pivot | all | 300 | 0.935375 | 0.313254 |
| v52_fvt_conv5way_step44000 | roundtrip_src_pivot | v5_target | 300 | 0.935375 | 0.313254 |
| v52_fvt_conv5way_step44000 | same_language_bible_adjacent | all | 300 | 0.978759 | 0.758441 |
| v52_fvt_conv5way_step44000 | same_language_bible_adjacent | v5_target | 300 | 0.978759 | 0.758441 |
| v52_fvt_conv5way_step44000 | same_language_tatoeba_adjacent | all | 300 | 0.947588 | 0.388683 |
| v52_fvt_conv5way_step44000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947588 | 0.388683 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
