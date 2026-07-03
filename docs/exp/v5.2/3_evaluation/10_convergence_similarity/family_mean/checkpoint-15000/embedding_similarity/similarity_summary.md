# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step15000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step15000 | aligned_bible_src_eng | all | 300 | 0.901362 | -0.012697 |
| v52_family_mean_conv5way_step15000 | aligned_bible_src_eng | v5_target | 300 | 0.901362 | -0.012697 |
| v52_family_mean_conv5way_step15000 | aligned_tatoeba_src_eng | all | 300 | 0.915605 | 0.196652 |
| v52_family_mean_conv5way_step15000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.915605 | 0.196652 |
| v52_family_mean_conv5way_step15000 | roundtrip_eng_pivot | all | 300 | 0.903266 | -0.033067 |
| v52_family_mean_conv5way_step15000 | roundtrip_eng_pivot | v5_target | 300 | 0.903266 | -0.033067 |
| v52_family_mean_conv5way_step15000 | roundtrip_src_eng | all | 300 | 0.897562 | -0.034991 |
| v52_family_mean_conv5way_step15000 | roundtrip_src_eng | v5_target | 300 | 0.897562 | -0.034991 |
| v52_family_mean_conv5way_step15000 | roundtrip_src_pivot | all | 300 | 0.931975 | 0.359259 |
| v52_family_mean_conv5way_step15000 | roundtrip_src_pivot | v5_target | 300 | 0.931975 | 0.359259 |
| v52_family_mean_conv5way_step15000 | same_language_bible_adjacent | all | 300 | 0.976377 | 0.772605 |
| v52_family_mean_conv5way_step15000 | same_language_bible_adjacent | v5_target | 300 | 0.976377 | 0.772605 |
| v52_family_mean_conv5way_step15000 | same_language_tatoeba_adjacent | all | 300 | 0.942564 | 0.404803 |
| v52_family_mean_conv5way_step15000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.942564 | 0.404803 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
