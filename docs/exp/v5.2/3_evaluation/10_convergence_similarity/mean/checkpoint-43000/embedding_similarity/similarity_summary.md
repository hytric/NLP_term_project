# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step43000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step43000 | aligned_bible_src_eng | all | 300 | 0.922770 | 0.055244 |
| v52_mean_conv5way_step43000 | aligned_bible_src_eng | v5_target | 300 | 0.922770 | 0.055244 |
| v52_mean_conv5way_step43000 | aligned_tatoeba_src_eng | all | 300 | 0.925668 | 0.196170 |
| v52_mean_conv5way_step43000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925668 | 0.196170 |
| v52_mean_conv5way_step43000 | roundtrip_eng_pivot | all | 300 | 0.919831 | 0.029549 |
| v52_mean_conv5way_step43000 | roundtrip_eng_pivot | v5_target | 300 | 0.919831 | 0.029549 |
| v52_mean_conv5way_step43000 | roundtrip_src_eng | all | 300 | 0.920394 | 0.035196 |
| v52_mean_conv5way_step43000 | roundtrip_src_eng | v5_target | 300 | 0.920394 | 0.035196 |
| v52_mean_conv5way_step43000 | roundtrip_src_pivot | all | 300 | 0.937978 | 0.315472 |
| v52_mean_conv5way_step43000 | roundtrip_src_pivot | v5_target | 300 | 0.937978 | 0.315472 |
| v52_mean_conv5way_step43000 | same_language_bible_adjacent | all | 300 | 0.979019 | 0.747771 |
| v52_mean_conv5way_step43000 | same_language_bible_adjacent | v5_target | 300 | 0.979019 | 0.747771 |
| v52_mean_conv5way_step43000 | same_language_tatoeba_adjacent | all | 300 | 0.945801 | 0.379262 |
| v52_mean_conv5way_step43000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945801 | 0.379262 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
