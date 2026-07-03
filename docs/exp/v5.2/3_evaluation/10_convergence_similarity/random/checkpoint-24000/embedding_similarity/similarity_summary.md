# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step24000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step24000 | aligned_bible_src_eng | all | 300 | 0.921052 | 0.043441 |
| v52_random_conv5way_step24000 | aligned_bible_src_eng | v5_target | 300 | 0.921052 | 0.043441 |
| v52_random_conv5way_step24000 | aligned_tatoeba_src_eng | all | 300 | 0.922250 | 0.186504 |
| v52_random_conv5way_step24000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922250 | 0.186504 |
| v52_random_conv5way_step24000 | roundtrip_eng_pivot | all | 300 | 0.918872 | 0.020280 |
| v52_random_conv5way_step24000 | roundtrip_eng_pivot | v5_target | 300 | 0.918872 | 0.020280 |
| v52_random_conv5way_step24000 | roundtrip_src_eng | all | 300 | 0.917838 | 0.021418 |
| v52_random_conv5way_step24000 | roundtrip_src_eng | v5_target | 300 | 0.917838 | 0.021418 |
| v52_random_conv5way_step24000 | roundtrip_src_pivot | all | 300 | 0.938507 | 0.341025 |
| v52_random_conv5way_step24000 | roundtrip_src_pivot | v5_target | 300 | 0.938507 | 0.341025 |
| v52_random_conv5way_step24000 | same_language_bible_adjacent | all | 300 | 0.977816 | 0.744452 |
| v52_random_conv5way_step24000 | same_language_bible_adjacent | v5_target | 300 | 0.977816 | 0.744452 |
| v52_random_conv5way_step24000 | same_language_tatoeba_adjacent | all | 300 | 0.943092 | 0.354535 |
| v52_random_conv5way_step24000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943092 | 0.354535 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
