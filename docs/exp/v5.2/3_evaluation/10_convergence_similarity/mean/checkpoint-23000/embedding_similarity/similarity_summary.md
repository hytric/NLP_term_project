# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step23000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step23000 | aligned_bible_src_eng | all | 300 | 0.921886 | 0.052767 |
| v52_mean_conv5way_step23000 | aligned_bible_src_eng | v5_target | 300 | 0.921886 | 0.052767 |
| v52_mean_conv5way_step23000 | aligned_tatoeba_src_eng | all | 300 | 0.924822 | 0.193981 |
| v52_mean_conv5way_step23000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.924822 | 0.193981 |
| v52_mean_conv5way_step23000 | roundtrip_eng_pivot | all | 300 | 0.918951 | 0.026720 |
| v52_mean_conv5way_step23000 | roundtrip_eng_pivot | v5_target | 300 | 0.918951 | 0.026720 |
| v52_mean_conv5way_step23000 | roundtrip_src_eng | all | 300 | 0.919487 | 0.032366 |
| v52_mean_conv5way_step23000 | roundtrip_src_eng | v5_target | 300 | 0.919487 | 0.032366 |
| v52_mean_conv5way_step23000 | roundtrip_src_pivot | all | 300 | 0.937450 | 0.314023 |
| v52_mean_conv5way_step23000 | roundtrip_src_pivot | v5_target | 300 | 0.937450 | 0.314023 |
| v52_mean_conv5way_step23000 | same_language_bible_adjacent | all | 300 | 0.978929 | 0.748369 |
| v52_mean_conv5way_step23000 | same_language_bible_adjacent | v5_target | 300 | 0.978929 | 0.748369 |
| v52_mean_conv5way_step23000 | same_language_tatoeba_adjacent | all | 300 | 0.945406 | 0.379945 |
| v52_mean_conv5way_step23000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945406 | 0.379945 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
