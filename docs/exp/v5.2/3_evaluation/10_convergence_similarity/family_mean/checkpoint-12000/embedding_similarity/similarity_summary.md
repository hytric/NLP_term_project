# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step12000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step12000 | aligned_bible_src_eng | all | 300 | 0.903451 | -0.027739 |
| v52_family_mean_conv5way_step12000 | aligned_bible_src_eng | v5_target | 300 | 0.903451 | -0.027739 |
| v52_family_mean_conv5way_step12000 | aligned_tatoeba_src_eng | all | 300 | 0.915428 | 0.170885 |
| v52_family_mean_conv5way_step12000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.915428 | 0.170885 |
| v52_family_mean_conv5way_step12000 | roundtrip_eng_pivot | all | 300 | 0.905618 | -0.038354 |
| v52_family_mean_conv5way_step12000 | roundtrip_eng_pivot | v5_target | 300 | 0.905618 | -0.038354 |
| v52_family_mean_conv5way_step12000 | roundtrip_src_eng | all | 300 | 0.900232 | -0.047440 |
| v52_family_mean_conv5way_step12000 | roundtrip_src_eng | v5_target | 300 | 0.900232 | -0.047440 |
| v52_family_mean_conv5way_step12000 | roundtrip_src_pivot | all | 300 | 0.936581 | 0.362648 |
| v52_family_mean_conv5way_step12000 | roundtrip_src_pivot | v5_target | 300 | 0.936581 | 0.362648 |
| v52_family_mean_conv5way_step12000 | same_language_bible_adjacent | all | 300 | 0.977517 | 0.766783 |
| v52_family_mean_conv5way_step12000 | same_language_bible_adjacent | v5_target | 300 | 0.977517 | 0.766783 |
| v52_family_mean_conv5way_step12000 | same_language_tatoeba_adjacent | all | 300 | 0.945466 | 0.414438 |
| v52_family_mean_conv5way_step12000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945466 | 0.414438 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
