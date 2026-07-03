# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step7000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step7000 | aligned_bible_src_eng | all | 300 | 0.914846 | 0.018459 |
| v52_mean_conv5way_step7000 | aligned_bible_src_eng | v5_target | 300 | 0.914846 | 0.018459 |
| v52_mean_conv5way_step7000 | aligned_tatoeba_src_eng | all | 300 | 0.916643 | 0.173014 |
| v52_mean_conv5way_step7000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.916643 | 0.173014 |
| v52_mean_conv5way_step7000 | roundtrip_eng_pivot | all | 300 | 0.912161 | -0.003500 |
| v52_mean_conv5way_step7000 | roundtrip_eng_pivot | v5_target | 300 | 0.912161 | -0.003500 |
| v52_mean_conv5way_step7000 | roundtrip_src_eng | all | 300 | 0.912125 | 0.000206 |
| v52_mean_conv5way_step7000 | roundtrip_src_eng | v5_target | 300 | 0.912125 | 0.000206 |
| v52_mean_conv5way_step7000 | roundtrip_src_pivot | all | 300 | 0.934881 | 0.319181 |
| v52_mean_conv5way_step7000 | roundtrip_src_pivot | v5_target | 300 | 0.934881 | 0.319181 |
| v52_mean_conv5way_step7000 | same_language_bible_adjacent | all | 300 | 0.978414 | 0.756265 |
| v52_mean_conv5way_step7000 | same_language_bible_adjacent | v5_target | 300 | 0.978414 | 0.756265 |
| v52_mean_conv5way_step7000 | same_language_tatoeba_adjacent | all | 300 | 0.940609 | 0.369923 |
| v52_mean_conv5way_step7000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.940609 | 0.369923 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
