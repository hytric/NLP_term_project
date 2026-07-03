# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step19000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step19000 | aligned_bible_src_eng | all | 300 | 0.920774 | 0.069716 |
| v52_fvt_conv5way_step19000 | aligned_bible_src_eng | v5_target | 300 | 0.920774 | 0.069716 |
| v52_fvt_conv5way_step19000 | aligned_tatoeba_src_eng | all | 300 | 0.925537 | 0.199449 |
| v52_fvt_conv5way_step19000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.925537 | 0.199449 |
| v52_fvt_conv5way_step19000 | roundtrip_eng_pivot | all | 300 | 0.917995 | 0.032316 |
| v52_fvt_conv5way_step19000 | roundtrip_eng_pivot | v5_target | 300 | 0.917995 | 0.032316 |
| v52_fvt_conv5way_step19000 | roundtrip_src_eng | all | 300 | 0.917620 | 0.047069 |
| v52_fvt_conv5way_step19000 | roundtrip_src_eng | v5_target | 300 | 0.917620 | 0.047069 |
| v52_fvt_conv5way_step19000 | roundtrip_src_pivot | all | 300 | 0.933765 | 0.304321 |
| v52_fvt_conv5way_step19000 | roundtrip_src_pivot | v5_target | 300 | 0.933765 | 0.304321 |
| v52_fvt_conv5way_step19000 | same_language_bible_adjacent | all | 300 | 0.978391 | 0.757553 |
| v52_fvt_conv5way_step19000 | same_language_bible_adjacent | v5_target | 300 | 0.978391 | 0.757553 |
| v52_fvt_conv5way_step19000 | same_language_tatoeba_adjacent | all | 300 | 0.946885 | 0.387919 |
| v52_fvt_conv5way_step19000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.946885 | 0.387919 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
