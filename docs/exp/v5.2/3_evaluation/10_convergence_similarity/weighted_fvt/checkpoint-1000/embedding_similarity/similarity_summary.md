# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step1000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step1000 | aligned_bible_src_eng | all | 300 | 0.913039 | -0.024446 |
| v52_weighted_fvt_conv5way_step1000 | aligned_bible_src_eng | v5_target | 300 | 0.913039 | -0.024446 |
| v52_weighted_fvt_conv5way_step1000 | aligned_tatoeba_src_eng | all | 300 | 0.909385 | 0.111509 |
| v52_weighted_fvt_conv5way_step1000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.909385 | 0.111509 |
| v52_weighted_fvt_conv5way_step1000 | roundtrip_eng_pivot | all | 300 | 0.914297 | -0.042098 |
| v52_weighted_fvt_conv5way_step1000 | roundtrip_eng_pivot | v5_target | 300 | 0.914297 | -0.042098 |
| v52_weighted_fvt_conv5way_step1000 | roundtrip_src_eng | all | 300 | 0.909521 | -0.048425 |
| v52_weighted_fvt_conv5way_step1000 | roundtrip_src_eng | v5_target | 300 | 0.909521 | -0.048425 |
| v52_weighted_fvt_conv5way_step1000 | roundtrip_src_pivot | all | 300 | 0.950935 | 0.441811 |
| v52_weighted_fvt_conv5way_step1000 | roundtrip_src_pivot | v5_target | 300 | 0.950935 | 0.441811 |
| v52_weighted_fvt_conv5way_step1000 | same_language_bible_adjacent | all | 300 | 0.975912 | 0.721249 |
| v52_weighted_fvt_conv5way_step1000 | same_language_bible_adjacent | v5_target | 300 | 0.975912 | 0.721249 |
| v52_weighted_fvt_conv5way_step1000 | same_language_tatoeba_adjacent | all | 300 | 0.940402 | 0.354809 |
| v52_weighted_fvt_conv5way_step1000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.940402 | 0.354809 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
