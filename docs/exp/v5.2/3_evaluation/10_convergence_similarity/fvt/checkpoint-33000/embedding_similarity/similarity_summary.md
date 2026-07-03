# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step33000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step33000 | aligned_bible_src_eng | all | 300 | 0.921809 | 0.072887 |
| v52_fvt_conv5way_step33000 | aligned_bible_src_eng | v5_target | 300 | 0.921809 | 0.072887 |
| v52_fvt_conv5way_step33000 | aligned_tatoeba_src_eng | all | 300 | 0.926299 | 0.198813 |
| v52_fvt_conv5way_step33000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926299 | 0.198813 |
| v52_fvt_conv5way_step33000 | roundtrip_eng_pivot | all | 300 | 0.918719 | 0.034901 |
| v52_fvt_conv5way_step33000 | roundtrip_eng_pivot | v5_target | 300 | 0.918719 | 0.034901 |
| v52_fvt_conv5way_step33000 | roundtrip_src_eng | all | 300 | 0.918672 | 0.050348 |
| v52_fvt_conv5way_step33000 | roundtrip_src_eng | v5_target | 300 | 0.918672 | 0.050348 |
| v52_fvt_conv5way_step33000 | roundtrip_src_pivot | all | 300 | 0.935182 | 0.313538 |
| v52_fvt_conv5way_step33000 | roundtrip_src_pivot | v5_target | 300 | 0.935182 | 0.313538 |
| v52_fvt_conv5way_step33000 | same_language_bible_adjacent | all | 300 | 0.978687 | 0.758208 |
| v52_fvt_conv5way_step33000 | same_language_bible_adjacent | v5_target | 300 | 0.978687 | 0.758208 |
| v52_fvt_conv5way_step33000 | same_language_tatoeba_adjacent | all | 300 | 0.947384 | 0.389940 |
| v52_fvt_conv5way_step33000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947384 | 0.389940 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
