# 04 Text Classification

Required Glot500 metric.

Report F1. Current local Taxi1500 materialization may be incomplete, so coverage
and data-access notes are mandatory.

## Next Step Gate

Move this metric to `../09_aggregation/` only after classification coverage and
F1 scores are reproducible.

Pass line:

- dataset name/version and train/dev/test split are recorded.
- language coverage and missing selected targets are documented.
- fine-tuning or probing setup is written.
- macro/micro F1 choice is explicit.
- every required model is included or has a failure/exclusion note.

Required artifacts:

- command log
- raw prediction or score output
- `summary.tsv` or `results.md`
- coverage reference
- hyperparameter note

If local Taxi1500 data is incomplete, write the exact missing path or download
blocker and keep the metric in the completion checklist as blocked, not omitted.

## Current Baseline And Reference Results

The `xlmr_base` baseline, `glot500_base` external-reference, and `v5_random`
Taxi1500 text-classification runs completed and have been parsed by
`09_aggregation/`.
Local coverage is English-only (`1/102`, target10 `0/10`), so this metric
currently supports limited head/all available rows rather than target10
downstream analysis.

Command log:

```text
/home/axt/mnt2/jongha/v5_glot50010/logs/text_classification_xlmr_base_20260627_023924.log
```

Output root:

```text
/home/axt/mnt2/jongha/v5_glot50010/evaluation/text_classification/taxi1500/xlmr_base
/home/axt/mnt2/jongha/v5_glot50010/evaluation/text_classification/taxi1500/glot500_base
/home/axt/mnt2/jongha/v5_glot50010/evaluation/text_classification/taxi1500/v5_random
```

Measured row:

| Group | Model | Macro-F1 | Accuracy | Source |
| --- | --- | ---: | ---: | --- |
| head/all available | `xlmr_base` | 0.592876 | 0.729730 | `../09_aggregation/main_head_tail_all.tsv` |
| head/all available | `glot500_base` | 0.743338 | 0.756757 | `../09_aggregation/main_head_tail_all.tsv` |
| head/all available | `v5_random` | 0.702956 | 0.747748 | `../09_aggregation/main_head_tail_all.tsv` |
