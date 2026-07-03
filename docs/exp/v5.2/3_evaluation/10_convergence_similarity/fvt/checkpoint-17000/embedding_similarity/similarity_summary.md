# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step17000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step17000 | aligned_bible_src_eng | all | 300 | 0.920881 | 0.067452 |
| v52_fvt_conv5way_step17000 | aligned_bible_src_eng | v5_target | 300 | 0.920881 | 0.067452 |
| v52_fvt_conv5way_step17000 | aligned_tatoeba_src_eng | all | 300 | 0.924378 | 0.196288 |
| v52_fvt_conv5way_step17000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.924378 | 0.196288 |
| v52_fvt_conv5way_step17000 | roundtrip_eng_pivot | all | 300 | 0.918353 | 0.034043 |
| v52_fvt_conv5way_step17000 | roundtrip_eng_pivot | v5_target | 300 | 0.918353 | 0.034043 |
| v52_fvt_conv5way_step17000 | roundtrip_src_eng | all | 300 | 0.917645 | 0.044602 |
| v52_fvt_conv5way_step17000 | roundtrip_src_eng | v5_target | 300 | 0.917645 | 0.044602 |
| v52_fvt_conv5way_step17000 | roundtrip_src_pivot | all | 300 | 0.935127 | 0.315475 |
| v52_fvt_conv5way_step17000 | roundtrip_src_pivot | v5_target | 300 | 0.935127 | 0.315475 |
| v52_fvt_conv5way_step17000 | same_language_bible_adjacent | all | 300 | 0.978431 | 0.757157 |
| v52_fvt_conv5way_step17000 | same_language_bible_adjacent | v5_target | 300 | 0.978431 | 0.757157 |
| v52_fvt_conv5way_step17000 | same_language_tatoeba_adjacent | all | 300 | 0.945643 | 0.385498 |
| v52_fvt_conv5way_step17000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945643 | 0.385498 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
