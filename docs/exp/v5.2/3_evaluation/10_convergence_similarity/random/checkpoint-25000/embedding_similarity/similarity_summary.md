# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step25000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step25000 | aligned_bible_src_eng | all | 300 | 0.920919 | 0.044917 |
| v52_random_conv5way_step25000 | aligned_bible_src_eng | v5_target | 300 | 0.920919 | 0.044917 |
| v52_random_conv5way_step25000 | aligned_tatoeba_src_eng | all | 300 | 0.922088 | 0.186908 |
| v52_random_conv5way_step25000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922088 | 0.186908 |
| v52_random_conv5way_step25000 | roundtrip_eng_pivot | all | 300 | 0.918742 | 0.021695 |
| v52_random_conv5way_step25000 | roundtrip_eng_pivot | v5_target | 300 | 0.918742 | 0.021695 |
| v52_random_conv5way_step25000 | roundtrip_src_eng | all | 300 | 0.917697 | 0.022699 |
| v52_random_conv5way_step25000 | roundtrip_src_eng | v5_target | 300 | 0.917697 | 0.022699 |
| v52_random_conv5way_step25000 | roundtrip_src_pivot | all | 300 | 0.938245 | 0.339850 |
| v52_random_conv5way_step25000 | roundtrip_src_pivot | v5_target | 300 | 0.938245 | 0.339850 |
| v52_random_conv5way_step25000 | same_language_bible_adjacent | all | 300 | 0.977729 | 0.744313 |
| v52_random_conv5way_step25000 | same_language_bible_adjacent | v5_target | 300 | 0.977729 | 0.744313 |
| v52_random_conv5way_step25000 | same_language_tatoeba_adjacent | all | 300 | 0.943001 | 0.354305 |
| v52_random_conv5way_step25000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943001 | 0.354305 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
