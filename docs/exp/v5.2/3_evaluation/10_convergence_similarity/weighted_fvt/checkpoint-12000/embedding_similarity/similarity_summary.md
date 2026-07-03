# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step12000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step12000 | aligned_bible_src_eng | all | 300 | 0.915774 | 0.046284 |
| v52_weighted_fvt_conv5way_step12000 | aligned_bible_src_eng | v5_target | 300 | 0.915774 | 0.046284 |
| v52_weighted_fvt_conv5way_step12000 | aligned_tatoeba_src_eng | all | 300 | 0.918331 | 0.183459 |
| v52_weighted_fvt_conv5way_step12000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.918331 | 0.183459 |
| v52_weighted_fvt_conv5way_step12000 | roundtrip_eng_pivot | all | 300 | 0.913454 | 0.011133 |
| v52_weighted_fvt_conv5way_step12000 | roundtrip_eng_pivot | v5_target | 300 | 0.913454 | 0.011133 |
| v52_weighted_fvt_conv5way_step12000 | roundtrip_src_eng | all | 300 | 0.912555 | 0.024894 |
| v52_weighted_fvt_conv5way_step12000 | roundtrip_src_eng | v5_target | 300 | 0.912555 | 0.024894 |
| v52_weighted_fvt_conv5way_step12000 | roundtrip_src_pivot | all | 300 | 0.931096 | 0.293429 |
| v52_weighted_fvt_conv5way_step12000 | roundtrip_src_pivot | v5_target | 300 | 0.931096 | 0.293429 |
| v52_weighted_fvt_conv5way_step12000 | same_language_bible_adjacent | all | 300 | 0.976903 | 0.752570 |
| v52_weighted_fvt_conv5way_step12000 | same_language_bible_adjacent | v5_target | 300 | 0.976903 | 0.752570 |
| v52_weighted_fvt_conv5way_step12000 | same_language_tatoeba_adjacent | all | 300 | 0.940894 | 0.368734 |
| v52_weighted_fvt_conv5way_step12000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.940894 | 0.368734 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
