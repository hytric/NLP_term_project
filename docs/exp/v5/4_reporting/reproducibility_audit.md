# v5 Reproducibility Package Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `reproducibility_needs_repair`

This generated audit checks whether the final report/PPT package has
enough reproducibility detail to rerun or inspect the controlled v5
experiment: local roots, data scope, target languages, commands, model
keys, metric families, result-promotion rules, and post-checkpoint
handoff commands.

| Item | Status | Evidence | Action |
| --- | --- | --- | --- |
| required reproducibility docs | ready | all required reproducibility docs exist | none |
| required reproducibility scripts | ready | all command scripts exist | none |
| appendix:scope_92_10 | ready | all required tokens present | none |
| appendix:target10_codes | ready | all required tokens present | none |
| appendix:local_roots | ready | all required tokens present | none |
| appendix:core_commands | ready | all required tokens present | none |
| appendix:model_keys | ready | all required tokens present | none |
| appendix:metric_families | ready | all required tokens present | none |
| appendix:promotion_rules | ready | all required tokens present | none |
| appendix:fidelity_boundary | ready | all required tokens present | none |
| source-map reproducibility links | ready | source_map links appendix, handoff runbook, queue, execution plan, update manifest, patch plan, and refresh sync audit | none |
| post-checkpoint execution plan | ready | execution plan records wrapper/preflight gate, GPU env, command logs, and WITH_PLOTS launch | none |
| post-checkpoint command consistency | ready | post_checkpoint_command_consistency=post_checkpoint_command_consistency_ready | none |
| post-checkpoint handoff commands | ready | handoff runbook contains watcher, status, and all commands | none |
| result promotion map | ready | result_insertion_matrix separates live logs, parsed results, and blockers | none |
| post-result update manifest | ready | post_result_update_manifest maps commands, evidence, report/PPT targets, and claim rules | none |
| post-result patch plan | ready | post_result_patch_plan_ko maps parsed result gates to concrete report/PPT file edits | none |
| metric fidelity dependency | needs_update | metric_fidelity_audit=metric_fidelity_needs_repair | repair metric_fidelity_audit before final handoff |

Final use:

- Keep this audit `reproducibility_ready_current` before freezing the
  final report/PPT.
- After matched checkpoints and downstream outputs arrive, rerun
  `python3 scripts/refresh_v5_reporting.py --with-plots` so selected
  checkpoint paths and final metric rows are reflected everywhere.
