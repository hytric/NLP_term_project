# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step48000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step48000 | aligned_bible_src_eng | all | 300 | 0.922151 | 0.070913 |
| v52_fvt_conv5way_step48000 | aligned_bible_src_eng | v5_target | 300 | 0.922151 | 0.070913 |
| v52_fvt_conv5way_step48000 | aligned_tatoeba_src_eng | all | 300 | 0.926726 | 0.199460 |
| v52_fvt_conv5way_step48000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926726 | 0.199460 |
| v52_fvt_conv5way_step48000 | roundtrip_eng_pivot | all | 300 | 0.919180 | 0.033815 |
| v52_fvt_conv5way_step48000 | roundtrip_eng_pivot | v5_target | 300 | 0.919180 | 0.033815 |
| v52_fvt_conv5way_step48000 | roundtrip_src_eng | all | 300 | 0.919004 | 0.048434 |
| v52_fvt_conv5way_step48000 | roundtrip_src_eng | v5_target | 300 | 0.919004 | 0.048434 |
| v52_fvt_conv5way_step48000 | roundtrip_src_pivot | all | 300 | 0.935375 | 0.313109 |
| v52_fvt_conv5way_step48000 | roundtrip_src_pivot | v5_target | 300 | 0.935375 | 0.313109 |
| v52_fvt_conv5way_step48000 | same_language_bible_adjacent | all | 300 | 0.978781 | 0.758625 |
| v52_fvt_conv5way_step48000 | same_language_bible_adjacent | v5_target | 300 | 0.978781 | 0.758625 |
| v52_fvt_conv5way_step48000 | same_language_tatoeba_adjacent | all | 300 | 0.947622 | 0.388893 |
| v52_fvt_conv5way_step48000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947622 | 0.388893 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
