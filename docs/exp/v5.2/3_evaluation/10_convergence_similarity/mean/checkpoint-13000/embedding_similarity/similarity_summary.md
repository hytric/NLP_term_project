# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step13000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step13000 | aligned_bible_src_eng | all | 300 | 0.919877 | 0.050893 |
| v52_mean_conv5way_step13000 | aligned_bible_src_eng | v5_target | 300 | 0.919877 | 0.050893 |
| v52_mean_conv5way_step13000 | aligned_tatoeba_src_eng | all | 300 | 0.921083 | 0.190663 |
| v52_mean_conv5way_step13000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.921083 | 0.190663 |
| v52_mean_conv5way_step13000 | roundtrip_eng_pivot | all | 300 | 0.917062 | 0.026734 |
| v52_mean_conv5way_step13000 | roundtrip_eng_pivot | v5_target | 300 | 0.917062 | 0.026734 |
| v52_mean_conv5way_step13000 | roundtrip_src_eng | all | 300 | 0.917431 | 0.030196 |
| v52_mean_conv5way_step13000 | roundtrip_src_eng | v5_target | 300 | 0.917431 | 0.030196 |
| v52_mean_conv5way_step13000 | roundtrip_src_pivot | all | 300 | 0.938273 | 0.332944 |
| v52_mean_conv5way_step13000 | roundtrip_src_pivot | v5_target | 300 | 0.938273 | 0.332944 |
| v52_mean_conv5way_step13000 | same_language_bible_adjacent | all | 300 | 0.978127 | 0.743303 |
| v52_mean_conv5way_step13000 | same_language_bible_adjacent | v5_target | 300 | 0.978127 | 0.743303 |
| v52_mean_conv5way_step13000 | same_language_tatoeba_adjacent | all | 300 | 0.942438 | 0.371617 |
| v52_mean_conv5way_step13000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.942438 | 0.371617 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
