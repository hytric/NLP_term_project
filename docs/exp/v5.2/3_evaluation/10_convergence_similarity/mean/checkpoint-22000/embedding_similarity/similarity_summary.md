# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step22000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step22000 | aligned_bible_src_eng | all | 300 | 0.921778 | 0.053086 |
| v52_mean_conv5way_step22000 | aligned_bible_src_eng | v5_target | 300 | 0.921778 | 0.053086 |
| v52_mean_conv5way_step22000 | aligned_tatoeba_src_eng | all | 300 | 0.924536 | 0.193965 |
| v52_mean_conv5way_step22000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.924536 | 0.193965 |
| v52_mean_conv5way_step22000 | roundtrip_eng_pivot | all | 300 | 0.918842 | 0.026884 |
| v52_mean_conv5way_step22000 | roundtrip_eng_pivot | v5_target | 300 | 0.918842 | 0.026884 |
| v52_mean_conv5way_step22000 | roundtrip_src_eng | all | 300 | 0.919404 | 0.032654 |
| v52_mean_conv5way_step22000 | roundtrip_src_eng | v5_target | 300 | 0.919404 | 0.032654 |
| v52_mean_conv5way_step22000 | roundtrip_src_pivot | all | 300 | 0.937283 | 0.313109 |
| v52_mean_conv5way_step22000 | roundtrip_src_pivot | v5_target | 300 | 0.937283 | 0.313109 |
| v52_mean_conv5way_step22000 | same_language_bible_adjacent | all | 300 | 0.978870 | 0.748018 |
| v52_mean_conv5way_step22000 | same_language_bible_adjacent | v5_target | 300 | 0.978870 | 0.748018 |
| v52_mean_conv5way_step22000 | same_language_tatoeba_adjacent | all | 300 | 0.945129 | 0.379399 |
| v52_mean_conv5way_step22000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945129 | 0.379399 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
