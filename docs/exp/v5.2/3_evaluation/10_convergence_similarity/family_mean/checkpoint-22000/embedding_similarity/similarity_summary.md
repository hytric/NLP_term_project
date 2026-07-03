# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step22000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step22000 | aligned_bible_src_eng | all | 300 | 0.910685 | 0.027059 |
| v52_family_mean_conv5way_step22000 | aligned_bible_src_eng | v5_target | 300 | 0.910685 | 0.027059 |
| v52_family_mean_conv5way_step22000 | aligned_tatoeba_src_eng | all | 300 | 0.917663 | 0.194095 |
| v52_family_mean_conv5way_step22000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.917663 | 0.194095 |
| v52_family_mean_conv5way_step22000 | roundtrip_eng_pivot | all | 300 | 0.910735 | 0.001914 |
| v52_family_mean_conv5way_step22000 | roundtrip_eng_pivot | v5_target | 300 | 0.910735 | 0.001914 |
| v52_family_mean_conv5way_step22000 | roundtrip_src_eng | all | 300 | 0.907139 | 0.003240 |
| v52_family_mean_conv5way_step22000 | roundtrip_src_eng | v5_target | 300 | 0.907139 | 0.003240 |
| v52_family_mean_conv5way_step22000 | roundtrip_src_pivot | all | 300 | 0.936382 | 0.356433 |
| v52_family_mean_conv5way_step22000 | roundtrip_src_pivot | v5_target | 300 | 0.936382 | 0.356433 |
| v52_family_mean_conv5way_step22000 | same_language_bible_adjacent | all | 300 | 0.977226 | 0.763429 |
| v52_family_mean_conv5way_step22000 | same_language_bible_adjacent | v5_target | 300 | 0.977226 | 0.763429 |
| v52_family_mean_conv5way_step22000 | same_language_tatoeba_adjacent | all | 300 | 0.944746 | 0.407357 |
| v52_family_mean_conv5way_step22000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944746 | 0.407357 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
