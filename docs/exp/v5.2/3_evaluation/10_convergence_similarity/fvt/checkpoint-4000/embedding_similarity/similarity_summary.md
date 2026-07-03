# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step4000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step4000 | aligned_bible_src_eng | all | 300 | 0.915270 | 0.030088 |
| v52_fvt_conv5way_step4000 | aligned_bible_src_eng | v5_target | 300 | 0.915270 | 0.030088 |
| v52_fvt_conv5way_step4000 | aligned_tatoeba_src_eng | all | 300 | 0.914109 | 0.153752 |
| v52_fvt_conv5way_step4000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.914109 | 0.153752 |
| v52_fvt_conv5way_step4000 | roundtrip_eng_pivot | all | 300 | 0.913468 | 0.006623 |
| v52_fvt_conv5way_step4000 | roundtrip_eng_pivot | v5_target | 300 | 0.913468 | 0.006623 |
| v52_fvt_conv5way_step4000 | roundtrip_src_eng | all | 300 | 0.912273 | 0.010962 |
| v52_fvt_conv5way_step4000 | roundtrip_src_eng | v5_target | 300 | 0.912273 | 0.010962 |
| v52_fvt_conv5way_step4000 | roundtrip_src_pivot | all | 300 | 0.935822 | 0.319913 |
| v52_fvt_conv5way_step4000 | roundtrip_src_pivot | v5_target | 300 | 0.935822 | 0.319913 |
| v52_fvt_conv5way_step4000 | same_language_bible_adjacent | all | 300 | 0.977334 | 0.746789 |
| v52_fvt_conv5way_step4000 | same_language_bible_adjacent | v5_target | 300 | 0.977334 | 0.746789 |
| v52_fvt_conv5way_step4000 | same_language_tatoeba_adjacent | all | 300 | 0.941135 | 0.369970 |
| v52_fvt_conv5way_step4000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.941135 | 0.369970 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
