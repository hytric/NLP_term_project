# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step41000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step41000 | aligned_bible_src_eng | all | 300 | 0.921811 | 0.043963 |
| v52_random_conv5way_step41000 | aligned_bible_src_eng | v5_target | 300 | 0.921811 | 0.043963 |
| v52_random_conv5way_step41000 | aligned_tatoeba_src_eng | all | 300 | 0.923099 | 0.186901 |
| v52_random_conv5way_step41000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.923099 | 0.186901 |
| v52_random_conv5way_step41000 | roundtrip_eng_pivot | all | 300 | 0.919448 | 0.020004 |
| v52_random_conv5way_step41000 | roundtrip_eng_pivot | v5_target | 300 | 0.919448 | 0.020004 |
| v52_random_conv5way_step41000 | roundtrip_src_eng | all | 300 | 0.918624 | 0.021958 |
| v52_random_conv5way_step41000 | roundtrip_src_eng | v5_target | 300 | 0.918624 | 0.021958 |
| v52_random_conv5way_step41000 | roundtrip_src_pivot | all | 300 | 0.938965 | 0.341359 |
| v52_random_conv5way_step41000 | roundtrip_src_pivot | v5_target | 300 | 0.938965 | 0.341359 |
| v52_random_conv5way_step41000 | same_language_bible_adjacent | all | 300 | 0.977956 | 0.744024 |
| v52_random_conv5way_step41000 | same_language_bible_adjacent | v5_target | 300 | 0.977956 | 0.744024 |
| v52_random_conv5way_step41000 | same_language_tatoeba_adjacent | all | 300 | 0.943727 | 0.355734 |
| v52_random_conv5way_step41000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943727 | 0.355734 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
