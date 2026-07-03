# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step36000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step36000 | aligned_bible_src_eng | all | 300 | 0.921913 | 0.071386 |
| v52_fvt_conv5way_step36000 | aligned_bible_src_eng | v5_target | 300 | 0.921913 | 0.071386 |
| v52_fvt_conv5way_step36000 | aligned_tatoeba_src_eng | all | 300 | 0.926572 | 0.198912 |
| v52_fvt_conv5way_step36000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926572 | 0.198912 |
| v52_fvt_conv5way_step36000 | roundtrip_eng_pivot | all | 300 | 0.918951 | 0.034515 |
| v52_fvt_conv5way_step36000 | roundtrip_eng_pivot | v5_target | 300 | 0.918951 | 0.034515 |
| v52_fvt_conv5way_step36000 | roundtrip_src_eng | all | 300 | 0.918772 | 0.048868 |
| v52_fvt_conv5way_step36000 | roundtrip_src_eng | v5_target | 300 | 0.918772 | 0.048868 |
| v52_fvt_conv5way_step36000 | roundtrip_src_pivot | all | 300 | 0.935330 | 0.314068 |
| v52_fvt_conv5way_step36000 | roundtrip_src_pivot | v5_target | 300 | 0.935330 | 0.314068 |
| v52_fvt_conv5way_step36000 | same_language_bible_adjacent | all | 300 | 0.978728 | 0.758357 |
| v52_fvt_conv5way_step36000 | same_language_bible_adjacent | v5_target | 300 | 0.978728 | 0.758357 |
| v52_fvt_conv5way_step36000 | same_language_tatoeba_adjacent | all | 300 | 0.947498 | 0.389417 |
| v52_fvt_conv5way_step36000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947498 | 0.389417 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
