# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step43000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step43000 | aligned_bible_src_eng | all | 300 | 0.916539 | 0.041206 |
| v52_family_mean_conv5way_step43000 | aligned_bible_src_eng | v5_target | 300 | 0.916539 | 0.041206 |
| v52_family_mean_conv5way_step43000 | aligned_tatoeba_src_eng | all | 300 | 0.925398 | 0.209625 |
| v52_family_mean_conv5way_step43000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925398 | 0.209625 |
| v52_family_mean_conv5way_step43000 | roundtrip_eng_pivot | all | 300 | 0.913731 | 0.002418 |
| v52_family_mean_conv5way_step43000 | roundtrip_eng_pivot | v5_target | 300 | 0.913731 | 0.002418 |
| v52_family_mean_conv5way_step43000 | roundtrip_src_eng | all | 300 | 0.913347 | 0.018577 |
| v52_family_mean_conv5way_step43000 | roundtrip_src_eng | v5_target | 300 | 0.913347 | 0.018577 |
| v52_family_mean_conv5way_step43000 | roundtrip_src_pivot | all | 300 | 0.936671 | 0.341148 |
| v52_family_mean_conv5way_step43000 | roundtrip_src_pivot | v5_target | 300 | 0.936671 | 0.341148 |
| v52_family_mean_conv5way_step43000 | same_language_bible_adjacent | all | 300 | 0.978488 | 0.763162 |
| v52_family_mean_conv5way_step43000 | same_language_bible_adjacent | v5_target | 300 | 0.978488 | 0.763162 |
| v52_family_mean_conv5way_step43000 | same_language_tatoeba_adjacent | all | 300 | 0.948811 | 0.412580 |
| v52_family_mean_conv5way_step43000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.948811 | 0.412580 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
