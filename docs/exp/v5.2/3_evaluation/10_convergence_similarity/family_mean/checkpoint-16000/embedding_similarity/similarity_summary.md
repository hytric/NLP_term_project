# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step16000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step16000 | aligned_bible_src_eng | all | 300 | 0.907406 | 0.006601 |
| v52_family_mean_conv5way_step16000 | aligned_bible_src_eng | v5_target | 300 | 0.907406 | 0.006601 |
| v52_family_mean_conv5way_step16000 | aligned_tatoeba_src_eng | all | 300 | 0.918818 | 0.194683 |
| v52_family_mean_conv5way_step16000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.918818 | 0.194683 |
| v52_family_mean_conv5way_step16000 | roundtrip_eng_pivot | all | 300 | 0.907601 | -0.017089 |
| v52_family_mean_conv5way_step16000 | roundtrip_eng_pivot | v5_target | 300 | 0.907601 | -0.017089 |
| v52_family_mean_conv5way_step16000 | roundtrip_src_eng | all | 300 | 0.903964 | -0.015388 |
| v52_family_mean_conv5way_step16000 | roundtrip_src_eng | v5_target | 300 | 0.903964 | -0.015388 |
| v52_family_mean_conv5way_step16000 | roundtrip_src_pivot | all | 300 | 0.936889 | 0.362801 |
| v52_family_mean_conv5way_step16000 | roundtrip_src_pivot | v5_target | 300 | 0.936889 | 0.362801 |
| v52_family_mean_conv5way_step16000 | same_language_bible_adjacent | all | 300 | 0.977534 | 0.766976 |
| v52_family_mean_conv5way_step16000 | same_language_bible_adjacent | v5_target | 300 | 0.977534 | 0.766976 |
| v52_family_mean_conv5way_step16000 | same_language_tatoeba_adjacent | all | 300 | 0.946565 | 0.414196 |
| v52_family_mean_conv5way_step16000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.946565 | 0.414196 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
