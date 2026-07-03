# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step18000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step18000 | aligned_bible_src_eng | all | 300 | 0.920323 | 0.052934 |
| v52_mean_conv5way_step18000 | aligned_bible_src_eng | v5_target | 300 | 0.920323 | 0.052934 |
| v52_mean_conv5way_step18000 | aligned_tatoeba_src_eng | all | 300 | 0.923593 | 0.195608 |
| v52_mean_conv5way_step18000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.923593 | 0.195608 |
| v52_mean_conv5way_step18000 | roundtrip_eng_pivot | all | 300 | 0.917719 | 0.026758 |
| v52_mean_conv5way_step18000 | roundtrip_eng_pivot | v5_target | 300 | 0.917719 | 0.026758 |
| v52_mean_conv5way_step18000 | roundtrip_src_eng | all | 300 | 0.917893 | 0.032799 |
| v52_mean_conv5way_step18000 | roundtrip_src_eng | v5_target | 300 | 0.917893 | 0.032799 |
| v52_mean_conv5way_step18000 | roundtrip_src_pivot | all | 300 | 0.936949 | 0.314887 |
| v52_mean_conv5way_step18000 | roundtrip_src_pivot | v5_target | 300 | 0.936949 | 0.314887 |
| v52_mean_conv5way_step18000 | same_language_bible_adjacent | all | 300 | 0.978715 | 0.750063 |
| v52_mean_conv5way_step18000 | same_language_bible_adjacent | v5_target | 300 | 0.978715 | 0.750063 |
| v52_mean_conv5way_step18000 | same_language_tatoeba_adjacent | all | 300 | 0.944059 | 0.376631 |
| v52_mean_conv5way_step18000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944059 | 0.376631 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
