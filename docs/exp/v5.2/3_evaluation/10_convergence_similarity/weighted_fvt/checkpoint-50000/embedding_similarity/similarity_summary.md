# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step50000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step50000 | aligned_bible_src_eng | all | 300 | 0.922629 | 0.061123 |
| v52_weighted_fvt_conv5way_step50000 | aligned_bible_src_eng | v5_target | 300 | 0.922629 | 0.061123 |
| v52_weighted_fvt_conv5way_step50000 | aligned_tatoeba_src_eng | all | 300 | 0.927035 | 0.208761 |
| v52_weighted_fvt_conv5way_step50000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.927035 | 0.208761 |
| v52_weighted_fvt_conv5way_step50000 | roundtrip_eng_pivot | all | 300 | 0.918847 | 0.014620 |
| v52_weighted_fvt_conv5way_step50000 | roundtrip_eng_pivot | v5_target | 300 | 0.918847 | 0.014620 |
| v52_weighted_fvt_conv5way_step50000 | roundtrip_src_eng | all | 300 | 0.919662 | 0.039386 |
| v52_weighted_fvt_conv5way_step50000 | roundtrip_src_eng | v5_target | 300 | 0.919662 | 0.039386 |
| v52_weighted_fvt_conv5way_step50000 | roundtrip_src_pivot | all | 300 | 0.933861 | 0.291908 |
| v52_weighted_fvt_conv5way_step50000 | roundtrip_src_pivot | v5_target | 300 | 0.933861 | 0.291908 |
| v52_weighted_fvt_conv5way_step50000 | same_language_bible_adjacent | all | 300 | 0.978829 | 0.758805 |
| v52_weighted_fvt_conv5way_step50000 | same_language_bible_adjacent | v5_target | 300 | 0.978829 | 0.758805 |
| v52_weighted_fvt_conv5way_step50000 | same_language_tatoeba_adjacent | all | 300 | 0.945517 | 0.370989 |
| v52_weighted_fvt_conv5way_step50000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945517 | 0.370989 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
