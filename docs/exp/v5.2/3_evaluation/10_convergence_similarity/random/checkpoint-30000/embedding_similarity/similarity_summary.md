# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step30000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step30000 | aligned_bible_src_eng | all | 300 | 0.921463 | 0.043340 |
| v52_random_conv5way_step30000 | aligned_bible_src_eng | v5_target | 300 | 0.921463 | 0.043340 |
| v52_random_conv5way_step30000 | aligned_tatoeba_src_eng | all | 300 | 0.922643 | 0.186718 |
| v52_random_conv5way_step30000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922643 | 0.186718 |
| v52_random_conv5way_step30000 | roundtrip_eng_pivot | all | 300 | 0.919246 | 0.019937 |
| v52_random_conv5way_step30000 | roundtrip_eng_pivot | v5_target | 300 | 0.919246 | 0.019937 |
| v52_random_conv5way_step30000 | roundtrip_src_eng | all | 300 | 0.918242 | 0.021112 |
| v52_random_conv5way_step30000 | roundtrip_src_eng | v5_target | 300 | 0.918242 | 0.021112 |
| v52_random_conv5way_step30000 | roundtrip_src_pivot | all | 300 | 0.938922 | 0.341603 |
| v52_random_conv5way_step30000 | roundtrip_src_pivot | v5_target | 300 | 0.938922 | 0.341603 |
| v52_random_conv5way_step30000 | same_language_bible_adjacent | all | 300 | 0.977962 | 0.744609 |
| v52_random_conv5way_step30000 | same_language_bible_adjacent | v5_target | 300 | 0.977962 | 0.744609 |
| v52_random_conv5way_step30000 | same_language_tatoeba_adjacent | all | 300 | 0.943554 | 0.355150 |
| v52_random_conv5way_step30000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943554 | 0.355150 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
