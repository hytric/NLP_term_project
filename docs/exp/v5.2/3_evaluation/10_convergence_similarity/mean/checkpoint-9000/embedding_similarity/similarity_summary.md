# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step9000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step9000 | aligned_bible_src_eng | all | 300 | 0.915683 | 0.040224 |
| v52_mean_conv5way_step9000 | aligned_bible_src_eng | v5_target | 300 | 0.915683 | 0.040224 |
| v52_mean_conv5way_step9000 | aligned_tatoeba_src_eng | all | 300 | 0.917879 | 0.174940 |
| v52_mean_conv5way_step9000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.917879 | 0.174940 |
| v52_mean_conv5way_step9000 | roundtrip_eng_pivot | all | 300 | 0.914030 | 0.029313 |
| v52_mean_conv5way_step9000 | roundtrip_eng_pivot | v5_target | 300 | 0.914030 | 0.029313 |
| v52_mean_conv5way_step9000 | roundtrip_src_eng | all | 300 | 0.913013 | 0.023098 |
| v52_mean_conv5way_step9000 | roundtrip_src_eng | v5_target | 300 | 0.913013 | 0.023098 |
| v52_mean_conv5way_step9000 | roundtrip_src_pivot | all | 300 | 0.934842 | 0.318283 |
| v52_mean_conv5way_step9000 | roundtrip_src_pivot | v5_target | 300 | 0.934842 | 0.318283 |
| v52_mean_conv5way_step9000 | same_language_bible_adjacent | all | 300 | 0.977964 | 0.749523 |
| v52_mean_conv5way_step9000 | same_language_bible_adjacent | v5_target | 300 | 0.977964 | 0.749523 |
| v52_mean_conv5way_step9000 | same_language_tatoeba_adjacent | all | 300 | 0.941641 | 0.374713 |
| v52_mean_conv5way_step9000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.941641 | 0.374713 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
