# Step 06 Plan: Downstream Proxy Tasks

## Goal

Evaluate whether the selected adapted encoder improves over original XLM-R on encoder-only downstream proxy tasks.

## Inputs

- Step 05 `Gate status: PASS`
- selected checkpoint from Step 05
- Step 01 downstream manifest
- `../downstream_tasks.md`

## Required Tasks

1. Book/genre classification
2. Verse retrieval/ranking
3. Parallel verse matching

Diagnostic only:

- Language identification

## Required Work

1. Build downstream datasets and document label/negative sampling.
2. Run majority/random baselines.
3. Run original XLM-R baseline.
4. Run selected adapted checkpoint.
5. Run 3 seeds for original XLM-R and selected best checkpoint.
6. Record per-language and hard-negative-only scores where applicable.
7. Produce sample predictions and failure cases.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `downstream_dataset_stats.tsv`
- `downstream_results.tsv`
- `sample_predictions.md`
- `failure_cases.md`
- `file_results.tsv`

## Score Table Contract

Each task/model/seed row must have all score columns filled. If a metric does not apply, write `NOT_APPLICABLE` and explain in `results.md`.

## Exit Criteria

- All three final tasks have dataset stats and baseline scores.
- Original XLM-R and selected adapted checkpoint are evaluated with 3 seeds.
- Language identification is reported only as diagnostic.
- Success is claimed only if retrieval/ranking or parallel matching improves over original XLM-R.
- `file_results.tsv` records every generated file with path, count or size, and status.
- `results.md` has `Gate status: PASS` or `PASS_NEGATIVE_RESULT`.

## Failure Return

If a task is too easy, rebuild negatives or labels inside Step 06. If adapted model underperforms due to checkpoint quality, return to Step 05. If task construction leaks labels, return to Step 01.
