# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step40000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step40000 | aligned_bible_src_eng | all | 300 | 0.922053 | 0.071770 |
| v52_fvt_conv5way_step40000 | aligned_bible_src_eng | v5_target | 300 | 0.922053 | 0.071770 |
| v52_fvt_conv5way_step40000 | aligned_tatoeba_src_eng | all | 300 | 0.926526 | 0.198889 |
| v52_fvt_conv5way_step40000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926526 | 0.198889 |
| v52_fvt_conv5way_step40000 | roundtrip_eng_pivot | all | 300 | 0.919083 | 0.035039 |
| v52_fvt_conv5way_step40000 | roundtrip_eng_pivot | v5_target | 300 | 0.919083 | 0.035039 |
| v52_fvt_conv5way_step40000 | roundtrip_src_eng | all | 300 | 0.918926 | 0.049348 |
| v52_fvt_conv5way_step40000 | roundtrip_src_eng | v5_target | 300 | 0.918926 | 0.049348 |
| v52_fvt_conv5way_step40000 | roundtrip_src_pivot | all | 300 | 0.935279 | 0.312305 |
| v52_fvt_conv5way_step40000 | roundtrip_src_pivot | v5_target | 300 | 0.935279 | 0.312305 |
| v52_fvt_conv5way_step40000 | same_language_bible_adjacent | all | 300 | 0.978738 | 0.758067 |
| v52_fvt_conv5way_step40000 | same_language_bible_adjacent | v5_target | 300 | 0.978738 | 0.758067 |
| v52_fvt_conv5way_step40000 | same_language_tatoeba_adjacent | all | 300 | 0.947531 | 0.389082 |
| v52_fvt_conv5way_step40000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947531 | 0.389082 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
