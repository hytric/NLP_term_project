# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step27000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step27000 | aligned_bible_src_eng | all | 300 | 0.920930 | 0.067872 |
| v52_weighted_fvt_conv5way_step27000 | aligned_bible_src_eng | v5_target | 300 | 0.920930 | 0.067872 |
| v52_weighted_fvt_conv5way_step27000 | aligned_tatoeba_src_eng | all | 300 | 0.925229 | 0.206071 |
| v52_weighted_fvt_conv5way_step27000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925229 | 0.206071 |
| v52_weighted_fvt_conv5way_step27000 | roundtrip_eng_pivot | all | 300 | 0.917989 | 0.027188 |
| v52_weighted_fvt_conv5way_step27000 | roundtrip_eng_pivot | v5_target | 300 | 0.917989 | 0.027188 |
| v52_weighted_fvt_conv5way_step27000 | roundtrip_src_eng | all | 300 | 0.917836 | 0.045573 |
| v52_weighted_fvt_conv5way_step27000 | roundtrip_src_eng | v5_target | 300 | 0.917836 | 0.045573 |
| v52_weighted_fvt_conv5way_step27000 | roundtrip_src_pivot | all | 300 | 0.932301 | 0.291278 |
| v52_weighted_fvt_conv5way_step27000 | roundtrip_src_pivot | v5_target | 300 | 0.932301 | 0.291278 |
| v52_weighted_fvt_conv5way_step27000 | same_language_bible_adjacent | all | 300 | 0.977993 | 0.755703 |
| v52_weighted_fvt_conv5way_step27000 | same_language_bible_adjacent | v5_target | 300 | 0.977993 | 0.755703 |
| v52_weighted_fvt_conv5way_step27000 | same_language_tatoeba_adjacent | all | 300 | 0.944668 | 0.372033 |
| v52_weighted_fvt_conv5way_step27000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944668 | 0.372033 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
