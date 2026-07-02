# Target10 Sentence Retrieval With CSLS

작성일: 2026-06-19

## Setup

- Task style: Glot500-like sentence retrieval on target10 Bible/dev rows.
- Source embeddings: existing MLM-dev feature caches.
- Representation: mean-pooled encoder output, L2-normalized.
- Score types: raw cosine, centered cosine, CSLS k=10, centered CSLS k=10.
- Scope: `3960` model/direction/score rows.

## Selected Macro Results

`xlmr_base` is kept in the raw TSV artifacts only. It is excluded from this report-ready table because base-tokenizer representations can be degenerate for several target10 scripts, making direct comparison with expanded-tokenizer `mlm200` variants hard to interpret.

| Model | Score | Margin | R@1 | R@5 | R@10 | MRR | Hubness@10 max |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `random_mlm200` | `centered_csls_k10` | -0.563356 | 0.012318 | 0.041759 | 0.068257 | 0.036425 | 0.077437 |
| `mean_mlm200` | `centered_csls_k10` | -0.637304 | 0.010675 | 0.038409 | 0.065668 | 0.03445 | 0.08429 |
| `align_mlm200` | `centered_csls_k10` | -0.473661 | 0.009456 | 0.034559 | 0.058497 | 0.031894 | 0.087349 |
| `fvt_mlm200` | `centered_csls_k10` | -0.480777 | 0.008798 | 0.032826 | 0.0576 | 0.030593 | 0.088414 |
| `focus_mlm200` | `centered_csls_k10` | -0.516167 | 0.00868 | 0.03344 | 0.057186 | 0.030713 | 0.085429 |

## Reading

This is a target10-wide sentence-retrieval diagnostic over `mlm200` variants. It should be read together with raw cosine, hard margin, Recall/MRR, and hubness. CSLS/centering is a hubness-calibrated scoring diagnostic, not proof of model-level improvement. If Recall@1 remains very low, the safe claim is weak retrieval signal, not robust semantic retrieval.

## Glot500 Scale Reference

Glot500 reports English-aligned Tatoeba/Bible Top-10 accuracy, so this target10 low-resource-to-low-resource proxy is not directly comparable. As a scale reference, Glot500-m reports `43.2%` Bible tail Top-10 accuracy, while the best v3.1 proxy R@10 here is `6.83%`.

## Artifacts

- Pair scores: `target10_sentence_retrieval_csls_scores.tsv`
- Summary: `target10_sentence_retrieval_csls_summary.tsv`
- Report-ready summary: `target10_sentence_retrieval_csls_summary_mlm200_only.tsv`
