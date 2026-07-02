# v5 Final Evidence Packet Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `final_evidence_packet_waiting_results`

This generated audit is the final claim-promotion packet for the v5
report/PPT. A metric row can be measured but not promotable: final
wording is unlocked only when checkpoint pair, metric rows, provenance,
materiality, claim gate, patch targets, and final freeze are all ready
in the same refreshed reporting package.

| Packet Item | Status | Evidence | Action |
| --- | --- | --- | --- |
| checkpoint_pair | ready | v5_random:ready_for_wrapper=yes;model_status=ready; v5_fvt:ready_for_wrapper=yes;model_status=ready; manifest=checkpoint_selection_contract_ready; preflight=post_checkpoint_preflight_ready_to_launch | none |
| metric_rows | waiting_results | pseudoperplexity:status=partial;measured=glot500_base,v5_random,xlmr_base;missing=v5_fvt;coverage=102/102;target10=10/10 \| retrieval_tatoeba:status=measured;measured=glot500_base,v5_fvt,v5_random,xlmr_base;missing=-;coverage=63/102;target10=0/10 \| retrieval_bible:status=measured;measured=glot500_base,v5_fvt,v5_random,xlmr_base;missing=-;coverage=74/102;target10=0/10 \| text_classification:status=measured;measured=glot500_base,v5_fvt,v5_random,xlmr_base;missing=-;coverage=1/102;target10=0/10 \| ner:status=partial;measured=glot500_base,v5_random,xlmr_base;missing=v5_fvt;coverage=78/102;target10=0/10 \| pos:status=partial;measured=glot500_base,v5_random,xlmr_base;missing=v5_fvt;coverage=58/102;target10=0/10 \| roundtrip_alignment:status=partial;measured=glot500_base,v5_random,xlmr_base;missing=v5_fvt;coverage=74/102;target10=0/10 | run guarded post-checkpoint evaluation or retain explicit blocked/coverage-limited rows |
| provenance | waiting_provenance | provenance=post_checkpoint_provenance_ready_waiting_models; parser=parser_contract_ready_waiting_models; command_consistency=post_checkpoint_command_consistency_ready | keep source files, run metadata, command logs, parser contract, and command guards synchronized |
| materiality | waiting_materiality | materiality=comparison_materiality_waiting_results; pending_after_mlm_or_downstream=pseudoperplexity/weighted_pseudo_perplexity,ner/f1,pos/f1,roundtrip_alignment/accuracy | wait for after-MLM/downstream rows and materiality bands before strengthening method wording |
| claim_gate | waiting_claim_gate | promotion=claim_boundaries_ready_pending_results; decision=decision_tree_waiting_for_results; conclusion_contract=conclusion_selection_contract_ready_waiting_results; freeze=claim_freeze_needs_update | keep final conclusion conditional until decision tree and claim-freeze audits select a non-pending outcome |
| patch_targets | waiting_patch_targets | patch_plan=post_result_patch_plan_ready_for_execution; insertion=result_insertion_contract_ready; table_sync=needs_table_sync; crosswalk_exists=True | use patch plan/result insertion contract before editing Report, paper drafts, slides, script, and claim ledger |
| final_freeze | waiting_final_freeze | rendered=rendered_artifact_freshness_ready; smoke=final_submission_smoke_needs_repair; package=needs_document_cleanup; release=release_bundle_audit_needs_repair | rerun refresh after final text/result edits and keep execution-draft outputs out of final-candidate claims |

Promotion rule:

```text
If any row is not ready, keep the relevant result as measured but not promotable.
Do not upgrade Report.md, paper_draft.md, final_deck_ko.md, slide 14,
or presenter_script_ko.md to a final method claim until this audit is ready.
```
