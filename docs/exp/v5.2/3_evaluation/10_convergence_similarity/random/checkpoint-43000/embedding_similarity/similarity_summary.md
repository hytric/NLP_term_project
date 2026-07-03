# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step43000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step43000 | aligned_bible_src_eng | all | 300 | 0.921831 | 0.044208 |
| v52_random_conv5way_step43000 | aligned_bible_src_eng | v5_target | 300 | 0.921831 | 0.044208 |
| v52_random_conv5way_step43000 | aligned_tatoeba_src_eng | all | 300 | 0.923116 | 0.187761 |
| v52_random_conv5way_step43000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.923116 | 0.187761 |
| v52_random_conv5way_step43000 | roundtrip_eng_pivot | all | 300 | 0.919536 | 0.020697 |
| v52_random_conv5way_step43000 | roundtrip_eng_pivot | v5_target | 300 | 0.919536 | 0.020697 |
| v52_random_conv5way_step43000 | roundtrip_src_eng | all | 300 | 0.918650 | 0.022291 |
| v52_random_conv5way_step43000 | roundtrip_src_eng | v5_target | 300 | 0.918650 | 0.022291 |
| v52_random_conv5way_step43000 | roundtrip_src_pivot | all | 300 | 0.939007 | 0.341605 |
| v52_random_conv5way_step43000 | roundtrip_src_pivot | v5_target | 300 | 0.939007 | 0.341605 |
| v52_random_conv5way_step43000 | same_language_bible_adjacent | all | 300 | 0.977956 | 0.744038 |
| v52_random_conv5way_step43000 | same_language_bible_adjacent | v5_target | 300 | 0.977956 | 0.744038 |
| v52_random_conv5way_step43000 | same_language_tatoeba_adjacent | all | 300 | 0.943752 | 0.355449 |
| v52_random_conv5way_step43000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943752 | 0.355449 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
