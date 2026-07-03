# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step31000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step31000 | aligned_bible_src_eng | all | 300 | 0.921650 | 0.073269 |
| v52_weighted_fvt_conv5way_step31000 | aligned_bible_src_eng | v5_target | 300 | 0.921650 | 0.073269 |
| v52_weighted_fvt_conv5way_step31000 | aligned_tatoeba_src_eng | all | 300 | 0.925484 | 0.209762 |
| v52_weighted_fvt_conv5way_step31000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925484 | 0.209762 |
| v52_weighted_fvt_conv5way_step31000 | roundtrip_eng_pivot | all | 300 | 0.918084 | 0.027672 |
| v52_weighted_fvt_conv5way_step31000 | roundtrip_eng_pivot | v5_target | 300 | 0.918084 | 0.027672 |
| v52_weighted_fvt_conv5way_step31000 | roundtrip_src_eng | all | 300 | 0.918662 | 0.050865 |
| v52_weighted_fvt_conv5way_step31000 | roundtrip_src_eng | v5_target | 300 | 0.918662 | 0.050865 |
| v52_weighted_fvt_conv5way_step31000 | roundtrip_src_pivot | all | 300 | 0.934293 | 0.299302 |
| v52_weighted_fvt_conv5way_step31000 | roundtrip_src_pivot | v5_target | 300 | 0.934293 | 0.299302 |
| v52_weighted_fvt_conv5way_step31000 | same_language_bible_adjacent | all | 300 | 0.978430 | 0.756768 |
| v52_weighted_fvt_conv5way_step31000 | same_language_bible_adjacent | v5_target | 300 | 0.978430 | 0.756768 |
| v52_weighted_fvt_conv5way_step31000 | same_language_tatoeba_adjacent | all | 300 | 0.944215 | 0.369673 |
| v52_weighted_fvt_conv5way_step31000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944215 | 0.369673 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
