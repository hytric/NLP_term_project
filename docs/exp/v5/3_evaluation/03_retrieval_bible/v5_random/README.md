# v5_random Bible Retrieval

This folder records the v5 Bible retrieval run for `v5_random`.

- Role: measured random-initialized continued-MLM row for the retained Glot500 Bible retrieval metric family.
- Input: local Bible retrieval data under `evaluation/download_data/download/retrieval_bible/`.
- Output: `/home/axt/mnt2/jongha/v5_glot50010/evaluation/retrieval_bible/v5_random/__home__axt__mnt2__jongha__v5_glot50010__runs__v5_random_mlm_10k/test_results.txt`.
- Current status: measured over 74 available language-scripts with target10 coverage `0/10`.
- Promotion gate: parsed by `scripts/aggregate_v5_metrics.py` into `3_evaluation/09_aggregation/`.

This row is random-checkpoint evidence only. FVT-vs-random downstream claims
remain locked until the matched `v5_fvt` row is measured and parsed.
