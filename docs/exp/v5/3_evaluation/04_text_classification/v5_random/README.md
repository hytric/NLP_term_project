# v5_random Taxi1500 Text Classification

This folder records the v5 Taxi1500 text-classification run for `v5_random`.

- Role: measured random-initialized continued-MLM row for the retained Glot500
  text-classification metric family.
- Input: local English Taxi1500 split under
  `evaluation/download_data/download/taxi1500/`.
- Output:
  `/home/axt/mnt2/jongha/v5_glot50010/evaluation/text_classification/taxi1500/v5_random/summary.json`.
- Current status: measured on the local English-only setting, with coverage
  `1/102` and target10 coverage `0/10`.
- Promotion gate: parsed by `scripts/aggregate_v5_metrics.py` into
  `3_evaluation/09_aggregation/`.

This row is available-language evidence for the random checkpoint only. It does
not support a target10 downstream claim, and FVT-vs-random classification claims
remain locked until the matched `v5_fvt` row is measured and parsed.
