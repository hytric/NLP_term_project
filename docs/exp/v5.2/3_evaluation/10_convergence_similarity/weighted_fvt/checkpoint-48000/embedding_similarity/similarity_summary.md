# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step48000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step48000 | aligned_bible_src_eng | all | 300 | 0.922431 | 0.066106 |
| v52_weighted_fvt_conv5way_step48000 | aligned_bible_src_eng | v5_target | 300 | 0.922431 | 0.066106 |
| v52_weighted_fvt_conv5way_step48000 | aligned_tatoeba_src_eng | all | 300 | 0.926527 | 0.211280 |
| v52_weighted_fvt_conv5way_step48000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926527 | 0.211280 |
| v52_weighted_fvt_conv5way_step48000 | roundtrip_eng_pivot | all | 300 | 0.918586 | 0.018541 |
| v52_weighted_fvt_conv5way_step48000 | roundtrip_eng_pivot | v5_target | 300 | 0.918586 | 0.018541 |
| v52_weighted_fvt_conv5way_step48000 | roundtrip_src_eng | all | 300 | 0.919488 | 0.044384 |
| v52_weighted_fvt_conv5way_step48000 | roundtrip_src_eng | v5_target | 300 | 0.919488 | 0.044384 |
| v52_weighted_fvt_conv5way_step48000 | roundtrip_src_pivot | all | 300 | 0.933583 | 0.291931 |
| v52_weighted_fvt_conv5way_step48000 | roundtrip_src_pivot | v5_target | 300 | 0.933583 | 0.291931 |
| v52_weighted_fvt_conv5way_step48000 | same_language_bible_adjacent | all | 300 | 0.978568 | 0.756308 |
| v52_weighted_fvt_conv5way_step48000 | same_language_bible_adjacent | v5_target | 300 | 0.978568 | 0.756308 |
| v52_weighted_fvt_conv5way_step48000 | same_language_tatoeba_adjacent | all | 300 | 0.944918 | 0.368187 |
| v52_weighted_fvt_conv5way_step48000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944918 | 0.368187 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
