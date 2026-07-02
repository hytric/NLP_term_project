# Table 10. NER Partial Results

Last updated: 2026-06-28 06:38 KST

Source:

```text
docs/exp/v5/3_evaluation/09_aggregation/main_head_tail_all.tsv
```

Raw result:

```text
/home/axt/mnt2/jongha/v5_glot50010/evaluation/ner/xlmr_base/xlm-roberta-base/test_results.txt
/home/axt/mnt2/jongha/v5_glot50010/evaluation/ner/glot500_base/glot500-base/test_results.txt
/home/axt/mnt2/jongha/v5_glot50010/evaluation/ner/v5_random/v5_random_mlm_10k/test_results.txt
```

| Metric | Model | Group | F1 | Coverage note |
| --- | --- | --- | ---: | --- |
| NER | `xlmr_base` | all available | 0.549858 | `164` actual runner language rows; aggregation status still tied to `78/102` v5 materialized coverage |
| NER | `xlmr_base` | head | 0.621207 | head languages present in the parsed output |
| NER | `xlmr_base` | v5-target actual intersection | 0.459364 | `fur_Latn` only; not a target10-wide downstream claim |
| NER | `glot500_base` | all available | 0.627108 | `164` actual runner language rows; external reference row |
| NER | `glot500_base` | head | 0.645915 | head languages present in the parsed output |
| NER | `glot500_base` | v5-target actual intersection | 0.553191 | `fur_Latn` only; not a target10-wide downstream claim |
| NER | `v5_random` | all available | 0.544628 | `164` actual runner language rows; random-initialized 10K checkpoint row |
| NER | `v5_random` | head | 0.608020 | head languages present in the parsed output |
| NER | `v5_random` | v5-target actual intersection | 0.560554 | `fur_Latn` only; not a target10-wide downstream claim |

Use this table as measured baseline/reference and random-checkpoint rows only.
The `v5_fvt` NER row remains pending until the matched MLM checkpoint exists.
