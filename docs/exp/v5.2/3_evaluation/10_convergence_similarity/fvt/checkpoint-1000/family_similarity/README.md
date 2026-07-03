# v5.2 Family Similarity

This directory contains tail-anchored sentence-vector diagnostics for language family and script effects.
Every comparison pair contains at least one v5.2 unseen tail language.

## Scope

- sampled languages: `38`
- sampled sentence points: `3708`
- pair rows: `11956`
- models: `v52_fvt_conv5way_step1000`
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
| v52_fvt_conv5way_step1000 | tail_head_different_family_different_script | 1856 | 0.903102 | -0.070229 |
| v52_fvt_conv5way_step1000 | tail_head_different_family_same_script | 6100 | 0.907815 | -0.043642 |
| v52_fvt_conv5way_step1000 | tail_head_same_family | 1050 | 0.923907 | 0.040737 |
| v52_fvt_conv5way_step1000 | tail_head_same_macro_family | 1550 | 0.918039 | -0.057776 |
| v52_fvt_conv5way_step1000 | tail_tail_different_family | 900 | 0.911725 | 0.099043 |
| v52_fvt_conv5way_step1000 | tail_tail_same_family | 50 | 0.945541 | 0.286305 |
| v52_fvt_conv5way_step1000 | tail_tail_same_macro_family | 100 | 0.935071 | 0.167605 |
| v52_fvt_conv5way_step1000 | tail_within_language | 350 | 0.952254 | 0.461177 |

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
