# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step16000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step16000 | aligned_bible_src_eng | all | 300 | 0.921041 | 0.050340 |
| v52_random_conv5way_step16000 | aligned_bible_src_eng | v5_target | 300 | 0.921041 | 0.050340 |
| v52_random_conv5way_step16000 | aligned_tatoeba_src_eng | all | 300 | 0.922138 | 0.193370 |
| v52_random_conv5way_step16000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922138 | 0.193370 |
| v52_random_conv5way_step16000 | roundtrip_eng_pivot | all | 300 | 0.918822 | 0.026741 |
| v52_random_conv5way_step16000 | roundtrip_eng_pivot | v5_target | 300 | 0.918822 | 0.026741 |
| v52_random_conv5way_step16000 | roundtrip_src_eng | all | 300 | 0.917819 | 0.029334 |
| v52_random_conv5way_step16000 | roundtrip_src_eng | v5_target | 300 | 0.917819 | 0.029334 |
| v52_random_conv5way_step16000 | roundtrip_src_pivot | all | 300 | 0.938435 | 0.338830 |
| v52_random_conv5way_step16000 | roundtrip_src_pivot | v5_target | 300 | 0.938435 | 0.338830 |
| v52_random_conv5way_step16000 | same_language_bible_adjacent | all | 300 | 0.978005 | 0.745487 |
| v52_random_conv5way_step16000 | same_language_bible_adjacent | v5_target | 300 | 0.978005 | 0.745487 |
| v52_random_conv5way_step16000 | same_language_tatoeba_adjacent | all | 300 | 0.942656 | 0.353341 |
| v52_random_conv5way_step16000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.942656 | 0.353341 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
