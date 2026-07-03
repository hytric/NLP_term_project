# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step22000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step22000 | aligned_bible_src_eng | all | 300 | 0.921774 | 0.069841 |
| v52_fvt_conv5way_step22000 | aligned_bible_src_eng | v5_target | 300 | 0.921774 | 0.069841 |
| v52_fvt_conv5way_step22000 | aligned_tatoeba_src_eng | all | 300 | 0.926511 | 0.199478 |
| v52_fvt_conv5way_step22000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926511 | 0.199478 |
| v52_fvt_conv5way_step22000 | roundtrip_eng_pivot | all | 300 | 0.918712 | 0.031977 |
| v52_fvt_conv5way_step22000 | roundtrip_eng_pivot | v5_target | 300 | 0.918712 | 0.031977 |
| v52_fvt_conv5way_step22000 | roundtrip_src_eng | all | 300 | 0.918620 | 0.047139 |
| v52_fvt_conv5way_step22000 | roundtrip_src_eng | v5_target | 300 | 0.918620 | 0.047139 |
| v52_fvt_conv5way_step22000 | roundtrip_src_pivot | all | 300 | 0.934943 | 0.310650 |
| v52_fvt_conv5way_step22000 | roundtrip_src_pivot | v5_target | 300 | 0.934943 | 0.310650 |
| v52_fvt_conv5way_step22000 | same_language_bible_adjacent | all | 300 | 0.978727 | 0.758791 |
| v52_fvt_conv5way_step22000 | same_language_bible_adjacent | v5_target | 300 | 0.978727 | 0.758791 |
| v52_fvt_conv5way_step22000 | same_language_tatoeba_adjacent | all | 300 | 0.947333 | 0.388010 |
| v52_fvt_conv5way_step22000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947333 | 0.388010 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
