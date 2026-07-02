# v5 Report-Slide Crosswalk

Last updated: 2026-06-28

This file ties the final report, final slides, and evidence artifacts together.
Use it as the assembly map before promoting the v5 package from execution draft
to final report/PPT.

## Section And Slide Map

| Report section | Slide(s) | Required evidence | Current promotion status |
| --- | --- | --- | --- |
| Title, abstract, and one-sentence claim | 1, 14 | `03_final_report/paper_draft.md`; `03_final_report/claim_ledger.md`; `current_result_snapshot.md` | execution draft; final claim waits for matched v5 rows |
| Introduction, motivation, and contributions | 2 | `03_final_report/contribution_summary.md`; `03_final_report/citation_source_map.md`; `../Plan.md`; `../README.md` | ready |
| Related work and positioning | 2, 3, 6, 7 | `03_final_report/citation_source_map.md`; `02_slides/slide_citation_map.md`; `03_final_report/references.bib` | ready |
| Scope boundary and research questions | 3 | `../goal_readiness.md`; `03_final_report/claim_ledger.md`; `00_tables/table_15_glot500_reproduction_fidelity.md`; `pending_result_registry.md` | ready with explicit pending gates |
| Data design: 92 seen + 10 target languages | 4, 5 | `00_tables/table_01_data_scope.md`; target manifest; merge report | ready |
| Tokenizer reproduction setup | 6 | `00_tables/table_02_tokenizer_audit.md`; `01_figures/generated/figure_02_tokenizer_fertility_delta.png` | ready for tokenizer evidence |
| Embedding initialization novelty | 7, 8, 9 | `00_tables/table_03_initialization_zero_step.md`; `01_figures/generated/figure_03_zero_step_initialization.png`; initialization reports | ready as audit + zero-step novelty evidence |
| Continued MLM training setup | 10 | `00_tables/table_05_training_status.md`; `../2_training/05_checkpoint_selection/selected_checkpoint_manifest.md`; `../3_evaluation/model_matrix.md`; `../3_evaluation/running_status.md` | live status only; final waits for selected checkpoints |
| Evaluation protocol | 11 | `00_tables/table_04_evaluation_coverage.md`; `00_tables/table_13_metric_fidelity_matrix.md`; `../3_evaluation/metric_mapping.md`; `../3_evaluation/glot500_metric_requirements.md` | ready as protocol; execution partial |
| Baseline/reference results and diagnostic v5-random rows | 12 | `00_tables/table_06_pppl_partial.md` through `00_tables/table_12_bible_partial.md`; `00_tables/table_14_roundtrip_partial.md`; `00_tables/table_09_blocked_metric_notes.md`; `00_tables/table_13_metric_fidelity_matrix.md`; `current_result_snapshot.md`; `../3_evaluation/09_aggregation/` | current baseline/reference rows and v5-random diagnostic rows ready; v5-FVT rows pending checkpoint |
| Novelty analysis and interpretation | 9, 14 | `03_final_report/result_interpretation_blocks.md`; `post_checkpoint_outcome_matrix_ko.md`; `03_final_report/claim_ledger.md`; `00_tables/table_03_initialization_zero_step.md` | zero-step analysis ready; final outcome waits for after-MLM rows |
| Limitations and fidelity boundary | 13 | `00_tables/table_04_evaluation_coverage.md`; `00_tables/table_09_blocked_metric_notes.md`; `00_tables/table_13_metric_fidelity_matrix.md`; `00_tables/table_15_glot500_reproduction_fidelity.md`; `../3_evaluation/07_roundtrip_alignment/blocker_audit.md`; `pending_result_registry.md` | ready |
| Conclusion and next steps | 14 | `03_final_report/claim_ledger.md`; `03_final_report/result_interpretation_blocks.md`; `post_checkpoint_outcome_matrix_ko.md`; `finalization_gate_status.md` | execution draft; final wording depends on v5 rows and the outcome matrix |
| Reproducibility appendix and backup | 15 | `03_final_report/reproducibility_appendix.md`; `03_final_report/citation_source_map.md`; `02_slides/slide_citation_map.md`; `../2_training/05_checkpoint_selection/selected_checkpoint_manifest.md`; `../3_evaluation/post_checkpoint_eval_queue.md`; `00_tables/source_map.md` | ready as command/path appendix |

## Promotion Rules

- Numeric claims must come from `../3_evaluation/09_aggregation/` or
  `00_tables/`; live logs can describe status but cannot become final results.
- Citations can support background and method lineage, but local measured
  values must come from tables, figures, aggregation files, or audit artifacts.
- `v5_random` rows that exist before `v5_fvt` are diagnostic and may show
  pipeline health, but they are not final method win/loss evidence.
- Paired `v5_random` and `v5_fvt` downstream claims are inserted only after
  matched checkpoints exist and the paired evaluation queue has been run.
- Target10 downstream coverage remains a limitation unless a metric has explicit
  target10 files. Current target10 coverage is PPPL only.
- Tatoeba, Bible, text classification, NER, POS, and Roundtrip baseline/reference rows are
  valid only for the local language coverage stated in their result tables.
- Bible retrieval currently has measured `xlmr_base`, `glot500_base`, and
  `v5_random` rows over 74 language-scripts; the `v5_fvt` row remains
  checkpoint-pending.
- Roundtrip currently has measured `xlmr_base`, `glot500_base`, and
  `v5_random` rows over 74 language-scripts; the `v5_fvt` row remains
  checkpoint-pending and target10 coverage remains `0/10`.
- The final claim should compare `v5_fvt` and `v5_random` under matched corpus,
  tokenizer, and training budget before saying the initialization method helped.

## Current Safe Story Line

- This is a controlled Glot500-style reproduction package, not a full rerun of
  every original Glot500 training condition.
- The data design is intentionally conservative: 92 XLM-R-seen Glot500
  language-scripts plus 10 diverse Glot500-internal target language-scripts.
- The novelty is in vocabulary-extension embedding initialization, especially
  the FVT initialization versus random initialization under the same setup.
- The strongest completed novelty evidence so far is zero-step MLM NLL on the
  target10 set, where FVT is better than random and mean initialization.
- The final empirical claim is not locked until matched `v5_random` and
  `v5_fvt` checkpoints finish and the required Glot500 metric families are
  replayed where local data exists.
