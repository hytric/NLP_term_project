# v5 Refresh Sequence Sync Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `refresh_sequence_sync_ready`

This generated audit checks that `scripts/refresh_v5_reporting.py`
and `4_reporting/result_insertion_matrix.md` agree on the
post-checkpoint gates and result-promotion refresh path. It prevents
the manual report/PPT update runbook from drifting away from the
actual generated reporting pipeline.

| Item | Status | Evidence | Action |
| --- | --- | --- | --- |
| refresh_script_exists | ready | /home/axt/jongha/Glot500-py39-eval/scripts/refresh_v5_reporting.py | none |
| result_insertion_matrix_exists | ready | /home/axt/jongha/Glot500-py39-eval/docs/exp/v5/4_reporting/result_insertion_matrix.md | none |
| refresh_required_steps | ready | all required sync-sensitive steps are in refresh_v5_reporting.py | none |
| matrix_required_steps | ready | result_insertion_matrix lists the refresh-sensitive steps | none |
| matrix_handoff_gate_tokens | ready | matrix includes the six post-checkpoint handoff gate artifacts | none |
| refresh_step_order | ready | order_ok | none |
| matrix_step_order | ready | order_ok | none |
| refresh_final_package_stabilization_order | ready | order_ok | none |
| matrix_final_package_stabilization_order | ready | order_ok | none |
| canonical_wording | ready | matrix points to refresh_v5_reporting.py and keeps the promotion rule | none |

Promotion invariant:

```text
metric output -> aggregation -> generated tables/audits -> report/PPT prose
```

Live progress, launcher state, and storage health are operational
evidence only; they must not replace parsed metric rows.
