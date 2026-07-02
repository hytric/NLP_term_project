# Table 7. Dataset Size Summary

Source of truth: `docs/exp/v5.1/3_evaluation/00_coverage/dataset_size_audit.tsv`

Counts below are actual local split/materialized counts for v5.1. Units differ
by task, so compare counts within each task family rather than across all rows.

## Raw Corpus / MLM / PPPL

| Data scope | Unit | Coverage | Train | Dev | Test | Total | Role |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Raw corpus strict split | raw text examples | 102 = 92 head + 10 target | 1,169,231,705 | 100,850 | 100,851 | 1,169,433,406 | Source corpus universe for tokenizer, MLM sampling, and held-out PPPL |
| MLM pretraining sample, strict 5% | sampled raw text lines | 102 = 92 head + 10 target | 8,130,401 | 0 | 0 | 8,130,401 | Actual train-only corpus used for continued MLM |
| PPPL held-out set | raw text examples | 102 = 92 head + 10 target | 0 | 100,850 | 100,851 | 201,701 | Dev/test held-out candidates; final PPPL should report test |

## Downstream Tasks

| Task | Unit | Coverage | Target10 coverage | Train | Dev | Test | Total | Metric / role |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Tatoeba retrieval | aligned sentence pairs | 66 / 102 | 3 / 10 | 0 | 0 | 57,479 | 57,479 | Top-10 accuracy; target10 evidence where available |
| Bible retrieval | aligned verse pairs | 80 / 102 | 6 / 10 | 0 | 0 | 622,393 | 622,393 | Top-10 accuracy; target10 evidence where available |
| Text classification, Taxi1500 | classification rows | 1 / 102 | 0 / 10 | 860 | 106 | 111 | 1,077 | Macro-F1; Glot500 replay only, not target10 evidence |
| NER | CoNLL sentence examples | 84 / 102 | 6 / 10 | 894,300 | 405,300 | 405,300 | 1,704,900 | F1; target10 evidence where available |
| POS | CoNLL sentence examples | 9 / 102 actual local count | 0 / 10 | 66,894 | 9,673 | 12,851 | 89,418 | F1; available-language replay only, not target10 evidence |
| Roundtrip alignment | roundtrip samples | 80 / 102 | 6 / 10 | 0 | 0 | 40,000 | 40,000 | Accuracy; target10 evidence where available |

## Auxiliary Diagnostic

| Item | Unit | Coverage | Train | Dev | Test / pairs | Total | Role |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Embedding similarity pairs | diagnostic pair rows | 1 / 102 | 0 | 0 | 22,600 | 22,600 | Auxiliary representation-analysis table, not a Glot500 downstream task |

## Reporting Notes

- Final PPPL must use the held-out `test` split, not the MLM train corpus.
- Target10 downstream claims should be promoted only for Tatoeba, Bible, NER,
  and Roundtrip where target-language data exists.
- Taxi1500 and POS remain useful Glot500-style replay metrics, but they do not
  support target10-specific claims in v5.1.
- POS has nominal broader coverage elsewhere, but the count above is the
  current actual local split/materialized count.
