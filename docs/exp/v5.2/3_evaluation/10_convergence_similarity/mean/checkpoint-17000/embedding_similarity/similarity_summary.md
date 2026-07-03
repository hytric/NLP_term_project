# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step17000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step17000 | aligned_bible_src_eng | all | 300 | 0.921168 | 0.055718 |
| v52_mean_conv5way_step17000 | aligned_bible_src_eng | v5_target | 300 | 0.921168 | 0.055718 |
| v52_mean_conv5way_step17000 | aligned_tatoeba_src_eng | all | 300 | 0.923151 | 0.198159 |
| v52_mean_conv5way_step17000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.923151 | 0.198159 |
| v52_mean_conv5way_step17000 | roundtrip_eng_pivot | all | 300 | 0.918696 | 0.032712 |
| v52_mean_conv5way_step17000 | roundtrip_eng_pivot | v5_target | 300 | 0.918696 | 0.032712 |
| v52_mean_conv5way_step17000 | roundtrip_src_eng | all | 300 | 0.918704 | 0.035890 |
| v52_mean_conv5way_step17000 | roundtrip_src_eng | v5_target | 300 | 0.918704 | 0.035890 |
| v52_mean_conv5way_step17000 | roundtrip_src_pivot | all | 300 | 0.937002 | 0.315747 |
| v52_mean_conv5way_step17000 | roundtrip_src_pivot | v5_target | 300 | 0.937002 | 0.315747 |
| v52_mean_conv5way_step17000 | same_language_bible_adjacent | all | 300 | 0.978647 | 0.748384 |
| v52_mean_conv5way_step17000 | same_language_bible_adjacent | v5_target | 300 | 0.978647 | 0.748384 |
| v52_mean_conv5way_step17000 | same_language_tatoeba_adjacent | all | 300 | 0.943159 | 0.371848 |
| v52_mean_conv5way_step17000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943159 | 0.371848 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
