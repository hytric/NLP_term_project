# v5_random Tatoeba Retrieval

This folder records the v5 Tatoeba retrieval run for `v5_random`.

- Role: measured random-initialized continued-MLM row for the retained Glot500
  Tatoeba retrieval metric family.
- Input: local Tatoeba retrieval data under
  `evaluation/download_data/download/retrieval_tatoeba/`.
- Output:
  `/home/axt/mnt2/jongha/v5_glot50010/evaluation/retrieval_tatoeba/v5_random/__home__axt__mnt2__jongha__v5_glot50010__runs__v5_random_mlm_10k/test_results.txt`.
- Current status: measured over 98 available language-scripts, with head split
  coverage 63 and target10 coverage `0/10`.
- Promotion gate: parsed by `scripts/aggregate_v5_metrics.py` into
  `3_evaluation/09_aggregation/`.

This row is random-checkpoint evidence only. FVT-vs-random downstream claims
remain locked until the matched `v5_fvt` row is measured and parsed.
