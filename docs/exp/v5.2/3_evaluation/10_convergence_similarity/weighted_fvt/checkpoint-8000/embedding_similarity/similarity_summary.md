# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step8000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step8000 | aligned_bible_src_eng | all | 300 | 0.912791 | 0.028733 |
| v52_weighted_fvt_conv5way_step8000 | aligned_bible_src_eng | v5_target | 300 | 0.912791 | 0.028733 |
| v52_weighted_fvt_conv5way_step8000 | aligned_tatoeba_src_eng | all | 300 | 0.913355 | 0.161617 |
| v52_weighted_fvt_conv5way_step8000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.913355 | 0.161617 |
| v52_weighted_fvt_conv5way_step8000 | roundtrip_eng_pivot | all | 300 | 0.912611 | 0.001228 |
| v52_weighted_fvt_conv5way_step8000 | roundtrip_eng_pivot | v5_target | 300 | 0.912611 | 0.001228 |
| v52_weighted_fvt_conv5way_step8000 | roundtrip_src_eng | all | 300 | 0.909398 | 0.007359 |
| v52_weighted_fvt_conv5way_step8000 | roundtrip_src_eng | v5_target | 300 | 0.909398 | 0.007359 |
| v52_weighted_fvt_conv5way_step8000 | roundtrip_src_pivot | all | 300 | 0.930646 | 0.293814 |
| v52_weighted_fvt_conv5way_step8000 | roundtrip_src_pivot | v5_target | 300 | 0.930646 | 0.293814 |
| v52_weighted_fvt_conv5way_step8000 | same_language_bible_adjacent | all | 300 | 0.976511 | 0.753389 |
| v52_weighted_fvt_conv5way_step8000 | same_language_bible_adjacent | v5_target | 300 | 0.976511 | 0.753389 |
| v52_weighted_fvt_conv5way_step8000 | same_language_tatoeba_adjacent | all | 300 | 0.937156 | 0.358671 |
| v52_weighted_fvt_conv5way_step8000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.937156 | 0.358671 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
