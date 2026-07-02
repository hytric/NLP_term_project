# 06 POS

Required Glot500 metric.

Report F1 and language coverage. Current selected-target intersection appears
limited, but the metric must still be run for available Glot500 eval languages.

## Next Step Gate

Move this metric to `../09_aggregation/` only after POS F1 and coverage are
complete for available languages.

Pass line:

- dataset/source and language list are recorded.
- training/evaluation protocol matches the Glot500-style setup as closely as
  possible.
- F1 or accuracy choice is explicit and consistent with the report table.
- selected target intersection is documented.
- every required model is included or has a failure/exclusion note.

Required artifacts:

- command log
- raw score output
- `summary.tsv` or `results.md`
- coverage reference
- hyperparameter note

If POS coverage does not overlap most selected targets, keep the metric as a
Glot500-required available-language evaluation and separate it from target-only
claims.

## Current Baseline Run

The `xlmr_base` POS baseline completed and has been parsed by
`09_aggregation/`.

Command:

```bash
TRAIN_LANGS=tur_Latn bash scripts/run_v5_eval_metric.sh pos xlmr_base 1
```

Why `tur_Latn`: the local POS materialization currently has no
`train-eng_Latn.tsv`. Available local POS train splits include `tur_Latn`, and
it is the largest available train split among the materialized POS languages.
This is a documented local-data deviation from an English-train tagging setup,
not a target10 claim.

Outer log:

```text
/home/axt/mnt2/jongha/v5_glot50010/logs/pos_xlmr_base_20260627_025850.outer.log
```

Output root:

```text
/home/axt/mnt2/jongha/v5_glot50010/evaluation/pos/xlmr_base/xlm-roberta-base
```

Promotion evidence, checked `2026-06-27 05:03 KST`:

- `test_results.txt`: `108` lines
- parsed by `scripts/aggregate_v5_metrics.py`
- parsed F1 rows:
  - all: `0.481336`
  - head: `0.571446`

## Current Reference Run

The `glot500_base` POS reference run completed and has been parsed by
`09_aggregation/`.

Command:

```bash
TRAIN_LANGS=tur_Latn bash scripts/run_v5_eval_metric.sh pos glot500_base 1
```

Outer log:

```text
/home/axt/mnt2/jongha/v5_glot50010/logs/pos_glot500_base_setsid_20260627_050224.outer.log
```

Output root:

```text
/home/axt/mnt2/jongha/v5_glot50010/evaluation/pos/glot500_base/glot500-base
```

Promotion evidence, checked `2026-06-27 07:12 KST`:

- `test_results.txt`: non-empty (`2658` bytes)
- parsed by `scripts/aggregate_v5_metrics.py`
- parsed F1 rows:
  - all: `0.567542`
  - head: `0.573832`
- train-language note: `TRAIN_LANGS=tur_Latn`

Operational fixes applied before this run:

- `evaluate_pos.py` now reads `pos_lang_list.txt` relative to the evaluator
  file.
- output and tokenized-cache directories are built with `os.path.join`.
- existing output dirs no longer disable training when `--overwrite_output_dir`
  is set.
- the train split is preprocessed for `args.train_langs`, enabling
  `TRAIN_LANGS=tur_Latn`.

## Current v5 Random Run

The `v5_random` POS run completed and has been parsed by `09_aggregation/`.
This row is available-language downstream evidence for the random-initialized
10K checkpoint; it is not a method-comparison win until the matched `v5_fvt`
POS row exists.

Command:

```bash
TRAIN_LANGS=tur_Latn bash scripts/run_v5_eval_metric.sh pos v5_random 0
```

Outer/command log:

```text
docs/exp/v5/3_evaluation/06_pos/v5_random/command_logs/run_v5_random_20260628_065606.log
```

Output root:

```text
/home/axt/mnt2/jongha/v5_glot50010/evaluation/pos/v5_random/v5_random_mlm_10k
```

Promotion evidence, checked `2026-06-28 09:08 KST`:

- `test_results.txt`: `108` lines
- parsed by `scripts/aggregate_v5_metrics.py`
- parsed F1 rows:
  - all: `0.481102`
  - head: `0.587430`
- train-language note: `TRAIN_LANGS=tur_Latn`
