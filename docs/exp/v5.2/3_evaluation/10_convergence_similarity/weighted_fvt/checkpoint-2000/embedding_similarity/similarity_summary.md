# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step2000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step2000 | aligned_bible_src_eng | all | 300 | 0.914130 | -0.013809 |
| v52_weighted_fvt_conv5way_step2000 | aligned_bible_src_eng | v5_target | 300 | 0.914130 | -0.013809 |
| v52_weighted_fvt_conv5way_step2000 | aligned_tatoeba_src_eng | all | 300 | 0.911605 | 0.126158 |
| v52_weighted_fvt_conv5way_step2000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.911605 | 0.126158 |
| v52_weighted_fvt_conv5way_step2000 | roundtrip_eng_pivot | all | 300 | 0.914224 | -0.039467 |
| v52_weighted_fvt_conv5way_step2000 | roundtrip_eng_pivot | v5_target | 300 | 0.914224 | -0.039467 |
| v52_weighted_fvt_conv5way_step2000 | roundtrip_src_eng | all | 300 | 0.911028 | -0.035565 |
| v52_weighted_fvt_conv5way_step2000 | roundtrip_src_eng | v5_target | 300 | 0.911028 | -0.035565 |
| v52_weighted_fvt_conv5way_step2000 | roundtrip_src_pivot | all | 300 | 0.946446 | 0.394491 |
| v52_weighted_fvt_conv5way_step2000 | roundtrip_src_pivot | v5_target | 300 | 0.946446 | 0.394491 |
| v52_weighted_fvt_conv5way_step2000 | same_language_bible_adjacent | all | 300 | 0.976673 | 0.730616 |
| v52_weighted_fvt_conv5way_step2000 | same_language_bible_adjacent | v5_target | 300 | 0.976673 | 0.730616 |
| v52_weighted_fvt_conv5way_step2000 | same_language_tatoeba_adjacent | all | 300 | 0.939358 | 0.356396 |
| v52_weighted_fvt_conv5way_step2000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.939358 | 0.356396 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
