# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step19000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step19000 | aligned_bible_src_eng | all | 300 | 0.909802 | 0.028487 |
| v52_family_mean_conv5way_step19000 | aligned_bible_src_eng | v5_target | 300 | 0.909802 | 0.028487 |
| v52_family_mean_conv5way_step19000 | aligned_tatoeba_src_eng | all | 300 | 0.920330 | 0.208317 |
| v52_family_mean_conv5way_step19000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.920330 | 0.208317 |
| v52_family_mean_conv5way_step19000 | roundtrip_eng_pivot | all | 300 | 0.911368 | 0.007194 |
| v52_family_mean_conv5way_step19000 | roundtrip_eng_pivot | v5_target | 300 | 0.911368 | 0.007194 |
| v52_family_mean_conv5way_step19000 | roundtrip_src_eng | all | 300 | 0.906349 | 0.005977 |
| v52_family_mean_conv5way_step19000 | roundtrip_src_eng | v5_target | 300 | 0.906349 | 0.005977 |
| v52_family_mean_conv5way_step19000 | roundtrip_src_pivot | all | 300 | 0.936022 | 0.357596 |
| v52_family_mean_conv5way_step19000 | roundtrip_src_pivot | v5_target | 300 | 0.936022 | 0.357596 |
| v52_family_mean_conv5way_step19000 | same_language_bible_adjacent | all | 300 | 0.977247 | 0.767341 |
| v52_family_mean_conv5way_step19000 | same_language_bible_adjacent | v5_target | 300 | 0.977247 | 0.767341 |
| v52_family_mean_conv5way_step19000 | same_language_tatoeba_adjacent | all | 300 | 0.946127 | 0.410110 |
| v52_family_mean_conv5way_step19000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.946127 | 0.410110 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
