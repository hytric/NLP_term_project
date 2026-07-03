# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step10000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step10000 | aligned_bible_src_eng | all | 300 | 0.917014 | 0.031047 |
| v52_random_conv5way_step10000 | aligned_bible_src_eng | v5_target | 300 | 0.917014 | 0.031047 |
| v52_random_conv5way_step10000 | aligned_tatoeba_src_eng | all | 300 | 0.918725 | 0.181497 |
| v52_random_conv5way_step10000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.918725 | 0.181497 |
| v52_random_conv5way_step10000 | roundtrip_eng_pivot | all | 300 | 0.914913 | 0.006904 |
| v52_random_conv5way_step10000 | roundtrip_eng_pivot | v5_target | 300 | 0.914913 | 0.006904 |
| v52_random_conv5way_step10000 | roundtrip_src_eng | all | 300 | 0.913651 | 0.009607 |
| v52_random_conv5way_step10000 | roundtrip_src_eng | v5_target | 300 | 0.913651 | 0.009607 |
| v52_random_conv5way_step10000 | roundtrip_src_pivot | all | 300 | 0.937678 | 0.350811 |
| v52_random_conv5way_step10000 | roundtrip_src_pivot | v5_target | 300 | 0.937678 | 0.350811 |
| v52_random_conv5way_step10000 | same_language_bible_adjacent | all | 300 | 0.976992 | 0.743693 |
| v52_random_conv5way_step10000 | same_language_bible_adjacent | v5_target | 300 | 0.976992 | 0.743693 |
| v52_random_conv5way_step10000 | same_language_tatoeba_adjacent | all | 300 | 0.941165 | 0.350815 |
| v52_random_conv5way_step10000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.941165 | 0.350815 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
