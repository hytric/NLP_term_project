# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step7000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step7000 | aligned_bible_src_eng | all | 300 | 0.914367 | 0.034224 |
| v52_fvt_conv5way_step7000 | aligned_bible_src_eng | v5_target | 300 | 0.914367 | 0.034224 |
| v52_fvt_conv5way_step7000 | aligned_tatoeba_src_eng | all | 300 | 0.916593 | 0.166120 |
| v52_fvt_conv5way_step7000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.916593 | 0.166120 |
| v52_fvt_conv5way_step7000 | roundtrip_eng_pivot | all | 300 | 0.911267 | -0.002998 |
| v52_fvt_conv5way_step7000 | roundtrip_eng_pivot | v5_target | 300 | 0.911267 | -0.002998 |
| v52_fvt_conv5way_step7000 | roundtrip_src_eng | all | 300 | 0.910949 | 0.011649 |
| v52_fvt_conv5way_step7000 | roundtrip_src_eng | v5_target | 300 | 0.910949 | 0.011649 |
| v52_fvt_conv5way_step7000 | roundtrip_src_pivot | all | 300 | 0.930608 | 0.307558 |
| v52_fvt_conv5way_step7000 | roundtrip_src_pivot | v5_target | 300 | 0.930608 | 0.307558 |
| v52_fvt_conv5way_step7000 | same_language_bible_adjacent | all | 300 | 0.977007 | 0.756684 |
| v52_fvt_conv5way_step7000 | same_language_bible_adjacent | v5_target | 300 | 0.977007 | 0.756684 |
| v52_fvt_conv5way_step7000 | same_language_tatoeba_adjacent | all | 300 | 0.941403 | 0.381018 |
| v52_fvt_conv5way_step7000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.941403 | 0.381018 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
