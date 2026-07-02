# v5 Aggregation Schema Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `aggregation_schema_ready`

This generated audit checks that aggregation outputs have the stable
schema required for final report/PPT promotion: metric completion rows,
normalized score rows, score directions, source files, and v5-target
subset consistency.

| Item | Status | Evidence | Action |
| --- | --- | --- | --- |
| aggregation output files | ready | all aggregation outputs exist | none |
| metric_completion columns | ready | columns=metric,primary_score,direction,coverage_languages,coverage_has_data_total,coverage_has_data_target,measured_models,missing_models,status,folder,note | none |
| score table columns | ready | main_columns=metric,summary_group,model_key,score_name,score_value,aux_score_name,aux_score_value,direction,source_file; target_columns=metric,summary_group,model_key,score_name,score_value,aux_score_name,aux_score_value,direction,source_file | none |
| required metric completion rows | ready | metrics=ner,pos,pseudoperplexity,retrieval_bible,retrieval_tatoeba,roundtrip_alignment,text_classification | none |
| metric score specs | ready | all primary scores, directions, statuses, and model sets are valid | none |
| normalized score rows | ready | rows=54 | none |
| v5 target subset consistency | ready | main_v5_target_rows=6; target_rows=6 | none |

Promotion rule:

- Final result values should be copied only from aggregation outputs
  after this audit is `aggregation_schema_ready`.
- If this audit fails, repair aggregation before updating report/PPT
  tables, conclusion text, or slide values.
