# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step11000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step11000 | aligned_bible_src_eng | all | 300 | 0.919197 | 0.039515 |
| v52_random_conv5way_step11000 | aligned_bible_src_eng | v5_target | 300 | 0.919197 | 0.039515 |
| v52_random_conv5way_step11000 | aligned_tatoeba_src_eng | all | 300 | 0.919032 | 0.178825 |
| v52_random_conv5way_step11000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.919032 | 0.178825 |
| v52_random_conv5way_step11000 | roundtrip_eng_pivot | all | 300 | 0.917635 | 0.018936 |
| v52_random_conv5way_step11000 | roundtrip_eng_pivot | v5_target | 300 | 0.917635 | 0.018936 |
| v52_random_conv5way_step11000 | roundtrip_src_eng | all | 300 | 0.916084 | 0.018518 |
| v52_random_conv5way_step11000 | roundtrip_src_eng | v5_target | 300 | 0.916084 | 0.018518 |
| v52_random_conv5way_step11000 | roundtrip_src_pivot | all | 300 | 0.938843 | 0.341063 |
| v52_random_conv5way_step11000 | roundtrip_src_pivot | v5_target | 300 | 0.938843 | 0.341063 |
| v52_random_conv5way_step11000 | same_language_bible_adjacent | all | 300 | 0.977592 | 0.741957 |
| v52_random_conv5way_step11000 | same_language_bible_adjacent | v5_target | 300 | 0.977592 | 0.741957 |
| v52_random_conv5way_step11000 | same_language_tatoeba_adjacent | all | 300 | 0.941387 | 0.351308 |
| v52_random_conv5way_step11000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.941387 | 0.351308 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
