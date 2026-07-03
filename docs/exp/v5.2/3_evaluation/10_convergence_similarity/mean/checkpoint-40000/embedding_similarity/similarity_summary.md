# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step40000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step40000 | aligned_bible_src_eng | all | 300 | 0.922518 | 0.054345 |
| v52_mean_conv5way_step40000 | aligned_bible_src_eng | v5_target | 300 | 0.922518 | 0.054345 |
| v52_mean_conv5way_step40000 | aligned_tatoeba_src_eng | all | 300 | 0.925556 | 0.195717 |
| v52_mean_conv5way_step40000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925556 | 0.195717 |
| v52_mean_conv5way_step40000 | roundtrip_eng_pivot | all | 300 | 0.919588 | 0.028832 |
| v52_mean_conv5way_step40000 | roundtrip_eng_pivot | v5_target | 300 | 0.919588 | 0.028832 |
| v52_mean_conv5way_step40000 | roundtrip_src_eng | all | 300 | 0.920144 | 0.034378 |
| v52_mean_conv5way_step40000 | roundtrip_src_eng | v5_target | 300 | 0.920144 | 0.034378 |
| v52_mean_conv5way_step40000 | roundtrip_src_pivot | all | 300 | 0.937851 | 0.314866 |
| v52_mean_conv5way_step40000 | roundtrip_src_pivot | v5_target | 300 | 0.937851 | 0.314866 |
| v52_mean_conv5way_step40000 | same_language_bible_adjacent | all | 300 | 0.979032 | 0.748260 |
| v52_mean_conv5way_step40000 | same_language_bible_adjacent | v5_target | 300 | 0.979032 | 0.748260 |
| v52_mean_conv5way_step40000 | same_language_tatoeba_adjacent | all | 300 | 0.945719 | 0.379592 |
| v52_mean_conv5way_step40000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945719 | 0.379592 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
