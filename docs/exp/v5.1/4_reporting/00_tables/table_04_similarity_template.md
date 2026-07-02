# Table 4. Embedding Similarity Result Template

Status: pending v5.1 checkpoints and similarity runner.

Use this table after running:

```bash
GPU=0 MODEL_KEYS=v51_random,v51_fvt bash scripts/run_v51_similarity.sh
```

## Pair Coverage

Current input:

```text
docs/exp/v5.1/3_evaluation/08_embedding_similarity/similarity_pairs.tsv
total_pairs = 22,600
```

## Summary Table

| Pair group | Head pairs | Target10 pairs | Random cosine | FVT cosine | Delta FVT-Random | Interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Tatoeba aligned | pending | pending | pending | pending | pending | same-meaning retrieval geometry |
| Tatoeba same-language | pending | pending | pending | pending | pending | language cluster compactness |
| Bible aligned | pending | pending | pending | pending | pending | cross-lingual semantic alignment |
| Bible same-language | pending | pending | pending | pending | pending | language cluster compactness |
| Roundtrip source-English | pending | pending | pending | pending | pending | direct alignment preservation |
| Roundtrip source-pivot | pending | pending | pending | pending | pending | pivot-mediated alignment preservation |

## 2D Map Outputs

| Artifact | Status |
| --- | --- |
| `similarity_scores.tsv` | pending |
| `similarity_summary.tsv` | pending |
| `embedding_map_2d.tsv` | pending |
| `embedding_map_2d.png` | pending |

## Claim Rules

- Similarity is diagnostic/qualitative evidence and does not replace Glot500 7-metric evaluation.
- Use layer 8 mean-pooled sentence embeddings to stay aligned with the retrieval setup.
- Interpret improvements only inside pair groups with enough target coverage.
