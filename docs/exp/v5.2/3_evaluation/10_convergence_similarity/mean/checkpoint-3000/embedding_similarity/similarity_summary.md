# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step3000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step3000 | aligned_bible_src_eng | all | 300 | 0.914516 | 0.015529 |
| v52_mean_conv5way_step3000 | aligned_bible_src_eng | v5_target | 300 | 0.914516 | 0.015529 |
| v52_mean_conv5way_step3000 | aligned_tatoeba_src_eng | all | 300 | 0.915961 | 0.157767 |
| v52_mean_conv5way_step3000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.915961 | 0.157767 |
| v52_mean_conv5way_step3000 | roundtrip_eng_pivot | all | 300 | 0.913056 | -0.001848 |
| v52_mean_conv5way_step3000 | roundtrip_eng_pivot | v5_target | 300 | 0.913056 | -0.001848 |
| v52_mean_conv5way_step3000 | roundtrip_src_eng | all | 300 | 0.911655 | -0.004065 |
| v52_mean_conv5way_step3000 | roundtrip_src_eng | v5_target | 300 | 0.911655 | -0.004065 |
| v52_mean_conv5way_step3000 | roundtrip_src_pivot | all | 300 | 0.941904 | 0.373524 |
| v52_mean_conv5way_step3000 | roundtrip_src_pivot | v5_target | 300 | 0.941904 | 0.373524 |
| v52_mean_conv5way_step3000 | same_language_bible_adjacent | all | 300 | 0.978066 | 0.745815 |
| v52_mean_conv5way_step3000 | same_language_bible_adjacent | v5_target | 300 | 0.978066 | 0.745815 |
| v52_mean_conv5way_step3000 | same_language_tatoeba_adjacent | all | 300 | 0.940362 | 0.356510 |
| v52_mean_conv5way_step3000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.940362 | 0.356510 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
