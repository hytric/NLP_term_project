# v5 Slide Completion Matrix

Last updated: 2026-06-28

This matrix maps each slide to its allowed evidence, current claim status, and
the gate that must be crossed before final wording changes. It complements
`slide_claim_checklist.md` by making the final deck update path explicit.

## Slide Matrix

| Slide | Evidence source | Safe message now | Status | Final update gate |
| --- | --- | --- | --- | --- |
| 1. Title | `claim_ledger.md`, `paper_draft.md` | controlled 102-language Glot500-style replay with vocabulary-extension initialization | ready | no change unless experiment scope changes |
| 2. Motivation And Contributions | Glot500 framing, `contribution_summary.md` | uneven multilingual coverage motivates a 92+10 replay, FVT initialization novelty, and Glot500 metric-family fidelity | ready | no final-result dependency |
| 3. Reproduction Boundary | `goal_readiness.md`, `claim_ledger.md` | reproduce Glot500 pattern, not full 511-language scale | ready | keep boundary locked |
| 4. Target10 Selection | target manifest, `Report.md` | 10 Glot500-internal non-XLM-R targets, each with at least 30K rows | ready | no change unless target set changes |
| 5. Corpus Construction | merge report, `table_01_data_scope.md` | 92+10 corpus, 92,452,251 merged lines, 0 missing dirs | ready | no change unless corpus regenerated |
| 6. Tokenizer Method | tokenizer audit, `table_02_tokenizer_audit.md` | Glot500-style SPM append; 118,685 appended tokens; `dzo_Tibt` regression visible | ready with caveat | no change unless tokenizer repaired |
| 7. Novelty | init reports, `contribution_summary.md` | novelty is initialization policy for appended rows | ready | no final-result dependency |
| 8. Initialization Audit | init reports | identity copy, `<mask>` remap, byte accounting, LM-head tying | ready | no final-result dependency |
| 9. Zero-Step Evidence | `table_03_initialization_zero_step.md`, zero-step summary | FVT strongly improves zero-step target MLM proxy, but this is intrinsic-only evidence | ready | matched after-MLM PPPL exists for `v5_random` and `v5_fvt` |
| 10. Training Setup | `running_status.md`, `table_05_training_status.md` | `v5_random` selected 10K checkpoint exists; `v5_fvt` is running; post-checkpoint evaluation locked | execution-in-progress | selected `v5_random` and `v5_fvt` checkpoints exist |
| 11. Glot500 Metrics | coverage audit, `metric_mapping.md` | all Glot500 metric families retained with coverage/status notes; Bible and Roundtrip baseline/reference measured | ready as protocol | update if coverage changes or v5 metric rows are measured |
| 12. Current Measured Rows | `09_aggregation/`, `00_tables/`, `current_result_snapshot.md` | baseline/reference rows and v5-random diagnostic rows are measured for available PPPL, Tatoeba, Bible, Taxi1500, NER, POS, and Roundtrip; v5-FVT rows wait for checkpoint | partial | paired v5 method rows measured or explicit blockers parsed |
| 13. Coverage And Limitations | `table_04_evaluation_coverage.md`, `table_09_blocked_metric_notes.md` | PPPL has target10 10/10 coverage; retained downstream task families have target10 0/10; pending v5 rows are explicit | ready | update if target task data is materialized |
| 14. Conclusion | `claim_ledger.md`, `result_interpretation_blocks.md`, `method_comparison_summary.md`, `comparison_materiality_audit.md`, `ppt_content.md` | current-safe setup + zero-step novelty conclusion is written; downstream remains pending; materiality bands will control final wording strength | partial | choose outcome block after v5 results are parsed, then avoid strong wording for `small` or `tie_band` comparisons |
| 15. Backup Artifacts | source map, runbooks, audit files | commands, artifacts, gates, and audits are available | ready | add selected checkpoint paths and final logs |

## Slide Claim Locks

| Risky slide claim | Current handling | Required evidence to unlock |
| --- | --- | --- |
| FVT improves after continued MLM | phrase as hypothesis | matched `v5_random`/`v5_fvt` PPPL rows |
| FVT improves downstream metrics | do not claim | available downstream rows for both v5 checkpoints |
| Target10 downstream improves | do not claim | target10 task coverage and parsed target results |
| Glot500-base is an equal-budget baseline | call it external reference | not unlockable in v5 |
| POS Glot500-base final score | measured row is allowed with `TRAIN_LANGS=tur_Latn` caveat | already parsed by aggregation |
| Full Glot500 reproduction | disallowed | not unlockable in 102-language scope |

## Deck Update Order

After a new measured result appears:

1. For v5 method rows, run `bash scripts/run_v5_post_checkpoint_evals.sh status`.
2. Confirm `post_checkpoint_execution_plan.md` for launch env, output/log paths, and promotion rules.
3. Prefer `SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all` for the current measured-row queue; use split PPPL/downstream phases only when staging long jobs.
4. Run `python3 scripts/refresh_v5_reporting.py --with-plots`.
5. If figure inputs did not change, `python3 scripts/refresh_v5_reporting.py` is enough.
6. Update the relevant `00_tables/table_*.md`.
7. Update `ppt_content.md` slide 12 result rows and slide 14 conclusion slots.
8. Check `comparison_materiality_audit.md` so tiny deltas do not become strong slide claims.
9. Update `presenter_script_ko.md` and `talk_track.md` with the same wording.
10. Update `slide_claim_checklist.md`, `slide_asset_manifest.md`, and this matrix if a slide status changes.
11. Run stale search for unresolved result slots, old live step snapshots, and unsupported
   numeric claims.

## Current Deck Verdict

The deck is rehearsal-ready as an execution draft. It is not final because the
core method-result slides still require matched `v5_random`/`v5_fvt`
checkpoints and parsed downstream outputs.
