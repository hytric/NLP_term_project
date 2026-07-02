# v5 Final Claim Freeze Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `claim_freeze_needs_update`

This generated audit checks whether final report/PPT claims are safe to
freeze. It sits after the claim-promotion matrix and final decision tree:
pending claims must stay locked while result gates are pending, disallowed
scope claims must remain disallowed, and the report/deck must use the
outcome block selected from parsed aggregation rows.

| Item | Status | Evidence | Action |
| --- | --- | --- | --- |
| decision_tree_conclusion | waiting_results | decision_tree_verdict=decision_tree_waiting_for_results; status=execution_draft; decision=current_safe_zero_step_only; evidence=pppl=waiting_for_matched_v5_rows; downstream=fvt_downstream_majority | keep report/PPT conclusion conditional |
| pending_method_claim_locks | ready | FVT improves after-MLM PPPL over random:state=locked_pending_result,gate=pending; FVT improves downstream performance:state=locked_pending_result,gate=pending | none |
| disallowed_claim_locks | ready | full 511-language Glot500 reproduction:state=disallowed; Glot500-base is an equal-budget baseline:state=disallowed; target10_downstream:state=disallowed_for_now,coverage={'retrieval_tatoeba': '0', 'retrieval_bible': '0', 'text_classification': '0', 'ner': '0', 'pos': '0'} | none |
| report_deck_conditional_wording | ready | Korean paper/deck keep after-MLM and downstream claims gated | none |
| outcome_and_insertion_coverage | ready | interpretation blocks and insertion matrix cover PPPL/downstream/blocked outcomes | none |
| decision_tree_metric_coverage | ready | final claim decision tree mentions every required metric family | none |
| supporting_audit_verdicts | needs_update | metric_fidelity=metric_fidelity_needs_repair; aggregation_schema=aggregation_schema_ready; training_parity=training_parity_ready; conclusion_selection=conclusion_selection_contract_ready_waiting_results; claim_evidence_trace=claim_evidence_trace_needs_repair; reproducibility=reproducibility_needs_repair; result_insertion_contract=result_insertion_contract_ready; result_promotion_readiness=result_promotion_readiness_needs_update | repair supporting audits before freezing final claims |

Freeze rule:

- `claim_freeze_waiting_for_results`: rehearse with conditional
  wording; do not freeze final after-MLM/downstream claims.
- `claim_freeze_final_candidate`: final v5 rows exist; choose the
  matching interpretation block and synchronize report/PPT.
- `claim_freeze_needs_update`: repair claim locks or wording before
  using the package for presentation/report submission.
