# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step27000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step27000 | aligned_bible_src_eng | all | 300 | 0.921016 | 0.042944 |
| v52_random_conv5way_step27000 | aligned_bible_src_eng | v5_target | 300 | 0.921016 | 0.042944 |
| v52_random_conv5way_step27000 | aligned_tatoeba_src_eng | all | 300 | 0.922442 | 0.186404 |
| v52_random_conv5way_step27000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922442 | 0.186404 |
| v52_random_conv5way_step27000 | roundtrip_eng_pivot | all | 300 | 0.918720 | 0.019385 |
| v52_random_conv5way_step27000 | roundtrip_eng_pivot | v5_target | 300 | 0.918720 | 0.019385 |
| v52_random_conv5way_step27000 | roundtrip_src_eng | all | 300 | 0.917783 | 0.020803 |
| v52_random_conv5way_step27000 | roundtrip_src_eng | v5_target | 300 | 0.917783 | 0.020803 |
| v52_random_conv5way_step27000 | roundtrip_src_pivot | all | 300 | 0.938309 | 0.340771 |
| v52_random_conv5way_step27000 | roundtrip_src_pivot | v5_target | 300 | 0.938309 | 0.340771 |
| v52_random_conv5way_step27000 | same_language_bible_adjacent | all | 300 | 0.977783 | 0.744332 |
| v52_random_conv5way_step27000 | same_language_bible_adjacent | v5_target | 300 | 0.977783 | 0.744332 |
| v52_random_conv5way_step27000 | same_language_tatoeba_adjacent | all | 300 | 0.943331 | 0.355495 |
| v52_random_conv5way_step27000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943331 | 0.355495 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
