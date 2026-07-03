# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_random_conv5way_step8000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step8000 | aligned_bible_src_eng | all | 300 | 0.915944 | 0.039882 |
| v52_random_conv5way_step8000 | aligned_bible_src_eng | v5_target | 300 | 0.915944 | 0.039882 |
| v52_random_conv5way_step8000 | aligned_tatoeba_src_eng | all | 300 | 0.916055 | 0.168077 |
| v52_random_conv5way_step8000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.916055 | 0.168077 |
| v52_random_conv5way_step8000 | roundtrip_eng_pivot | all | 300 | 0.913204 | 0.018981 |
| v52_random_conv5way_step8000 | roundtrip_eng_pivot | v5_target | 300 | 0.913204 | 0.018981 |
| v52_random_conv5way_step8000 | roundtrip_src_eng | all | 300 | 0.912428 | 0.019052 |
| v52_random_conv5way_step8000 | roundtrip_src_eng | v5_target | 300 | 0.912428 | 0.019052 |
| v52_random_conv5way_step8000 | roundtrip_src_pivot | all | 300 | 0.935583 | 0.344104 |
| v52_random_conv5way_step8000 | roundtrip_src_pivot | v5_target | 300 | 0.935583 | 0.344104 |
| v52_random_conv5way_step8000 | same_language_bible_adjacent | all | 300 | 0.976690 | 0.740074 |
| v52_random_conv5way_step8000 | same_language_bible_adjacent | v5_target | 300 | 0.976690 | 0.740074 |
| v52_random_conv5way_step8000 | same_language_tatoeba_adjacent | all | 300 | 0.940188 | 0.358915 |
| v52_random_conv5way_step8000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.940188 | 0.358915 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
