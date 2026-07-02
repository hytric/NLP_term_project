# v5 Roundtrip Alignment Blocker Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `roundtrip_inputs_ready_pending_results`

This generated audit documents whether the Glot500 roundtrip-alignment
metric has local inputs, a v5 runner, and parsed model outputs.

| Item | Status | Evidence | Action |
| --- | --- | --- | --- |
| coverage_summary | available_language_ready | roundtrip_alignment coverage=74/102; target10=0/10 | review newly available rows and rerun aggregation |
| coverage_detail_reasons | ready | available=74; missing_local_materialization=8; not_in_task_or_bible_proxy_flag_zero=20 | keep per-language exclusions visible in 00_coverage |
| repo_roundtrip_data_root | has_files | evaluation/download_data/download/roundtrip_alignment | create or link a materialized roundtrip_alignment dataset here |
| v5_roundtrip_data_root | has_files | /home/axt/mnt2/jongha/v5_glot50010/eval_data_download/roundtrip_alignment | create or link a materialized roundtrip_alignment dataset here |
| materialization_summary | ready | docs/exp/v5/3_evaluation/07_roundtrip_alignment/materialization_summary.tsv | run scripts/materialize_v5_roundtrip_alignment.py if missing or stale |
| inherited_evaluator | class_demo_exists | evaluation/round-trip/evaluate_roundtrip.py | keep as the inherited scoring implementation |
| v5_batch_runner | ready | evaluation/round-trip/evaluate_roundtrip_v5.py | add or repair the v5 JSONL batch runner |
| v5_metric_runner | ready | scripts/run_v5_eval_metric.sh | use scripts/run_v5_eval_metric.sh roundtrip_alignment <model_key> <gpu> |

Promotion rule:

- Do not convert roundtrip alignment to a measured metric until
  parsed per-model outputs are visible in `3_evaluation/09_aggregation/`.
- If inputs and runner exist but model outputs do not, keep the metric
  as pending/model-blocked accounting rather than omitting it.
