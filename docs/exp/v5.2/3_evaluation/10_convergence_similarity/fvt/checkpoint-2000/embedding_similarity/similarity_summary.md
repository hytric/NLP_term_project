# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step2000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step2000 | aligned_bible_src_eng | all | 300 | 0.915830 | 0.020905 |
| v52_fvt_conv5way_step2000 | aligned_bible_src_eng | v5_target | 300 | 0.915830 | 0.020905 |
| v52_fvt_conv5way_step2000 | aligned_tatoeba_src_eng | all | 300 | 0.910869 | 0.136407 |
| v52_fvt_conv5way_step2000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.910869 | 0.136407 |
| v52_fvt_conv5way_step2000 | roundtrip_eng_pivot | all | 300 | 0.914158 | -0.007198 |
| v52_fvt_conv5way_step2000 | roundtrip_eng_pivot | v5_target | 300 | 0.914158 | -0.007198 |
| v52_fvt_conv5way_step2000 | roundtrip_src_eng | all | 300 | 0.912909 | 0.000618 |
| v52_fvt_conv5way_step2000 | roundtrip_src_eng | v5_target | 300 | 0.912909 | 0.000618 |
| v52_fvt_conv5way_step2000 | roundtrip_src_pivot | all | 300 | 0.940441 | 0.353430 |
| v52_fvt_conv5way_step2000 | roundtrip_src_pivot | v5_target | 300 | 0.940441 | 0.353430 |
| v52_fvt_conv5way_step2000 | same_language_bible_adjacent | all | 300 | 0.977250 | 0.741088 |
| v52_fvt_conv5way_step2000 | same_language_bible_adjacent | v5_target | 300 | 0.977250 | 0.741088 |
| v52_fvt_conv5way_step2000 | same_language_tatoeba_adjacent | all | 300 | 0.939904 | 0.364384 |
| v52_fvt_conv5way_step2000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.939904 | 0.364384 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
