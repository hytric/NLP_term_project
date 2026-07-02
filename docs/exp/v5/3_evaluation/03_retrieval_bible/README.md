# 03 Retrieval Bible

Required Glot500 metric.

Report Top-10 accuracy and task coverage. The inherited evaluator exists, and
v5 now has a materialized Bible retrieval set for the Glot500 Bible task
languages that are available in the local parallel Bible corpus.

## Next Step Gate

Move this metric to `../09_aggregation/` only after Bible retrieval coverage and
Top-10 accuracy are recorded.

Pass line:

- Bible/PBC source version and preprocessing are written.
- evaluated languages and verse/sentence counts are recorded.
- Top-10 accuracy is reported for every available model.
- selected target coverage and missing targets are documented.
- leakage or overlap concerns are noted if relevant.

Required artifacts:

- command log
- raw output or score file
- `summary.tsv` or `results.md`
- coverage reference
- data-source note

If Bible coverage differs from Tatoeba coverage, keep both tables separate and
do not average them without labeling.

## Current Status

Status: `partial_measured`.

Evidence:

- Coverage summary: `../00_coverage/coverage_summary.tsv` reports
  `retrieval_bible` coverage `74/102`, target coverage `0/10`.
- Materialization summary:
  `materialization_summary.tsv`.
- Local materialized data root:
  `evaluation/download_data/download/retrieval_bible`.
- Materialized file count: `148` text files, one source and one English file
  for each of `74` evaluated language-scripts.
- `evaluation/retrieval/bible_lang_list.txt` contains `369` candidate rows,
  and the v5 materializer respects the Glot500-style flag `1` rows by default.
- The inherited evaluator expects files named like
  `bible.<src_lang>-eng_Latn.<src_lang>` and
  `bible.<src_lang>-eng_Latn.eng_Latn` one directory above its model-specific
  tokenization cache.
- `xlmr_base` completed over all `74` materialized language-scripts. The parsed
  aggregate is Top-10 accuracy `0.381153`, recorded in
  `../09_aggregation/results.md`.
- `glot500_base` completed over all `74` materialized language-scripts. The
  parsed aggregate is Top-10 accuracy `0.509356`, recorded in
  `../09_aggregation/results.md`.
- Remaining required rows: `v5_random` and `v5_fvt` wait for matched
  checkpoints.

Data-source caveat:

- `san_Latn` materializes from local source `san-x-bible.txt`; sampled text
  appears Devanagari despite the Glot500 task label. Keep this as a local corpus
  script-label caveat and do not use this row for script-specific claims without
  manual verification.

Important target10 note:

The selected v5 target10 still has `0/10` Bible retrieval coverage under the
Glot500 Bible task flags. Several target Bible files exist locally, but their
`bible_lang_list.txt` flags are `0` or they are absent from the task list.
Therefore Bible retrieval cannot support a target10 downstream improvement
claim unless an explicitly labeled target-only auxiliary evaluation is added.

Runner status:

- `evaluation/retrieval/evaluate_retrieval_bible.sh`
- `evaluation/retrieval/evaluate_retrieval_bible.py`

The runner is preserved as a required metric path. `xlmr_base` and
`glot500_base` are measured, and `v5_random` and `v5_fvt` wait for matched
checkpoints.

Materialization command:

```bash
python3 scripts/materialize_v5_bible_retrieval.py
python3 scripts/audit_v5_eval_coverage.py
python3 scripts/refresh_v5_reporting.py
```

Execution checklist:

1. Run `bash scripts/run_v5_eval_metric.sh retrieval_bible xlmr_base <gpu>`.
2. Run `bash scripts/run_v5_eval_metric.sh retrieval_bible glot500_base <gpu>`.
3. After matched v5 checkpoints exist, run
   `bash scripts/run_v5_post_checkpoint_evals.sh bible`.
4. Promote only parsed `test_results.txt` rows into `09_aggregation/`.
