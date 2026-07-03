# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step43000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step43000 | aligned_bible_src_eng | all | 300 | 0.921861 | 0.070256 |
| v52_fvt_conv5way_step43000 | aligned_bible_src_eng | v5_target | 300 | 0.921861 | 0.070256 |
| v52_fvt_conv5way_step43000 | aligned_tatoeba_src_eng | all | 300 | 0.926567 | 0.199508 |
| v52_fvt_conv5way_step43000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926567 | 0.199508 |
| v52_fvt_conv5way_step43000 | roundtrip_eng_pivot | all | 300 | 0.918929 | 0.033572 |
| v52_fvt_conv5way_step43000 | roundtrip_eng_pivot | v5_target | 300 | 0.918929 | 0.033572 |
| v52_fvt_conv5way_step43000 | roundtrip_src_eng | all | 300 | 0.918707 | 0.047817 |
| v52_fvt_conv5way_step43000 | roundtrip_src_eng | v5_target | 300 | 0.918707 | 0.047817 |
| v52_fvt_conv5way_step43000 | roundtrip_src_pivot | all | 300 | 0.935185 | 0.312820 |
| v52_fvt_conv5way_step43000 | roundtrip_src_pivot | v5_target | 300 | 0.935185 | 0.312820 |
| v52_fvt_conv5way_step43000 | same_language_bible_adjacent | all | 300 | 0.978727 | 0.758708 |
| v52_fvt_conv5way_step43000 | same_language_bible_adjacent | v5_target | 300 | 0.978727 | 0.758708 |
| v52_fvt_conv5way_step43000 | same_language_tatoeba_adjacent | all | 300 | 0.947535 | 0.389090 |
| v52_fvt_conv5way_step43000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947535 | 0.389090 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
