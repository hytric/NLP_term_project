# v5.2 Family Similarity

This directory contains tail-anchored sentence-vector diagnostics for language family and script effects.
Every comparison pair contains at least one v5.2 unseen tail language.

## Scope

- sampled languages: `38`
- sampled sentence points: `3708`
- pair rows: `11956`
- models: `v52_family_mean_conv5way_step26000`
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
| v52_family_mean_conv5way_step26000 | tail_head_different_family_different_script | 1856 | 0.895978 | -0.074159 |
| v52_family_mean_conv5way_step26000 | tail_head_different_family_same_script | 6100 | 0.901684 | -0.045013 |
| v52_family_mean_conv5way_step26000 | tail_head_same_family | 1050 | 0.922993 | 0.062564 |
| v52_family_mean_conv5way_step26000 | tail_head_same_macro_family | 1550 | 0.915984 | -0.046961 |
| v52_family_mean_conv5way_step26000 | tail_tail_different_family | 900 | 0.901734 | 0.079854 |
| v52_family_mean_conv5way_step26000 | tail_tail_same_family | 50 | 0.942997 | 0.278881 |
| v52_family_mean_conv5way_step26000 | tail_tail_same_macro_family | 100 | 0.930774 | 0.149311 |
| v52_family_mean_conv5way_step26000 | tail_within_language | 350 | 0.952386 | 0.488055 |

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
