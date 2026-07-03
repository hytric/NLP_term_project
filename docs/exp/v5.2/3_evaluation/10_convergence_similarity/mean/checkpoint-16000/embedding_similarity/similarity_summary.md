# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step16000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step16000 | aligned_bible_src_eng | all | 300 | 0.919263 | 0.051604 |
| v52_mean_conv5way_step16000 | aligned_bible_src_eng | v5_target | 300 | 0.919263 | 0.051604 |
| v52_mean_conv5way_step16000 | aligned_tatoeba_src_eng | all | 300 | 0.923698 | 0.202785 |
| v52_mean_conv5way_step16000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.923698 | 0.202785 |
| v52_mean_conv5way_step16000 | roundtrip_eng_pivot | all | 300 | 0.917056 | 0.029859 |
| v52_mean_conv5way_step16000 | roundtrip_eng_pivot | v5_target | 300 | 0.917056 | 0.029859 |
| v52_mean_conv5way_step16000 | roundtrip_src_eng | all | 300 | 0.916834 | 0.033175 |
| v52_mean_conv5way_step16000 | roundtrip_src_eng | v5_target | 300 | 0.916834 | 0.033175 |
| v52_mean_conv5way_step16000 | roundtrip_src_pivot | all | 300 | 0.936268 | 0.316397 |
| v52_mean_conv5way_step16000 | roundtrip_src_pivot | v5_target | 300 | 0.936268 | 0.316397 |
| v52_mean_conv5way_step16000 | same_language_bible_adjacent | all | 300 | 0.978481 | 0.750659 |
| v52_mean_conv5way_step16000 | same_language_bible_adjacent | v5_target | 300 | 0.978481 | 0.750659 |
| v52_mean_conv5way_step16000 | same_language_tatoeba_adjacent | all | 300 | 0.943270 | 0.374017 |
| v52_mean_conv5way_step16000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943270 | 0.374017 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
