# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step18000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step18000 | aligned_bible_src_eng | all | 300 | 0.919456 | 0.068048 |
| v52_weighted_fvt_conv5way_step18000 | aligned_bible_src_eng | v5_target | 300 | 0.919456 | 0.068048 |
| v52_weighted_fvt_conv5way_step18000 | aligned_tatoeba_src_eng | all | 300 | 0.921677 | 0.197352 |
| v52_weighted_fvt_conv5way_step18000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.921677 | 0.197352 |
| v52_weighted_fvt_conv5way_step18000 | roundtrip_eng_pivot | all | 300 | 0.916525 | 0.025730 |
| v52_weighted_fvt_conv5way_step18000 | roundtrip_eng_pivot | v5_target | 300 | 0.916525 | 0.025730 |
| v52_weighted_fvt_conv5way_step18000 | roundtrip_src_eng | all | 300 | 0.916296 | 0.046102 |
| v52_weighted_fvt_conv5way_step18000 | roundtrip_src_eng | v5_target | 300 | 0.916296 | 0.046102 |
| v52_weighted_fvt_conv5way_step18000 | roundtrip_src_pivot | all | 300 | 0.932579 | 0.292481 |
| v52_weighted_fvt_conv5way_step18000 | roundtrip_src_pivot | v5_target | 300 | 0.932579 | 0.292481 |
| v52_weighted_fvt_conv5way_step18000 | same_language_bible_adjacent | all | 300 | 0.978176 | 0.758544 |
| v52_weighted_fvt_conv5way_step18000 | same_language_bible_adjacent | v5_target | 300 | 0.978176 | 0.758544 |
| v52_weighted_fvt_conv5way_step18000 | same_language_tatoeba_adjacent | all | 300 | 0.943063 | 0.372717 |
| v52_weighted_fvt_conv5way_step18000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943063 | 0.372717 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
