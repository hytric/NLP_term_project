# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step20000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step20000 | aligned_bible_src_eng | all | 300 | 0.921412 | 0.069192 |
| v52_fvt_conv5way_step20000 | aligned_bible_src_eng | v5_target | 300 | 0.921412 | 0.069192 |
| v52_fvt_conv5way_step20000 | aligned_tatoeba_src_eng | all | 300 | 0.926265 | 0.199510 |
| v52_fvt_conv5way_step20000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926265 | 0.199510 |
| v52_fvt_conv5way_step20000 | roundtrip_eng_pivot | all | 300 | 0.918443 | 0.030944 |
| v52_fvt_conv5way_step20000 | roundtrip_eng_pivot | v5_target | 300 | 0.918443 | 0.030944 |
| v52_fvt_conv5way_step20000 | roundtrip_src_eng | all | 300 | 0.918243 | 0.046423 |
| v52_fvt_conv5way_step20000 | roundtrip_src_eng | v5_target | 300 | 0.918243 | 0.046423 |
| v52_fvt_conv5way_step20000 | roundtrip_src_pivot | all | 300 | 0.934705 | 0.308493 |
| v52_fvt_conv5way_step20000 | roundtrip_src_pivot | v5_target | 300 | 0.934705 | 0.308493 |
| v52_fvt_conv5way_step20000 | same_language_bible_adjacent | all | 300 | 0.978589 | 0.757391 |
| v52_fvt_conv5way_step20000 | same_language_bible_adjacent | v5_target | 300 | 0.978589 | 0.757391 |
| v52_fvt_conv5way_step20000 | same_language_tatoeba_adjacent | all | 300 | 0.947259 | 0.388320 |
| v52_fvt_conv5way_step20000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947259 | 0.388320 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
