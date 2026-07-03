# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step3000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step3000 | aligned_bible_src_eng | all | 300 | 0.909967 | -0.009076 |
| v52_random_conv5way_step3000 | aligned_bible_src_eng | v5_target | 300 | 0.909967 | -0.009076 |
| v52_random_conv5way_step3000 | aligned_tatoeba_src_eng | all | 300 | 0.913146 | 0.148003 |
| v52_random_conv5way_step3000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.913146 | 0.148003 |
| v52_random_conv5way_step3000 | roundtrip_eng_pivot | all | 300 | 0.907680 | -0.035304 |
| v52_random_conv5way_step3000 | roundtrip_eng_pivot | v5_target | 300 | 0.907680 | -0.035304 |
| v52_random_conv5way_step3000 | roundtrip_src_eng | all | 300 | 0.906057 | -0.033890 |
| v52_random_conv5way_step3000 | roundtrip_src_eng | v5_target | 300 | 0.906057 | -0.033890 |
| v52_random_conv5way_step3000 | roundtrip_src_pivot | all | 300 | 0.942243 | 0.413929 |
| v52_random_conv5way_step3000 | roundtrip_src_pivot | v5_target | 300 | 0.942243 | 0.413929 |
| v52_random_conv5way_step3000 | same_language_bible_adjacent | all | 300 | 0.975767 | 0.738977 |
| v52_random_conv5way_step3000 | same_language_bible_adjacent | v5_target | 300 | 0.975767 | 0.738977 |
| v52_random_conv5way_step3000 | same_language_tatoeba_adjacent | all | 300 | 0.939558 | 0.348846 |
| v52_random_conv5way_step3000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.939558 | 0.348846 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
