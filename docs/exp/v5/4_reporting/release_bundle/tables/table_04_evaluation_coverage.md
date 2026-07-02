# Table 4. Evaluation Coverage Boundary

Last updated: 2026-06-28 18:08 KST

Caption draft:

```text
All Glot500 metric families are retained, but local and upstream task
coverage differs by metric. The selected target10 has raw-text PPPL
coverage, while the currently materialized downstream task lists do
not include the selected target10 language-scripts.
```

| Metric | Local data / 102 | Head data / 92 | Target10 data / 10 | Blocked or missing / 102 | Current interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| Pseudoperplexity | 102 | 92 | 10 | 0 | raw-text intrinsic metric; target10 coverage is available; v5_random is measured and v5_fvt waits for its matched checkpoint |
| Tatoeba retrieval | 63 | 63 | 0 | 39 | available-language retrieval replay; selected target10 is absent from local task flags |
| Bible retrieval | 74 | 74 | 0 | 28 | available-language retrieval replay over the local Bible set; selected target10 is absent from task flags |
| Text classification | 1 | 1 | 0 | 101 | local Taxi1500 materialization is narrow; selected target10 is absent from local splits |
| NER | 78 | 78 | 0 | 24 | available-language tagging replay; selected target10 is absent from local PAN-X task flags |
| POS | 58 | 58 | 0 | 44 | available-language tagging replay; selected target10 is absent from local UD-POS task flags |
| Roundtrip alignment | 74 | 74 | 0 | 28 | available-language alignment replay using the local Bible-proxy materialization; selected target10 is absent from task flags |

Report rule:

Downstream results should be presented as available-language/head/all
Glot500 metric replay. Target10 downstream improvement should not be
claimed unless new task data is acquired, materialized, and documented.

Source artifacts:

- `docs/exp/v5/3_evaluation/00_coverage/coverage_summary.tsv`
- `docs/exp/v5/3_evaluation/00_coverage/results.md`
- `docs/exp/v5/3_evaluation/09_aggregation/metric_completion.tsv`
