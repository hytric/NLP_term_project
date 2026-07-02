# v5 Manuscript Completion Matrix

Last updated: 2026-06-28

This matrix maps the final paper-style report sections to the evidence that is
already safe to use and the gates that still control final wording. It prevents
the final report from mixing measured results, live progress, and blocked-data
limitations.
Current checkpoint progress should be read from `../final_action_dashboard_ko.md`
or `bash scripts/run_v5_post_checkpoint_evals.sh status`; this matrix tracks
section-level completion and final wording gates.

## Section Matrix

| Report section | Current source | Evidence already available | Status | Finalization action |
| --- | --- | --- | --- | --- |
| Title and abstract | `paper_draft.md`, `contribution_summary.md`, `result_interpretation_blocks.md`, `../post_checkpoint_outcome_matrix_ko.md` | controlled 102-language scope; zero-step FVT advantage; downstream caveat; outcome-specific abstract update blocks | draft-ready | revise final abstract result sentences from `Final Abstract Update Choices` after matched v5 PPPL/downstream rows exist |
| Introduction | `paper_draft.md`, `Report.md` | motivation, Glot500 controlled-replay framing, embedding-init novelty | ready | keep full-Glot500 boundary explicit |
| Related work | `Report.md`, `paper_draft.md`, `citation_source_map.md` | dedicated paper section distinguishes Glot500 reproduction target from Yamaguchi-style vocabulary-expansion inspiration | ready | keep Yamaguchi as inspiration/ablation label, not v5 tokenizer method |
| Data | `README.md`, `Plan.md`, tokenizer data manifests | target10 manifest, 92+10 design, full merge PASS | ready | no change unless data scope changes |
| Tokenizer method | `Report.md`, tokenizer audit tables | extended vocab 368,687; appended 118,685; `<mask>` id remap; fertility audit | ready with caveat | keep `dzo_Tibt` regression in main text |
| Embedding initialization method | `Report.md`, init reports, zero-step summary | identity row copy; `<mask>` diff 0.0; byte-row accounting; LM-head tied | ready | no final-result dependency |
| Continued MLM setup | `Report.md`, `running_status.md`, training status table | paired launcher active; same tokenizer/corpus/schedule planned | execution-in-progress | replace live status with selected checkpoint paths after both runs finish |
| Evaluation protocol | `metric_mapping.md`, `glot500_metric_requirements.md`, coverage audits | all Glot500 metric families retained; coverage files exist; Bible and Roundtrip baseline/reference rows measured for available languages | ready as protocol | keep Bible/Roundtrip v5 checkpoint gaps explicit unless measured |
| Baseline/reference results and diagnostic random rows | `09_aggregation/`, `00_tables/` | PPPL, Tatoeba, Bible, Taxi1500, NER, POS, and Roundtrip XLM-R/Glot500-base rows where local data exists; v5-random rows parsed as diagnostic evidence | ready with coverage caveats | keep POS `TRAIN_LANGS=tur_Latn`, downstream coverage notes, and the single-model diagnostic boundary visible |
| v5 method results: paired comparisons | `09_aggregation/` | zero-step intrinsic rows and v5-random diagnostic rows exist | pending | add paired after-MLM PPPL and downstream comparisons only after matched v5-FVT rows parse |
| Analysis | `result_interpretation_blocks.md`, `../post_checkpoint_outcome_matrix_ko.md`, `claim_ledger.md`, `../method_comparison_summary.md`, `../comparison_materiality_audit.md`, `../final_claim_decision_tree.md` | FVT zero-step advantage; tokenizer fertility result; coverage limitations; practical materiality bands for final wording | draft-ready | select the decision-tree outcome after v5 rows exist, then use materiality bands to control wording strength |
| Limitations | `paper_draft.md`, `claim_ledger.md` | no full 511-language claim; target10 downstream coverage 0/10; external reference caveat | ready | update only if coverage or blocked metrics change |
| Conclusion | `claim_ledger.md`, `result_interpretation_blocks.md`, `../post_checkpoint_outcome_matrix_ko.md`, `../final_claim_decision_tree.md` | setup completed; zero-step novelty supported | partial | final paragraph follows the generated decision-tree outcome and Korean outcome matrix |
| Reproducibility appendix | `reproducibility_appendix.md` | paths, commands, wrapper, promotion rules | ready | add selected checkpoint paths and final command logs |
| References | `paper_draft.md`, `paper_draft_ko.md`, `references.bib`, `citation_source_map.md` | Glot500 and Yamaguchi references listed with BibTeX/Korean entries and claim boundaries | ready | format according to final submission style if needed |

Assembly-level source:

```text
paper_build_spec.md
```

Use it as the final section-by-section build checklist before freezing the
paper.

## Final Report Claim Locks

| Locked claim | Current wording | Unlock gate |
| --- | --- | --- |
| after-MLM FVT improvement | hypothesis / pending result | both `v5_random` and `v5_fvt` selected checkpoints exist and PPPL is parsed |
| downstream FVT improvement | not claimed | available downstream tasks are parsed for both v5 checkpoints |
| target10 downstream improvement | disallowed for now | target10 downstream task data is materialized and evaluated |
| Glot500-base as equal-budget baseline | disallowed | not unlockable without equal-budget retraining |
| full 511-language reproduction | disallowed | not unlockable within the 102-language v5 scope |
| POS Glot500-base final row | measured with `TRAIN_LANGS=tur_Latn` caveat | already parsed by aggregation |

## Finalization Order

Use this order after any new result appears:

1. For v5 model results, first run `bash scripts/run_v5_post_checkpoint_evals.sh status`.
2. Confirm `post_checkpoint_execution_plan.md` for launch env, output/log paths, and promotion rules.
3. Prefer `SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all` for the current measured-row queue; use split PPPL/downstream phases only when staging long jobs.
4. `python3 scripts/refresh_v5_reporting.py --with-plots`
5. If figure inputs did not change, `python3 scripts/refresh_v5_reporting.py` is enough.
6. Check `finalization_gate_status.md` and `reporting_package_audit.md`.
7. Update `00_tables/`.
8. Update `Report.md` and `paper_draft.md`.
9. Check `final_claim_decision_tree.md` and `post_checkpoint_outcome_matrix_ko.md` before choosing conclusion wording.
10. Check `comparison_materiality_audit.md`; treat `tie_band` as no clear
   practical separation and keep `small` wins cautious.
11. Update `claim_ledger.md` and `result_interpretation_blocks.md` if claim
   status changes.
12. Update the abstract using `Final Abstract Update Choices` before freezing
   the final paper.
13. Update `ppt_content.md`, `presenter_script_ko.md`, and
   `slide_claim_checklist.md`.
14. Run a stale search for live snapshots, unresolved result slots, and
   unsupported numeric claims.

## Ready-To-Write Position

The final manuscript can already be written as a strong execution draft with
three completed pillars:

- controlled Glot500-style replay setup over `92 + 10` language-scripts;
- structurally audited SentencePiece vocabulary expansion and initialization;
- zero-step evidence that FVT improves target MLM proxy loss over random.

The paper should remain an execution draft until the fourth pillar is proven:
matched after-MLM and available downstream results for `v5_random` and
`v5_fvt`.
