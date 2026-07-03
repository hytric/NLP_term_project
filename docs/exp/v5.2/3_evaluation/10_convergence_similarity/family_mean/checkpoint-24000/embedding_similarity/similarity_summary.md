# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step24000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step24000 | aligned_bible_src_eng | all | 300 | 0.909349 | 0.021400 |
| v52_family_mean_conv5way_step24000 | aligned_bible_src_eng | v5_target | 300 | 0.909349 | 0.021400 |
| v52_family_mean_conv5way_step24000 | aligned_tatoeba_src_eng | all | 300 | 0.917884 | 0.193879 |
| v52_family_mean_conv5way_step24000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.917884 | 0.193879 |
| v52_family_mean_conv5way_step24000 | roundtrip_eng_pivot | all | 300 | 0.908774 | -0.004853 |
| v52_family_mean_conv5way_step24000 | roundtrip_eng_pivot | v5_target | 300 | 0.908774 | -0.004853 |
| v52_family_mean_conv5way_step24000 | roundtrip_src_eng | all | 300 | 0.905868 | -0.001939 |
| v52_family_mean_conv5way_step24000 | roundtrip_src_eng | v5_target | 300 | 0.905868 | -0.001939 |
| v52_family_mean_conv5way_step24000 | roundtrip_src_pivot | all | 300 | 0.935256 | 0.351872 |
| v52_family_mean_conv5way_step24000 | roundtrip_src_pivot | v5_target | 300 | 0.935256 | 0.351872 |
| v52_family_mean_conv5way_step24000 | same_language_bible_adjacent | all | 300 | 0.977653 | 0.767708 |
| v52_family_mean_conv5way_step24000 | same_language_bible_adjacent | v5_target | 300 | 0.977653 | 0.767708 |
| v52_family_mean_conv5way_step24000 | same_language_tatoeba_adjacent | all | 300 | 0.945267 | 0.409379 |
| v52_family_mean_conv5way_step24000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945267 | 0.409379 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
