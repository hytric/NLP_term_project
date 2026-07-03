# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step19000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step19000 | aligned_bible_src_eng | all | 300 | 0.921081 | 0.051125 |
| v52_mean_conv5way_step19000 | aligned_bible_src_eng | v5_target | 300 | 0.921081 | 0.051125 |
| v52_mean_conv5way_step19000 | aligned_tatoeba_src_eng | all | 300 | 0.923622 | 0.192606 |
| v52_mean_conv5way_step19000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.923622 | 0.192606 |
| v52_mean_conv5way_step19000 | roundtrip_eng_pivot | all | 300 | 0.918296 | 0.025247 |
| v52_mean_conv5way_step19000 | roundtrip_eng_pivot | v5_target | 300 | 0.918296 | 0.025247 |
| v52_mean_conv5way_step19000 | roundtrip_src_eng | all | 300 | 0.918751 | 0.030924 |
| v52_mean_conv5way_step19000 | roundtrip_src_eng | v5_target | 300 | 0.918751 | 0.030924 |
| v52_mean_conv5way_step19000 | roundtrip_src_pivot | all | 300 | 0.937140 | 0.310722 |
| v52_mean_conv5way_step19000 | roundtrip_src_pivot | v5_target | 300 | 0.937140 | 0.310722 |
| v52_mean_conv5way_step19000 | same_language_bible_adjacent | all | 300 | 0.978737 | 0.747180 |
| v52_mean_conv5way_step19000 | same_language_bible_adjacent | v5_target | 300 | 0.978737 | 0.747180 |
| v52_mean_conv5way_step19000 | same_language_tatoeba_adjacent | all | 300 | 0.944591 | 0.377692 |
| v52_mean_conv5way_step19000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944591 | 0.377692 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
