# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step14000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step14000 | aligned_bible_src_eng | all | 300 | 0.918053 | 0.037945 |
| v52_mean_conv5way_step14000 | aligned_bible_src_eng | v5_target | 300 | 0.918053 | 0.037945 |
| v52_mean_conv5way_step14000 | aligned_tatoeba_src_eng | all | 300 | 0.921539 | 0.190489 |
| v52_mean_conv5way_step14000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.921539 | 0.190489 |
| v52_mean_conv5way_step14000 | roundtrip_eng_pivot | all | 300 | 0.915505 | 0.017058 |
| v52_mean_conv5way_step14000 | roundtrip_eng_pivot | v5_target | 300 | 0.915505 | 0.017058 |
| v52_mean_conv5way_step14000 | roundtrip_src_eng | all | 300 | 0.915495 | 0.018587 |
| v52_mean_conv5way_step14000 | roundtrip_src_eng | v5_target | 300 | 0.915495 | 0.018587 |
| v52_mean_conv5way_step14000 | roundtrip_src_pivot | all | 300 | 0.935657 | 0.319676 |
| v52_mean_conv5way_step14000 | roundtrip_src_pivot | v5_target | 300 | 0.935657 | 0.319676 |
| v52_mean_conv5way_step14000 | same_language_bible_adjacent | all | 300 | 0.978216 | 0.748754 |
| v52_mean_conv5way_step14000 | same_language_bible_adjacent | v5_target | 300 | 0.978216 | 0.748754 |
| v52_mean_conv5way_step14000 | same_language_tatoeba_adjacent | all | 300 | 0.943047 | 0.373717 |
| v52_mean_conv5way_step14000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943047 | 0.373717 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
