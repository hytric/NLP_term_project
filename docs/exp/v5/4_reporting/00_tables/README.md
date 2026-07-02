# 00 Tables

Use this folder for final TSV/CSV/Markdown tables used in slides and report.

## Next Step Gate

Move tables into `../02_slides/` and `../03_final_report/` only after every
number has a traceable source.

Pass line:

- each table has a source result path or aggregation command.
- metric direction and units are written.
- head/tail/all and v5-target subset tables are separated.
- missing or blocked metrics are labeled, not blank.
- table values match `../../3_evaluation/09_aggregation/`.

Required artifacts:

- final table file
- source-path note
- table caption draft
- last-updated note

If a table is manually edited, record the raw source file and copied columns.

Current draft tables:

- `table_01_data_scope.md`
- `table_02_tokenizer_audit.md`
- `table_03_initialization_zero_step.md`
- `table_04_evaluation_coverage.md`
- `table_04_evaluation_coverage.tsv`
- `table_05_training_status.md`
- `table_06_pppl_partial.md`
- `table_07_tatoeba_partial.md`
- `table_08_text_classification_partial.md`
- `table_09_blocked_metric_notes.md`
- `table_10_ner_partial.md`
- `table_11_pos_partial.md`
- `table_12_bible_partial.md`
- `table_13_metric_fidelity_matrix.md`
- `table_14_roundtrip_partial.md`
- `table_15_glot500_reproduction_fidelity.md`
- `source_map.md`

These tables are draft-ready for slides/report, but final downstream result
tables still wait on matched MLM checkpoints and metric execution.
