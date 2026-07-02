# v5 Post-Checkpoint Parser Contract Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `parser_contract_ready_waiting_models`

This generated audit checks the contract between post-checkpoint
evaluation wrappers and `scripts/aggregate_v5_metrics.py`. It does not
measure results. It verifies that, once `v5_random` and `v5_fvt` outputs
exist, the aggregation layer knows where to parse them and which files
may be promoted into report/PPT tables.

| Item | Status | Evidence | Action |
| --- | --- | --- | --- |
| metric_contract:pppl | ready | expected_output=docs/exp/v5/3_evaluation/01_pseudoperplexity/<model_key>/summary.tsv | none |
| metric_contract:retrieval_tatoeba | ready | expected_output=/home/axt/mnt2/jongha/v5_glot50010/evaluation/retrieval_tatoeba/<model_key>/test_results.txt | none |
| metric_contract:retrieval_bible | ready | expected_output=/home/axt/mnt2/jongha/v5_glot50010/evaluation/retrieval_bible/<model_key>/test_results.txt | none |
| metric_contract:text_classification | ready | expected_output=/home/axt/mnt2/jongha/v5_glot50010/evaluation/text_classification/taxi1500/<model_key>/summary.json | none |
| metric_contract:ner | ready | expected_output=/home/axt/mnt2/jongha/v5_glot50010/evaluation/ner/<model_key>/test_results.txt | none |
| metric_contract:pos | ready | expected_output=/home/axt/mnt2/jongha/v5_glot50010/evaluation/pos/<model_key>/test_results.txt | none |
| metric_contract:roundtrip_alignment | ready | expected_output=/home/axt/mnt2/jongha/v5_glot50010/evaluation/roundtrip_alignment/<model_key>/test_results.txt | none |
| paired_wrapper_modes | ready | status/pppl/bible/roundtrip/downstream/tagging/all modes and readiness guard present | none |
| aggregation_output_files | ready | metric_completion, main_head_tail_all, and v5_target_subset outputs are written | none |
| required_v5_model_rows | ready | v5_random:required=yes;downstream=yes;ready=yes;status=ready; v5_fvt:required=yes;downstream=yes;ready=yes;status=ready | none |
| recovery_runbook_commands | ready | status/all/split/individual rerun commands and aggregation promotion rule are documented | none |
| current_baseline_parser_sources | ready | baseline/reference parser source files exist for current measured rows | none |

Use this with:

- `post_checkpoint_eval_queue.md` for row readiness.
- `post_checkpoint_eval_recovery.md` for reruns and failure handling.
- `09_aggregation/metric_completion.tsv` for final promotion status.
