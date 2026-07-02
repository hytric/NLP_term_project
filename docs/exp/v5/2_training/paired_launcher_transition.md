# v5 Paired Launcher Transition Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `paired_launcher_transition_matched_ready`

This generated audit checks whether the detached paired MLM launcher is
still in the expected random-then-FVT transition path. It is operational
evidence only; model-quality claims still require parsed evaluation rows.

| Item | Status | Evidence | Action |
| --- | --- | --- | --- |
| launcher_script_sequence | ready | random_before_fvt=True; train_script_calls=2; distinct_ports=True | none |
| launcher_process | complete_or_missing | launcher_active=False; random_running=False; fvt_running=False | none |
| transition_state | matched_ready | random_ready=True; random_status=ready; fvt_ready=True; fvt_status=ready; fvt_log_exists=True | none |
| launch_log | stale | path=/home/axt/mnt2/jongha/v5_glot50010/runs/launch_logs/launch_random_fvt_10k_setsid_20260627_005616.log; age_seconds=8080; bytes=10820414 | check whether training stopped or log path changed |
| random_log | completed | path=/home/axt/mnt2/jongha/v5_glot50010/runs/logs/train_v5_v5_random_mlm_10k_20260627_005616.log; age_seconds=77809; bytes=10039660 | none |
| critical_transition_log_patterns | clean | critical=0 | none |

Transition rule:

- While random is running, FVT should be waiting and no FVT log is expected.
- After random writes the selected checkpoint, FVT should start from the
  same launcher with the same train script and 10K schedule.
- Do not run post-checkpoint evaluation until both model rows are
  `ready_for_wrapper=yes` and `post_checkpoint_preflight.md` reports
  `post_checkpoint_preflight_ready_to_launch`.
