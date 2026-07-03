# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step4000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step4000 | aligned_bible_src_eng | all | 300 | 0.914422 | 0.019084 |
| v52_random_conv5way_step4000 | aligned_bible_src_eng | v5_target | 300 | 0.914422 | 0.019084 |
| v52_random_conv5way_step4000 | aligned_tatoeba_src_eng | all | 300 | 0.912770 | 0.148302 |
| v52_random_conv5way_step4000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.912770 | 0.148302 |
| v52_random_conv5way_step4000 | roundtrip_eng_pivot | all | 300 | 0.911650 | -0.004976 |
| v52_random_conv5way_step4000 | roundtrip_eng_pivot | v5_target | 300 | 0.911650 | -0.004976 |
| v52_random_conv5way_step4000 | roundtrip_src_eng | all | 300 | 0.911214 | -0.002460 |
| v52_random_conv5way_step4000 | roundtrip_src_eng | v5_target | 300 | 0.911214 | -0.002460 |
| v52_random_conv5way_step4000 | roundtrip_src_pivot | all | 300 | 0.940984 | 0.372734 |
| v52_random_conv5way_step4000 | roundtrip_src_pivot | v5_target | 300 | 0.940984 | 0.372734 |
| v52_random_conv5way_step4000 | same_language_bible_adjacent | all | 300 | 0.976520 | 0.732979 |
| v52_random_conv5way_step4000 | same_language_bible_adjacent | v5_target | 300 | 0.976520 | 0.732979 |
| v52_random_conv5way_step4000 | same_language_tatoeba_adjacent | all | 300 | 0.939074 | 0.350062 |
| v52_random_conv5way_step4000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.939074 | 0.350062 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
