# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step23000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step23000 | aligned_bible_src_eng | all | 300 | 0.921715 | 0.070593 |
| v52_fvt_conv5way_step23000 | aligned_bible_src_eng | v5_target | 300 | 0.921715 | 0.070593 |
| v52_fvt_conv5way_step23000 | aligned_tatoeba_src_eng | all | 300 | 0.926610 | 0.199524 |
| v52_fvt_conv5way_step23000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926610 | 0.199524 |
| v52_fvt_conv5way_step23000 | roundtrip_eng_pivot | all | 300 | 0.918765 | 0.033758 |
| v52_fvt_conv5way_step23000 | roundtrip_eng_pivot | v5_target | 300 | 0.918765 | 0.033758 |
| v52_fvt_conv5way_step23000 | roundtrip_src_eng | all | 300 | 0.918576 | 0.048223 |
| v52_fvt_conv5way_step23000 | roundtrip_src_eng | v5_target | 300 | 0.918576 | 0.048223 |
| v52_fvt_conv5way_step23000 | roundtrip_src_pivot | all | 300 | 0.934929 | 0.310196 |
| v52_fvt_conv5way_step23000 | roundtrip_src_pivot | v5_target | 300 | 0.934929 | 0.310196 |
| v52_fvt_conv5way_step23000 | same_language_bible_adjacent | all | 300 | 0.978685 | 0.758080 |
| v52_fvt_conv5way_step23000 | same_language_bible_adjacent | v5_target | 300 | 0.978685 | 0.758080 |
| v52_fvt_conv5way_step23000 | same_language_tatoeba_adjacent | all | 300 | 0.947417 | 0.388347 |
| v52_fvt_conv5way_step23000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947417 | 0.388347 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
