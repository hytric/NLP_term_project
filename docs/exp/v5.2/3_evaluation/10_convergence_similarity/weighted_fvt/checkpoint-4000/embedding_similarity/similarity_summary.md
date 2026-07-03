# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step4000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step4000 | aligned_bible_src_eng | all | 300 | 0.913611 | 0.004846 |
| v52_weighted_fvt_conv5way_step4000 | aligned_bible_src_eng | v5_target | 300 | 0.913611 | 0.004846 |
| v52_weighted_fvt_conv5way_step4000 | aligned_tatoeba_src_eng | all | 300 | 0.912193 | 0.144151 |
| v52_weighted_fvt_conv5way_step4000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.912193 | 0.144151 |
| v52_weighted_fvt_conv5way_step4000 | roundtrip_eng_pivot | all | 300 | 0.913849 | -0.018622 |
| v52_weighted_fvt_conv5way_step4000 | roundtrip_eng_pivot | v5_target | 300 | 0.913849 | -0.018622 |
| v52_weighted_fvt_conv5way_step4000 | roundtrip_src_eng | all | 300 | 0.910341 | -0.017589 |
| v52_weighted_fvt_conv5way_step4000 | roundtrip_src_eng | v5_target | 300 | 0.910341 | -0.017589 |
| v52_weighted_fvt_conv5way_step4000 | roundtrip_src_pivot | all | 300 | 0.938553 | 0.335309 |
| v52_weighted_fvt_conv5way_step4000 | roundtrip_src_pivot | v5_target | 300 | 0.938553 | 0.335309 |
| v52_weighted_fvt_conv5way_step4000 | same_language_bible_adjacent | all | 300 | 0.976906 | 0.743201 |
| v52_weighted_fvt_conv5way_step4000 | same_language_bible_adjacent | v5_target | 300 | 0.976906 | 0.743201 |
| v52_weighted_fvt_conv5way_step4000 | same_language_tatoeba_adjacent | all | 300 | 0.937449 | 0.350939 |
| v52_weighted_fvt_conv5way_step4000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.937449 | 0.350939 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
