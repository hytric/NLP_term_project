# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step35000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step35000 | aligned_bible_src_eng | all | 300 | 0.921957 | 0.063648 |
| v52_weighted_fvt_conv5way_step35000 | aligned_bible_src_eng | v5_target | 300 | 0.921957 | 0.063648 |
| v52_weighted_fvt_conv5way_step35000 | aligned_tatoeba_src_eng | all | 300 | 0.925109 | 0.205519 |
| v52_weighted_fvt_conv5way_step35000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925109 | 0.205519 |
| v52_weighted_fvt_conv5way_step35000 | roundtrip_eng_pivot | all | 300 | 0.918355 | 0.016672 |
| v52_weighted_fvt_conv5way_step35000 | roundtrip_eng_pivot | v5_target | 300 | 0.918355 | 0.016672 |
| v52_weighted_fvt_conv5way_step35000 | roundtrip_src_eng | all | 300 | 0.919033 | 0.041638 |
| v52_weighted_fvt_conv5way_step35000 | roundtrip_src_eng | v5_target | 300 | 0.919033 | 0.041638 |
| v52_weighted_fvt_conv5way_step35000 | roundtrip_src_pivot | all | 300 | 0.934129 | 0.293551 |
| v52_weighted_fvt_conv5way_step35000 | roundtrip_src_pivot | v5_target | 300 | 0.934129 | 0.293551 |
| v52_weighted_fvt_conv5way_step35000 | same_language_bible_adjacent | all | 300 | 0.978444 | 0.755415 |
| v52_weighted_fvt_conv5way_step35000 | same_language_bible_adjacent | v5_target | 300 | 0.978444 | 0.755415 |
| v52_weighted_fvt_conv5way_step35000 | same_language_tatoeba_adjacent | all | 300 | 0.944012 | 0.369452 |
| v52_weighted_fvt_conv5way_step35000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944012 | 0.369452 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
