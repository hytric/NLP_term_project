# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step16000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step16000 | aligned_bible_src_eng | all | 300 | 0.919204 | 0.066014 |
| v52_weighted_fvt_conv5way_step16000 | aligned_bible_src_eng | v5_target | 300 | 0.919204 | 0.066014 |
| v52_weighted_fvt_conv5way_step16000 | aligned_tatoeba_src_eng | all | 300 | 0.920987 | 0.198701 |
| v52_weighted_fvt_conv5way_step16000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.920987 | 0.198701 |
| v52_weighted_fvt_conv5way_step16000 | roundtrip_eng_pivot | all | 300 | 0.916445 | 0.026558 |
| v52_weighted_fvt_conv5way_step16000 | roundtrip_eng_pivot | v5_target | 300 | 0.916445 | 0.026558 |
| v52_weighted_fvt_conv5way_step16000 | roundtrip_src_eng | all | 300 | 0.916079 | 0.045595 |
| v52_weighted_fvt_conv5way_step16000 | roundtrip_src_eng | v5_target | 300 | 0.916079 | 0.045595 |
| v52_weighted_fvt_conv5way_step16000 | roundtrip_src_pivot | all | 300 | 0.932004 | 0.291339 |
| v52_weighted_fvt_conv5way_step16000 | roundtrip_src_pivot | v5_target | 300 | 0.932004 | 0.291339 |
| v52_weighted_fvt_conv5way_step16000 | same_language_bible_adjacent | all | 300 | 0.977420 | 0.752091 |
| v52_weighted_fvt_conv5way_step16000 | same_language_bible_adjacent | v5_target | 300 | 0.977420 | 0.752091 |
| v52_weighted_fvt_conv5way_step16000 | same_language_tatoeba_adjacent | all | 300 | 0.941125 | 0.368046 |
| v52_weighted_fvt_conv5way_step16000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.941125 | 0.368046 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
