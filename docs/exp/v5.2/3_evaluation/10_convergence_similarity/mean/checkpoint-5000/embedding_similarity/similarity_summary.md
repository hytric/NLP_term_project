# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step5000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step5000 | aligned_bible_src_eng | all | 300 | 0.916824 | 0.025826 |
| v52_mean_conv5way_step5000 | aligned_bible_src_eng | v5_target | 300 | 0.916824 | 0.025826 |
| v52_mean_conv5way_step5000 | aligned_tatoeba_src_eng | all | 300 | 0.916427 | 0.162259 |
| v52_mean_conv5way_step5000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.916427 | 0.162259 |
| v52_mean_conv5way_step5000 | roundtrip_eng_pivot | all | 300 | 0.914805 | 0.009285 |
| v52_mean_conv5way_step5000 | roundtrip_eng_pivot | v5_target | 300 | 0.914805 | 0.009285 |
| v52_mean_conv5way_step5000 | roundtrip_src_eng | all | 300 | 0.913995 | 0.005063 |
| v52_mean_conv5way_step5000 | roundtrip_src_eng | v5_target | 300 | 0.913995 | 0.005063 |
| v52_mean_conv5way_step5000 | roundtrip_src_pivot | all | 300 | 0.941654 | 0.354343 |
| v52_mean_conv5way_step5000 | roundtrip_src_pivot | v5_target | 300 | 0.941654 | 0.354343 |
| v52_mean_conv5way_step5000 | same_language_bible_adjacent | all | 300 | 0.978761 | 0.747927 |
| v52_mean_conv5way_step5000 | same_language_bible_adjacent | v5_target | 300 | 0.978761 | 0.747927 |
| v52_mean_conv5way_step5000 | same_language_tatoeba_adjacent | all | 300 | 0.941264 | 0.363703 |
| v52_mean_conv5way_step5000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.941264 | 0.363703 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
