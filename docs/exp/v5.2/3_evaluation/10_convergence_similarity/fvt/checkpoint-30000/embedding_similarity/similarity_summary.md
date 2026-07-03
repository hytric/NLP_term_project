# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step30000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step30000 | aligned_bible_src_eng | all | 300 | 0.921997 | 0.071583 |
| v52_fvt_conv5way_step30000 | aligned_bible_src_eng | v5_target | 300 | 0.921997 | 0.071583 |
| v52_fvt_conv5way_step30000 | aligned_tatoeba_src_eng | all | 300 | 0.926545 | 0.199337 |
| v52_fvt_conv5way_step30000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926545 | 0.199337 |
| v52_fvt_conv5way_step30000 | roundtrip_eng_pivot | all | 300 | 0.918943 | 0.033906 |
| v52_fvt_conv5way_step30000 | roundtrip_eng_pivot | v5_target | 300 | 0.918943 | 0.033906 |
| v52_fvt_conv5way_step30000 | roundtrip_src_eng | all | 300 | 0.918870 | 0.048916 |
| v52_fvt_conv5way_step30000 | roundtrip_src_eng | v5_target | 300 | 0.918870 | 0.048916 |
| v52_fvt_conv5way_step30000 | roundtrip_src_pivot | all | 300 | 0.935345 | 0.313072 |
| v52_fvt_conv5way_step30000 | roundtrip_src_pivot | v5_target | 300 | 0.935345 | 0.313072 |
| v52_fvt_conv5way_step30000 | same_language_bible_adjacent | all | 300 | 0.978759 | 0.758138 |
| v52_fvt_conv5way_step30000 | same_language_bible_adjacent | v5_target | 300 | 0.978759 | 0.758138 |
| v52_fvt_conv5way_step30000 | same_language_tatoeba_adjacent | all | 300 | 0.947410 | 0.388230 |
| v52_fvt_conv5way_step30000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947410 | 0.388230 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
