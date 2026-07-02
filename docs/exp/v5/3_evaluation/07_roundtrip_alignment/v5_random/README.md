# v5_random Roundtrip Alignment

This folder records the v5 Roundtrip alignment run for `v5_random`.

- Role: measured random-initialized continued-MLM row for the retained Glot500 Roundtrip metric family.
- Input: `evaluation/download_data/download/roundtrip_alignment/roundtrip.*.jsonl`.
- Output: `/home/axt/mnt2/jongha/v5_glot50010/evaluation/roundtrip_alignment/v5_random/summary.tsv` and `test_results.txt`.
- Current status: measured over 74 available language-scripts with target10 coverage `0/10`.
- Promotion gate: parsed by `scripts/aggregate_v5_metrics.py` into `3_evaluation/09_aggregation/`.

This row is random-checkpoint evidence only. FVT-vs-random downstream claims
remain locked until the matched `v5_fvt` row is measured and parsed.
