# Plan: Release Audit

Status: goal audit complete; public release cleanup pending

## Goal

Close the project-management loop before final paper/GitHub packaging. This stage checks that the target10 low-resource adaptation work is documented in order, that large artifacts stay outside the repository, that source-specific license evidence is recorded, and that the remaining public-release risks are explicit.

## Scope

This is not a new modeling stage. It audits the completed target10 pipeline and the Coptic/Syriac diagnostic experiments:

- final goal and target10 scope;
- ordered `docs/exp/` stage folders and `plan.md` files;
- GPU policy and physical GPU 3 usage;
- `/disk1` storage layout for large data/checkpoints;
- untracked/modified workspace state;
- source-specific data license evidence;
- paper-ready claim boundaries after the negative 10C source-grounding gate.

## Planned Work

1. Create an artifact inventory for docs, scripts, data symlinks, generated files, and release risks.
2. Update the root experiment README and release manifest so stage 11 appears after stage 10.
3. Update reproducibility and final-submission checklists with 10C and release-audit evidence.
4. Record local license evidence from source files found under `data/raw`.
5. Mark release-blocking items separately from completed paper-writing items.
6. Re-run lightweight validation commands and remove local Python caches after checks.

## Success Gate

This phase passes when:

- `release_audit_summary.md` explains what is ready, what is risky, and what should not be claimed;
- `artifact_inventory.tsv` lists release actions for docs, scripts, data symlinks, archives, and checkpoints;
- `docs/exp/README.md`, `experiment_manifest.tsv`, `reproducibility_checklist.md`, `final_submission_checklist.md`, and `data_license_notes.md` all reflect the current state;
- accidental archives/checkpoints are ignored or removed before public release;
- the remaining worktree cleanup and license-distribution decisions are clearly documented.

Current result:

- Passed for the active experiment-progress goal.
- Public GitHub release is still pending worktree cleanup and final source-by-source redistribution decisions.

## Decision Rule

The paper can claim target10 tokenizer adaptation, mean-initialized MLM readiness, strong retrieval baselines, and negative source-grounding diagnostics. It should not claim direct Coptic/Syriac neural translation, Greek pivoting, back-translation, or neural retrieval editing as solved.
