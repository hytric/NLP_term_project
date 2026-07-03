# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step13000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step13000 | aligned_bible_src_eng | all | 300 | 0.919480 | 0.063991 |
| v52_fvt_conv5way_step13000 | aligned_bible_src_eng | v5_target | 300 | 0.919480 | 0.063991 |
| v52_fvt_conv5way_step13000 | aligned_tatoeba_src_eng | all | 300 | 0.923739 | 0.190860 |
| v52_fvt_conv5way_step13000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.923739 | 0.190860 |
| v52_fvt_conv5way_step13000 | roundtrip_eng_pivot | all | 300 | 0.916638 | 0.026574 |
| v52_fvt_conv5way_step13000 | roundtrip_eng_pivot | v5_target | 300 | 0.916638 | 0.026574 |
| v52_fvt_conv5way_step13000 | roundtrip_src_eng | all | 300 | 0.916230 | 0.042344 |
| v52_fvt_conv5way_step13000 | roundtrip_src_eng | v5_target | 300 | 0.916230 | 0.042344 |
| v52_fvt_conv5way_step13000 | roundtrip_src_pivot | all | 300 | 0.934119 | 0.312539 |
| v52_fvt_conv5way_step13000 | roundtrip_src_pivot | v5_target | 300 | 0.934119 | 0.312539 |
| v52_fvt_conv5way_step13000 | same_language_bible_adjacent | all | 300 | 0.977922 | 0.754135 |
| v52_fvt_conv5way_step13000 | same_language_bible_adjacent | v5_target | 300 | 0.977922 | 0.754135 |
| v52_fvt_conv5way_step13000 | same_language_tatoeba_adjacent | all | 300 | 0.946728 | 0.390809 |
| v52_fvt_conv5way_step13000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.946728 | 0.390809 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
