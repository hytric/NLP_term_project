# Table 6. PPPL Partial Results

Last updated: 2026-06-28

Caption draft:

```text
Pseudoperplexity is the first Glot500 metric with measured baseline/reference
and v5 continued-MLM output. Lower weighted PPPL and lower weighted mean NLL
are better. The table is partial: `xlmr_base`, `glot500_base`, and
`v5_random` are measured, while `v5_fvt` still requires its matched checkpoint
before the initialization-method comparison can be promoted.
```

| Model | Group | Weighted PPPL | Weighted mean NLL | Status |
| --- | --- | ---: | ---: | --- |
| `xlmr_base` | head | 8.117338 | 2.094002 | measured |
| `xlmr_base` | v5 target / tail | 61.980216 | 4.126815 | measured |
| `xlmr_base` | all | 9.986271 | 2.301211 | measured |
| `glot500_base` | head | 10.213100 | 2.323671 | measured |
| `glot500_base` | v5 target / tail | 15.102934 | 2.714889 | measured |
| `glot500_base` | all | 10.640353 | 2.364654 | measured |
| `v5_random` | head | 18.726452 | 2.929937 | measured |
| `v5_random` | v5 target / tail | 39.222875 | 3.669260 | measured |
| `v5_random` | all | 20.138927 | 3.002655 | measured |
| `v5_fvt` | head | waiting checkpoint | waiting checkpoint | waiting for matched checkpoint |
| `v5_fvt` | v5 target / tail | waiting checkpoint | waiting checkpoint | waiting for matched checkpoint |
| `v5_fvt` | all | waiting checkpoint | waiting checkpoint | waiting for matched checkpoint |

Source artifacts:

- `docs/exp/v5/3_evaluation/01_pseudoperplexity/xlmr_base/summary.tsv`
- `docs/exp/v5/3_evaluation/01_pseudoperplexity/glot500_base/summary.tsv`
- `docs/exp/v5/3_evaluation/01_pseudoperplexity/v5_random/summary.tsv`
- `docs/exp/v5/3_evaluation/09_aggregation/main_head_tail_all.tsv`
- `docs/exp/v5/3_evaluation/09_aggregation/metric_completion.tsv`
