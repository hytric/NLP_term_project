# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step12000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step12000 | aligned_bible_src_eng | all | 300 | 0.917955 | 0.043775 |
| v52_mean_conv5way_step12000 | aligned_bible_src_eng | v5_target | 300 | 0.917955 | 0.043775 |
| v52_mean_conv5way_step12000 | aligned_tatoeba_src_eng | all | 300 | 0.920700 | 0.190743 |
| v52_mean_conv5way_step12000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.920700 | 0.190743 |
| v52_mean_conv5way_step12000 | roundtrip_eng_pivot | all | 300 | 0.915710 | 0.024281 |
| v52_mean_conv5way_step12000 | roundtrip_eng_pivot | v5_target | 300 | 0.915710 | 0.024281 |
| v52_mean_conv5way_step12000 | roundtrip_src_eng | all | 300 | 0.915483 | 0.024491 |
| v52_mean_conv5way_step12000 | roundtrip_src_eng | v5_target | 300 | 0.915483 | 0.024491 |
| v52_mean_conv5way_step12000 | roundtrip_src_pivot | all | 300 | 0.936336 | 0.320064 |
| v52_mean_conv5way_step12000 | roundtrip_src_pivot | v5_target | 300 | 0.936336 | 0.320064 |
| v52_mean_conv5way_step12000 | same_language_bible_adjacent | all | 300 | 0.978273 | 0.749227 |
| v52_mean_conv5way_step12000 | same_language_bible_adjacent | v5_target | 300 | 0.978273 | 0.749227 |
| v52_mean_conv5way_step12000 | same_language_tatoeba_adjacent | all | 300 | 0.942591 | 0.373980 |
| v52_mean_conv5way_step12000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.942591 | 0.373980 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
