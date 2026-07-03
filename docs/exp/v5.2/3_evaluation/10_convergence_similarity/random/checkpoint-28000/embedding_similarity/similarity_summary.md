# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step28000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step28000 | aligned_bible_src_eng | all | 300 | 0.921093 | 0.042151 |
| v52_random_conv5way_step28000 | aligned_bible_src_eng | v5_target | 300 | 0.921093 | 0.042151 |
| v52_random_conv5way_step28000 | aligned_tatoeba_src_eng | all | 300 | 0.922423 | 0.186010 |
| v52_random_conv5way_step28000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922423 | 0.186010 |
| v52_random_conv5way_step28000 | roundtrip_eng_pivot | all | 300 | 0.918817 | 0.018708 |
| v52_random_conv5way_step28000 | roundtrip_eng_pivot | v5_target | 300 | 0.918817 | 0.018708 |
| v52_random_conv5way_step28000 | roundtrip_src_eng | all | 300 | 0.917880 | 0.020210 |
| v52_random_conv5way_step28000 | roundtrip_src_eng | v5_target | 300 | 0.917880 | 0.020210 |
| v52_random_conv5way_step28000 | roundtrip_src_pivot | all | 300 | 0.938597 | 0.341199 |
| v52_random_conv5way_step28000 | roundtrip_src_pivot | v5_target | 300 | 0.938597 | 0.341199 |
| v52_random_conv5way_step28000 | same_language_bible_adjacent | all | 300 | 0.977838 | 0.744143 |
| v52_random_conv5way_step28000 | same_language_bible_adjacent | v5_target | 300 | 0.977838 | 0.744143 |
| v52_random_conv5way_step28000 | same_language_tatoeba_adjacent | all | 300 | 0.943365 | 0.355567 |
| v52_random_conv5way_step28000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943365 | 0.355567 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
