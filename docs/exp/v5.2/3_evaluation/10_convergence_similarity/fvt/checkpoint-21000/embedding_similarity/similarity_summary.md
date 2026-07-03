# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step21000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step21000 | aligned_bible_src_eng | all | 300 | 0.921699 | 0.070416 |
| v52_fvt_conv5way_step21000 | aligned_bible_src_eng | v5_target | 300 | 0.921699 | 0.070416 |
| v52_fvt_conv5way_step21000 | aligned_tatoeba_src_eng | all | 300 | 0.926495 | 0.199645 |
| v52_fvt_conv5way_step21000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926495 | 0.199645 |
| v52_fvt_conv5way_step21000 | roundtrip_eng_pivot | all | 300 | 0.918635 | 0.032191 |
| v52_fvt_conv5way_step21000 | roundtrip_eng_pivot | v5_target | 300 | 0.918635 | 0.032191 |
| v52_fvt_conv5way_step21000 | roundtrip_src_eng | all | 300 | 0.918554 | 0.047697 |
| v52_fvt_conv5way_step21000 | roundtrip_src_eng | v5_target | 300 | 0.918554 | 0.047697 |
| v52_fvt_conv5way_step21000 | roundtrip_src_pivot | all | 300 | 0.935014 | 0.309922 |
| v52_fvt_conv5way_step21000 | roundtrip_src_pivot | v5_target | 300 | 0.935014 | 0.309922 |
| v52_fvt_conv5way_step21000 | same_language_bible_adjacent | all | 300 | 0.978739 | 0.758299 |
| v52_fvt_conv5way_step21000 | same_language_bible_adjacent | v5_target | 300 | 0.978739 | 0.758299 |
| v52_fvt_conv5way_step21000 | same_language_tatoeba_adjacent | all | 300 | 0.947416 | 0.388092 |
| v52_fvt_conv5way_step21000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947416 | 0.388092 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
