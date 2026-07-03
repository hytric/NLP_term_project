# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step6000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step6000 | aligned_bible_src_eng | all | 300 | 0.914480 | 0.036937 |
| v52_fvt_conv5way_step6000 | aligned_bible_src_eng | v5_target | 300 | 0.914480 | 0.036937 |
| v52_fvt_conv5way_step6000 | aligned_tatoeba_src_eng | all | 300 | 0.918331 | 0.174316 |
| v52_fvt_conv5way_step6000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.918331 | 0.174316 |
| v52_fvt_conv5way_step6000 | roundtrip_eng_pivot | all | 300 | 0.911256 | -0.000819 |
| v52_fvt_conv5way_step6000 | roundtrip_eng_pivot | v5_target | 300 | 0.911256 | -0.000819 |
| v52_fvt_conv5way_step6000 | roundtrip_src_eng | all | 300 | 0.911107 | 0.015488 |
| v52_fvt_conv5way_step6000 | roundtrip_src_eng | v5_target | 300 | 0.911107 | 0.015488 |
| v52_fvt_conv5way_step6000 | roundtrip_src_pivot | all | 300 | 0.931150 | 0.309022 |
| v52_fvt_conv5way_step6000 | roundtrip_src_pivot | v5_target | 300 | 0.931150 | 0.309022 |
| v52_fvt_conv5way_step6000 | same_language_bible_adjacent | all | 300 | 0.976640 | 0.749021 |
| v52_fvt_conv5way_step6000 | same_language_bible_adjacent | v5_target | 300 | 0.976640 | 0.749021 |
| v52_fvt_conv5way_step6000 | same_language_tatoeba_adjacent | all | 300 | 0.942988 | 0.380348 |
| v52_fvt_conv5way_step6000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.942988 | 0.380348 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
