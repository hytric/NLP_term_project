# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step37000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step37000 | aligned_bible_src_eng | all | 300 | 0.922415 | 0.055587 |
| v52_mean_conv5way_step37000 | aligned_bible_src_eng | v5_target | 300 | 0.922415 | 0.055587 |
| v52_mean_conv5way_step37000 | aligned_tatoeba_src_eng | all | 300 | 0.925541 | 0.196578 |
| v52_mean_conv5way_step37000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925541 | 0.196578 |
| v52_mean_conv5way_step37000 | roundtrip_eng_pivot | all | 300 | 0.919457 | 0.029559 |
| v52_mean_conv5way_step37000 | roundtrip_eng_pivot | v5_target | 300 | 0.919457 | 0.029559 |
| v52_mean_conv5way_step37000 | roundtrip_src_eng | all | 300 | 0.920042 | 0.035361 |
| v52_mean_conv5way_step37000 | roundtrip_src_eng | v5_target | 300 | 0.920042 | 0.035361 |
| v52_mean_conv5way_step37000 | roundtrip_src_pivot | all | 300 | 0.937848 | 0.315822 |
| v52_mean_conv5way_step37000 | roundtrip_src_pivot | v5_target | 300 | 0.937848 | 0.315822 |
| v52_mean_conv5way_step37000 | same_language_bible_adjacent | all | 300 | 0.979016 | 0.748599 |
| v52_mean_conv5way_step37000 | same_language_bible_adjacent | v5_target | 300 | 0.979016 | 0.748599 |
| v52_mean_conv5way_step37000 | same_language_tatoeba_adjacent | all | 300 | 0.945765 | 0.380351 |
| v52_mean_conv5way_step37000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945765 | 0.380351 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
