# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_weighted_fvt_conv5way_step29000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_weighted_fvt_conv5way_step29000 | aligned_bible_src_eng | all | 300 | 0.921097 | 0.070367 |
| v52_weighted_fvt_conv5way_step29000 | aligned_bible_src_eng | v5_target | 300 | 0.921097 | 0.070367 |
| v52_weighted_fvt_conv5way_step29000 | aligned_tatoeba_src_eng | all | 300 | 0.925124 | 0.206493 |
| v52_weighted_fvt_conv5way_step29000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925124 | 0.206493 |
| v52_weighted_fvt_conv5way_step29000 | roundtrip_eng_pivot | all | 300 | 0.917788 | 0.025766 |
| v52_weighted_fvt_conv5way_step29000 | roundtrip_eng_pivot | v5_target | 300 | 0.917788 | 0.025766 |
| v52_weighted_fvt_conv5way_step29000 | roundtrip_src_eng | all | 300 | 0.918007 | 0.047693 |
| v52_weighted_fvt_conv5way_step29000 | roundtrip_src_eng | v5_target | 300 | 0.918007 | 0.047693 |
| v52_weighted_fvt_conv5way_step29000 | roundtrip_src_pivot | all | 300 | 0.934179 | 0.304428 |
| v52_weighted_fvt_conv5way_step29000 | roundtrip_src_pivot | v5_target | 300 | 0.934179 | 0.304428 |
| v52_weighted_fvt_conv5way_step29000 | same_language_bible_adjacent | all | 300 | 0.978515 | 0.759965 |
| v52_weighted_fvt_conv5way_step29000 | same_language_bible_adjacent | v5_target | 300 | 0.978515 | 0.759965 |
| v52_weighted_fvt_conv5way_step29000 | same_language_tatoeba_adjacent | all | 300 | 0.945000 | 0.374397 |
| v52_weighted_fvt_conv5way_step29000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.945000 | 0.374397 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
