# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step40000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step40000 | aligned_bible_src_eng | all | 300 | 0.922304 | 0.057605 |
| v52_weighted_fvt_conv5way_step40000 | aligned_bible_src_eng | v5_target | 300 | 0.922304 | 0.057605 |
| v52_weighted_fvt_conv5way_step40000 | aligned_tatoeba_src_eng | all | 300 | 0.925582 | 0.204103 |
| v52_weighted_fvt_conv5way_step40000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925582 | 0.204103 |
| v52_weighted_fvt_conv5way_step40000 | roundtrip_eng_pivot | all | 300 | 0.918992 | 0.013582 |
| v52_weighted_fvt_conv5way_step40000 | roundtrip_eng_pivot | v5_target | 300 | 0.918992 | 0.013582 |
| v52_weighted_fvt_conv5way_step40000 | roundtrip_src_eng | all | 300 | 0.919350 | 0.036559 |
| v52_weighted_fvt_conv5way_step40000 | roundtrip_src_eng | v5_target | 300 | 0.919350 | 0.036559 |
| v52_weighted_fvt_conv5way_step40000 | roundtrip_src_pivot | all | 300 | 0.934620 | 0.296551 |
| v52_weighted_fvt_conv5way_step40000 | roundtrip_src_pivot | v5_target | 300 | 0.934620 | 0.296551 |
| v52_weighted_fvt_conv5way_step40000 | same_language_bible_adjacent | all | 300 | 0.978671 | 0.756717 |
| v52_weighted_fvt_conv5way_step40000 | same_language_bible_adjacent | v5_target | 300 | 0.978671 | 0.756717 |
| v52_weighted_fvt_conv5way_step40000 | same_language_tatoeba_adjacent | all | 300 | 0.944806 | 0.370101 |
| v52_weighted_fvt_conv5way_step40000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944806 | 0.370101 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
