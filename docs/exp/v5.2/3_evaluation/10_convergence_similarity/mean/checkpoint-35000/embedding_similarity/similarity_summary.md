# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step35000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step35000 | aligned_bible_src_eng | all | 300 | 0.922337 | 0.054002 |
| v52_mean_conv5way_step35000 | aligned_bible_src_eng | v5_target | 300 | 0.922337 | 0.054002 |
| v52_mean_conv5way_step35000 | aligned_tatoeba_src_eng | all | 300 | 0.925303 | 0.195370 |
| v52_mean_conv5way_step35000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925303 | 0.195370 |
| v52_mean_conv5way_step35000 | roundtrip_eng_pivot | all | 300 | 0.919359 | 0.027818 |
| v52_mean_conv5way_step35000 | roundtrip_eng_pivot | v5_target | 300 | 0.919359 | 0.027818 |
| v52_mean_conv5way_step35000 | roundtrip_src_eng | all | 300 | 0.919954 | 0.033785 |
| v52_mean_conv5way_step35000 | roundtrip_src_eng | v5_target | 300 | 0.919954 | 0.033785 |
| v52_mean_conv5way_step35000 | roundtrip_src_pivot | all | 300 | 0.937850 | 0.315630 |
| v52_mean_conv5way_step35000 | roundtrip_src_pivot | v5_target | 300 | 0.937850 | 0.315630 |
| v52_mean_conv5way_step35000 | same_language_bible_adjacent | all | 300 | 0.979002 | 0.748426 |
| v52_mean_conv5way_step35000 | same_language_bible_adjacent | v5_target | 300 | 0.979002 | 0.748426 |
| v52_mean_conv5way_step35000 | same_language_tatoeba_adjacent | all | 300 | 0.945612 | 0.380302 |
| v52_mean_conv5way_step35000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945612 | 0.380302 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
