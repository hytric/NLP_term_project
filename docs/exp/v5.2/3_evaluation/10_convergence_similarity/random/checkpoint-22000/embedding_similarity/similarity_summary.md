# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step22000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step22000 | aligned_bible_src_eng | all | 300 | 0.920903 | 0.041443 |
| v52_random_conv5way_step22000 | aligned_bible_src_eng | v5_target | 300 | 0.920903 | 0.041443 |
| v52_random_conv5way_step22000 | aligned_tatoeba_src_eng | all | 300 | 0.921730 | 0.185066 |
| v52_random_conv5way_step22000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.921730 | 0.185066 |
| v52_random_conv5way_step22000 | roundtrip_eng_pivot | all | 300 | 0.918676 | 0.017990 |
| v52_random_conv5way_step22000 | roundtrip_eng_pivot | v5_target | 300 | 0.918676 | 0.017990 |
| v52_random_conv5way_step22000 | roundtrip_src_eng | all | 300 | 0.917690 | 0.019397 |
| v52_random_conv5way_step22000 | roundtrip_src_eng | v5_target | 300 | 0.917690 | 0.019397 |
| v52_random_conv5way_step22000 | roundtrip_src_pivot | all | 300 | 0.938448 | 0.340166 |
| v52_random_conv5way_step22000 | roundtrip_src_pivot | v5_target | 300 | 0.938448 | 0.340166 |
| v52_random_conv5way_step22000 | same_language_bible_adjacent | all | 300 | 0.977798 | 0.744319 |
| v52_random_conv5way_step22000 | same_language_bible_adjacent | v5_target | 300 | 0.977798 | 0.744319 |
| v52_random_conv5way_step22000 | same_language_tatoeba_adjacent | all | 300 | 0.942703 | 0.353602 |
| v52_random_conv5way_step22000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.942703 | 0.353602 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
