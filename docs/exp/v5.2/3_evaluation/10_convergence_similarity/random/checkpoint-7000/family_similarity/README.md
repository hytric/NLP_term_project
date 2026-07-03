# v5.2 Family Similarity

This directory contains tail-anchored sentence-vector diagnostics for language family and script effects.
Every comparison pair contains at least one v5.2 unseen tail language.

## Scope

- sampled languages: `38`
- sampled sentence points: `3708`
- pair rows: `11956`
- models: `v52_random_conv5way_step7000`
- layer index: `7` (0-indexed layer 8)

## Relation Types

| Relation | Meaning |
| --- | --- |
| `tail_within_language` | same unseen tail language, adjacent raw sentences |
| `tail_tail_same_family` | two unseen tail languages with the same family label |
| `tail_tail_same_macro_family` | two unseen tail languages with the same macro-family but different family label |
| `tail_tail_different_family` | two unseen tail languages from different families |
| `tail_head_same_family` | unseen tail and XLM-R-seen head language with the same family label |
| `tail_head_same_macro_family` | unseen tail and head with same macro-family but different family label |
| `tail_head_different_family_same_script` | unseen tail and head, both Latin script, different family |
| `tail_head_different_family_different_script` | unseen tail and head, different script and family |

## Summary

| Model | Relation | Pairs | Mean cosine | Mean centered cosine |
| --- | --- | ---: | ---: | ---: |
| v52_random_conv5way_step7000 | tail_head_different_family_different_script | 1856 | 0.902491 | -0.062399 |
| v52_random_conv5way_step7000 | tail_head_different_family_same_script | 6100 | 0.906413 | -0.048152 |
| v52_random_conv5way_step7000 | tail_head_same_family | 1050 | 0.921857 | 0.022550 |
| v52_random_conv5way_step7000 | tail_head_same_macro_family | 1550 | 0.916483 | -0.065538 |
| v52_random_conv5way_step7000 | tail_tail_different_family | 900 | 0.911736 | 0.118518 |
| v52_random_conv5way_step7000 | tail_tail_same_family | 50 | 0.945889 | 0.294637 |
| v52_random_conv5way_step7000 | tail_tail_same_macro_family | 100 | 0.934085 | 0.185072 |
| v52_random_conv5way_step7000 | tail_within_language | 350 | 0.952357 | 0.468507 |

## Outputs

- `family_points.tsv`: sampled raw sentences and language metadata.
- `family_pair_scores.tsv`: cosine scores for tail-anchored pair comparisons.
- `family_pair_summary.tsv`: mean similarity by model and relation type.
- `family_centroid_similarity_<model>.tsv`: language centroid cosine matrix in long TSV form.
- `family_pair_boxplot_<model>.png`: relation-type similarity distributions.
- `family_centroid_heatmap_<model>.png`: language centroid cosine heatmap.
- `family_point_map_all_<model>.png`: PCA point map for tail and selected head languages.
- `family_point_map_tail_only_<model>.png`: PCA point map among tail languages only.
- `family_point_map_tail_by_language_<model>.png`: tail-only PCA point map colored by language.
- `family_point_map_all_tail_highlight_<model>.png`: all-language PCA map with head languages greyed out and tail languages highlighted.
- `family_centroid_map_<model>.png`: PCA map of language centroids.

Interpretation boundary: these raw-sentence comparisons diagnose representational
geometry by language/script/family. They are not translation-aligned semantic
retrieval scores, so high similarity can reflect language identity or corpus style.
