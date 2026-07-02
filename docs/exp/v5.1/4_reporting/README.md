# v5.1 Reporting

This folder is the report/PPT surface for the corrected strict experiment.
The current version is a live scaffold: methodology, data scope, evaluation
coverage, and claim boundaries are ready; metric values are inserted after
the `v51_random` and `v51_fvt` checkpoints finish.

## Source Of Truth

| Need | Source |
| --- | --- |
| experiment end summary | `../EXPERIMENT_END_SUMMARY_KO.md` |
| current status / ETA | `../CURRENT_STATUS_KO.md` |
| execution plan | `../Plan.md` |
| data composition | `../0_tokenizer/00_data_scope/strict_data_composition_by_language.md` |
| evaluation coverage | `../3_evaluation/00_coverage/coverage_summary.tsv` |
| post-checkpoint evaluation | `../3_evaluation/POST_CHECKPOINT_EVAL_RUNBOOK_KO.md` |
| aggregated metrics | `../3_evaluation/09_aggregation/main_head_tail_all.tsv` |
| data/eval coverage table | `00_tables/table_01_data_eval_coverage.md` |
| live training table | `00_tables/table_02_training_status.md` |
| training curve figure | `01_figures/training_loss_lr.svg` |
| main metric result table | `00_tables/table_03_main_metric_results.md` |
| main metric template | `00_tables/table_03_main_metric_template.md` |
| similarity result table | `00_tables/table_04_similarity_results.md` |
| similarity template | `00_tables/table_04_similarity_template.md` |
| training trace | `00_tables/table_05_training_trace.md` |
| metric completion gate | `00_tables/table_06_metric_completion.md` |
| dataset size summary | `00_tables/table_07_dataset_sizes.md` |
| data/language selection slides | `02_slides/data_language_selection_ppt_ko.md` |
| report draft | `03_final_report/paper_draft_ko.md` |
| PPT content | `02_slides/ppt_content_ko.md` |

## Current Claim Boundary

```text
Main experiment = v5.1 strict 5% / 3K matched pair
Main novelty = random vs FVT new-token embedding initialization
Final PPPL = held-out test only
v5 train-source PPPL = diagnostic/fallback only
```

Target10 downstream claims are allowed for Tatoeba, Bible, NER, and Roundtrip
only where target data exists. POS and Taxi1500 remain available-language
Glot500 metric replays, not target10 evidence.

## Live Status Refresh

Use this one-command refresh to update the visible dashboard, training table,
training curve figure, model matrix, and checkpoint readiness status while MLM
is running:

```bash
bash scripts/refresh_v51_live_status.sh
```

Internally this reads the trainer log, process status, GPU snapshot, model
matrix, post-checkpoint readiness gate, and metric aggregation status, then
copies the latest step/loss/ETA into the top-level README, current status,
checklist, evaluation README, report draft, PPT content, and training trace
table. It also regenerates `01_figures/training_loss_lr.svg` and generated
metric/similarity result tables for the report/PPT.
