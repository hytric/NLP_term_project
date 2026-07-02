# Table 7. Tatoeba Retrieval Partial Results

Last updated: 2026-06-28

Caption draft:

```text
Tatoeba sentence retrieval is the first measured downstream baseline in v5.
Top-10 accuracy is higher-is-better. The table is partial: `xlmr_base` and
`glot500_base` are measured, `v5_random` is measured after the 10K random
checkpoint, and `v5_fvt` still requires matching model output.
```

| Model | Group | Top-10 accuracy | Languages | Status |
| --- | --- | ---: | ---: | --- |
| `xlmr_base` | head | 0.656309 | 63 | measured |
| `xlmr_base` | all available | 0.566067 | 98 | measured |
| `xlmr_base` | v5 target / tail | N/A | 0 | coverage-limited |
| `glot500_base` | head | 0.743755 | 63 | measured |
| `glot500_base` | all available | 0.706649 | 98 | measured |
| `glot500_base` | v5 target / tail | N/A | 0 | coverage-limited |
| `v5_random` | head | 0.700285 | 63 | measured random checkpoint |
| `v5_random` | all available | 0.610353 | 98 | measured random checkpoint |
| `v5_fvt` | head | waiting checkpoint | waiting checkpoint | waiting for matched checkpoint |
| `v5_fvt` | all available | waiting checkpoint | waiting checkpoint | waiting for matched checkpoint |

Source artifacts:

- `/home/axt/mnt2/jongha/v5_glot50010/evaluation/retrieval_tatoeba/xlmr_base/xlm-roberta-base/test_results.txt`
- `/home/axt/mnt2/jongha/v5_glot50010/evaluation/retrieval_tatoeba/glot500_base/cis-lmu__glot500-base/test_results.txt`
- `/home/axt/mnt2/jongha/v5_glot50010/evaluation/retrieval_tatoeba/v5_random/__home__axt__mnt2__jongha__v5_glot50010__runs__v5_random_mlm_10k/test_results.txt`
- `docs/exp/v5/3_evaluation/09_aggregation/main_head_tail_all.tsv`
- `docs/exp/v5/3_evaluation/09_aggregation/metric_completion.tsv`
