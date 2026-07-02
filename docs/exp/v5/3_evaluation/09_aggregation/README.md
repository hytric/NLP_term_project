# 09 Aggregation

Use this folder for final metric aggregation scripts and summary tables.

Expected outputs:

- Glot500-style head/tail/all table
- v5-target subset table
- metric completion checklist
- coverage summary

Current generator:

```bash
python3 scripts/aggregate_v5_metrics.py
```

Currently parsed result formats:

- PPPL `summary.tsv`
- retrieval `test_results.txt` with `Acc10`, including evaluator outputs nested
  as `<metric>/<model_key>/<hf_model_name>/test_results.txt`
- Taxi1500 `summary.json`
- tagging `test_results.txt` with `f1`

Roundtrip alignment is represented as pending until the v5 runner writes a
machine-readable model output.

Current generated files:

- `metric_completion.tsv`
- `main_head_tail_all.tsv`
- `v5_target_subset.tsv`
- `results.md`

## Next Step Gate

Move to `../../4_reporting/` only after all metric outputs are normalized into
final tables.

Pass line:

- every required Glot500 metric is marked measured, blocked, or excluded with
  reason.
- head/tail/all table includes `xlmr_base`, `glot500_base`, `v5_random`, and
  `v5_fvt`.
- v5-target subset table is separate from all-language results.
- coverage summary is linked for every metric.
- table generation source paths are recorded.

Required artifacts:

- metric completion checklist
- main head/tail/all table
- v5-target subset table
- coverage summary table
- aggregation command or script path

If aggregation requires manual edits, write exactly which values were copied
from which raw result files.
