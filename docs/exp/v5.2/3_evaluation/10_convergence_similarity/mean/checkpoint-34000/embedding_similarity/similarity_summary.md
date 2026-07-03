# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step34000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step34000 | aligned_bible_src_eng | all | 300 | 0.922671 | 0.055850 |
| v52_mean_conv5way_step34000 | aligned_bible_src_eng | v5_target | 300 | 0.922671 | 0.055850 |
| v52_mean_conv5way_step34000 | aligned_tatoeba_src_eng | all | 300 | 0.925579 | 0.195630 |
| v52_mean_conv5way_step34000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925579 | 0.195630 |
| v52_mean_conv5way_step34000 | roundtrip_eng_pivot | all | 300 | 0.919661 | 0.029371 |
| v52_mean_conv5way_step34000 | roundtrip_eng_pivot | v5_target | 300 | 0.919661 | 0.029371 |
| v52_mean_conv5way_step34000 | roundtrip_src_eng | all | 300 | 0.920286 | 0.035579 |
| v52_mean_conv5way_step34000 | roundtrip_src_eng | v5_target | 300 | 0.920286 | 0.035579 |
| v52_mean_conv5way_step34000 | roundtrip_src_pivot | all | 300 | 0.938120 | 0.316644 |
| v52_mean_conv5way_step34000 | roundtrip_src_pivot | v5_target | 300 | 0.938120 | 0.316644 |
| v52_mean_conv5way_step34000 | same_language_bible_adjacent | all | 300 | 0.979067 | 0.748382 |
| v52_mean_conv5way_step34000 | same_language_bible_adjacent | v5_target | 300 | 0.979067 | 0.748382 |
| v52_mean_conv5way_step34000 | same_language_tatoeba_adjacent | all | 300 | 0.945902 | 0.380706 |
| v52_mean_conv5way_step34000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945902 | 0.380706 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
