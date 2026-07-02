# 02 Retrieval Tatoeba

Required Glot500 metric.

Report Top-10 accuracy and task coverage. If selected v5 target languages are
not present in Tatoeba, record the missing languages in `../00_coverage/`.

## Next Step Gate

Move this metric to `../09_aggregation/` only after Top-10 retrieval results and
coverage notes are complete.

Pass line:

- evaluated language pairs and direction are written.
- Top-10 accuracy is reported for every available model.
- missing selected target languages are listed in coverage.
- sentence embedding extraction settings are recorded.
- raw nearest-neighbor or score outputs are saved when practical.

Required artifacts:

- command log
- raw output or score file
- `summary.tsv` or `results.md`
- coverage reference
- model path list

If Tatoeba has no selected target coverage, still report head/all available
coverage and mark the v5-target subset as unavailable with reason.

## Current Measured Results

The `xlmr_base` baseline and `glot500_base` external-reference Tatoeba
retrieval runs completed and have been parsed by `09_aggregation/`.

Command logs:

```text
/home/axt/mnt2/jongha/v5_glot50010/logs/retrieval_tatoeba_xlmr_base_20260627_020823.log
/home/axt/mnt2/jongha/v5_glot50010/logs/retrieval_tatoeba_glot500_base_20260627_023323.log
```

Output roots:

```text
/home/axt/mnt2/jongha/v5_glot50010/evaluation/retrieval_tatoeba/xlmr_base/xlm-roberta-base
/home/axt/mnt2/jongha/v5_glot50010/evaluation/retrieval_tatoeba/glot500_base/cis-lmu__glot500-base
```

Measured rows:

| Group | Model | Top-10 accuracy | Languages | Source |
| --- | --- | ---: | ---: | --- |
| head | `xlmr_base` | 0.656309 | 63 | `../09_aggregation/main_head_tail_all.tsv` |
| all available | `xlmr_base` | 0.566067 | 98 | `../09_aggregation/main_head_tail_all.tsv` |
| head | `glot500_base` | 0.743755 | 63 | `../09_aggregation/main_head_tail_all.tsv` |
| all available | `glot500_base` | 0.706649 | 98 | `../09_aggregation/main_head_tail_all.tsv` |

The selected v5 target10 remains `0/10` for Tatoeba coverage, so this metric
currently supports available-language/head/all replay rather than target10
downstream improvement.

Operational fix:

- `evaluate_retrieval_tatoeba.py` now reads `tatoeba_lang_list.txt` relative to
  the evaluator file, so the v5 wrapper can run it from the repository root.
- `evaluate_retrieval_bible.py` received the same path fix for
  `bible_lang_list.txt`.
