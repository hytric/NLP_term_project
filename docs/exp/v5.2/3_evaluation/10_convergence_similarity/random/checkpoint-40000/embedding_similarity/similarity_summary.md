# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step40000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step40000 | aligned_bible_src_eng | all | 300 | 0.921786 | 0.044075 |
| v52_random_conv5way_step40000 | aligned_bible_src_eng | v5_target | 300 | 0.921786 | 0.044075 |
| v52_random_conv5way_step40000 | aligned_tatoeba_src_eng | all | 300 | 0.923205 | 0.187568 |
| v52_random_conv5way_step40000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.923205 | 0.187568 |
| v52_random_conv5way_step40000 | roundtrip_eng_pivot | all | 300 | 0.919451 | 0.020409 |
| v52_random_conv5way_step40000 | roundtrip_eng_pivot | v5_target | 300 | 0.919451 | 0.020409 |
| v52_random_conv5way_step40000 | roundtrip_src_eng | all | 300 | 0.918590 | 0.022047 |
| v52_random_conv5way_step40000 | roundtrip_src_eng | v5_target | 300 | 0.918590 | 0.022047 |
| v52_random_conv5way_step40000 | roundtrip_src_pivot | all | 300 | 0.938914 | 0.340783 |
| v52_random_conv5way_step40000 | roundtrip_src_pivot | v5_target | 300 | 0.938914 | 0.340783 |
| v52_random_conv5way_step40000 | same_language_bible_adjacent | all | 300 | 0.977969 | 0.744081 |
| v52_random_conv5way_step40000 | same_language_bible_adjacent | v5_target | 300 | 0.977969 | 0.744081 |
| v52_random_conv5way_step40000 | same_language_tatoeba_adjacent | all | 300 | 0.943801 | 0.355342 |
| v52_random_conv5way_step40000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943801 | 0.355342 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
