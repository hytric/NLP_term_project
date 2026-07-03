# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step12000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step12000 | aligned_bible_src_eng | all | 300 | 0.914750 | 0.025549 |
| v52_random_conv5way_step12000 | aligned_bible_src_eng | v5_target | 300 | 0.914750 | 0.025549 |
| v52_random_conv5way_step12000 | aligned_tatoeba_src_eng | all | 300 | 0.917094 | 0.185359 |
| v52_random_conv5way_step12000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.917094 | 0.185359 |
| v52_random_conv5way_step12000 | roundtrip_eng_pivot | all | 300 | 0.912717 | 0.003816 |
| v52_random_conv5way_step12000 | roundtrip_eng_pivot | v5_target | 300 | 0.912717 | 0.003816 |
| v52_random_conv5way_step12000 | roundtrip_src_eng | all | 300 | 0.911501 | 0.004548 |
| v52_random_conv5way_step12000 | roundtrip_src_eng | v5_target | 300 | 0.911501 | 0.004548 |
| v52_random_conv5way_step12000 | roundtrip_src_pivot | all | 300 | 0.936678 | 0.351892 |
| v52_random_conv5way_step12000 | roundtrip_src_pivot | v5_target | 300 | 0.936678 | 0.351892 |
| v52_random_conv5way_step12000 | same_language_bible_adjacent | all | 300 | 0.976884 | 0.747150 |
| v52_random_conv5way_step12000 | same_language_bible_adjacent | v5_target | 300 | 0.976884 | 0.747150 |
| v52_random_conv5way_step12000 | same_language_tatoeba_adjacent | all | 300 | 0.939374 | 0.348858 |
| v52_random_conv5way_step12000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.939374 | 0.348858 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
