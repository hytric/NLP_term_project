# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step20000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step20000 | aligned_bible_src_eng | all | 300 | 0.912274 | 0.038453 |
| v52_family_mean_conv5way_step20000 | aligned_bible_src_eng | v5_target | 300 | 0.912274 | 0.038453 |
| v52_family_mean_conv5way_step20000 | aligned_tatoeba_src_eng | all | 300 | 0.918509 | 0.194824 |
| v52_family_mean_conv5way_step20000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.918509 | 0.194824 |
| v52_family_mean_conv5way_step20000 | roundtrip_eng_pivot | all | 300 | 0.911833 | 0.009058 |
| v52_family_mean_conv5way_step20000 | roundtrip_eng_pivot | v5_target | 300 | 0.911833 | 0.009058 |
| v52_family_mean_conv5way_step20000 | roundtrip_src_eng | all | 300 | 0.909108 | 0.015861 |
| v52_family_mean_conv5way_step20000 | roundtrip_src_eng | v5_target | 300 | 0.909108 | 0.015861 |
| v52_family_mean_conv5way_step20000 | roundtrip_src_pivot | all | 300 | 0.938808 | 0.360278 |
| v52_family_mean_conv5way_step20000 | roundtrip_src_pivot | v5_target | 300 | 0.938808 | 0.360278 |
| v52_family_mean_conv5way_step20000 | same_language_bible_adjacent | all | 300 | 0.977928 | 0.763407 |
| v52_family_mean_conv5way_step20000 | same_language_bible_adjacent | v5_target | 300 | 0.977928 | 0.763407 |
| v52_family_mean_conv5way_step20000 | same_language_tatoeba_adjacent | all | 300 | 0.945098 | 0.406693 |
| v52_family_mean_conv5way_step20000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945098 | 0.406693 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
