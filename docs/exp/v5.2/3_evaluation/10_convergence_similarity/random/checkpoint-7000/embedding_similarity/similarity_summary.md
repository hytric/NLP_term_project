# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step7000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step7000 | aligned_bible_src_eng | all | 300 | 0.913963 | 0.031016 |
| v52_random_conv5way_step7000 | aligned_bible_src_eng | v5_target | 300 | 0.913963 | 0.031016 |
| v52_random_conv5way_step7000 | aligned_tatoeba_src_eng | all | 300 | 0.914309 | 0.164060 |
| v52_random_conv5way_step7000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.914309 | 0.164060 |
| v52_random_conv5way_step7000 | roundtrip_eng_pivot | all | 300 | 0.911152 | 0.004903 |
| v52_random_conv5way_step7000 | roundtrip_eng_pivot | v5_target | 300 | 0.911152 | 0.004903 |
| v52_random_conv5way_step7000 | roundtrip_src_eng | all | 300 | 0.910334 | 0.007595 |
| v52_random_conv5way_step7000 | roundtrip_src_eng | v5_target | 300 | 0.910334 | 0.007595 |
| v52_random_conv5way_step7000 | roundtrip_src_pivot | all | 300 | 0.935830 | 0.355221 |
| v52_random_conv5way_step7000 | roundtrip_src_pivot | v5_target | 300 | 0.935830 | 0.355221 |
| v52_random_conv5way_step7000 | same_language_bible_adjacent | all | 300 | 0.976712 | 0.746995 |
| v52_random_conv5way_step7000 | same_language_bible_adjacent | v5_target | 300 | 0.976712 | 0.746995 |
| v52_random_conv5way_step7000 | same_language_tatoeba_adjacent | all | 300 | 0.940814 | 0.360347 |
| v52_random_conv5way_step7000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.940814 | 0.360347 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
