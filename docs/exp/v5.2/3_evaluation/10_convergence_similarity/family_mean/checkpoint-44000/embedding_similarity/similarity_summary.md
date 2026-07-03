# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step44000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step44000 | aligned_bible_src_eng | all | 300 | 0.915522 | 0.040027 |
| v52_family_mean_conv5way_step44000 | aligned_bible_src_eng | v5_target | 300 | 0.915522 | 0.040027 |
| v52_family_mean_conv5way_step44000 | aligned_tatoeba_src_eng | all | 300 | 0.924357 | 0.208163 |
| v52_family_mean_conv5way_step44000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.924357 | 0.208163 |
| v52_family_mean_conv5way_step44000 | roundtrip_eng_pivot | all | 300 | 0.913031 | 0.002874 |
| v52_family_mean_conv5way_step44000 | roundtrip_eng_pivot | v5_target | 300 | 0.913031 | 0.002874 |
| v52_family_mean_conv5way_step44000 | roundtrip_src_eng | all | 300 | 0.912222 | 0.017468 |
| v52_family_mean_conv5way_step44000 | roundtrip_src_eng | v5_target | 300 | 0.912222 | 0.017468 |
| v52_family_mean_conv5way_step44000 | roundtrip_src_pivot | all | 300 | 0.935791 | 0.336405 |
| v52_family_mean_conv5way_step44000 | roundtrip_src_pivot | v5_target | 300 | 0.935791 | 0.336405 |
| v52_family_mean_conv5way_step44000 | same_language_bible_adjacent | all | 300 | 0.978132 | 0.762061 |
| v52_family_mean_conv5way_step44000 | same_language_bible_adjacent | v5_target | 300 | 0.978132 | 0.762061 |
| v52_family_mean_conv5way_step44000 | same_language_tatoeba_adjacent | all | 300 | 0.948252 | 0.413490 |
| v52_family_mean_conv5way_step44000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.948252 | 0.413490 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
