# v5 Final Claim Decision Tree

Last checked: 2026-06-28 18:08 KST

Verdict: `decision_tree_waiting_for_results`

This generated file decides which report/PPT conclusion wording is allowed
after v5 results are parsed. It is intentionally conservative: a claim
can move only from aggregation rows and finalization gates.

| Decision item | Status | Decision | Evidence | Report instruction | Slide instruction |
| --- | --- | --- | --- | --- | --- |
| zero_step_initialization | ready | intrinsic_fvt_win | random=18.411756; fvt=8.785518; delta=-9.626238; relative=-52.28% | Promote as intrinsic pre-MLM initialization evidence only. | Use on initialization slides; keep after-MLM/downstream claims locked. |
| after_mlm_pppl | pending_result | waiting_for_matched_v5_rows | matched_gate=ready; pppl_gate=pending; v5_random=True; v5_fvt=False | Keep after-MLM method claim as a hypothesis. | Keep slide 12/14 in execution-draft wording. |
| available_downstream_transfer | result_ready | fvt_downstream_majority | paired_measured=3; v5_random_diagnostic_measured=6; fvt_wins=3; fvt_nonwins=0; pending_or_incomplete=3; retrieval_tatoeba:all:fvt_wins:delta=0.007154; retrieval_bible:all:fvt_wins:delta=0.042330; text_classification:all:fvt_wins:delta=0.014840; ner:pending(status=partial; missing=v5_fvt); pos:pending(status=partial; missing=v5_fvt); roundtrip_alignment:pending(status=partial; missing=v5_fvt) | Use the positive downstream block, bounded to available-language coverage. | Upgrade slide 14 to a bounded downstream-transfer claim. |
| target10_downstream_claim | locked_coverage_limited | do_not_claim_target10_downstream | retrieval_tatoeba:0/10; retrieval_bible:0/10; text_classification:0/10; ner:0/10; pos:0/10; roundtrip_alignment:0/10 | Restrict target10 claims to tokenization, zero-step, and after-MLM PPPL. | Frame downstream replay as available-language/head/all, not target10 transfer. |
| roundtrip_alignment_claim | pending_result | waiting_for_roundtrip_rows | status=partial; measured=glot500_base,v5_random,xlmr_base; missing=v5_fvt | Roundtrip baseline/reference rows are measured, but v5 method rows are not final. | Report available-language reference rows; do not claim v5 method performance yet. |
| final_conclusion_block | execution_draft | current_safe_zero_step_only | pppl=waiting_for_matched_v5_rows; downstream=fvt_downstream_majority | Use current-safe conclusion: setup fidelity plus zero-step novelty, with final claims pending. | Slide 14 should remain conditional. |

Use with:

- `4_reporting/03_final_report/result_interpretation_blocks.md` for prose blocks.
- `4_reporting/claim_promotion_matrix.md` for claim locks.
- `3_evaluation/09_aggregation/` for numeric evidence.

Final safety rule: if this tree says `pending_result`, the report and
slides must keep the claim conditional even if a live log looks promising.
