# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step9000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step9000 | aligned_bible_src_eng | all | 300 | 0.917221 | 0.049325 |
| v52_random_conv5way_step9000 | aligned_bible_src_eng | v5_target | 300 | 0.917221 | 0.049325 |
| v52_random_conv5way_step9000 | aligned_tatoeba_src_eng | all | 300 | 0.916398 | 0.174703 |
| v52_random_conv5way_step9000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.916398 | 0.174703 |
| v52_random_conv5way_step9000 | roundtrip_eng_pivot | all | 300 | 0.915356 | 0.033111 |
| v52_random_conv5way_step9000 | roundtrip_eng_pivot | v5_target | 300 | 0.915356 | 0.033111 |
| v52_random_conv5way_step9000 | roundtrip_src_eng | all | 300 | 0.913872 | 0.028451 |
| v52_random_conv5way_step9000 | roundtrip_src_eng | v5_target | 300 | 0.913872 | 0.028451 |
| v52_random_conv5way_step9000 | roundtrip_src_pivot | all | 300 | 0.937428 | 0.349884 |
| v52_random_conv5way_step9000 | roundtrip_src_pivot | v5_target | 300 | 0.937428 | 0.349884 |
| v52_random_conv5way_step9000 | same_language_bible_adjacent | all | 300 | 0.977056 | 0.743443 |
| v52_random_conv5way_step9000 | same_language_bible_adjacent | v5_target | 300 | 0.977056 | 0.743443 |
| v52_random_conv5way_step9000 | same_language_tatoeba_adjacent | all | 300 | 0.940628 | 0.357893 |
| v52_random_conv5way_step9000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.940628 | 0.357893 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
