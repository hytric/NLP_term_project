# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step17000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step17000 | aligned_bible_src_eng | all | 300 | 0.920075 | 0.049447 |
| v52_random_conv5way_step17000 | aligned_bible_src_eng | v5_target | 300 | 0.920075 | 0.049447 |
| v52_random_conv5way_step17000 | aligned_tatoeba_src_eng | all | 300 | 0.919665 | 0.186244 |
| v52_random_conv5way_step17000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.919665 | 0.186244 |
| v52_random_conv5way_step17000 | roundtrip_eng_pivot | all | 300 | 0.918068 | 0.028899 |
| v52_random_conv5way_step17000 | roundtrip_eng_pivot | v5_target | 300 | 0.918068 | 0.028899 |
| v52_random_conv5way_step17000 | roundtrip_src_eng | all | 300 | 0.916775 | 0.028372 |
| v52_random_conv5way_step17000 | roundtrip_src_eng | v5_target | 300 | 0.916775 | 0.028372 |
| v52_random_conv5way_step17000 | roundtrip_src_pivot | all | 300 | 0.937422 | 0.345381 |
| v52_random_conv5way_step17000 | roundtrip_src_pivot | v5_target | 300 | 0.937422 | 0.345381 |
| v52_random_conv5way_step17000 | same_language_bible_adjacent | all | 300 | 0.977362 | 0.744967 |
| v52_random_conv5way_step17000 | same_language_bible_adjacent | v5_target | 300 | 0.977362 | 0.744967 |
| v52_random_conv5way_step17000 | same_language_tatoeba_adjacent | all | 300 | 0.940602 | 0.349240 |
| v52_random_conv5way_step17000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.940602 | 0.349240 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
