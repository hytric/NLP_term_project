# Table 14. Roundtrip Alignment Partial Results

Last updated: 2026-06-28

Caption draft:

```text
Roundtrip alignment is retained as a required Glot500 metric family. Accuracy
is higher-is-better. The current local Roundtrip materialization uses
Bible-derived JSONL inputs for 74/102 available language-scripts and 0/10
selected v5 target languages. The table is partial: `xlmr_base`,
`glot500_base`, and `v5_random` are measured, while `v5_fvt` still requires
its matched model output before a method comparison can be promoted.
```

| Model | Group | Accuracy | Languages | Status |
| --- | --- | ---: | ---: | --- |
| `xlmr_base` | head | 0.185300 | 74 | measured |
| `xlmr_base` | all available | 0.185300 | 74 | measured |
| `xlmr_base` | v5 target / tail | N/A | 0 | coverage-limited |
| `glot500_base` | head | 0.205189 | 74 | measured external reference |
| `glot500_base` | all available | 0.205189 | 74 | measured external reference |
| `glot500_base` | v5 target / tail | N/A | 0 | coverage-limited |
| `v5_random` | head | 0.190300 | 74 | measured |
| `v5_random` | all available | 0.190300 | 74 | measured |
| `v5_fvt` | head | waiting checkpoint | waiting checkpoint | waiting for matched checkpoint |
| `v5_fvt` | all available | waiting checkpoint | waiting checkpoint | waiting for matched checkpoint |

Interpretation notes:

- The current `head` and `all available` Roundtrip scores are identical because
  all 74 materialized Roundtrip rows belong to the available head group.
- The selected v5 target10 has `0/10` Roundtrip coverage under the local
  Bible-derived task materialization, so Roundtrip cannot support a target10
  downstream improvement claim.
- Roundtrip is now measured for baseline/reference models and `v5_random`, not
  a blocked-data stand-in. The remaining model gap is the matched `v5_fvt`
  row.

Source artifacts:

- `/home/axt/mnt2/jongha/v5_glot50010/evaluation/roundtrip_alignment/xlmr_base/test_results.txt`
- `/home/axt/mnt2/jongha/v5_glot50010/evaluation/roundtrip_alignment/glot500_base/test_results.txt`
- `/home/axt/mnt2/jongha/v5_glot50010/evaluation/roundtrip_alignment/v5_random/test_results.txt`
- `docs/exp/v5/3_evaluation/00_coverage/coverage_roundtrip_alignment.tsv`
- `docs/exp/v5/3_evaluation/07_roundtrip_alignment/materialization_summary.tsv`
- `docs/exp/v5/3_evaluation/09_aggregation/main_head_tail_all.tsv`
- `docs/exp/v5/3_evaluation/09_aggregation/metric_completion.tsv`
