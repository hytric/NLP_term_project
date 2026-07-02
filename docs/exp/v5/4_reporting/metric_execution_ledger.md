# v5 Metric Execution Ledger

Last checked: 2026-06-28 18:08 KST

Verdict: `metric_execution_ledger_current`

This ledger is the report/PPT answer to whether the Glot500 metric
families are being faithfully retained. It records each metric family,
coverage boundary, measured model rows, waiting v5 rows, and claim rule.
It is not a replacement for aggregation outputs.

| Metric | Score | Direction | State | Coverage | Target10 | Measured | Missing | v5 random | v5 FVT | Claim rule |
| --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- | --- |
| PPPL | `weighted_pseudo_perplexity` | lower_is_better | partial | 102/102 | 10/10 | glot500_base,v5_random,xlmr_base | v5_fvt | measured | ready | May support target10 intrinsic/after-MLM claims after paired v5 rows parse. |
| Tatoeba retrieval | `top10_accuracy` | higher_is_better | measured | 63/102 | 0/10 | glot500_base,v5_fvt,v5_random,xlmr_base | - | measured | measured | Available-language retrieval only; selected target10 coverage is 0/10. |
| Bible retrieval | `top10_accuracy` | higher_is_better | measured | 74/102 | 0/10 | glot500_base,v5_fvt,v5_random,xlmr_base | - | measured | measured | Available-language Bible retrieval only; selected target10 coverage is 0/10. |
| Taxi1500 text classification | `macro_f1` | higher_is_better | measured | 1/102 | 0/10 | glot500_base,v5_fvt,v5_random,xlmr_base | - | measured | measured | Narrow local classification evidence only; selected target10 coverage is 0/10. |
| NER | `f1` | higher_is_better | partial | 78/102 | 0/10 | glot500_base,v5_random,xlmr_base | v5_fvt | measured | ready | Available-language tagging evidence; single target-language rows are not target10-wide evidence. |
| POS | `f1` | higher_is_better | partial | 58/102 | 0/10 | glot500_base,v5_random,xlmr_base | v5_fvt | measured | ready | Available-language tagging evidence with local POS train-language caveat. |
| Roundtrip alignment | `accuracy` | higher_is_better | partial | 74/102 | 0/10 | glot500_base,v5_random,xlmr_base | v5_fvt | measured | ready | Retained alignment family; no claim until parsed v5 rows exist. |

## Gate Summary

| Metric | Metric gate | Matched checkpoint gate | Preflight | Next action |
| --- | --- | --- | --- | --- |
| PPPL | pending | ready | post_checkpoint_preflight_ready_to_launch | Run PPPL mode after matched checkpoints and preflight. |
| Tatoeba retrieval | pending | ready | post_checkpoint_preflight_ready_to_launch | Run downstream/all mode after matched checkpoints and preflight. |
| Bible retrieval | pending | ready | post_checkpoint_preflight_ready_to_launch | Run downstream/all mode after matched checkpoints and preflight. |
| Taxi1500 text classification | pending | ready | post_checkpoint_preflight_ready_to_launch | Run downstream/all mode after matched checkpoints and preflight. |
| NER | pending | ready | post_checkpoint_preflight_ready_to_launch | Run downstream/all mode after matched checkpoints and preflight. |
| POS | pending | ready | post_checkpoint_preflight_ready_to_launch | Run downstream/all mode after matched checkpoints and preflight. |
| Roundtrip alignment | pending | ready | post_checkpoint_preflight_ready_to_launch | Run downstream/all mode after matched checkpoints and preflight. |

Use:

- In the report, cite this ledger when explaining that metric families are retained but not all v5 rows are measured yet.
- In the PPT/Q&A, use the state column to distinguish `measured`, `waiting_for_fvt_checkpoint`, and `coverage_target10=0/10`.
- Do not promote method claims from this ledger; promote only from aggregation rows after `refresh_v5_reporting.py --with-plots`.

Machine-readable TSV:

```text
metric_execution_ledger.tsv
```
