# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step47000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step47000 | aligned_bible_src_eng | all | 300 | 0.917045 | 0.038893 |
| v52_family_mean_conv5way_step47000 | aligned_bible_src_eng | v5_target | 300 | 0.917045 | 0.038893 |
| v52_family_mean_conv5way_step47000 | aligned_tatoeba_src_eng | all | 300 | 0.926559 | 0.210561 |
| v52_family_mean_conv5way_step47000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926559 | 0.210561 |
| v52_family_mean_conv5way_step47000 | roundtrip_eng_pivot | all | 300 | 0.914621 | 0.002013 |
| v52_family_mean_conv5way_step47000 | roundtrip_eng_pivot | v5_target | 300 | 0.914621 | 0.002013 |
| v52_family_mean_conv5way_step47000 | roundtrip_src_eng | all | 300 | 0.913779 | 0.016538 |
| v52_family_mean_conv5way_step47000 | roundtrip_src_eng | v5_target | 300 | 0.913779 | 0.016538 |
| v52_family_mean_conv5way_step47000 | roundtrip_src_pivot | all | 300 | 0.936111 | 0.332511 |
| v52_family_mean_conv5way_step47000 | roundtrip_src_pivot | v5_target | 300 | 0.936111 | 0.332511 |
| v52_family_mean_conv5way_step47000 | same_language_bible_adjacent | all | 300 | 0.978509 | 0.763175 |
| v52_family_mean_conv5way_step47000 | same_language_bible_adjacent | v5_target | 300 | 0.978509 | 0.763175 |
| v52_family_mean_conv5way_step47000 | same_language_tatoeba_adjacent | all | 300 | 0.949792 | 0.413058 |
| v52_family_mean_conv5way_step47000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.949792 | 0.413058 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
