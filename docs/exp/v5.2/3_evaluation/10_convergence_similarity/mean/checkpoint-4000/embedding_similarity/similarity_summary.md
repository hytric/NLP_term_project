# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step4000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step4000 | aligned_bible_src_eng | all | 300 | 0.916644 | 0.026644 |
| v52_mean_conv5way_step4000 | aligned_bible_src_eng | v5_target | 300 | 0.916644 | 0.026644 |
| v52_mean_conv5way_step4000 | aligned_tatoeba_src_eng | all | 300 | 0.916233 | 0.159050 |
| v52_mean_conv5way_step4000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.916233 | 0.159050 |
| v52_mean_conv5way_step4000 | roundtrip_eng_pivot | all | 300 | 0.914211 | 0.010171 |
| v52_mean_conv5way_step4000 | roundtrip_eng_pivot | v5_target | 300 | 0.914211 | 0.010171 |
| v52_mean_conv5way_step4000 | roundtrip_src_eng | all | 300 | 0.914086 | 0.009732 |
| v52_mean_conv5way_step4000 | roundtrip_src_eng | v5_target | 300 | 0.914086 | 0.009732 |
| v52_mean_conv5way_step4000 | roundtrip_src_pivot | all | 300 | 0.941632 | 0.354573 |
| v52_mean_conv5way_step4000 | roundtrip_src_pivot | v5_target | 300 | 0.941632 | 0.354573 |
| v52_mean_conv5way_step4000 | same_language_bible_adjacent | all | 300 | 0.978477 | 0.743238 |
| v52_mean_conv5way_step4000 | same_language_bible_adjacent | v5_target | 300 | 0.978477 | 0.743238 |
| v52_mean_conv5way_step4000 | same_language_tatoeba_adjacent | all | 300 | 0.940845 | 0.360745 |
| v52_mean_conv5way_step4000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.940845 | 0.360745 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
