# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step25000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step25000 | aligned_bible_src_eng | all | 300 | 0.921983 | 0.072891 |
| v52_fvt_conv5way_step25000 | aligned_bible_src_eng | v5_target | 300 | 0.921983 | 0.072891 |
| v52_fvt_conv5way_step25000 | aligned_tatoeba_src_eng | all | 300 | 0.926405 | 0.199912 |
| v52_fvt_conv5way_step25000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926405 | 0.199912 |
| v52_fvt_conv5way_step25000 | roundtrip_eng_pivot | all | 300 | 0.918955 | 0.035555 |
| v52_fvt_conv5way_step25000 | roundtrip_eng_pivot | v5_target | 300 | 0.918955 | 0.035555 |
| v52_fvt_conv5way_step25000 | roundtrip_src_eng | all | 300 | 0.918850 | 0.050324 |
| v52_fvt_conv5way_step25000 | roundtrip_src_eng | v5_target | 300 | 0.918850 | 0.050324 |
| v52_fvt_conv5way_step25000 | roundtrip_src_pivot | all | 300 | 0.935133 | 0.311228 |
| v52_fvt_conv5way_step25000 | roundtrip_src_pivot | v5_target | 300 | 0.935133 | 0.311228 |
| v52_fvt_conv5way_step25000 | same_language_bible_adjacent | all | 300 | 0.978649 | 0.757389 |
| v52_fvt_conv5way_step25000 | same_language_bible_adjacent | v5_target | 300 | 0.978649 | 0.757389 |
| v52_fvt_conv5way_step25000 | same_language_tatoeba_adjacent | all | 300 | 0.947293 | 0.387984 |
| v52_fvt_conv5way_step25000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947293 | 0.387984 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
