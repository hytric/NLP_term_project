# v5.2 Embedding Similarity Results

- layer index: `7` (Glot500 retrieval convention: 0-indexed layer 8)
- pooling: `mean over non-special tokens`
- max length: `128`
- models: `v52_mean_conv5way_step20000`

| Model | Pair type | Group | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | --- | ---: | ---: | ---: |
| v52_mean_conv5way_step20000 | aligned_bible_src_eng | all | 300 | 0.921177 | 0.051968 |
| v52_mean_conv5way_step20000 | aligned_bible_src_eng | v5_target | 300 | 0.921177 | 0.051968 |
| v52_mean_conv5way_step20000 | aligned_tatoeba_src_eng | all | 300 | 0.924207 | 0.194757 |
| v52_mean_conv5way_step20000 | aligned_tatoeba_src_eng | v5_target | 300 | 0.924207 | 0.194757 |
| v52_mean_conv5way_step20000 | roundtrip_eng_pivot | all | 300 | 0.918230 | 0.025142 |
| v52_mean_conv5way_step20000 | roundtrip_eng_pivot | v5_target | 300 | 0.918230 | 0.025142 |
| v52_mean_conv5way_step20000 | roundtrip_src_eng | all | 300 | 0.918798 | 0.031472 |
| v52_mean_conv5way_step20000 | roundtrip_src_eng | v5_target | 300 | 0.918798 | 0.031472 |
| v52_mean_conv5way_step20000 | roundtrip_src_pivot | all | 300 | 0.937405 | 0.315794 |
| v52_mean_conv5way_step20000 | roundtrip_src_pivot | v5_target | 300 | 0.937405 | 0.315794 |
| v52_mean_conv5way_step20000 | same_language_bible_adjacent | all | 300 | 0.978841 | 0.748582 |
| v52_mean_conv5way_step20000 | same_language_bible_adjacent | v5_target | 300 | 0.978841 | 0.748582 |
| v52_mean_conv5way_step20000 | same_language_tatoeba_adjacent | all | 300 | 0.944935 | 0.378972 |
| v52_mean_conv5way_step20000 | same_language_tatoeba_adjacent | v5_target | 300 | 0.944935 | 0.378972 |

Interpretation boundary: this is a qualitative/diagnostic sentence-vector
analysis. It supports interpretation of PPPL/downstream behavior but does
not replace Glot500 metric scores.
