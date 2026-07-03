# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step1000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step1000 | aligned_bible_src_eng | all | 300 | 0.918164 | 0.044813 |
| v52_fvt_conv5way_step1000 | aligned_bible_src_eng | v5_target | 300 | 0.918164 | 0.044813 |
| v52_fvt_conv5way_step1000 | aligned_tatoeba_src_eng | all | 300 | 0.913475 | 0.148025 |
| v52_fvt_conv5way_step1000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.913475 | 0.148025 |
| v52_fvt_conv5way_step1000 | roundtrip_eng_pivot | all | 300 | 0.918324 | 0.030503 |
| v52_fvt_conv5way_step1000 | roundtrip_eng_pivot | v5_target | 300 | 0.918324 | 0.030503 |
| v52_fvt_conv5way_step1000 | roundtrip_src_eng | all | 300 | 0.915197 | 0.024635 |
| v52_fvt_conv5way_step1000 | roundtrip_src_eng | v5_target | 300 | 0.915197 | 0.024635 |
| v52_fvt_conv5way_step1000 | roundtrip_src_pivot | all | 300 | 0.941186 | 0.362163 |
| v52_fvt_conv5way_step1000 | roundtrip_src_pivot | v5_target | 300 | 0.941186 | 0.362163 |
| v52_fvt_conv5way_step1000 | same_language_bible_adjacent | all | 300 | 0.977255 | 0.740101 |
| v52_fvt_conv5way_step1000 | same_language_bible_adjacent | v5_target | 300 | 0.977255 | 0.740101 |
| v52_fvt_conv5way_step1000 | same_language_tatoeba_adjacent | all | 300 | 0.941336 | 0.365732 |
| v52_fvt_conv5way_step1000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.941336 | 0.365732 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
