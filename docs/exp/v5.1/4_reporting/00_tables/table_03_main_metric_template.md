# Table 3. Main Metric Result Template

Status: pending v5.1 checkpoints and post-checkpoint evaluation.

Use this table for the final report/PPT after
`docs/exp/v5.1/3_evaluation/09_aggregation/main_head_tail_all.tsv` is populated.

## Definitions

```text
head = XLM-R-seen subset among the fixed 92 languages with metric data
target10 = selected XLM-R-unseen subset with metric data
all = head + target10 inside the v5.1 102-language universe
Random = v51_strict5pct_random_mlm_3k
FVT = v51_strict5pct_fvt_mlm_3k
```

## Main Result Table

| Metric | XLM-R Base head | Glot500 head | Random head | FVT head | XLM-R Base target10 | Glot500 target10 | Random target10 | FVT target10 | XLM-R Base all | Glot500 all | Random all | FVT all | Direction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| PPPL | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | lower better |
| Tatoeba Top-10 Acc. | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | higher better |
| Bible Top-10 Acc. | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | higher better |
| Taxi1500 F1 | pending | pending | pending | pending | n/a | n/a | n/a | n/a | pending | pending | pending | pending | higher better |
| NER F1 | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | higher better |
| POS F1 | pending | pending | pending | pending | n/a | n/a | n/a | n/a | pending | pending | pending | pending | higher better |
| Roundtrip Acc. | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | higher better |

## Claim Rules

- PPPL must come from held-out `test`, not train-source diagnostics.
- POS and Taxi1500 have no target10 coverage, so target-side claims must be `n/a`.
- Main novelty claim is Random vs FVT under matched corpus/tokenizer/step/batch/schedule.
- XLM-R Base and Glot500 Base are reference rows, not trained under the v5.1 budget.

## Source Files

```text
docs/exp/v5.1/3_evaluation/09_aggregation/main_head_tail_all.tsv
docs/exp/v5.1/3_evaluation/09_aggregation/v5_target_subset.tsv
docs/exp/v5.1/3_evaluation/09_aggregation/results.md
```
