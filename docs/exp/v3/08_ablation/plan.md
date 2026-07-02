# Stage 08 Plan: Ablation Study Packaging

## Goal

`first_try`와 `second_try` 결과를 main experiment가 아니라 ablation/failure analysis로 재배치한다.

## Inputs

- `../ablation_study.md`
- `docs/exp/first_try/`
- `docs/exp/second_try/`
- `../07_main_claim/evidence_table.tsv`, available after Stage 07

## Required Work

1. Existing experiment를 axis별로 분류한다.
2. Vocab size, init, fallback, training, data, objective/repair, downstream proxy 축을 만든다.
3. 각 기존 결과가 main claim을 대체할 수 없는 이유를 기록한다.
4. Negative diagnostic으로 재사용 가능한 결론을 정리한다.
5. Report 본문, ablation section, appendix 배치를 나눈다.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `file_results.tsv`
- `ablation_matrix.tsv`
- `second_try_mapping.tsv`
- `first_try_mapping.tsv`
- `negative_diagnostic_summary.md`
- `report_placement.md`

## Score Table Contract

`score_table.tsv`는 아래 항목을 포함한다.

| Metric | Expected |
| --- | --- |
| unmapped prior experiments | 0 |
| prior experiments labeled main | 0 |
| allowed ablation claims recorded | yes |
| blocked overclaims recorded | yes |

## Exit Criteria

- 기존 실험이 모두 ablation/failure analysis로 라벨링되어 있다.
- Target10 final model result와 ablation이 표와 문구에서 분리되어 있다.
- Negative diagnostic이 어떤 main 설계 필요성을 설명하는지 연결되어 있다.
- `results.md`에 `Gate status: PASS_ABLATION_PACKAGE_READY`가 있다.

## Failure Return

기존 실험의 evidence 위치가 불명확하면 first_try/second_try 문서를 다시 inventory한다. Ablation이 main claim처럼 쓰이면 Stage 08 wording을 수정한다.
