# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step10000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step10000 | aligned_bible_src_eng | all | 300 | 0.901754 | -0.029308 |
| v52_family_mean_conv5way_step10000 | aligned_bible_src_eng | v5_target | 300 | 0.901754 | -0.029308 |
| v52_family_mean_conv5way_step10000 | aligned_tatoeba_src_eng | all | 300 | 0.913049 | 0.170350 |
| v52_family_mean_conv5way_step10000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.913049 | 0.170350 |
| v52_family_mean_conv5way_step10000 | roundtrip_eng_pivot | all | 300 | 0.904139 | -0.040722 |
| v52_family_mean_conv5way_step10000 | roundtrip_eng_pivot | v5_target | 300 | 0.904139 | -0.040722 |
| v52_family_mean_conv5way_step10000 | roundtrip_src_eng | all | 300 | 0.897916 | -0.047831 |
| v52_family_mean_conv5way_step10000 | roundtrip_src_eng | v5_target | 300 | 0.897916 | -0.047831 |
| v52_family_mean_conv5way_step10000 | roundtrip_src_pivot | all | 300 | 0.936399 | 0.382965 |
| v52_family_mean_conv5way_step10000 | roundtrip_src_pivot | v5_target | 300 | 0.936399 | 0.382965 |
| v52_family_mean_conv5way_step10000 | same_language_bible_adjacent | all | 300 | 0.976029 | 0.760868 |
| v52_family_mean_conv5way_step10000 | same_language_bible_adjacent | v5_target | 300 | 0.976029 | 0.760868 |
| v52_family_mean_conv5way_step10000 | same_language_tatoeba_adjacent | all | 300 | 0.943511 | 0.411146 |
| v52_family_mean_conv5way_step10000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.943511 | 0.411146 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
