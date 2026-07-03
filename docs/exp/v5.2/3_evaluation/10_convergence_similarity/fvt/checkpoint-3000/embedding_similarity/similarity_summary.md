# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_fvt_conv5way_step3000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_fvt_conv5way_step3000 | aligned_bible_src_eng | all | 300 | 0.914912 | 0.038952 |
| v52_fvt_conv5way_step3000 | aligned_bible_src_eng | v5_target | 300 | 0.914912 | 0.038952 |
| v52_fvt_conv5way_step3000 | aligned_tatoeba_src_eng | all | 300 | 0.912897 | 0.158665 |
| v52_fvt_conv5way_step3000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.912897 | 0.158665 |
| v52_fvt_conv5way_step3000 | roundtrip_eng_pivot | all | 300 | 0.913782 | 0.012412 |
| v52_fvt_conv5way_step3000 | roundtrip_eng_pivot | v5_target | 300 | 0.913782 | 0.012412 |
| v52_fvt_conv5way_step3000 | roundtrip_src_eng | all | 300 | 0.911889 | 0.016790 |
| v52_fvt_conv5way_step3000 | roundtrip_src_eng | v5_target | 300 | 0.911889 | 0.016790 |
| v52_fvt_conv5way_step3000 | roundtrip_src_pivot | all | 300 | 0.936199 | 0.341895 |
| v52_fvt_conv5way_step3000 | roundtrip_src_pivot | v5_target | 300 | 0.936199 | 0.341895 |
| v52_fvt_conv5way_step3000 | same_language_bible_adjacent | all | 300 | 0.976712 | 0.747554 |
| v52_fvt_conv5way_step3000 | same_language_bible_adjacent | v5_target | 300 | 0.976712 | 0.747554 |
| v52_fvt_conv5way_step3000 | same_language_tatoeba_adjacent | all | 300 | 0.939682 | 0.369849 |
| v52_fvt_conv5way_step3000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.939682 | 0.369849 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
