# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step47000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step47000 | aligned_bible_src_eng | all | 300 | 0.922198 | 0.071148 |
| v52_fvt_conv5way_step47000 | aligned_bible_src_eng | v5_target | 300 | 0.922198 | 0.071148 |
| v52_fvt_conv5way_step47000 | aligned_tatoeba_src_eng | all | 300 | 0.926762 | 0.199743 |
| v52_fvt_conv5way_step47000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926762 | 0.199743 |
| v52_fvt_conv5way_step47000 | roundtrip_eng_pivot | all | 300 | 0.919230 | 0.034036 |
| v52_fvt_conv5way_step47000 | roundtrip_eng_pivot | v5_target | 300 | 0.919230 | 0.034036 |
| v52_fvt_conv5way_step47000 | roundtrip_src_eng | all | 300 | 0.919050 | 0.048676 |
| v52_fvt_conv5way_step47000 | roundtrip_src_eng | v5_target | 300 | 0.919050 | 0.048676 |
| v52_fvt_conv5way_step47000 | roundtrip_src_pivot | all | 300 | 0.935403 | 0.313044 |
| v52_fvt_conv5way_step47000 | roundtrip_src_pivot | v5_target | 300 | 0.935403 | 0.313044 |
| v52_fvt_conv5way_step47000 | same_language_bible_adjacent | all | 300 | 0.978788 | 0.758579 |
| v52_fvt_conv5way_step47000 | same_language_bible_adjacent | v5_target | 300 | 0.978788 | 0.758579 |
| v52_fvt_conv5way_step47000 | same_language_tatoeba_adjacent | all | 300 | 0.947630 | 0.388772 |
| v52_fvt_conv5way_step47000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947630 | 0.388772 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
