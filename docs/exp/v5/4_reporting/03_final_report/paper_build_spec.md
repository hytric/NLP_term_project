# v5 Paper Build Spec

Last updated: 2026-06-28

This file turns `paper_draft.md` into an assembly-oriented checklist for the
final report. Use it with `manuscript_completion_matrix.md`,
`claim_ledger.md`, `result_interpretation_blocks.md` including its
`Final Abstract Update Choices`, `Korean Final Conclusion Choices`,
`../post_checkpoint_outcome_matrix_ko.md`, and
`../final_claim_decision_tree.md`.
Use `../final_action_dashboard_ko.md` and
`bash scripts/run_v5_post_checkpoint_evals.sh status` for live checkpoint
state; this build spec records the static report assembly contract.

Generate browser/print report artifacts with:

```bash
python3 scripts/build_v5_report_html.py
```

Outputs:

```text
docs/exp/v5/4_reporting/03_final_report/paper_draft.html
docs/exp/v5/4_reporting/03_final_report/paper_draft_ko.html
```

Generate PDF report artifacts with:

```bash
bash scripts/build_v5_report_pdf.sh
```

Outputs:

```text
docs/exp/v5/4_reporting/03_final_report/paper_draft.pdf
docs/exp/v5/4_reporting/03_final_report/paper_draft_ko.pdf
```

## Paper Rule

The final report should read like an executed experiment paper, not a proposal.
Completed setup evidence, measured metric rows, and explicit blocked-data notes
can be promoted. Live training steps, dev scores, and waiting checkpoints cannot
be promoted as result claims.

## Section Build Spec

| Section | Required content | Primary source | Claim gate |
| --- | --- | --- | --- |
| Title | controlled 102-language Glot500-style replay + vocabulary-extension initialization | `paper_draft.md`; `contribution_summary.md` | scope unchanged |
| Abstract | scope, method novelty, strongest measured evidence, remaining gate | `current_result_snapshot.md`; `claim_ledger.md`; `result_interpretation_blocks.md` `Final Abstract Update Choices` | update final result sentences after v5 rows using the decision-tree outcome |
| Introduction | uneven multilingual coverage, Glot500 motivation, appended-row initialization question | `Report.md`; `contribution_summary.md` | no final-result dependency |
| Related Work | Glot500 as reproduction target; Yamaguchi-style vocabulary expansion as inspiration/contrast | `Report.md`; `references.bib`; `citation_source_map.md` | citations retained |
| Scope Boundary | controlled subset claim; no full 511-language claim; Glot500-base external reference | `claim_ledger.md`; `goal_readiness.md` | boundary locked |
| Data | 92 seen + 10 target; target10 criteria; merge size and paths | `table_01_data_scope.md`; target manifest | merge unchanged |
| Tokenizer | Glot500-style SPM append; `<mask>` movement; fertility audit; `dzo_Tibt` caveat | `table_02_tokenizer_audit.md` | tokenizer unchanged |
| Initialization | random/mean/FVT definitions; identity copy; `<mask>` remap; byte rows; LM head tying | `table_03_initialization_zero_step.md`; init reports | no final-result dependency |
| Training | paired random/FVT 10K design, selected checkpoint rule, identical comparison budget | `running_status.md`; `model_matrix.md`; checkpoint selection docs | matched checkpoint paths |
| Evaluation | all Glot500 metric families retained, coverage and blocker accounting | `metric_mapping.md`; `table_04_evaluation_coverage.md`; `table_09_blocked_metric_notes.md`; `table_13_metric_fidelity_matrix.md` | coverage changes |
| Results: setup | corpus/tokenizer/init/zero-step rows | `00_tables/`; `current_result_snapshot.md` | ready now |
| Results: baselines | XLM-R and Glot500-base PPPL/downstream rows with coverage caveats | `09_aggregation/`; tables 06-13 | ready for measured rows |
| Results: v5 methods | after-MLM PPPL and available downstream `v5_random`/`v5_fvt` rows | `09_aggregation/`; `post_checkpoint_eval_queue.md`; `post_checkpoint_execution_plan.md` | matched model outputs parsed |
| Analysis | explain zero-step vs after-MLM vs downstream, tokenizer failure case, coverage effects | `result_interpretation_blocks.md`; `claim_ledger.md`; `../post_checkpoint_outcome_matrix_ko.md`; `../final_claim_decision_tree.md` | choose the generated decision-tree outcome and matching Korean conclusion block |
| Limitations | no full-scale reproduction, target10 downstream coverage gap, Bible/Roundtrip v5 checkpoint gaps, external reference caveat | `claim_ledger.md`; status tables | ready now |
| Reproducibility | local paths, commands, model keys, promotion rules, selected checkpoints | `reproducibility_appendix.md`; `source_map.md` | add final command logs |
| References | cited papers and code artifacts with claim boundaries | `references.bib`; `citation_source_map.md`; `paper_draft_ko.md` section 10 | ready |

## Build Artifacts

| Artifact | Source | Purpose | Final gate |
| --- | --- | --- | --- |
| `paper_draft.md` | maintained paper-style Markdown | English paper report source | update after result insertion |
| `paper_draft.html` | `scripts/build_v5_report_html.py` from `paper_draft.md` | browser/print English report artifact | regenerate after paper source changes |
| `paper_draft.pdf` | `scripts/build_v5_report_pdf.sh` from `paper_draft.html` | PDF English report artifact | regenerate after paper source changes |
| `paper_draft_ko.md` | maintained Korean paper-style Markdown | Korean final report/PPT writing source | update after result insertion |
| `paper_draft_ko.html` | `scripts/build_v5_report_html.py` from `paper_draft_ko.md` | browser/print Korean report artifact | regenerate after Korean paper source changes |
| `paper_draft_ko.pdf` | `scripts/build_v5_report_pdf.sh` from `paper_draft_ko.html` | PDF Korean report artifact | regenerate after Korean paper source changes |

## Must-Show Evidence

| Evidence | Required value/current value | Source |
| --- | ---: | --- |
| language scope | 92 seen + 10 target | `table_01_data_scope.md` |
| merged corpus lines | 92,452,251 | `table_01_data_scope.md` |
| missing language dirs | 0 | merge report |
| extended HF tokens | 368,687 | `table_02_tokenizer_audit.md` |
| appended token strings | 118,685 | `table_02_tokenizer_audit.md` |
| audited tokenizer improvement | 29/30 | `table_02_tokenizer_audit.md` |
| target10 tokenizer improvement | 9/10 | `table_02_tokenizer_audit.md` |
| documented tokenizer regression | `dzo_Tibt` 4.223938 -> 5.552124 tokens/word | `table_02_tokenizer_audit.md` |
| FVT rows | 118,427 | `table_03_initialization_zero_step.md` |
| `<mask>` max abs diff | 0.0 | init reports |
| LM head tied | true | init reports |
| zero-step target NLL random | 18.411756 | `table_03_initialization_zero_step.md` |
| zero-step target NLL FVT | 8.785518 | `table_03_initialization_zero_step.md` |
| FVT - random zero-step target NLL | -9.626238 | `table_03_initialization_zero_step.md` |
| XLM-R target PPPL | 61.980216 | `table_06_pppl_partial.md` |
| Glot500-base target PPPL | 15.102934 | `table_06_pppl_partial.md` |
| XLM-R Bible Top-10 | 0.381153 | `table_12_bible_partial.md` |
| Glot500-base Bible Top-10 | 0.509356 | `table_12_bible_partial.md` |
| XLM-R Roundtrip accuracy | 0.185300 | `table_14_roundtrip_partial.md` |
| Glot500-base Roundtrip accuracy | 0.205189 | `table_14_roundtrip_partial.md` |
| Glot500-base NER all F1 | 0.627108 | `table_10_ner_partial.md` |
| Glot500-base POS all F1 | 0.567542 | `table_11_pos_partial.md` |

## Outcome Decision Table

| Parsed result pattern | Final paper conclusion | PPT conclusion line | Claim status |
| --- | --- | --- | --- |
| FVT beats random on after-MLM PPPL and downstream is positive or neutral | initialization effect survives MLM; downstream evidence is supportive within coverage | FVT keeps its intrinsic advantage after matched MLM | method claim strengthened |
| FVT beats random on PPPL but downstream is mixed | intrinsic adaptation improves; downstream transfer is task/coverage-dependent | intrinsic gains are clearer than downstream transfer | bounded positive |
| FVT wins zero-step only, random catches up after MLM | FVT is an early-adaptation initializer, not a final-performance improvement under this budget | FVT gives a better start; MLM can wash out the gap | diagnostic contribution |
| FVT loses or is unstable after MLM | initialization changes early behavior but is insufficient alone; analyze tokenizer/coverage/training budget | initialization is not a guaranteed final gain | negative but useful |
| Bible and Roundtrip v5 rows remain checkpoint-pending | Bible and Roundtrip baseline/reference rows are reported as measured; v5 rows are pending | status rows are reported rather than silently dropped | fidelity boundary |
| target10 downstream coverage remains absent | target10 claims restricted to tokenization, initialization, and PPPL | target10 evidence is intrinsic | coverage-limited |

## Forbidden Paper Claims

- Full 511-language Glot500 reproduction.
- Equal-budget comparison with `cis-lmu/glot500-base`.
- Target10 downstream improvement while target10 downstream task coverage is
  absent outside PPPL.
- FVT after-MLM or downstream improvement before matched `v5_random` and
  `v5_fvt` outputs are parsed.
- Live training step, dev F1, or partially written output as a final result.
- Tokenizer improvement for every target language.

## Post-Checkpoint Paper Update

After both v5 checkpoints are `ready_for_wrapper=yes` and
`post_checkpoint_preflight.md` reports `post_checkpoint_preflight_ready_to_launch`:

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
python3 scripts/refresh_v5_reporting.py --with-plots
```

Use split phases only when staging long jobs:

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh pppl
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream
```

Then update in this order:

1. `2_training/05_checkpoint_selection/selected_checkpoint_manifest.md`
2. `00_tables/table_06_pppl_partial.md`
3. downstream tables 07, 08, 10, 11, and 12 where outputs exist
4. `00_tables/table_13_metric_fidelity_matrix.md` if coverage or blocker status changed
5. `01_figures/generated/figure_manifest.tsv` and `captions.md` if figure sources changed
6. `paper_draft.md` sections 7-12
7. `paper_draft_ko.md` sections 5-10, including reproducibility summary and Korean references
8. `claim_ledger.md`
9. `final_claim_decision_tree.md` to select the allowed outcome block
10. `post_checkpoint_outcome_matrix_ko.md` and `result_interpretation_blocks.md`, especially `Final Abstract Update Choices` and `Korean Final Conclusion Choices`, if outcome language changes
11. `citation_source_map.md` if related-work or citation boundaries changed
12. `manuscript_completion_matrix.md`
13. `reproducibility_appendix.md` with selected checkpoint paths and final logs
14. `Report.md`
15. `report_slide_crosswalk.md`
16. slide files under `02_slides/`

Before final handoff, run `scripts/refresh_v5_reporting.py` and confirm
`reporting_package_audit.md` reports no stale result-slot/live-snapshot hits.
