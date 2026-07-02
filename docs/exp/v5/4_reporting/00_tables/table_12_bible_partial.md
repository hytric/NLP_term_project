# Table 12. Bible Retrieval Partial Results

Last updated: 2026-06-27

Caption draft:

```text
Bible sentence retrieval is retained as a required Glot500 metric family.
Top-10 accuracy is higher-is-better. The current local Bible materialization
covers 74/102 language-scripts, all in the head/available group, and 0/10
selected v5 target languages. The table is partial: `xlmr_base` and
`glot500_base` and `v5_random` are measured, while `v5_fvt` still requires
the matched checkpoint output.
```

| Model | Group | Top-10 accuracy | Languages | Status |
| --- | --- | ---: | ---: | --- |
| `xlmr_base` | head | 0.381153 | 74 | measured |
| `xlmr_base` | all available | 0.381153 | 74 | measured |
| `xlmr_base` | v5 target / tail | N/A | 0 | coverage-limited |
| `glot500_base` | head | 0.509356 | 74 | measured external reference |
| `glot500_base` | all available | 0.509356 | 74 | measured external reference |
| `glot500_base` | v5 target / tail | N/A | 0 | coverage-limited |
| `v5_random` | head | 0.328019 | 74 | measured |
| `v5_random` | all available | 0.328019 | 74 | measured |
| `v5_fvt` | head | waiting checkpoint | waiting checkpoint | waiting for matched checkpoint |
| `v5_fvt` | all available | waiting checkpoint | waiting checkpoint | waiting for matched checkpoint |

Interpretation notes:

- The current `head` and `all available` Bible scores are identical because all
  74 materialized Bible retrieval rows belong to the head group.
- The selected v5 target10 has `0/10` Bible retrieval coverage under the
  Glot500 Bible task flags, so Bible retrieval cannot support a target10
  downstream improvement claim.
- `san_Latn` has a local source/script-label caveat documented in
  `../../3_evaluation/03_retrieval_bible/README.md`; do not use it for
  script-specific claims without manual verification.

Source artifacts:

- `/home/axt/mnt2/jongha/v5_glot50010/evaluation/retrieval_bible/xlmr_base/xlm-roberta-base/test_results.txt`
- `/home/axt/mnt2/jongha/v5_glot50010/evaluation/retrieval_bible/glot500_base/cis-lmu__glot500-base/test_results.txt`
- `/home/axt/mnt2/jongha/v5_glot50010/evaluation/retrieval_bible/v5_random/__home__axt__mnt2__jongha__v5_glot50010__runs__v5_random_mlm_10k/test_results.txt`
- `docs/exp/v5/3_evaluation/00_coverage/coverage_retrieval_bible.tsv`
- `docs/exp/v5/3_evaluation/09_aggregation/main_head_tail_all.tsv`
- `docs/exp/v5/3_evaluation/09_aggregation/metric_completion.tsv`
