# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step5000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step5000 | aligned_bible_src_eng | all | 300 | 0.916668 | 0.036702 |
| v52_fvt_conv5way_step5000 | aligned_bible_src_eng | v5_target | 300 | 0.916668 | 0.036702 |
| v52_fvt_conv5way_step5000 | aligned_tatoeba_src_eng | all | 300 | 0.917015 | 0.169470 |
| v52_fvt_conv5way_step5000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.917015 | 0.169470 |
| v52_fvt_conv5way_step5000 | roundtrip_eng_pivot | all | 300 | 0.914475 | 0.006693 |
| v52_fvt_conv5way_step5000 | roundtrip_eng_pivot | v5_target | 300 | 0.914475 | 0.006693 |
| v52_fvt_conv5way_step5000 | roundtrip_src_eng | all | 300 | 0.913529 | 0.013895 |
| v52_fvt_conv5way_step5000 | roundtrip_src_eng | v5_target | 300 | 0.913529 | 0.013895 |
| v52_fvt_conv5way_step5000 | roundtrip_src_pivot | all | 300 | 0.936007 | 0.329650 |
| v52_fvt_conv5way_step5000 | roundtrip_src_pivot | v5_target | 300 | 0.936007 | 0.329650 |
| v52_fvt_conv5way_step5000 | same_language_bible_adjacent | all | 300 | 0.977002 | 0.745974 |
| v52_fvt_conv5way_step5000 | same_language_bible_adjacent | v5_target | 300 | 0.977002 | 0.745974 |
| v52_fvt_conv5way_step5000 | same_language_tatoeba_adjacent | all | 300 | 0.941895 | 0.374375 |
| v52_fvt_conv5way_step5000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.941895 | 0.374375 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
