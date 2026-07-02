# Experiment 1 Plan: Cross-Lingual Semantic Embedding Alignment

작성일: 2026-06-18

## Goal

Check whether target10 low-resource languages are attached to the shared semantic embedding space.

The target property is:

> Same meaning across different languages should be close; different meaning should be far; nearest-neighbor structure should follow semantics rather than language/script.

## Input

| Input | Requirement |
| --- | --- |
| parallel item text | `item_id`, `language_id`, `text`, `split` |
| model checkpoints | XLM-R-base and candidate checkpoints |
| tokenizer | checkpoint-matched tokenizer |
| target language list | fixed target10 from v3 |

Minimum viable data:

- all target10 Bible verses with shared verse ids;
- English as anchor;
- high-resource control languages if available.

Preferred data:

- target-target shared verse matrix, not only English-target;
- dev/test split by book/chapter group.

## Embedding Extraction

Default:

| Setting | Value |
| --- | --- |
| layer | 8 |
| pooling | attention-mask mean pooling |
| normalization | L2 normalize |
| max length | fixed 256 or 512 |
| batch order | deterministic |

Ablations:

- last layer;
- average of last 4 layers;
- CLS pooling;
- cosine vs CSLS-sensitive retrieval for hubness analysis.

## Pair Definitions

| Pair | Definition |
| --- | --- |
| positive | same `item_id`, different languages |
| hard negative | different `item_id`, same book/chapter/topic |
| easy negative | different `item_id`, distant book/topic |
| same-language negative | different `item_id`, same language |
| high-resource control | same `item_id` among high-resource languages |

Hard negatives are required. Without them, the model can look good by domain/topic shortcuts.

## Metrics

| Metric | File |
| --- | --- |
| positive cosine mean | `alignment_scores.tsv` |
| hard-negative cosine mean | `semantic_margin_scores.tsv` |
| positive-minus-hard-negative margin | `semantic_margin_scores.tsv` |
| Recall@1, Recall@5 | `retrieval_scores.tsv` |
| MRR, median rank | `retrieval_scores.tsv` |
| centroid variance by `item_id` | `alignment_scores.tsv` |
| language silo score | `alignment_scores.tsv` |
| hubness@k | `hubness_scores.tsv` |
| semantic-vs-language silhouette delta | `alignment_scores.tsv` |

## 2D Map

Generate UMAP first; t-SNE and PCA are sensitivity checks.

Required figures:

| Figure | Color / Facet | Purpose |
| --- | --- | --- |
| `umap_by_language.png` | language/script | detect language silos |
| `umap_by_item_group.png` | semantic item group | detect meaning clusters |
| `umap_base_vs_candidate.png` | model + item group | compare XLM-R-base and candidate |
| `umap_hubness_overlay.png` | hubness@k | detect hub vectors/languages |

Interpretation:

- Good: same `item_id` clusters together across languages.
- Bad: Coptic/Syriac/Cherokee/Ojibwa form isolated script islands.
- Bad: English/German vectors become hubs for unrelated target items.
- Diagnostic only: a visually nice map without metric gains cannot support positive claim.

## Gate

`PASS_ALIGNMENT_READY` requires:

1. macro target10 alignment margin improves over XLM-R-base;
2. macro MRR or Recall@1 improves over XLM-R-base;
3. at least `7/10` target languages improve on alignment margin or retrieval MRR;
4. `cop` and `syr` have explicit rows;
5. language silo score does not worsen sharply;
6. hubness does not concentrate in one high-resource language or one script group;
7. high-resource control pairs remain stable.

Failure labels:

| Label | Meaning |
| --- | --- |
| `DIAGNOSTIC_MAP_ONLY` | map looks better but metrics fail |
| `FAIL_LANGUAGE_SILO` | points cluster by language/script |
| `FAIL_HUBNESS` | nearest neighbors dominated by a hub language/vector |
| `FAIL_COPTIC_SYRIAC_BOUNDARY` | Coptic/Syriac omitted or negative without explicit discussion |

## Outputs

| Artifact | Path |
| --- | --- |
| manifest | `parallel_item_manifest.tsv` |
| split manifest | `split_manifest.tsv` |
| embedding cache manifest | `embedding_cache_manifest.tsv` |
| scores | `alignment_scores.tsv`, `semantic_margin_scores.tsv`, `retrieval_scores.tsv`, `hubness_scores.tsv` |
| plot points | `map_points.tsv` |
| figures | `figures/*.png` |
| summary | `results.md` |

