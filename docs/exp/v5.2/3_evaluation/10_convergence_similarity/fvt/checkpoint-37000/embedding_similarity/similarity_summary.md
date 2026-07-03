# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step37000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step37000 | aligned_bible_src_eng | all | 300 | 0.921903 | 0.071706 |
| v52_fvt_conv5way_step37000 | aligned_bible_src_eng | v5_target | 300 | 0.921903 | 0.071706 |
| v52_fvt_conv5way_step37000 | aligned_tatoeba_src_eng | all | 300 | 0.926567 | 0.199711 |
| v52_fvt_conv5way_step37000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926567 | 0.199711 |
| v52_fvt_conv5way_step37000 | roundtrip_eng_pivot | all | 300 | 0.918941 | 0.034692 |
| v52_fvt_conv5way_step37000 | roundtrip_eng_pivot | v5_target | 300 | 0.918941 | 0.034692 |
| v52_fvt_conv5way_step37000 | roundtrip_src_eng | all | 300 | 0.918750 | 0.049062 |
| v52_fvt_conv5way_step37000 | roundtrip_src_eng | v5_target | 300 | 0.918750 | 0.049062 |
| v52_fvt_conv5way_step37000 | roundtrip_src_pivot | all | 300 | 0.935277 | 0.313544 |
| v52_fvt_conv5way_step37000 | roundtrip_src_pivot | v5_target | 300 | 0.935277 | 0.313544 |
| v52_fvt_conv5way_step37000 | same_language_bible_adjacent | all | 300 | 0.978752 | 0.758906 |
| v52_fvt_conv5way_step37000 | same_language_bible_adjacent | v5_target | 300 | 0.978752 | 0.758906 |
| v52_fvt_conv5way_step37000 | same_language_tatoeba_adjacent | all | 300 | 0.947467 | 0.389280 |
| v52_fvt_conv5way_step37000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947467 | 0.389280 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
