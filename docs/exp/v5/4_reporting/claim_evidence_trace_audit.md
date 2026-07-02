# v5 Claim-Evidence Trace Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `claim_evidence_trace_needs_repair`

This generated audit checks that the main report/PPT claims are traceable
from the claim ledger to the claim-promotion matrix, local evidence
artifacts, and visible report/slide surfaces. It is a traceability guard,
not a claim that pending after-MLM or downstream results already exist.

| Claim ID | Status | Promotion state | Evidence | Action |
| --- | --- | --- | --- | --- |
| controlled_subset_replay | ready | promotable_now | ledger + promotion matrix + evidence files + report/PPT surfaces align | none |
| full_glot500_disallowed | ready | disallowed | ledger + promotion matrix + evidence files + report/PPT surfaces align | none |
| target10_internal_selection | ready | promotable_now | ledger + promotion matrix + evidence files + report/PPT surfaces align | none |
| tokenizer_structural_validity | ready | promotable_with_caveat | ledger + promotion matrix + evidence files + report/PPT surfaces align | none |
| zero_step_fvt_intrinsic | ready | promotable_now | ledger + promotion matrix + evidence files + report/PPT surfaces align | none |
| after_mlm_pending | ready | locked_pending_result | ledger + promotion matrix + evidence files + report/PPT surfaces align | none |
| downstream_pending | ready | locked_pending_result | ledger + promotion matrix + evidence files + report/PPT surfaces align | none |
| metric_family_retained | ready | promotable_as_protocol_execution_partial | ledger + promotion matrix + evidence files + report/PPT surfaces align | none |
| target10_downstream_disallowed | ready | disallowed_for_now | ledger + promotion matrix + evidence files + report/PPT surfaces align | none |
| glot500_base_external_reference | ready | disallowed | ledger + promotion matrix + evidence files + report/PPT surfaces align | none |
| supporting_trace_audits | needs_update | not_applicable | bad_verdicts=metric_fidelity=metric_fidelity_needs_repair | repair supporting trace audits |

Use:

- Keep this audit ready before final report/PPT freeze.
- If a claim is upgraded after new metrics arrive, rerun
  `python3 scripts/refresh_v5_reporting.py` and check this file before
  editing the final conclusion.
