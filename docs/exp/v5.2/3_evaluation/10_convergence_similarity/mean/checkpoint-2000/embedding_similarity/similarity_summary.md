# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step2000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step2000 | aligned_bible_src_eng | all | 300 | 0.919127 | 0.025237 |
| v52_mean_conv5way_step2000 | aligned_bible_src_eng | v5_target | 300 | 0.919127 | 0.025237 |
| v52_mean_conv5way_step2000 | aligned_tatoeba_src_eng | all | 300 | 0.914413 | 0.138286 |
| v52_mean_conv5way_step2000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.914413 | 0.138286 |
| v52_mean_conv5way_step2000 | roundtrip_eng_pivot | all | 300 | 0.917320 | 0.013617 |
| v52_mean_conv5way_step2000 | roundtrip_eng_pivot | v5_target | 300 | 0.917320 | 0.013617 |
| v52_mean_conv5way_step2000 | roundtrip_src_eng | all | 300 | 0.916210 | 0.007015 |
| v52_mean_conv5way_step2000 | roundtrip_src_eng | v5_target | 300 | 0.916210 | 0.007015 |
| v52_mean_conv5way_step2000 | roundtrip_src_pivot | all | 300 | 0.943464 | 0.369381 |
| v52_mean_conv5way_step2000 | roundtrip_src_pivot | v5_target | 300 | 0.943464 | 0.369381 |
| v52_mean_conv5way_step2000 | same_language_bible_adjacent | all | 300 | 0.978183 | 0.736420 |
| v52_mean_conv5way_step2000 | same_language_bible_adjacent | v5_target | 300 | 0.978183 | 0.736420 |
| v52_mean_conv5way_step2000 | same_language_tatoeba_adjacent | all | 300 | 0.941472 | 0.353213 |
| v52_mean_conv5way_step2000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.941472 | 0.353213 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
