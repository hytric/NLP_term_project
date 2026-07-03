# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step41000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step41000 | aligned_bible_src_eng | all | 300 | 0.917683 | 0.047524 |
| v52_family_mean_conv5way_step41000 | aligned_bible_src_eng | v5_target | 300 | 0.917683 | 0.047524 |
| v52_family_mean_conv5way_step41000 | aligned_tatoeba_src_eng | all | 300 | 0.926476 | 0.215156 |
| v52_family_mean_conv5way_step41000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926476 | 0.215156 |
| v52_family_mean_conv5way_step41000 | roundtrip_eng_pivot | all | 300 | 0.915372 | 0.011312 |
| v52_family_mean_conv5way_step41000 | roundtrip_eng_pivot | v5_target | 300 | 0.915372 | 0.011312 |
| v52_family_mean_conv5way_step41000 | roundtrip_src_eng | all | 300 | 0.914461 | 0.025903 |
| v52_family_mean_conv5way_step41000 | roundtrip_src_eng | v5_target | 300 | 0.914461 | 0.025903 |
| v52_family_mean_conv5way_step41000 | roundtrip_src_pivot | all | 300 | 0.937113 | 0.343305 |
| v52_family_mean_conv5way_step41000 | roundtrip_src_pivot | v5_target | 300 | 0.937113 | 0.343305 |
| v52_family_mean_conv5way_step41000 | same_language_bible_adjacent | all | 300 | 0.978483 | 0.763582 |
| v52_family_mean_conv5way_step41000 | same_language_bible_adjacent | v5_target | 300 | 0.978483 | 0.763582 |
| v52_family_mean_conv5way_step41000 | same_language_tatoeba_adjacent | all | 300 | 0.949274 | 0.414489 |
| v52_family_mean_conv5way_step41000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.949274 | 0.414489 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
