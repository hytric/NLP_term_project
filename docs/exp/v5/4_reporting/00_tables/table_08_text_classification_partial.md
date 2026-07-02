# Table 8. Text Classification Partial Results

Last updated: 2026-06-28

Caption draft:

```text
Taxi1500 text classification is currently available locally only for English.
Macro-F1 is higher-is-better. The row is useful as a limited head/all baseline,
but it does not support target10 downstream claims.
```

| Model | Group | Macro-F1 | Accuracy | Status |
| --- | --- | ---: | ---: | --- |
| `xlmr_base` | head / all available | 0.592876 | 0.729730 | measured |
| `xlmr_base` | v5 target / tail | N/A | N/A | coverage-limited |
| `glot500_base` | head / all available | 0.743338 | 0.756757 | measured external reference |
| `v5_random` | head / all available | 0.702956 | 0.747748 | measured random checkpoint |
| `v5_fvt` | head / all available | waiting checkpoint | waiting checkpoint | waiting for matched checkpoint |

Source artifacts:

- `/home/axt/mnt2/jongha/v5_glot50010/evaluation/text_classification/taxi1500/xlmr_base/summary.json`
- `/home/axt/mnt2/jongha/v5_glot50010/evaluation/text_classification/taxi1500/glot500_base/summary.json`
- `/home/axt/mnt2/jongha/v5_glot50010/evaluation/text_classification/taxi1500/v5_random/summary.json`
- `docs/exp/v5/3_evaluation/09_aggregation/main_head_tail_all.tsv`
- `docs/exp/v5/3_evaluation/09_aggregation/metric_completion.tsv`
