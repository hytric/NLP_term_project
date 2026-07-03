# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step26000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step26000 | aligned_bible_src_eng | all | 300 | 0.921817 | 0.071818 |
| v52_fvt_conv5way_step26000 | aligned_bible_src_eng | v5_target | 300 | 0.921817 | 0.071818 |
| v52_fvt_conv5way_step26000 | aligned_tatoeba_src_eng | all | 300 | 0.926238 | 0.198892 |
| v52_fvt_conv5way_step26000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926238 | 0.198892 |
| v52_fvt_conv5way_step26000 | roundtrip_eng_pivot | all | 300 | 0.918766 | 0.034013 |
| v52_fvt_conv5way_step26000 | roundtrip_eng_pivot | v5_target | 300 | 0.918766 | 0.034013 |
| v52_fvt_conv5way_step26000 | roundtrip_src_eng | all | 300 | 0.918699 | 0.049514 |
| v52_fvt_conv5way_step26000 | roundtrip_src_eng | v5_target | 300 | 0.918699 | 0.049514 |
| v52_fvt_conv5way_step26000 | roundtrip_src_pivot | all | 300 | 0.934998 | 0.310782 |
| v52_fvt_conv5way_step26000 | roundtrip_src_pivot | v5_target | 300 | 0.934998 | 0.310782 |
| v52_fvt_conv5way_step26000 | same_language_bible_adjacent | all | 300 | 0.978662 | 0.757948 |
| v52_fvt_conv5way_step26000 | same_language_bible_adjacent | v5_target | 300 | 0.978662 | 0.757948 |
| v52_fvt_conv5way_step26000 | same_language_tatoeba_adjacent | all | 300 | 0.947159 | 0.388591 |
| v52_fvt_conv5way_step26000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947159 | 0.388591 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
