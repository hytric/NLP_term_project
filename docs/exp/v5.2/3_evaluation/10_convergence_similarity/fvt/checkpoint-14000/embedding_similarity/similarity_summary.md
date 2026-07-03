# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step14000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step14000 | aligned_bible_src_eng | all | 300 | 0.916877 | 0.053926 |
| v52_fvt_conv5way_step14000 | aligned_bible_src_eng | v5_target | 300 | 0.916877 | 0.053926 |
| v52_fvt_conv5way_step14000 | aligned_tatoeba_src_eng | all | 300 | 0.920948 | 0.189254 |
| v52_fvt_conv5way_step14000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.920948 | 0.189254 |
| v52_fvt_conv5way_step14000 | roundtrip_eng_pivot | all | 300 | 0.913677 | 0.015488 |
| v52_fvt_conv5way_step14000 | roundtrip_eng_pivot | v5_target | 300 | 0.913677 | 0.015488 |
| v52_fvt_conv5way_step14000 | roundtrip_src_eng | all | 300 | 0.913440 | 0.031527 |
| v52_fvt_conv5way_step14000 | roundtrip_src_eng | v5_target | 300 | 0.913440 | 0.031527 |
| v52_fvt_conv5way_step14000 | roundtrip_src_pivot | all | 300 | 0.931181 | 0.309702 |
| v52_fvt_conv5way_step14000 | roundtrip_src_pivot | v5_target | 300 | 0.931181 | 0.309702 |
| v52_fvt_conv5way_step14000 | same_language_bible_adjacent | all | 300 | 0.977512 | 0.758355 |
| v52_fvt_conv5way_step14000 | same_language_bible_adjacent | v5_target | 300 | 0.977512 | 0.758355 |
| v52_fvt_conv5way_step14000 | same_language_tatoeba_adjacent | all | 300 | 0.944671 | 0.387983 |
| v52_fvt_conv5way_step14000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944671 | 0.387983 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
