# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step14000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step14000 | aligned_bible_src_eng | all | 300 | 0.916727 | 0.048609 |
| v52_weighted_fvt_conv5way_step14000 | aligned_bible_src_eng | v5_target | 300 | 0.916727 | 0.048609 |
| v52_weighted_fvt_conv5way_step14000 | aligned_tatoeba_src_eng | all | 300 | 0.918028 | 0.182488 |
| v52_weighted_fvt_conv5way_step14000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.918028 | 0.182488 |
| v52_weighted_fvt_conv5way_step14000 | roundtrip_eng_pivot | all | 300 | 0.914012 | 0.009044 |
| v52_weighted_fvt_conv5way_step14000 | roundtrip_eng_pivot | v5_target | 300 | 0.914012 | 0.009044 |
| v52_weighted_fvt_conv5way_step14000 | roundtrip_src_eng | all | 300 | 0.913326 | 0.027086 |
| v52_weighted_fvt_conv5way_step14000 | roundtrip_src_eng | v5_target | 300 | 0.913326 | 0.027086 |
| v52_weighted_fvt_conv5way_step14000 | roundtrip_src_pivot | all | 300 | 0.930008 | 0.292866 |
| v52_weighted_fvt_conv5way_step14000 | roundtrip_src_pivot | v5_target | 300 | 0.930008 | 0.292866 |
| v52_weighted_fvt_conv5way_step14000 | same_language_bible_adjacent | all | 300 | 0.977135 | 0.755300 |
| v52_weighted_fvt_conv5way_step14000 | same_language_bible_adjacent | v5_target | 300 | 0.977135 | 0.755300 |
| v52_weighted_fvt_conv5way_step14000 | same_language_tatoeba_adjacent | all | 300 | 0.942015 | 0.374564 |
| v52_weighted_fvt_conv5way_step14000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.942015 | 0.374564 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
