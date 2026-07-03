# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_family_mean_conv5way_step48000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_family_mean_conv5way_step48000 | aligned_bible_src_eng | all | 300 | 0.916983 | 0.039499 |
| v52_family_mean_conv5way_step48000 | aligned_bible_src_eng | v5_target | 300 | 0.916983 | 0.039499 |
| v52_family_mean_conv5way_step48000 | aligned_tatoeba_src_eng | all | 300 | 0.926782 | 0.210303 |
| v52_family_mean_conv5way_step48000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.926782 | 0.210303 |
| v52_family_mean_conv5way_step48000 | roundtrip_eng_pivot | all | 300 | 0.914465 | 0.002527 |
| v52_family_mean_conv5way_step48000 | roundtrip_eng_pivot | v5_target | 300 | 0.914465 | 0.002527 |
| v52_family_mean_conv5way_step48000 | roundtrip_src_eng | all | 300 | 0.913700 | 0.017356 |
| v52_family_mean_conv5way_step48000 | roundtrip_src_eng | v5_target | 300 | 0.913700 | 0.017356 |
| v52_family_mean_conv5way_step48000 | roundtrip_src_pivot | all | 300 | 0.935982 | 0.332806 |
| v52_family_mean_conv5way_step48000 | roundtrip_src_pivot | v5_target | 300 | 0.935982 | 0.332806 |
| v52_family_mean_conv5way_step48000 | same_language_bible_adjacent | all | 300 | 0.978569 | 0.764397 |
| v52_family_mean_conv5way_step48000 | same_language_bible_adjacent | v5_target | 300 | 0.978569 | 0.764397 |
| v52_family_mean_conv5way_step48000 | same_language_tatoeba_adjacent | all | 300 | 0.950026 | 0.414935 |
| v52_family_mean_conv5way_step48000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.950026 | 0.414935 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
