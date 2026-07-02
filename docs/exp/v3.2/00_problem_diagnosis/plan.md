# Stage 00: Problem Diagnosis

작성일: 2026-06-19

## Goal

Freeze the `v3.1` failure analysis before changing the model.

This stage prevents `v3.2` from optimizing the wrong metric. The main mistake to avoid is treating all-token pseudoPPL or raw cosine as evidence of real language understanding.

## Inputs

| Input | Source |
| --- | --- |
| content-token top-k scores | `docs/exp/v3.1/05_additional/pseudoperplexity_accuracy_scores.tsv` |
| model-level pseudoPPL summary | `docs/exp/v3.1/05_additional/pseudoperplexity_accuracy_summary.tsv` |
| tokenization diagnostics | `docs/exp/v3.1/05_additional/pseudoperplexity_tokenization_diagnostics.tsv` |
| target10 CSLS retrieval | `docs/exp/v3.1/05_additional/target10_sentence_retrieval_csls_scores.tsv` |
| v3.1 final interpretation | `docs/exp/v3.1/05_additional/method_task_results.md` |

## Required Outputs

| Artifact | Purpose |
| --- | --- |
| `v31_failure_matrix.tsv` | one row per language, with content-token and retrieval bottleneck status |
| `metric_contract.md` | define primary, secondary, and forbidden metrics |
| `language_priority.md` | classify languages into urgent, watch, and stable groups |

## Language Priority

Initial grouping from v3.1:

| Group | Languages | Reason |
| --- | --- | --- |
| urgent content-token repair | `chr`, `cop`, `oji` | structured init content-token top-10 is `0` |
| urgent retrieval repair | `syr`, `cop` | lowest source/target centered-CSLS R@1 |
| watch | `acu`, `kbh`, `nhg`, `bsn` | content-token top-k is low but nonzero |
| relatively stronger | `ake`, `usp` | highest content-token top-k among target10 |

## Exit Gate

`V32_DIAGNOSIS_FROZEN` when:

- the failure matrix is written;
- primary metrics are fixed;
- all later stages agree to report language macro and worst-language scores;
- `xlmr_base` pseudoPPL is explicitly excluded from expanded-tokenizer quality claims.

