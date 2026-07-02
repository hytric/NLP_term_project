# Step 06 Results: Downstream Proxy Tasks

Status: COMPLETED

Run id: step06_downstream_20260613_154514

Completed date: 2026-06-13

Gate status: PASS

## Required Artifact Check

| Artifact | Path | Present? | Notes |
| --- | --- | --- | --- |
| score table | `score_table.tsv` | yes | all task/model/seed rows filled |
| file results | `file_results.tsv` | yes | per-output file status recorded |
| dataset stats | `downstream_dataset_stats.tsv` | yes | construction notes |
| downstream results | `downstream_results.tsv` | yes | frozen encoder proxy scores |
| sample predictions | `sample_predictions.md` | yes | selected checkpoint and task note |
| failure cases | `failure_cases.md` | yes | adapted underperformance notes |

## Summary

Step 06 evaluated original XLM-R and the Step 05 selected checkpoint using frozen encoder proxy tasks with 3 seeds. Classification and diagnostic language identification use an internal split from Step 01 train data. Retrieval and parallel matching use held-out John test verses with shared verse IDs.

| Metric | Original | Selected Adapted |
| --- | --- | --- |
| retrieval recall@1 avg | 0.022037 | 0.023111 |
| parallel matching AUC avg | 0.570167 | 0.567759 |
| book/genre accuracy avg | 1.000000 | 1.000000 |

## Downstream Success Decision

Retrieval improves: `True`.

Parallel matching improves: `False`.

Success is claimed only if retrieval/ranking or parallel matching improves over original XLM-R. Gate status is `PASS`.

## Gate Evidence

Evidence:

- `score_table.tsv` has no `TBD`, blank, or unchecked fields.
- all three final tasks have dataset stats and baseline scores.
- original XLM-R and selected adapted checkpoint are evaluated with 3 seeds.
- language identification is reported only as diagnostic.

## Failure Return

Failed gate: NOT_APPLICABLE

Observed evidence: NOT_APPLICABLE

Return-to step: NOT_APPLICABLE

Required fix: NOT_APPLICABLE
