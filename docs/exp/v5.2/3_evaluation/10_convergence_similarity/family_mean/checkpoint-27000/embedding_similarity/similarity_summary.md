# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step27000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step27000 | aligned_bible_src_eng | all | 300 | 0.913304 | 0.035776 |
| v52_family_mean_conv5way_step27000 | aligned_bible_src_eng | v5_target | 300 | 0.913304 | 0.035776 |
| v52_family_mean_conv5way_step27000 | aligned_tatoeba_src_eng | all | 300 | 0.922024 | 0.210147 |
| v52_family_mean_conv5way_step27000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.922024 | 0.210147 |
| v52_family_mean_conv5way_step27000 | roundtrip_eng_pivot | all | 300 | 0.911732 | 0.001727 |
| v52_family_mean_conv5way_step27000 | roundtrip_eng_pivot | v5_target | 300 | 0.911732 | 0.001727 |
| v52_family_mean_conv5way_step27000 | roundtrip_src_eng | all | 300 | 0.909962 | 0.012601 |
| v52_family_mean_conv5way_step27000 | roundtrip_src_eng | v5_target | 300 | 0.909962 | 0.012601 |
| v52_family_mean_conv5way_step27000 | roundtrip_src_pivot | all | 300 | 0.937099 | 0.353817 |
| v52_family_mean_conv5way_step27000 | roundtrip_src_pivot | v5_target | 300 | 0.937099 | 0.353817 |
| v52_family_mean_conv5way_step27000 | same_language_bible_adjacent | all | 300 | 0.977815 | 0.763255 |
| v52_family_mean_conv5way_step27000 | same_language_bible_adjacent | v5_target | 300 | 0.977815 | 0.763255 |
| v52_family_mean_conv5way_step27000 | same_language_tatoeba_adjacent | all | 300 | 0.946681 | 0.408083 |
| v52_family_mean_conv5way_step27000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.946681 | 0.408083 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
