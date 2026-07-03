# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step27000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step27000 | aligned_bible_src_eng | all | 300 | 0.922363 | 0.054748 |
| v52_mean_conv5way_step27000 | aligned_bible_src_eng | v5_target | 300 | 0.922363 | 0.054748 |
| v52_mean_conv5way_step27000 | aligned_tatoeba_src_eng | all | 300 | 0.925349 | 0.195030 |
| v52_mean_conv5way_step27000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925349 | 0.195030 |
| v52_mean_conv5way_step27000 | roundtrip_eng_pivot | all | 300 | 0.919475 | 0.029131 |
| v52_mean_conv5way_step27000 | roundtrip_eng_pivot | v5_target | 300 | 0.919475 | 0.029131 |
| v52_mean_conv5way_step27000 | roundtrip_src_eng | all | 300 | 0.919966 | 0.034321 |
| v52_mean_conv5way_step27000 | roundtrip_src_eng | v5_target | 300 | 0.919966 | 0.034321 |
| v52_mean_conv5way_step27000 | roundtrip_src_pivot | all | 300 | 0.937763 | 0.315139 |
| v52_mean_conv5way_step27000 | roundtrip_src_pivot | v5_target | 300 | 0.937763 | 0.315139 |
| v52_mean_conv5way_step27000 | same_language_bible_adjacent | all | 300 | 0.978975 | 0.748227 |
| v52_mean_conv5way_step27000 | same_language_bible_adjacent | v5_target | 300 | 0.978975 | 0.748227 |
| v52_mean_conv5way_step27000 | same_language_tatoeba_adjacent | all | 300 | 0.945816 | 0.380527 |
| v52_mean_conv5way_step27000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945816 | 0.380527 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
