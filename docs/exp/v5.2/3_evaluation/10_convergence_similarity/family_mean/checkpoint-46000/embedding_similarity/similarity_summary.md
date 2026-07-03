# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step46000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step46000 | aligned_bible_src_eng | all | 300 | 0.917099 | 0.041817 |
| v52_family_mean_conv5way_step46000 | aligned_bible_src_eng | v5_target | 300 | 0.917099 | 0.041817 |
| v52_family_mean_conv5way_step46000 | aligned_tatoeba_src_eng | all | 300 | 0.926057 | 0.209320 |
| v52_family_mean_conv5way_step46000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926057 | 0.209320 |
| v52_family_mean_conv5way_step46000 | roundtrip_eng_pivot | all | 300 | 0.914749 | 0.005554 |
| v52_family_mean_conv5way_step46000 | roundtrip_eng_pivot | v5_target | 300 | 0.914749 | 0.005554 |
| v52_family_mean_conv5way_step46000 | roundtrip_src_eng | all | 300 | 0.913798 | 0.019699 |
| v52_family_mean_conv5way_step46000 | roundtrip_src_eng | v5_target | 300 | 0.913798 | 0.019699 |
| v52_family_mean_conv5way_step46000 | roundtrip_src_pivot | all | 300 | 0.936693 | 0.337815 |
| v52_family_mean_conv5way_step46000 | roundtrip_src_pivot | v5_target | 300 | 0.936693 | 0.337815 |
| v52_family_mean_conv5way_step46000 | same_language_bible_adjacent | all | 300 | 0.978519 | 0.762982 |
| v52_family_mean_conv5way_step46000 | same_language_bible_adjacent | v5_target | 300 | 0.978519 | 0.762982 |
| v52_family_mean_conv5way_step46000 | same_language_tatoeba_adjacent | all | 300 | 0.949628 | 0.414047 |
| v52_family_mean_conv5way_step46000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.949628 | 0.414047 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
