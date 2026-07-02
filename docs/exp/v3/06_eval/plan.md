# Stage 06 Plan: Target10 Downstream Evaluation

## Goal

XLM-R-B와 third_try main model을 target10 downstream task에서 비교한다. PPPL/retrieval/alignment는 representation evidence로 쓰고, 최종 성공은 downstream 개선까지 요구한다.

## Inputs

- `../05_mlm/checkpoint_selection.md`
- `../02_baseline/baseline_eval.tsv`
- `../00_scope/task_availability.tsv`
- held-out test splits from `../01_data/`

## Required Work

1. PPPL을 held-out test에서 계산한다.
2. Bible/Tatoeba sentence retrieval을 가능한 target10 language에서 계산한다.
3. Roundtrip alignment를 가능한 target10 language에서 계산한다.
4. Target10 downstream task를 실행한다.
5. Official task가 없으면 Bible-domain downstream/proxy task를 명확히 proxy로 표시하고 leakage-safe split으로 평가한다.
6. High-resource replay/control language는 forgetting sanity check로만 평가한다.
7. Target10 평균, language별 score, seed 평균/표준편차를 작성한다.
8. Unavailable task는 이유를 기록하고 positive claim에서 제외한다.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `file_results.tsv`
- `pppl.tsv`
- `roundtrip.tsv`
- `sentence_retrieval.tsv`
- `text_classification.tsv`
- `ner.tsv`
- `pos.tsv`
- `target10_downstream.tsv`
- `target10_seed_summary.tsv`
- `target10_summary.tsv`
- `high_resource_control_summary.tsv`
- `task_coverage.tsv`

## Score Table Contract

`score_table.tsv`는 아래 항목을 포함한다.

| Metric | Expected |
| --- | --- |
| XLM-R-B comparison present | yes |
| third_try comparison present | yes |
| target10 downstream summary present | yes |
| seed variance recorded | yes |
| task language count recorded | yes |
| unavailable task reasons recorded | yes |
| high-resource control summary present | yes |

## Exit Criteria

- XLM-R-B vs third_try model 비교가 task별로 있다.
- Target10 평균과 language별 score가 있다.
- Final model-dependent result가 3개 이상 seed로 요약되어 있다.
- High-resource replay/control collapse 여부가 기록되어 있다.
- Task별 available language count가 표시되어 있다.
- 불가능한 task는 이유가 기록되어 있다.
- `results.md`에 `Gate status: PASS` 또는 `PASS_NEGATIVE_RESULT`가 있다.

## Failure Return

Evaluation artifact가 부족하면 Stage 06을 반복한다. Downstream 개선이 없으면 positive claim을 만들지 않고 `PASS_NEGATIVE_RESULT`로 닫거나 Stage 03-05로 돌아가 tokenizer/init/training design을 수정한다.
