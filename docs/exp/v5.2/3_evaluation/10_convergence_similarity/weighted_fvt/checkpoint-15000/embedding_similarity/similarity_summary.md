# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step15000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step15000 | aligned_bible_src_eng | all | 300 | 0.920789 | 0.065834 |
| v52_weighted_fvt_conv5way_step15000 | aligned_bible_src_eng | v5_target | 300 | 0.920789 | 0.065834 |
| v52_weighted_fvt_conv5way_step15000 | aligned_tatoeba_src_eng | all | 300 | 0.922638 | 0.200952 |
| v52_weighted_fvt_conv5way_step15000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922638 | 0.200952 |
| v52_weighted_fvt_conv5way_step15000 | roundtrip_eng_pivot | all | 300 | 0.918188 | 0.026323 |
| v52_weighted_fvt_conv5way_step15000 | roundtrip_eng_pivot | v5_target | 300 | 0.918188 | 0.026323 |
| v52_weighted_fvt_conv5way_step15000 | roundtrip_src_eng | all | 300 | 0.917630 | 0.044433 |
| v52_weighted_fvt_conv5way_step15000 | roundtrip_src_eng | v5_target | 300 | 0.917630 | 0.044433 |
| v52_weighted_fvt_conv5way_step15000 | roundtrip_src_pivot | all | 300 | 0.933371 | 0.293797 |
| v52_weighted_fvt_conv5way_step15000 | roundtrip_src_pivot | v5_target | 300 | 0.933371 | 0.293797 |
| v52_weighted_fvt_conv5way_step15000 | same_language_bible_adjacent | all | 300 | 0.978173 | 0.756054 |
| v52_weighted_fvt_conv5way_step15000 | same_language_bible_adjacent | v5_target | 300 | 0.978173 | 0.756054 |
| v52_weighted_fvt_conv5way_step15000 | same_language_tatoeba_adjacent | all | 300 | 0.943038 | 0.364545 |
| v52_weighted_fvt_conv5way_step15000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943038 | 0.364545 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
