# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step50000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step50000 | aligned_bible_src_eng | all | 300 | 0.917646 | 0.043604 |
| v52_family_mean_conv5way_step50000 | aligned_bible_src_eng | v5_target | 300 | 0.917646 | 0.043604 |
| v52_family_mean_conv5way_step50000 | aligned_tatoeba_src_eng | all | 300 | 0.926728 | 0.211494 |
| v52_family_mean_conv5way_step50000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926728 | 0.211494 |
| v52_family_mean_conv5way_step50000 | roundtrip_eng_pivot | all | 300 | 0.915054 | 0.006781 |
| v52_family_mean_conv5way_step50000 | roundtrip_eng_pivot | v5_target | 300 | 0.915054 | 0.006781 |
| v52_family_mean_conv5way_step50000 | roundtrip_src_eng | all | 300 | 0.914374 | 0.021298 |
| v52_family_mean_conv5way_step50000 | roundtrip_src_eng | v5_target | 300 | 0.914374 | 0.021298 |
| v52_family_mean_conv5way_step50000 | roundtrip_src_pivot | all | 300 | 0.936302 | 0.334108 |
| v52_family_mean_conv5way_step50000 | roundtrip_src_pivot | v5_target | 300 | 0.936302 | 0.334108 |
| v52_family_mean_conv5way_step50000 | same_language_bible_adjacent | all | 300 | 0.978612 | 0.763382 |
| v52_family_mean_conv5way_step50000 | same_language_bible_adjacent | v5_target | 300 | 0.978612 | 0.763382 |
| v52_family_mean_conv5way_step50000 | same_language_tatoeba_adjacent | all | 300 | 0.949765 | 0.413482 |
| v52_family_mean_conv5way_step50000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.949765 | 0.413482 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
