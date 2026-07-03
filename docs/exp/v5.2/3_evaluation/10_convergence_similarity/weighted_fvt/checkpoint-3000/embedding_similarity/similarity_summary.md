# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step3000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step3000 | aligned_bible_src_eng | all | 300 | 0.914900 | 0.007906 |
| v52_weighted_fvt_conv5way_step3000 | aligned_bible_src_eng | v5_target | 300 | 0.914900 | 0.007906 |
| v52_weighted_fvt_conv5way_step3000 | aligned_tatoeba_src_eng | all | 300 | 0.912549 | 0.149435 |
| v52_weighted_fvt_conv5way_step3000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.912549 | 0.149435 |
| v52_weighted_fvt_conv5way_step3000 | roundtrip_eng_pivot | all | 300 | 0.915639 | -0.016472 |
| v52_weighted_fvt_conv5way_step3000 | roundtrip_eng_pivot | v5_target | 300 | 0.915639 | -0.016472 |
| v52_weighted_fvt_conv5way_step3000 | roundtrip_src_eng | all | 300 | 0.911799 | -0.016496 |
| v52_weighted_fvt_conv5way_step3000 | roundtrip_src_eng | v5_target | 300 | 0.911799 | -0.016496 |
| v52_weighted_fvt_conv5way_step3000 | roundtrip_src_pivot | all | 300 | 0.941753 | 0.362686 |
| v52_weighted_fvt_conv5way_step3000 | roundtrip_src_pivot | v5_target | 300 | 0.941753 | 0.362686 |
| v52_weighted_fvt_conv5way_step3000 | same_language_bible_adjacent | all | 300 | 0.976892 | 0.740549 |
| v52_weighted_fvt_conv5way_step3000 | same_language_bible_adjacent | v5_target | 300 | 0.976892 | 0.740549 |
| v52_weighted_fvt_conv5way_step3000 | same_language_tatoeba_adjacent | all | 300 | 0.937486 | 0.351128 |
| v52_weighted_fvt_conv5way_step3000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.937486 | 0.351128 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
