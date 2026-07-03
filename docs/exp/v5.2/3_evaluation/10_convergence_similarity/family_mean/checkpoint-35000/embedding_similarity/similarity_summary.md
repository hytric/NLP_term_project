# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step35000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step35000 | aligned_bible_src_eng | all | 300 | 0.914567 | 0.040721 |
| v52_family_mean_conv5way_step35000 | aligned_bible_src_eng | v5_target | 300 | 0.914567 | 0.040721 |
| v52_family_mean_conv5way_step35000 | aligned_tatoeba_src_eng | all | 300 | 0.923420 | 0.207074 |
| v52_family_mean_conv5way_step35000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.923420 | 0.207074 |
| v52_family_mean_conv5way_step35000 | roundtrip_eng_pivot | all | 300 | 0.913369 | 0.009216 |
| v52_family_mean_conv5way_step35000 | roundtrip_eng_pivot | v5_target | 300 | 0.913369 | 0.009216 |
| v52_family_mean_conv5way_step35000 | roundtrip_src_eng | all | 300 | 0.911344 | 0.018122 |
| v52_family_mean_conv5way_step35000 | roundtrip_src_eng | v5_target | 300 | 0.911344 | 0.018122 |
| v52_family_mean_conv5way_step35000 | roundtrip_src_pivot | all | 300 | 0.934802 | 0.324634 |
| v52_family_mean_conv5way_step35000 | roundtrip_src_pivot | v5_target | 300 | 0.934802 | 0.324634 |
| v52_family_mean_conv5way_step35000 | same_language_bible_adjacent | all | 300 | 0.977850 | 0.760253 |
| v52_family_mean_conv5way_step35000 | same_language_bible_adjacent | v5_target | 300 | 0.977850 | 0.760253 |
| v52_family_mean_conv5way_step35000 | same_language_tatoeba_adjacent | all | 300 | 0.947922 | 0.411204 |
| v52_family_mean_conv5way_step35000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.947922 | 0.411204 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
