# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step42000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step42000 | aligned_bible_src_eng | all | 300 | 0.921934 | 0.070890 |
| v52_fvt_conv5way_step42000 | aligned_bible_src_eng | v5_target | 300 | 0.921934 | 0.070890 |
| v52_fvt_conv5way_step42000 | aligned_tatoeba_src_eng | all | 300 | 0.926543 | 0.199284 |
| v52_fvt_conv5way_step42000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926543 | 0.199284 |
| v52_fvt_conv5way_step42000 | roundtrip_eng_pivot | all | 300 | 0.918926 | 0.033794 |
| v52_fvt_conv5way_step42000 | roundtrip_eng_pivot | v5_target | 300 | 0.918926 | 0.033794 |
| v52_fvt_conv5way_step42000 | roundtrip_src_eng | all | 300 | 0.918793 | 0.048445 |
| v52_fvt_conv5way_step42000 | roundtrip_src_eng | v5_target | 300 | 0.918793 | 0.048445 |
| v52_fvt_conv5way_step42000 | roundtrip_src_pivot | all | 300 | 0.935219 | 0.312741 |
| v52_fvt_conv5way_step42000 | roundtrip_src_pivot | v5_target | 300 | 0.935219 | 0.312741 |
| v52_fvt_conv5way_step42000 | same_language_bible_adjacent | all | 300 | 0.978738 | 0.758563 |
| v52_fvt_conv5way_step42000 | same_language_bible_adjacent | v5_target | 300 | 0.978738 | 0.758563 |
| v52_fvt_conv5way_step42000 | same_language_tatoeba_adjacent | all | 300 | 0.947514 | 0.389147 |
| v52_fvt_conv5way_step42000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947514 | 0.389147 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
