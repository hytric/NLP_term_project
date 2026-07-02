# v5 Live Training Health Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `live_training_health_ready_for_post_checkpoint_status`

This generated audit is an operational guard for the paired 10K MLM
run. It checks active process state, ETA artifact state, recent log
movement, critical failure patterns, GPU 2/3 activity, and the
post-checkpoint evaluation gate.

It is not a model-quality result. Keep final after-MLM and downstream
claims locked until both `v5_random` and `v5_fvt` are
`ready_for_wrapper=yes`.

| Area | Status | Evidence | Action |
| --- | --- | --- | --- |
| progress_artifact | ready | mlm_progress=mlm_progress_ready_for_post_checkpoint_status | none |
| random_trainer_process | ready | latest_step=10000/10000; status=ready | none |
| fvt_trainer_or_queue | ready | status=ready; launcher_running=False | none |
| random_log_freshness | completed | 77809s old; path=/home/axt/mnt2/jongha/v5_glot50010/runs/logs/train_v5_v5_random_mlm_10k_20260627_005616.log | none |
| critical_log_patterns | clean | critical=0; benign_matches=8 | none |
| gpu_2_3_activity | low_or_unknown | gpu2=11/49140MB 0%; gpu3=124/49140MB 0% | confirm this is an intentional idle/wait state |
| post_checkpoint_eval_gate | ready | v5_random_ready=True; v5_fvt_ready=True | run status wrapper |

Next safe command while locked:

```bash
python3 scripts/write_v5_mlm_progress_eta.py
python3 scripts/audit_v5_live_training_health.py
```

First command after both wrapper-ready flags become `yes`; keep long evaluation locked until `post_checkpoint_preflight.md` reports `post_checkpoint_preflight_ready_to_launch`:

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
```
