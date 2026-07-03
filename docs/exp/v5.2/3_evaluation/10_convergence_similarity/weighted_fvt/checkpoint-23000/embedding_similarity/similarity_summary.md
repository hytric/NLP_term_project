# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step23000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step23000 | aligned_bible_src_eng | all | 300 | 0.923051 | 0.076797 |
| v52_weighted_fvt_conv5way_step23000 | aligned_bible_src_eng | v5_target | 300 | 0.923051 | 0.076797 |
| v52_weighted_fvt_conv5way_step23000 | aligned_tatoeba_src_eng | all | 300 | 0.924994 | 0.205442 |
| v52_weighted_fvt_conv5way_step23000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.924994 | 0.205442 |
| v52_weighted_fvt_conv5way_step23000 | roundtrip_eng_pivot | all | 300 | 0.919784 | 0.034570 |
| v52_weighted_fvt_conv5way_step23000 | roundtrip_eng_pivot | v5_target | 300 | 0.919784 | 0.034570 |
| v52_weighted_fvt_conv5way_step23000 | roundtrip_src_eng | all | 300 | 0.920132 | 0.055152 |
| v52_weighted_fvt_conv5way_step23000 | roundtrip_src_eng | v5_target | 300 | 0.920132 | 0.055152 |
| v52_weighted_fvt_conv5way_step23000 | roundtrip_src_pivot | all | 300 | 0.934547 | 0.297343 |
| v52_weighted_fvt_conv5way_step23000 | roundtrip_src_pivot | v5_target | 300 | 0.934547 | 0.297343 |
| v52_weighted_fvt_conv5way_step23000 | same_language_bible_adjacent | all | 300 | 0.978238 | 0.751810 |
| v52_weighted_fvt_conv5way_step23000 | same_language_bible_adjacent | v5_target | 300 | 0.978238 | 0.751810 |
| v52_weighted_fvt_conv5way_step23000 | same_language_tatoeba_adjacent | all | 300 | 0.944566 | 0.370745 |
| v52_weighted_fvt_conv5way_step23000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944566 | 0.370745 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
