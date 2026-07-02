# v5 Checkpoint Selection Contract Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `checkpoint_selection_contract_ready`

This generated audit checks that final v5 model promotion uses the fixed
matched 10K rule: prefer the root Trainer output if it has a model file,
otherwise use a complete `checkpoint-10000`, and promote the main method
comparison only when both `v5_random` and `v5_fvt` have
`selection_status=ready_10k`.

| Item | Status | Evidence | Action |
| --- | --- | --- | --- |
| model_matrix_checkpoint_fallback | ready | model matrix prefers root final model and falls back to complete checkpoint-10000 | none |
| selected_manifest_10k_gate | ready | selected checkpoint manifest requires model file plus global_step=10000 for main v5 claim eligibility | none |
| selection_plan_contract | ready | selection plan documents matched 10K rule, checkpoint-10000 fallback, and failed-run downgrade | none |
| main_v5_checkpoint_pair | ready | v5_random and v5_fvt have selection_status=ready_10k and can be evaluated as matched checkpoints | none |

Promotion rule:

- `ready_for_wrapper=yes` is necessary for evaluation execution.
- `selection_status=ready_10k` for both v5 rows is necessary for the
  final novelty comparison claim.
- A partial or failed side stays `waiting_models` or `needs_update`; it
  must not be promoted by inspecting downstream scores first.
