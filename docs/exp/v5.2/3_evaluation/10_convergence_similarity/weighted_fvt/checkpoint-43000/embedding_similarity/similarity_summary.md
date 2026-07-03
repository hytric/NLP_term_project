# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step43000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step43000 | aligned_bible_src_eng | all | 300 | 0.921693 | 0.061339 |
| v52_weighted_fvt_conv5way_step43000 | aligned_bible_src_eng | v5_target | 300 | 0.921693 | 0.061339 |
| v52_weighted_fvt_conv5way_step43000 | aligned_tatoeba_src_eng | all | 300 | 0.926387 | 0.212051 |
| v52_weighted_fvt_conv5way_step43000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926387 | 0.212051 |
| v52_weighted_fvt_conv5way_step43000 | roundtrip_eng_pivot | all | 300 | 0.917988 | 0.013754 |
| v52_weighted_fvt_conv5way_step43000 | roundtrip_eng_pivot | v5_target | 300 | 0.917988 | 0.013754 |
| v52_weighted_fvt_conv5way_step43000 | roundtrip_src_eng | all | 300 | 0.918661 | 0.039395 |
| v52_weighted_fvt_conv5way_step43000 | roundtrip_src_eng | v5_target | 300 | 0.918661 | 0.039395 |
| v52_weighted_fvt_conv5way_step43000 | roundtrip_src_pivot | all | 300 | 0.933979 | 0.299400 |
| v52_weighted_fvt_conv5way_step43000 | roundtrip_src_pivot | v5_target | 300 | 0.933979 | 0.299400 |
| v52_weighted_fvt_conv5way_step43000 | same_language_bible_adjacent | all | 300 | 0.978510 | 0.758370 |
| v52_weighted_fvt_conv5way_step43000 | same_language_bible_adjacent | v5_target | 300 | 0.978510 | 0.758370 |
| v52_weighted_fvt_conv5way_step43000 | same_language_tatoeba_adjacent | all | 300 | 0.944874 | 0.370922 |
| v52_weighted_fvt_conv5way_step43000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944874 | 0.370922 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
