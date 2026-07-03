# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step6000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step6000 | aligned_bible_src_eng | all | 300 | 0.914658 | 0.023971 |
| v52_random_conv5way_step6000 | aligned_bible_src_eng | v5_target | 300 | 0.914658 | 0.023971 |
| v52_random_conv5way_step6000 | aligned_tatoeba_src_eng | all | 300 | 0.914703 | 0.167471 |
| v52_random_conv5way_step6000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.914703 | 0.167471 |
| v52_random_conv5way_step6000 | roundtrip_eng_pivot | all | 300 | 0.911580 | -0.004413 |
| v52_random_conv5way_step6000 | roundtrip_eng_pivot | v5_target | 300 | 0.911580 | -0.004413 |
| v52_random_conv5way_step6000 | roundtrip_src_eng | all | 300 | 0.911256 | 0.002107 |
| v52_random_conv5way_step6000 | roundtrip_src_eng | v5_target | 300 | 0.911256 | 0.002107 |
| v52_random_conv5way_step6000 | roundtrip_src_pivot | all | 300 | 0.936456 | 0.352396 |
| v52_random_conv5way_step6000 | roundtrip_src_pivot | v5_target | 300 | 0.936456 | 0.352396 |
| v52_random_conv5way_step6000 | same_language_bible_adjacent | all | 300 | 0.976455 | 0.736618 |
| v52_random_conv5way_step6000 | same_language_bible_adjacent | v5_target | 300 | 0.976455 | 0.736618 |
| v52_random_conv5way_step6000 | same_language_tatoeba_adjacent | all | 300 | 0.938495 | 0.346580 |
| v52_random_conv5way_step6000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.938495 | 0.346580 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
