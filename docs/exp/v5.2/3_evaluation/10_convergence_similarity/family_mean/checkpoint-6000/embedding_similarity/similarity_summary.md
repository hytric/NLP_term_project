# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step6000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step6000 | aligned_bible_src_eng | all | 300 | 0.906279 | -0.030162 |
| v52_family_mean_conv5way_step6000 | aligned_bible_src_eng | v5_target | 300 | 0.906279 | -0.030162 |
| v52_family_mean_conv5way_step6000 | aligned_tatoeba_src_eng | all | 300 | 0.911624 | 0.154205 |
| v52_family_mean_conv5way_step6000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.911624 | 0.154205 |
| v52_family_mean_conv5way_step6000 | roundtrip_eng_pivot | all | 300 | 0.908266 | -0.042730 |
| v52_family_mean_conv5way_step6000 | roundtrip_eng_pivot | v5_target | 300 | 0.908266 | -0.042730 |
| v52_family_mean_conv5way_step6000 | roundtrip_src_eng | all | 300 | 0.902609 | -0.051193 |
| v52_family_mean_conv5way_step6000 | roundtrip_src_eng | v5_target | 300 | 0.902609 | -0.051193 |
| v52_family_mean_conv5way_step6000 | roundtrip_src_pivot | all | 300 | 0.940777 | 0.388775 |
| v52_family_mean_conv5way_step6000 | roundtrip_src_pivot | v5_target | 300 | 0.940777 | 0.388775 |
| v52_family_mean_conv5way_step6000 | same_language_bible_adjacent | all | 300 | 0.977155 | 0.761795 |
| v52_family_mean_conv5way_step6000 | same_language_bible_adjacent | v5_target | 300 | 0.977155 | 0.761795 |
| v52_family_mean_conv5way_step6000 | same_language_tatoeba_adjacent | all | 300 | 0.945592 | 0.410292 |
| v52_family_mean_conv5way_step6000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945592 | 0.410292 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
