# Table 11. POS Partial Results

Last updated: 2026-06-28 09:08 KST.

Source:

```text
docs/exp/v5/3_evaluation/09_aggregation/main_head_tail_all.tsv
/home/axt/mnt2/jongha/v5_glot50010/evaluation/pos/xlmr_base/xlm-roberta-base/test_results.txt
/home/axt/mnt2/jongha/v5_glot50010/evaluation/pos/glot500_base/glot500-base/test_results.txt
/home/axt/mnt2/jongha/v5_glot50010/evaluation/pos/v5_random/v5_random_mlm_10k/test_results.txt
```

Metric direction: higher F1 is better.

Coverage note: local POS materialization covers available task languages only
and has target10 coverage `0/10`. The `xlmr_base`, `glot500_base`, and
`v5_random` runs use `TRAIN_LANGS=tur_Latn` because local POS has no
`train-eng_Latn.tsv`.

| Group | Model | F1 | Languages | Source |
| --- | --- | ---: | ---: | --- |
| all available | `xlmr_base` | 0.481336 | 18 | `09_aggregation/main_head_tail_all.tsv` |
| head | `xlmr_base` | 0.571446 | 9 | `09_aggregation/main_head_tail_all.tsv` |
| all available | `glot500_base` | 0.567542 | 18 | `09_aggregation/main_head_tail_all.tsv` |
| head | `glot500_base` | 0.573832 | 9 | `09_aggregation/main_head_tail_all.tsv` |
| all available | `v5_random` | 0.481102 | 18 | `09_aggregation/main_head_tail_all.tsv` |
| head | `v5_random` | 0.587430 | 9 | `09_aggregation/main_head_tail_all.tsv` |

Pending rows:

- `v5_fvt`: waiting for matched MLM checkpoint.
