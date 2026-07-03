# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step15000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step15000 | aligned_bible_src_eng | all | 300 | 0.917283 | 0.038611 |
| v52_random_conv5way_step15000 | aligned_bible_src_eng | v5_target | 300 | 0.917283 | 0.038611 |
| v52_random_conv5way_step15000 | aligned_tatoeba_src_eng | all | 300 | 0.919875 | 0.190080 |
| v52_random_conv5way_step15000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.919875 | 0.190080 |
| v52_random_conv5way_step15000 | roundtrip_eng_pivot | all | 300 | 0.914923 | 0.014747 |
| v52_random_conv5way_step15000 | roundtrip_eng_pivot | v5_target | 300 | 0.914923 | 0.014747 |
| v52_random_conv5way_step15000 | roundtrip_src_eng | all | 300 | 0.913853 | 0.018422 |
| v52_random_conv5way_step15000 | roundtrip_src_eng | v5_target | 300 | 0.913853 | 0.018422 |
| v52_random_conv5way_step15000 | roundtrip_src_pivot | all | 300 | 0.936290 | 0.346131 |
| v52_random_conv5way_step15000 | roundtrip_src_pivot | v5_target | 300 | 0.936290 | 0.346131 |
| v52_random_conv5way_step15000 | same_language_bible_adjacent | all | 300 | 0.977353 | 0.749083 |
| v52_random_conv5way_step15000 | same_language_bible_adjacent | v5_target | 300 | 0.977353 | 0.749083 |
| v52_random_conv5way_step15000 | same_language_tatoeba_adjacent | all | 300 | 0.941195 | 0.356597 |
| v52_random_conv5way_step15000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.941195 | 0.356597 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
