# v5 Result Promotion Readiness Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `result_promotion_readiness_needs_update`

This generated audit checks whether parsed v5 outputs are sufficient
to promote final report/PPT claims. It verifies the matched checkpoint
pair, required metric/model aggregation rows, gate-to-claim lock
synchronization, and supporting claim/fidelity audits.

It should be `result_promotion_readiness_ready_for_claim_review` before
after-MLM or downstream method claims are upgraded in the paper or deck.

| Item | Status | Evidence | Action |
| --- | --- | --- | --- |
| matched_checkpoint_pair | ready | v5_random:ready=yes;selection=ready_10k;step=10000; v5_fvt:ready=yes;selection=ready_10k;step=10000 | none |
| metric_pair:pseudoperplexity | needs_review | completion=partial; missing_models=v5_fvt; v5_random:aggregate_v5_target=True;queue=measured; v5_fvt:aggregate_v5_target=False;queue=ready | inspect metric completion and aggregation parser outputs |
| metric_pair:retrieval_tatoeba | ready | completion=measured; missing_models=; v5_random:aggregate_all=True;queue=measured; v5_fvt:aggregate_all=True;queue=measured | none |
| metric_pair:retrieval_bible | ready | completion=measured; missing_models=; v5_random:aggregate_all=True;queue=measured; v5_fvt:aggregate_all=True;queue=measured | none |
| metric_pair:text_classification | ready | completion=measured; missing_models=; v5_random:aggregate_all=True;queue=measured; v5_fvt:aggregate_all=True;queue=measured | none |
| metric_pair:ner | needs_review | completion=partial; missing_models=v5_fvt; v5_random:aggregate_all=True;queue=measured; v5_fvt:aggregate_all=False;queue=ready | inspect metric completion and aggregation parser outputs |
| metric_pair:pos | needs_review | completion=partial; missing_models=v5_fvt; v5_random:aggregate_all=True;queue=measured; v5_fvt:aggregate_all=False;queue=ready | inspect metric completion and aggregation parser outputs |
| metric_pair:roundtrip_alignment | needs_review | completion=partial; missing_models=v5_fvt; v5_random:aggregate_all=True;queue=measured; v5_fvt:aggregate_all=False;queue=ready | inspect metric completion and aggregation parser outputs |
| gate_claim_synchronization | ready | matched=ready; pppl=pending; downstream=pending; pppl_claim=locked_pending_result; downstream_claim=locked_pending_result; target10_claim=disallowed_for_now | none |
| supporting_promotion_inputs | needs_update | decision_tree=decision_tree_waiting_for_results; result_insertion=result_insertion_contract_ready; table_sync=needs_table_sync; metric_fidelity=metric_fidelity_needs_repair | repair supporting result/claim audits before final promotion |

Promotion rule:

- `waiting_checkpoints`: do not run long post-checkpoint evaluation yet.
- `waiting_results`: checkpoints are expected, but parsed metric rows are incomplete.
- `needs_update`: a gate, claim lock, parser, or source table is inconsistent.
- `ready_for_claim_review`: choose the final conclusion via the decision tree,
  then refresh report/PPT and rerun all final audits.
