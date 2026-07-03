# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step26000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step26000 | aligned_bible_src_eng | all | 300 | 0.921805 | 0.053270 |
| v52_mean_conv5way_step26000 | aligned_bible_src_eng | v5_target | 300 | 0.921805 | 0.053270 |
| v52_mean_conv5way_step26000 | aligned_tatoeba_src_eng | all | 300 | 0.924863 | 0.194641 |
| v52_mean_conv5way_step26000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.924863 | 0.194641 |
| v52_mean_conv5way_step26000 | roundtrip_eng_pivot | all | 300 | 0.918929 | 0.027571 |
| v52_mean_conv5way_step26000 | roundtrip_eng_pivot | v5_target | 300 | 0.918929 | 0.027571 |
| v52_mean_conv5way_step26000 | roundtrip_src_eng | all | 300 | 0.919374 | 0.032703 |
| v52_mean_conv5way_step26000 | roundtrip_src_eng | v5_target | 300 | 0.919374 | 0.032703 |
| v52_mean_conv5way_step26000 | roundtrip_src_pivot | all | 300 | 0.937376 | 0.314084 |
| v52_mean_conv5way_step26000 | roundtrip_src_pivot | v5_target | 300 | 0.937376 | 0.314084 |
| v52_mean_conv5way_step26000 | same_language_bible_adjacent | all | 300 | 0.978888 | 0.748653 |
| v52_mean_conv5way_step26000 | same_language_bible_adjacent | v5_target | 300 | 0.978888 | 0.748653 |
| v52_mean_conv5way_step26000 | same_language_tatoeba_adjacent | all | 300 | 0.945416 | 0.379848 |
| v52_mean_conv5way_step26000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945416 | 0.379848 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
