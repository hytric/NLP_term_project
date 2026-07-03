# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step26000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step26000 | aligned_bible_src_eng | all | 300 | 0.920514 | 0.042498 |
| v52_random_conv5way_step26000 | aligned_bible_src_eng | v5_target | 300 | 0.920514 | 0.042498 |
| v52_random_conv5way_step26000 | aligned_tatoeba_src_eng | all | 300 | 0.922056 | 0.186805 |
| v52_random_conv5way_step26000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922056 | 0.186805 |
| v52_random_conv5way_step26000 | roundtrip_eng_pivot | all | 300 | 0.918250 | 0.018636 |
| v52_random_conv5way_step26000 | roundtrip_eng_pivot | v5_target | 300 | 0.918250 | 0.018636 |
| v52_random_conv5way_step26000 | roundtrip_src_eng | all | 300 | 0.917278 | 0.020425 |
| v52_random_conv5way_step26000 | roundtrip_src_eng | v5_target | 300 | 0.917278 | 0.020425 |
| v52_random_conv5way_step26000 | roundtrip_src_pivot | all | 300 | 0.938143 | 0.340667 |
| v52_random_conv5way_step26000 | roundtrip_src_pivot | v5_target | 300 | 0.938143 | 0.340667 |
| v52_random_conv5way_step26000 | same_language_bible_adjacent | all | 300 | 0.977692 | 0.744487 |
| v52_random_conv5way_step26000 | same_language_bible_adjacent | v5_target | 300 | 0.977692 | 0.744487 |
| v52_random_conv5way_step26000 | same_language_tatoeba_adjacent | all | 300 | 0.942963 | 0.355293 |
| v52_random_conv5way_step26000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.942963 | 0.355293 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
