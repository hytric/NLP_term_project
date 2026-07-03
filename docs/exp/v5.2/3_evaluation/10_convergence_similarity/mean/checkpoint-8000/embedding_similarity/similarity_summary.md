# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step8000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step8000 | aligned_bible_src_eng | all | 300 | 0.914250 | 0.030829 |
| v52_mean_conv5way_step8000 | aligned_bible_src_eng | v5_target | 300 | 0.914250 | 0.030829 |
| v52_mean_conv5way_step8000 | aligned_tatoeba_src_eng | all | 300 | 0.917282 | 0.180035 |
| v52_mean_conv5way_step8000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.917282 | 0.180035 |
| v52_mean_conv5way_step8000 | roundtrip_eng_pivot | all | 300 | 0.912344 | 0.017453 |
| v52_mean_conv5way_step8000 | roundtrip_eng_pivot | v5_target | 300 | 0.912344 | 0.017453 |
| v52_mean_conv5way_step8000 | roundtrip_src_eng | all | 300 | 0.911537 | 0.013673 |
| v52_mean_conv5way_step8000 | roundtrip_src_eng | v5_target | 300 | 0.911537 | 0.013673 |
| v52_mean_conv5way_step8000 | roundtrip_src_pivot | all | 300 | 0.934144 | 0.329489 |
| v52_mean_conv5way_step8000 | roundtrip_src_pivot | v5_target | 300 | 0.934144 | 0.329489 |
| v52_mean_conv5way_step8000 | same_language_bible_adjacent | all | 300 | 0.977701 | 0.751924 |
| v52_mean_conv5way_step8000 | same_language_bible_adjacent | v5_target | 300 | 0.977701 | 0.751924 |
| v52_mean_conv5way_step8000 | same_language_tatoeba_adjacent | all | 300 | 0.940437 | 0.375685 |
| v52_mean_conv5way_step8000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.940437 | 0.375685 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
