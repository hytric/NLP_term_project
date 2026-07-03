# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step22000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step22000 | aligned_bible_src_eng | all | 300 | 0.920234 | 0.062746 |
| v52_weighted_fvt_conv5way_step22000 | aligned_bible_src_eng | v5_target | 300 | 0.920234 | 0.062746 |
| v52_weighted_fvt_conv5way_step22000 | aligned_tatoeba_src_eng | all | 300 | 0.925037 | 0.208732 |
| v52_weighted_fvt_conv5way_step22000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925037 | 0.208732 |
| v52_weighted_fvt_conv5way_step22000 | roundtrip_eng_pivot | all | 300 | 0.916772 | 0.019681 |
| v52_weighted_fvt_conv5way_step22000 | roundtrip_eng_pivot | v5_target | 300 | 0.916772 | 0.019681 |
| v52_weighted_fvt_conv5way_step22000 | roundtrip_src_eng | all | 300 | 0.917016 | 0.039648 |
| v52_weighted_fvt_conv5way_step22000 | roundtrip_src_eng | v5_target | 300 | 0.917016 | 0.039648 |
| v52_weighted_fvt_conv5way_step22000 | roundtrip_src_pivot | all | 300 | 0.931907 | 0.295205 |
| v52_weighted_fvt_conv5way_step22000 | roundtrip_src_pivot | v5_target | 300 | 0.931907 | 0.295205 |
| v52_weighted_fvt_conv5way_step22000 | same_language_bible_adjacent | all | 300 | 0.977997 | 0.757678 |
| v52_weighted_fvt_conv5way_step22000 | same_language_bible_adjacent | v5_target | 300 | 0.977997 | 0.757678 |
| v52_weighted_fvt_conv5way_step22000 | same_language_tatoeba_adjacent | all | 300 | 0.943853 | 0.368428 |
| v52_weighted_fvt_conv5way_step22000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943853 | 0.368428 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
