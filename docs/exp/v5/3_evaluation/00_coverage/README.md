# 00 Coverage

Use this folder for task coverage audits. Every required metric must have a
coverage file with at least:

```text
task	language_script	group	has_data	reason
```

Do not silently drop languages from final tables.

Canonical command:

```bash
python3 scripts/audit_v5_eval_coverage.py
```

Current local coverage summary is stored in:

```text
coverage_summary.tsv
results.md
```

Language-source and overlap explanation:

```text
../../LANGUAGE_SOURCE_OVERLAP_KO.md
```

Interpretation note: the coverage counts in this folder are intersections
between the controlled v5 `102` Glot500 language-script subset and each locally
materialized evaluation resource. PPPL covers all `102` raw-text languages;
Tatoeba/Bible/Roundtrip/Taxi1500/NER/POS cover only the available task subsets.

Current evaluation model matrix is stored in:

```text
../model_matrix.tsv
../model_matrix.md
```

## Next Step Gate

Move to metric-specific folders only after coverage is explicit for every
required Glot500 metric.

Pass line:

- one coverage file exists for each required metric.
- every selected target language is marked covered, missing, or not applicable.
- every measured head/seen language is labeled.
- exclusion reasons use stable labels such as `missing_dataset`,
  `missing_parallel_text`, `unsupported_script`, or `not_in_task`.
- model matrix for evaluation is written.

Required artifacts:

- `coverage_pseudoperplexity.tsv`
- `coverage_retrieval_tatoeba.tsv`
- `coverage_retrieval_bible.tsv`
- `coverage_text_classification.tsv`
- `coverage_ner.tsv`
- `coverage_pos.tsv`
- `coverage_roundtrip_alignment.tsv`
- coverage summary table
- evaluation model matrix

If coverage is incomplete, metric runs may start for debugging but final
aggregation must wait.
