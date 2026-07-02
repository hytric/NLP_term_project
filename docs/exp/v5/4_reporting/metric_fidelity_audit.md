# v5 Glot500 Metric Fidelity Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `metric_fidelity_needs_repair`

This generated audit verifies that every Glot500 metric family is
present in the v5 requirement document, wrapper/mapping layer, coverage
artifacts, aggregation completion table, and reporting fidelity matrix.
It does not claim final v5 method results; it checks whether the metric
surface is faithfully retained and explicitly gated.

| Metric | Status | Requirements | Mapping | Wrapper | Coverage | Completion | Measured | Missing | Table 13 | Claim boundary | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pseudoperplexity | ready | ready | ready | ready | 102/102; target=10/10 | partial | glot500_base,v5_random,xlmr_base | v5_fvt | ready | target10 intrinsic evidence allowed; v5_random diagnostic row measured; v5_fvt pending | none |
| retrieval_tatoeba | needs_repair | ready | ready | ready | 63/102; target=0/10 | measured | glot500_base,v5_fvt,v5_random,xlmr_base | - | ready | available-language downstream replay; target10 coverage-limited; paired v5 rows measured; promote only through claim gates | repair accounting |
| retrieval_bible | needs_repair | ready | ready | ready | 74/102; target=0/10 | measured | glot500_base,v5_fvt,v5_random,xlmr_base | - | ready | available-language downstream replay; target10 coverage-limited; paired v5 rows measured; promote only through claim gates | repair accounting |
| text_classification | needs_repair | ready | ready | ready | 1/102; target=0/10 | measured | glot500_base,v5_fvt,v5_random,xlmr_base | - | ready | narrow local classification evidence; target10 coverage-limited; paired v5 rows measured; promote only through claim gates | repair accounting |
| ner | ready | ready | ready | ready | 78/102; target=0/10 | partial | glot500_base,v5_random,xlmr_base | v5_fvt | ready | available-language tagging replay; target10 coverage-limited; v5_random diagnostic row measured; v5_fvt pending | none |
| pos | ready | ready | ready | ready | 58/102; target=0/10 | partial | glot500_base,v5_random,xlmr_base | v5_fvt | ready | available-language tagging replay with local train-language caveat; v5_random diagnostic row measured; v5_fvt pending | none |
| roundtrip_alignment | ready | ready | ready | ready | 74/102; target=0/10 | partial | glot500_base,v5_random,xlmr_base | v5_fvt | ready | available-language alignment evidence; target10 coverage-limited; v5_random diagnostic row measured; v5_fvt pending | none |

Interpretation rule:

- `ready_current_v5_pending` means the metric family is faithfully
  retained, baseline/reference rows are accounted for where local data
  exists, and the remaining gap is the matched v5 model rows.
- `accepted_blocked` means the metric family remains required but is
  explicitly blocked by local data/runner availability.
- This audit must be refreshed after checkpoint promotion and after any
  downstream data materialization change.
