# 05 NER

Required Glot500 metric.

Report F1 and language coverage. Current selected-target intersection appears
limited, but the metric must still be run for available Glot500 eval languages.

## Next Step Gate

Move this metric to `../09_aggregation/` only after NER F1 and coverage are
complete for available languages.

Pass line:

- dataset/source and language list are recorded.
- training/evaluation protocol matches the Glot500-style setup as closely as
  possible.
- F1 type is explicit.
- selected target intersection is documented.
- every required model is included or has a failure/exclusion note.

Required artifacts:

- command log
- raw score output
- `summary.tsv` or `results.md`
- coverage reference
- hyperparameter note

If selected-target coverage is tiny, report it honestly and use head/tail/all
available-language tables for the main metric.

## Current Baseline Run

The `xlmr_base` NER baseline completed after a predict-only rerun.

Command:

```bash
TRAIN_LANGS=eng_Latn bash scripts/run_v5_eval_metric.sh ner xlmr_base 0
```

Outer log:

```text
/home/axt/mnt2/jongha/v5_glot50010/logs/ner_xlmr_base_20260627_025850.outer.log
```

Output root:

```text
/home/axt/mnt2/jongha/v5_glot50010/evaluation/ner/xlmr_base/xlm-roberta-base
```

Final result file:

```text
/home/axt/mnt2/jongha/v5_glot50010/evaluation/ner/xlmr_base/xlm-roberta-base/test_results.txt
```

Promotion evidence, checked `2026-06-27 04:34 KST`:

- `test_results.txt`: `984` lines
- `language=` rows: `164`
- parsed by `scripts/aggregate_v5_metrics.py`
- parsed F1 rows:
  - all: `0.549858`
  - head: `0.621207`
  - v5-target actual evaluated intersection: `0.459364`

Coverage note: the v5 materialized coverage audit still reports PAN-X/NER as
`78/102` with selected target10 `0/10` under
`/home/axt/mnt2/jongha/v5_glot50010/eval_data_download/ner`. The actual NER
runner evaluated a wider `164`-language candidate list from
`evaluation/download_data/download/ner/xlm-roberta-base`, including
`fur_Latn`. Treat the v5-target NER row as a narrow actual-evaluated
intersection, not a target10 downstream coverage claim.

Operational fixes applied before this run:

- `evaluate_ner.py` now reads `ner_lang_list.txt` relative to the evaluator
  file.
- output and tokenized-cache directories are built with `os.path.join`.
- existing output dirs no longer disable training when `--overwrite_output_dir`
  is set.
- the train split is preprocessed for `args.train_langs`, not only hard-coded
  `eng_Latn`.
- `run_tag.py` now skips prediction-file writing when text/index alignment
  fails, while preserving the metric row in `test_results.txt`.

## Current Reference Run

The `glot500_base` NER reference row completed and is parsed by
`scripts/aggregate_v5_metrics.py`.

Launch pattern:

```bash
setsid bash -lc 'cd /home/axt/jongha/Glot500-py39-eval; export PYTHONUNBUFFERED=1 TRAIN_LANGS=eng_Latn; bash scripts/run_v5_eval_metric.sh ner glot500_base 0'
```

Outer log:

```text
/home/axt/mnt2/jongha/v5_glot50010/logs/ner_glot500_base_setsid_20260627_045309.outer.log
```

Command log:

```text
docs/exp/v5/3_evaluation/05_ner/glot500_base/command_logs/run_glot500_base_20260627_045309.log
```

Final result file:

```text
/home/axt/mnt2/jongha/v5_glot50010/evaluation/ner/glot500_base/glot500-base/test_results.txt
```

Promotion evidence, checked `2026-06-27 06:28 KST`:

- `test_results.txt`: non-empty, `24194` bytes at the time of promotion.
- evaluator process: not running.
- parsed by `scripts/aggregate_v5_metrics.py`.
- parsed F1 rows:
  - all: `0.627108`
  - head: `0.645915`
  - v5-target actual evaluated intersection: `0.553191`

The v5-target row is still a narrow `fur_Latn` actual-evaluated intersection,
not a target10-wide downstream claim.

## Current v5_random Run

The `v5_random_mlm_10k` NER post-checkpoint row completed and is ready for
aggregation.

Command:

```bash
TRAIN_LANGS=eng_Latn bash scripts/run_v5_eval_metric.sh ner v5_random 0
```

Command log:

```text
docs/exp/v5/3_evaluation/05_ner/v5_random/command_logs/run_v5_random_20260628_051124.log
```

Final result file:

```text
/home/axt/mnt2/jongha/v5_glot50010/evaluation/ner/v5_random/v5_random_mlm_10k/test_results.txt
```

Promotion evidence, checked `2026-06-28 06:38 KST`:

- `test_results.txt`: `984` lines.
- `language=` rows: `164`.
- dev/best checkpoint row recorded in `eval_results.txt`.
- parsed by `scripts/aggregate_v5_metrics.py`.

The v5-target row must remain a narrow actual-evaluated intersection, not a
target10-wide downstream claim.
