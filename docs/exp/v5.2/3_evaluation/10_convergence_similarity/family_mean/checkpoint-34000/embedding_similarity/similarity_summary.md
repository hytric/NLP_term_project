# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step34000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step34000 | aligned_bible_src_eng | all | 300 | 0.913874 | 0.029990 |
| v52_family_mean_conv5way_step34000 | aligned_bible_src_eng | v5_target | 300 | 0.913874 | 0.029990 |
| v52_family_mean_conv5way_step34000 | aligned_tatoeba_src_eng | all | 300 | 0.924154 | 0.212035 |
| v52_family_mean_conv5way_step34000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.924154 | 0.212035 |
| v52_family_mean_conv5way_step34000 | roundtrip_eng_pivot | all | 300 | 0.911705 | -0.007004 |
| v52_family_mean_conv5way_step34000 | roundtrip_eng_pivot | v5_target | 300 | 0.911705 | -0.007004 |
| v52_family_mean_conv5way_step34000 | roundtrip_src_eng | all | 300 | 0.910559 | 0.007456 |
| v52_family_mean_conv5way_step34000 | roundtrip_src_eng | v5_target | 300 | 0.910559 | 0.007456 |
| v52_family_mean_conv5way_step34000 | roundtrip_src_pivot | all | 300 | 0.935458 | 0.336606 |
| v52_family_mean_conv5way_step34000 | roundtrip_src_pivot | v5_target | 300 | 0.935458 | 0.336606 |
| v52_family_mean_conv5way_step34000 | same_language_bible_adjacent | all | 300 | 0.978105 | 0.764534 |
| v52_family_mean_conv5way_step34000 | same_language_bible_adjacent | v5_target | 300 | 0.978105 | 0.764534 |
| v52_family_mean_conv5way_step34000 | same_language_tatoeba_adjacent | all | 300 | 0.947796 | 0.407870 |
| v52_family_mean_conv5way_step34000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947796 | 0.407870 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
