# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step15000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step15000 | aligned_bible_src_eng | all | 300 | 0.920035 | 0.048103 |
| v52_mean_conv5way_step15000 | aligned_bible_src_eng | v5_target | 300 | 0.920035 | 0.048103 |
| v52_mean_conv5way_step15000 | aligned_tatoeba_src_eng | all | 300 | 0.922198 | 0.195656 |
| v52_mean_conv5way_step15000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922198 | 0.195656 |
| v52_mean_conv5way_step15000 | roundtrip_eng_pivot | all | 300 | 0.917212 | 0.024825 |
| v52_mean_conv5way_step15000 | roundtrip_eng_pivot | v5_target | 300 | 0.917212 | 0.024825 |
| v52_mean_conv5way_step15000 | roundtrip_src_eng | all | 300 | 0.917473 | 0.030020 |
| v52_mean_conv5way_step15000 | roundtrip_src_eng | v5_target | 300 | 0.917473 | 0.030020 |
| v52_mean_conv5way_step15000 | roundtrip_src_pivot | all | 300 | 0.936576 | 0.317428 |
| v52_mean_conv5way_step15000 | roundtrip_src_pivot | v5_target | 300 | 0.936576 | 0.317428 |
| v52_mean_conv5way_step15000 | same_language_bible_adjacent | all | 300 | 0.978686 | 0.749658 |
| v52_mean_conv5way_step15000 | same_language_bible_adjacent | v5_target | 300 | 0.978686 | 0.749658 |
| v52_mean_conv5way_step15000 | same_language_tatoeba_adjacent | all | 300 | 0.942658 | 0.371844 |
| v52_mean_conv5way_step15000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.942658 | 0.371844 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
