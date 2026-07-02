# v5 Result Insertion Contract Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `result_insertion_contract_ready`

This generated audit checks that every post-checkpoint metric family
has an explicit path from raw result output to provenance, aggregation,
report table, slide target, and claim boundary. It is a wiring audit: it does
not claim that pending v5 method results already exist.

| Item | Status | Evidence | Action |
| --- | --- | --- | --- |
| required insertion artifacts | ready | all insertion/slot/queue artifacts exist | none |
| metric_result_contract:pseudoperplexity | ready | slot=after_mlm_pppl; queue_rows=4 | none |
| metric_result_contract:retrieval_tatoeba | ready | slot=tatoeba_retrieval; queue_rows=4 | none |
| metric_result_contract:retrieval_bible | ready | slot=bible_retrieval; queue_rows=4 | none |
| metric_result_contract:text_classification | ready | slot=text_classification; queue_rows=4 | none |
| metric_result_contract:ner | ready | slot=ner_pos_tagging; queue_rows=4 | none |
| metric_result_contract:pos | ready | slot=ner_pos_tagging; queue_rows=4 | none |
| metric_result_contract:roundtrip_alignment | ready | slot=roundtrip_alignment; queue_rows=4 | none |
| global_contract:checkpoint_handoff | ready | all required terms present | none |
| global_contract:target10_downstream_boundary | ready | all required terms present | none |
| global_contract:refresh_sequence | ready | all required terms present | none |
| global_contract:post_result_update_manifest | ready | all required terms present | none |
| global_contract:post_result_patch_plan | ready | all required terms present | none |
| global_contract:final_evidence_packet | ready | all required terms present | none |
| global_contract:metric_family_acceptance_rule | ready | all required terms present | none |
| global_contract:post_result_manifest_command_support | ready | checked_wrapper_commands=7; supported_modes=all,bible,downstream,pppl,roundtrip,status,tagging | none |

Use:

- Keep this audit ready before running post-checkpoint evaluation.
- If a metric output appears but this audit is not ready, repair the
  insertion path before promoting the value into final report/PPT prose.
- Promotion also requires `post_checkpoint_provenance_audit.md` to
  retain the source file, run metadata, and command log trail.
- The post-result manifest commands must be supported by
  `run_v5_post_checkpoint_evals.sh`; long modes must retain
  explicit `GPU_RANDOM` and `GPU_FVT` bindings.
