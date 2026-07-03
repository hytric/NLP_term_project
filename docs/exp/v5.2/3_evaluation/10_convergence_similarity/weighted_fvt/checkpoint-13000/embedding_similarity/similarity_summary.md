# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step13000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step13000 | aligned_bible_src_eng | all | 300 | 0.919395 | 0.060074 |
| v52_weighted_fvt_conv5way_step13000 | aligned_bible_src_eng | v5_target | 300 | 0.919395 | 0.060074 |
| v52_weighted_fvt_conv5way_step13000 | aligned_tatoeba_src_eng | all | 300 | 0.921980 | 0.189240 |
| v52_weighted_fvt_conv5way_step13000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.921980 | 0.189240 |
| v52_weighted_fvt_conv5way_step13000 | roundtrip_eng_pivot | all | 300 | 0.917619 | 0.025390 |
| v52_weighted_fvt_conv5way_step13000 | roundtrip_eng_pivot | v5_target | 300 | 0.917619 | 0.025390 |
| v52_weighted_fvt_conv5way_step13000 | roundtrip_src_eng | all | 300 | 0.916190 | 0.039384 |
| v52_weighted_fvt_conv5way_step13000 | roundtrip_src_eng | v5_target | 300 | 0.916190 | 0.039384 |
| v52_weighted_fvt_conv5way_step13000 | roundtrip_src_pivot | all | 300 | 0.934087 | 0.305067 |
| v52_weighted_fvt_conv5way_step13000 | roundtrip_src_pivot | v5_target | 300 | 0.934087 | 0.305067 |
| v52_weighted_fvt_conv5way_step13000 | same_language_bible_adjacent | all | 300 | 0.977387 | 0.750105 |
| v52_weighted_fvt_conv5way_step13000 | same_language_bible_adjacent | v5_target | 300 | 0.977387 | 0.750105 |
| v52_weighted_fvt_conv5way_step13000 | same_language_tatoeba_adjacent | all | 300 | 0.943797 | 0.370251 |
| v52_weighted_fvt_conv5way_step13000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943797 | 0.370251 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
