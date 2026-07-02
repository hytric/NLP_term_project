# Stage 02 Plan: XLM-R Baseline Audit

## Goal

Target10 main run 전에 XLM-R-base baseline의 tokenizer 병목과 representation/downstream baseline을 측정한다. `xlm-roberta-large`는 사용하지 않는다.

## Inputs

- `../01_data/split_manifest.tsv`
- `../01_data/corpus_manifest.tsv`
- `../00_scope/task_availability.tsv`
- `xlm-roberta-base`

## Required Work

1. XLM-R-base tokenization metrics를 target10 language별로 계산한다.
2. held-out test PPPL을 측정한다.
3. Target10 downstream task 가능 여부와 baseline score를 기록한다.
4. Bible/Tatoeba sentence retrieval 가능 여부와 baseline score를 기록한다.
5. roundtrip alignment 가능 여부와 baseline score를 기록한다.
6. High-resource replay/control language의 forgetting baseline을 필요한 만큼 기록한다.
7. target10 평균과 language별 편차를 분리한다.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `file_results.tsv`
- `tokenization_metrics.tsv`
- `baseline_eval.tsv`
- `tokenization_samples.md`
- `target10_baseline_summary.tsv`
- `high_resource_control_baseline.tsv`

## Score Table Contract

`score_table.tsv`는 아래 항목을 포함한다.

| Metric | Expected |
| --- | --- |
| missing tokenization metrics | 0 |
| target10 baseline summary present | yes |
| XLM-R-large rows | 0 |
| available task count recorded | yes |
| unavailable task reason recorded | yes |

## Exit Criteria

- tokens/word, tokens/character, single-character token ratio, `<unk>` rate가 target10 language별로 있다.
- PPPL 또는 task-unavailable reason이 language별로 있다.
- downstream task가 없는 경우 proxy 여부가 아니라 unavailable reason으로 먼저 기록되어 있다.
- `results.md`에 `Gate status: PASS`가 있다.

## Failure Return

Baseline table이 비면 Stage 01로 돌아가 split/source를 보강한다. Target10 bottleneck 또는 downstream baseline을 측정할 수 없으면 Stage 00으로 돌아가 task availability를 재검토한다.
