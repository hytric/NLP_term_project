# Step 28 Plan: Appended-Token Solution Roadmap

Created: 2026-06-12

## Goal

Turn the Step17 appended-token failure diagnosis into concrete solution proposals and falsifiable experiment protocols.

This step does not claim that the solutions work. It defines what should be tried next, why each remedy targets the diagnosed bottleneck, and what gate each remedy must pass before a future positive model claim can reopen.

## Scope

- Use only `second_try` evidence as motivation.
- Do not read `ACT` final data.
- Do not claim model improvement unless a future experiment passes Step15/16-style controls.
- Focus on appended-token prediction failure, not generic MLM tuning.

## Required Outputs

1. `solution_roadmap.md`: narrative explanation of recommended remedies.
2. `solution_candidates.tsv`: candidate solution table with rationale and expected mechanism.
3. `experiment_protocol.tsv`: concrete experiments, metrics, pass gates, and return paths.
4. `presentation_insert.md`: short Korean insert for presentation slides.
5. `score_table.tsv`: completion gates for this roadmap.
6. `v2_no_final_access_audit.tsv`: no-final-access audit.
7. `results.md`: summary and recommendation.
8. `file_results.tsv`: output ledger.

## Exit Criteria

- At least four concrete solution candidates are listed.
- Each solution candidate targets appended-token prediction directly.
- Each proposed experiment has pass/fail gates using existing Step15/16/17 metrics.
- Positive claim remains blocked until a future experiment passes those gates.

## Failure Return

If a solution is worded as already proven, return to Step28 and rewrite it as a hypothesis.

If positive model performance is required, implement the highest-priority Step28 experiment and rerun Step15/16 controls before any downstream or translation final readout.
