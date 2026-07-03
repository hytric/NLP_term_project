# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step34000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step34000 | aligned_bible_src_eng | all | 300 | 0.923370 | 0.064134 |
| v52_weighted_fvt_conv5way_step34000 | aligned_bible_src_eng | v5_target | 300 | 0.923370 | 0.064134 |
| v52_weighted_fvt_conv5way_step34000 | aligned_tatoeba_src_eng | all | 300 | 0.926372 | 0.206019 |
| v52_weighted_fvt_conv5way_step34000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926372 | 0.206019 |
| v52_weighted_fvt_conv5way_step34000 | roundtrip_eng_pivot | all | 300 | 0.919785 | 0.016482 |
| v52_weighted_fvt_conv5way_step34000 | roundtrip_eng_pivot | v5_target | 300 | 0.919785 | 0.016482 |
| v52_weighted_fvt_conv5way_step34000 | roundtrip_src_eng | all | 300 | 0.920552 | 0.042522 |
| v52_weighted_fvt_conv5way_step34000 | roundtrip_src_eng | v5_target | 300 | 0.920552 | 0.042522 |
| v52_weighted_fvt_conv5way_step34000 | roundtrip_src_pivot | all | 300 | 0.935921 | 0.296885 |
| v52_weighted_fvt_conv5way_step34000 | roundtrip_src_pivot | v5_target | 300 | 0.935921 | 0.296885 |
| v52_weighted_fvt_conv5way_step34000 | same_language_bible_adjacent | all | 300 | 0.978924 | 0.755246 |
| v52_weighted_fvt_conv5way_step34000 | same_language_bible_adjacent | v5_target | 300 | 0.978924 | 0.755246 |
| v52_weighted_fvt_conv5way_step34000 | same_language_tatoeba_adjacent | all | 300 | 0.944999 | 0.368361 |
| v52_weighted_fvt_conv5way_step34000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944999 | 0.368361 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
