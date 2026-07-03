# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step49000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step49000 | aligned_bible_src_eng | all | 300 | 0.917710 | 0.043894 |
| v52_family_mean_conv5way_step49000 | aligned_bible_src_eng | v5_target | 300 | 0.917710 | 0.043894 |
| v52_family_mean_conv5way_step49000 | aligned_tatoeba_src_eng | all | 300 | 0.926773 | 0.211527 |
| v52_family_mean_conv5way_step49000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926773 | 0.211527 |
| v52_family_mean_conv5way_step49000 | roundtrip_eng_pivot | all | 300 | 0.915122 | 0.007162 |
| v52_family_mean_conv5way_step49000 | roundtrip_eng_pivot | v5_target | 300 | 0.915122 | 0.007162 |
| v52_family_mean_conv5way_step49000 | roundtrip_src_eng | all | 300 | 0.914426 | 0.021594 |
| v52_family_mean_conv5way_step49000 | roundtrip_src_eng | v5_target | 300 | 0.914426 | 0.021594 |
| v52_family_mean_conv5way_step49000 | roundtrip_src_pivot | all | 300 | 0.936266 | 0.333688 |
| v52_family_mean_conv5way_step49000 | roundtrip_src_pivot | v5_target | 300 | 0.936266 | 0.333688 |
| v52_family_mean_conv5way_step49000 | same_language_bible_adjacent | all | 300 | 0.978610 | 0.763388 |
| v52_family_mean_conv5way_step49000 | same_language_bible_adjacent | v5_target | 300 | 0.978610 | 0.763388 |
| v52_family_mean_conv5way_step49000 | same_language_tatoeba_adjacent | all | 300 | 0.949824 | 0.413585 |
| v52_family_mean_conv5way_step49000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.949824 | 0.413585 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
