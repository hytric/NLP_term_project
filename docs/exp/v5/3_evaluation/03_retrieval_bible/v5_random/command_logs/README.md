# v5_random Bible Retrieval Command Logs

This folder stores the command log for the `v5_random` Bible retrieval run.

- Main log: `run_v5_random_20260628_040040.log`
- Command source: `bash scripts/run_v5_eval_metric.sh retrieval_bible v5_random 0`
- Promotion rule: treat logs as provenance; use parsed aggregation rows and
  coverage notes for report/PPT tables.

The expected model warnings about unused MLM-head weights and newly initialized
pooler weights are normal for loading an MLM checkpoint as `XLMRobertaModel` for
sentence embedding retrieval.
