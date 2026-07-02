# v5 Storage Readiness Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `storage_readiness_ready_current`

This generated audit checks whether the live v5 MLM run has enough
storage and writable output paths to finish the current 10K checkpoint,
start the queued FVT run, and later write post-checkpoint evaluation
artifacts. It is operational evidence, not a model-quality result.

| Item | Status | Evidence | Action |
| --- | --- | --- | --- |
| disk:v5_root | ready | path=/home/axt/mnt2/jongha/v5_glot50010; total_gb=12935.1; used_gb=8489.3; free_gb=3793.9; min_free_gb=100.0 | none |
| disk:repo_root | ready | path=/home/axt/jongha/Glot500-py39-eval; total_gb=878.2; used_gb=749.5; free_gb=84.1; min_free_gb=5.0 | none |
| path:main_corpus | ready | file=/home/axt/mnt2/jongha/v5_glot50010/data/Glot500_v5_glot50010_xlmr100.txt; exists=True; bytes=20125131060 | none |
| path:tokenizer | ready | dir=/home/axt/mnt2/jongha/v5_glot50010/tokenization/output/Glot500_extended_spm; exists=True; bytes=7631671 | none |
| path:initialized_random | ready | dir=/home/axt/mnt2/jongha/v5_glot50010/initialized_models/v5_random; exists=True; bytes=1504105329 | none |
| path:initialized_fvt | ready | dir=/home/axt/mnt2/jongha/v5_glot50010/initialized_models/v5_fvt; exists=True; bytes=1510767098 | none |
| path:runs_root | ready | dir=/home/axt/mnt2/jongha/v5_glot50010/runs; exists=True; bytes=11880507407 | none |
| path:cache_mlm10k | ready | dir=/home/axt/mnt2/jongha/v5_glot50010/cache_mlm10k; exists=True; bytes=64184375911 | none |
| path:evaluation_root | ready | dir=/home/axt/mnt2/jongha/v5_glot50010/evaluation; exists=True; bytes=22545879667 | none |
| writable:random_run_dir | ready | target=/home/axt/mnt2/jongha/v5_glot50010/runs/v5_random_mlm_10k; path=/home/axt/mnt2/jongha/v5_glot50010/runs/v5_random_mlm_10k; target_exists=True; mode=0o40755 | none |
| writable:fvt_run_dir_or_parent | ready | target=/home/axt/mnt2/jongha/v5_glot50010/runs/v5_fvt_mlm_10k; path=/home/axt/mnt2/jongha/v5_glot50010/runs/v5_fvt_mlm_10k; target_exists=True; mode=0o40755 | none |
| writable:logs_dir | ready | target=/home/axt/mnt2/jongha/v5_glot50010/runs/logs; path=/home/axt/mnt2/jongha/v5_glot50010/runs/logs; target_exists=True; mode=0o40755 | none |
| writable:launch_logs_dir | ready | target=/home/axt/mnt2/jongha/v5_glot50010/runs/launch_logs; path=/home/axt/mnt2/jongha/v5_glot50010/runs/launch_logs; target_exists=True; mode=0o40755 | none |
| checkpoint_size_reference | ready | random_model_gb=1.38; fvt_model_gb=1.38; expected_single_checkpoint_gb~=1.38 | none |
| current_random_log | ready | log=/home/axt/mnt2/jongha/v5_glot50010/runs/logs/train_v5_v5_random_mlm_10k_20260627_005616.log; bytes=10039660 | none |

Use:

- Keep this audit ready while `v5_random` and `v5_fvt` train.
- If it reports `needs_space`, do not wait for checkpoint failure;
  free space or move outputs before the next save boundary.
- Re-run after checkpoint creation, cache cleanup, or evaluation reruns.
