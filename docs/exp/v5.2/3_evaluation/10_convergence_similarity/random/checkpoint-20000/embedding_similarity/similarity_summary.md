# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step20000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step20000 | aligned_bible_src_eng | all | 300 | 0.920111 | 0.041669 |
| v52_random_conv5way_step20000 | aligned_bible_src_eng | v5_target | 300 | 0.920111 | 0.041669 |
| v52_random_conv5way_step20000 | aligned_tatoeba_src_eng | all | 300 | 0.921209 | 0.184705 |
| v52_random_conv5way_step20000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.921209 | 0.184705 |
| v52_random_conv5way_step20000 | roundtrip_eng_pivot | all | 300 | 0.917907 | 0.017738 |
| v52_random_conv5way_step20000 | roundtrip_eng_pivot | v5_target | 300 | 0.917907 | 0.017738 |
| v52_random_conv5way_step20000 | roundtrip_src_eng | all | 300 | 0.916852 | 0.019243 |
| v52_random_conv5way_step20000 | roundtrip_src_eng | v5_target | 300 | 0.916852 | 0.019243 |
| v52_random_conv5way_step20000 | roundtrip_src_pivot | all | 300 | 0.938094 | 0.342339 |
| v52_random_conv5way_step20000 | roundtrip_src_pivot | v5_target | 300 | 0.938094 | 0.342339 |
| v52_random_conv5way_step20000 | same_language_bible_adjacent | all | 300 | 0.977593 | 0.744150 |
| v52_random_conv5way_step20000 | same_language_bible_adjacent | v5_target | 300 | 0.977593 | 0.744150 |
| v52_random_conv5way_step20000 | same_language_tatoeba_adjacent | all | 300 | 0.942591 | 0.355492 |
| v52_random_conv5way_step20000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.942591 | 0.355492 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
