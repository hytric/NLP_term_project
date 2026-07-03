# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step33000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step33000 | aligned_bible_src_eng | all | 300 | 0.922394 | 0.072874 |
| v52_weighted_fvt_conv5way_step33000 | aligned_bible_src_eng | v5_target | 300 | 0.922394 | 0.072874 |
| v52_weighted_fvt_conv5way_step33000 | aligned_tatoeba_src_eng | all | 300 | 0.925569 | 0.208859 |
| v52_weighted_fvt_conv5way_step33000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925569 | 0.208859 |
| v52_weighted_fvt_conv5way_step33000 | roundtrip_eng_pivot | all | 300 | 0.918313 | 0.021392 |
| v52_weighted_fvt_conv5way_step33000 | roundtrip_eng_pivot | v5_target | 300 | 0.918313 | 0.021392 |
| v52_weighted_fvt_conv5way_step33000 | roundtrip_src_eng | all | 300 | 0.919489 | 0.050664 |
| v52_weighted_fvt_conv5way_step33000 | roundtrip_src_eng | v5_target | 300 | 0.919489 | 0.050664 |
| v52_weighted_fvt_conv5way_step33000 | roundtrip_src_pivot | all | 300 | 0.934649 | 0.294821 |
| v52_weighted_fvt_conv5way_step33000 | roundtrip_src_pivot | v5_target | 300 | 0.934649 | 0.294821 |
| v52_weighted_fvt_conv5way_step33000 | same_language_bible_adjacent | all | 300 | 0.978519 | 0.754907 |
| v52_weighted_fvt_conv5way_step33000 | same_language_bible_adjacent | v5_target | 300 | 0.978519 | 0.754907 |
| v52_weighted_fvt_conv5way_step33000 | same_language_tatoeba_adjacent | all | 300 | 0.944908 | 0.371093 |
| v52_weighted_fvt_conv5way_step33000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944908 | 0.371093 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
