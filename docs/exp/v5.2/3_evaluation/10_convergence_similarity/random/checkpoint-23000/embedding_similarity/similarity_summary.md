# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step23000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step23000 | aligned_bible_src_eng | all | 300 | 0.920835 | 0.041855 |
| v52_random_conv5way_step23000 | aligned_bible_src_eng | v5_target | 300 | 0.920835 | 0.041855 |
| v52_random_conv5way_step23000 | aligned_tatoeba_src_eng | all | 300 | 0.922136 | 0.186915 |
| v52_random_conv5way_step23000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922136 | 0.186915 |
| v52_random_conv5way_step23000 | roundtrip_eng_pivot | all | 300 | 0.918640 | 0.018520 |
| v52_random_conv5way_step23000 | roundtrip_eng_pivot | v5_target | 300 | 0.918640 | 0.018520 |
| v52_random_conv5way_step23000 | roundtrip_src_eng | all | 300 | 0.917634 | 0.020010 |
| v52_random_conv5way_step23000 | roundtrip_src_eng | v5_target | 300 | 0.917634 | 0.020010 |
| v52_random_conv5way_step23000 | roundtrip_src_pivot | all | 300 | 0.938493 | 0.340687 |
| v52_random_conv5way_step23000 | roundtrip_src_pivot | v5_target | 300 | 0.938493 | 0.340687 |
| v52_random_conv5way_step23000 | same_language_bible_adjacent | all | 300 | 0.977816 | 0.744656 |
| v52_random_conv5way_step23000 | same_language_bible_adjacent | v5_target | 300 | 0.977816 | 0.744656 |
| v52_random_conv5way_step23000 | same_language_tatoeba_adjacent | all | 300 | 0.942908 | 0.354271 |
| v52_random_conv5way_step23000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.942908 | 0.354271 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
