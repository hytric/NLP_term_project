# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step41000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step41000 | aligned_bible_src_eng | all | 300 | 0.922171 | 0.071299 |
| v52_fvt_conv5way_step41000 | aligned_bible_src_eng | v5_target | 300 | 0.922171 | 0.071299 |
| v52_fvt_conv5way_step41000 | aligned_tatoeba_src_eng | all | 300 | 0.926729 | 0.198943 |
| v52_fvt_conv5way_step41000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926729 | 0.198943 |
| v52_fvt_conv5way_step41000 | roundtrip_eng_pivot | all | 300 | 0.919160 | 0.034309 |
| v52_fvt_conv5way_step41000 | roundtrip_eng_pivot | v5_target | 300 | 0.919160 | 0.034309 |
| v52_fvt_conv5way_step41000 | roundtrip_src_eng | all | 300 | 0.919040 | 0.048904 |
| v52_fvt_conv5way_step41000 | roundtrip_src_eng | v5_target | 300 | 0.919040 | 0.048904 |
| v52_fvt_conv5way_step41000 | roundtrip_src_pivot | all | 300 | 0.935381 | 0.312914 |
| v52_fvt_conv5way_step41000 | roundtrip_src_pivot | v5_target | 300 | 0.935381 | 0.312914 |
| v52_fvt_conv5way_step41000 | same_language_bible_adjacent | all | 300 | 0.978775 | 0.758324 |
| v52_fvt_conv5way_step41000 | same_language_bible_adjacent | v5_target | 300 | 0.978775 | 0.758324 |
| v52_fvt_conv5way_step41000 | same_language_tatoeba_adjacent | all | 300 | 0.947669 | 0.389464 |
| v52_fvt_conv5way_step41000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947669 | 0.389464 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
