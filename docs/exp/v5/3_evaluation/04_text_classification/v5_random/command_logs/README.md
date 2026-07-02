# v5_random Taxi1500 Command Logs

This folder stores the command log for the `v5_random` Taxi1500
text-classification run.

- Main log: `run_v5_random_20260628_050138.log`
- Command source: `bash scripts/run_v5_eval_metric.sh text_classification v5_random 0`
- Promotion rule: treat logs as provenance; use parsed aggregation rows and
  coverage notes for report/PPT tables.

The expected model warnings about unused MLM-head weights and newly initialized
classification-head weights are normal for fine-tuning an MLM checkpoint on the
Taxi1500 classification task.
