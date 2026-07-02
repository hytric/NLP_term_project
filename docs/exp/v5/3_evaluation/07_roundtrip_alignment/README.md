# 07 Roundtrip Alignment

Required Glot500 metric.

Report alignment accuracy and language coverage. Include command logs and any
SimAlign/Bible data availability notes.

## Next Step Gate

Move this metric to `../09_aggregation/` only after roundtrip alignment accuracy
and coverage notes are complete.

Pass line:

- alignment data source and language pairs are recorded.
- SimAlign or alignment tool version/config is written.
- roundtrip accuracy is reported for every available model.
- selected target coverage and missing targets are documented.
- failures from script/tokenization mismatch are noted.

Required artifacts:

- command log
- raw alignment output or score file
- per-model summary/result files under the v5 evaluation output root
- coverage reference
- tool/config note
- generated readiness/blocker audit:
  `blocker_audit.md` and `blocker_audit.tsv`

If alignment data is unavailable for selected targets, still run available
Glot500 languages and record target exclusions.

## Current Gate

Status: `pending_model_outputs`.

Evidence:

- Coverage summary: `../00_coverage/coverage_summary.tsv` reports
  `roundtrip_alignment` coverage `74/102`, target coverage `0/10`.
- Coverage detail: `../00_coverage/coverage_roundtrip_alignment.tsv` uses the
  Bible task list as a conservative proxy and marks materialized rows as
  `available`.
- Local expected data root now contains Bible-derived JSONL inputs:
  `evaluation/download_data/download/roundtrip_alignment`.
- The v5 eval data root is a symlink to
  `/home/axt/mnt2/jongha/v5_glot50010/eval_data_download`; the
  `roundtrip_alignment` subdirectory is materialized there.
- The inherited `RoundTripEvaluator` is wrapped by
  `evaluation/round-trip/evaluate_roundtrip_v5.py`.

Important target10 note:

The selected v5 target10 has `0/10` roundtrip coverage in the current coverage
audit. Therefore roundtrip alignment cannot support a target10 downstream
improvement claim unless new local parallel data is added.

Runner status:

- inherited scorer: `evaluation/round-trip/evaluate_roundtrip.py`
- v5 batch runner: `evaluation/round-trip/evaluate_roundtrip_v5.py`
- wrapper command: `scripts/run_v5_eval_metric.sh roundtrip_alignment <model_key> <gpu>`
- generated readiness audit:
  `docs/exp/v5/3_evaluation/07_roundtrip_alignment/blocker_audit.md`

Keep this metric in the completion checklist as pending until model outputs are
parsed. Do not omit it.

Unlock checklist:

1. Run available baseline/reference rows when compute allows:
   `bash scripts/run_v5_eval_metric.sh roundtrip_alignment xlmr_base <gpu>` and
   `bash scripts/run_v5_eval_metric.sh roundtrip_alignment glot500_base <gpu>`.
2. After matched v5 checkpoints exist, run the same metric for `v5_random` and
   `v5_fvt`.
3. Promote only parsed alignment result rows into `09_aggregation/`.
