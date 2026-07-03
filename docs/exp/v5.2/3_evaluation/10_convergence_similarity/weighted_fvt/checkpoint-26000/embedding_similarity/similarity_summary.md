# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step26000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step26000 | aligned_bible_src_eng | all | 300 | 0.921523 | 0.068892 |
| v52_weighted_fvt_conv5way_step26000 | aligned_bible_src_eng | v5_target | 300 | 0.921523 | 0.068892 |
| v52_weighted_fvt_conv5way_step26000 | aligned_tatoeba_src_eng | all | 300 | 0.924756 | 0.205369 |
| v52_weighted_fvt_conv5way_step26000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.924756 | 0.205369 |
| v52_weighted_fvt_conv5way_step26000 | roundtrip_eng_pivot | all | 300 | 0.918147 | 0.023804 |
| v52_weighted_fvt_conv5way_step26000 | roundtrip_eng_pivot | v5_target | 300 | 0.918147 | 0.023804 |
| v52_weighted_fvt_conv5way_step26000 | roundtrip_src_eng | all | 300 | 0.918472 | 0.046449 |
| v52_weighted_fvt_conv5way_step26000 | roundtrip_src_eng | v5_target | 300 | 0.918472 | 0.046449 |
| v52_weighted_fvt_conv5way_step26000 | roundtrip_src_pivot | all | 300 | 0.933951 | 0.298010 |
| v52_weighted_fvt_conv5way_step26000 | roundtrip_src_pivot | v5_target | 300 | 0.933951 | 0.298010 |
| v52_weighted_fvt_conv5way_step26000 | same_language_bible_adjacent | all | 300 | 0.978179 | 0.755156 |
| v52_weighted_fvt_conv5way_step26000 | same_language_bible_adjacent | v5_target | 300 | 0.978179 | 0.755156 |
| v52_weighted_fvt_conv5way_step26000 | same_language_tatoeba_adjacent | all | 300 | 0.943935 | 0.370929 |
| v52_weighted_fvt_conv5way_step26000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943935 | 0.370929 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
