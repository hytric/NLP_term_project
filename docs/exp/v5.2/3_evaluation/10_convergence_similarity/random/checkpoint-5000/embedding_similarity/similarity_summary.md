# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step5000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step5000 | aligned_bible_src_eng | all | 300 | 0.913452 | 0.011271 |
| v52_random_conv5way_step5000 | aligned_bible_src_eng | v5_target | 300 | 0.913452 | 0.011271 |
| v52_random_conv5way_step5000 | aligned_tatoeba_src_eng | all | 300 | 0.915191 | 0.160785 |
| v52_random_conv5way_step5000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.915191 | 0.160785 |
| v52_random_conv5way_step5000 | roundtrip_eng_pivot | all | 300 | 0.911081 | -0.015182 |
| v52_random_conv5way_step5000 | roundtrip_eng_pivot | v5_target | 300 | 0.911081 | -0.015182 |
| v52_random_conv5way_step5000 | roundtrip_src_eng | all | 300 | 0.909786 | -0.013897 |
| v52_random_conv5way_step5000 | roundtrip_src_eng | v5_target | 300 | 0.909786 | -0.013897 |
| v52_random_conv5way_step5000 | roundtrip_src_pivot | all | 300 | 0.940034 | 0.379547 |
| v52_random_conv5way_step5000 | roundtrip_src_pivot | v5_target | 300 | 0.940034 | 0.379547 |
| v52_random_conv5way_step5000 | same_language_bible_adjacent | all | 300 | 0.976455 | 0.740223 |
| v52_random_conv5way_step5000 | same_language_bible_adjacent | v5_target | 300 | 0.976455 | 0.740223 |
| v52_random_conv5way_step5000 | same_language_tatoeba_adjacent | all | 300 | 0.941189 | 0.357007 |
| v52_random_conv5way_step5000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.941189 | 0.357007 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
