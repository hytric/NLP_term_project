# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step1000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step1000 | aligned_bible_src_eng | all | 300 | 0.895922 | -0.087897 |
| v52_family_mean_conv5way_step1000 | aligned_bible_src_eng | v5_target | 300 | 0.895922 | -0.087897 |
| v52_family_mean_conv5way_step1000 | aligned_tatoeba_src_eng | all | 300 | 0.905907 | 0.128820 |
| v52_family_mean_conv5way_step1000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.905907 | 0.128820 |
| v52_family_mean_conv5way_step1000 | roundtrip_eng_pivot | all | 300 | 0.904949 | -0.080989 |
| v52_family_mean_conv5way_step1000 | roundtrip_eng_pivot | v5_target | 300 | 0.904949 | -0.080989 |
| v52_family_mean_conv5way_step1000 | roundtrip_src_eng | all | 300 | 0.890867 | -0.112535 |
| v52_family_mean_conv5way_step1000 | roundtrip_src_eng | v5_target | 300 | 0.890867 | -0.112535 |
| v52_family_mean_conv5way_step1000 | roundtrip_src_pivot | all | 300 | 0.938855 | 0.420351 |
| v52_family_mean_conv5way_step1000 | roundtrip_src_pivot | v5_target | 300 | 0.938855 | 0.420351 |
| v52_family_mean_conv5way_step1000 | same_language_bible_adjacent | all | 300 | 0.975502 | 0.768885 |
| v52_family_mean_conv5way_step1000 | same_language_bible_adjacent | v5_target | 300 | 0.975502 | 0.768885 |
| v52_family_mean_conv5way_step1000 | same_language_tatoeba_adjacent | all | 300 | 0.939710 | 0.386158 |
| v52_family_mean_conv5way_step1000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.939710 | 0.386158 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
