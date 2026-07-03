# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step35000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step35000 | aligned_bible_src_eng | all | 300 | 0.921440 | 0.043692 |
| v52_random_conv5way_step35000 | aligned_bible_src_eng | v5_target | 300 | 0.921440 | 0.043692 |
| v52_random_conv5way_step35000 | aligned_tatoeba_src_eng | all | 300 | 0.922652 | 0.186977 |
| v52_random_conv5way_step35000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922652 | 0.186977 |
| v52_random_conv5way_step35000 | roundtrip_eng_pivot | all | 300 | 0.919069 | 0.019631 |
| v52_random_conv5way_step35000 | roundtrip_eng_pivot | v5_target | 300 | 0.919069 | 0.019631 |
| v52_random_conv5way_step35000 | roundtrip_src_eng | all | 300 | 0.918236 | 0.021606 |
| v52_random_conv5way_step35000 | roundtrip_src_eng | v5_target | 300 | 0.918236 | 0.021606 |
| v52_random_conv5way_step35000 | roundtrip_src_pivot | all | 300 | 0.938942 | 0.342018 |
| v52_random_conv5way_step35000 | roundtrip_src_pivot | v5_target | 300 | 0.938942 | 0.342018 |
| v52_random_conv5way_step35000 | same_language_bible_adjacent | all | 300 | 0.977952 | 0.744461 |
| v52_random_conv5way_step35000 | same_language_bible_adjacent | v5_target | 300 | 0.977952 | 0.744461 |
| v52_random_conv5way_step35000 | same_language_tatoeba_adjacent | all | 300 | 0.943386 | 0.355535 |
| v52_random_conv5way_step35000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943386 | 0.355535 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
