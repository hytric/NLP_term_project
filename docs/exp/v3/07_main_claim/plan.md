# Stage 07 Plan: Main Claim Synthesis

## Goal

Stage 00-06 evidence를 바탕으로 허용되는 main claim과 금지되는 claim을 분리한다. Tokenizer-only improvement를 downstream improvement처럼 쓰지 않는다.

## Inputs

- `../06_eval/target10_summary.tsv`
- `../06_eval/target10_seed_summary.tsv`
- `../06_eval/high_resource_control_summary.tsv`
- `../06_eval/task_coverage.tsv`
- `../03_tokenizer/tokenization_before_after.tsv`
- `../05_mlm/init_method_mlm_summary.tsv`
- `../05_mlm/deviation_from_protocol.tsv`
- `../ablation_study.md`

## Required Work

1. Target10 language에서 어떤 downstream task가 XLM-R-B보다 개선되었는지 정리한다.
2. Seed 3개 이상에서 개선이 안정적인지 확인한다.
3. High-resource replay/control 성능이 무너졌는지 확인한다.
4. Embedding initialization method별 차이가 downstream까지 이어지는지 정리한다.
5. Tokenization 개선과 downstream 개선의 방향 일치를 확인한다.
6. Allowed claims와 blocked claims를 분리해서 작성한다.
7. Negative result일 경우 positive wording을 제거하고 diagnostic claim으로 닫는다.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `file_results.tsv`
- `evidence_table.tsv`
- `allowed_claims.md`
- `blocked_claims.md`
- `main_result_summary.md`
- `novelty_claims.md`
- `limitation_and_deviation_summary.md`

## Score Table Contract

`score_table.tsv`는 아래 항목을 포함한다.

| Metric | Expected |
| --- | --- |
| tokenizer claim separated | yes |
| downstream claim separated | yes |
| seed stability recorded | yes |
| high-resource control recorded | yes |
| init-method evidence recorded | yes |
| unsupported positive claims | 0 |
| deviation impact discussed | yes |

## Exit Criteria

- Target10 downstream improvement, seed stability, high-resource control, task coverage, deviation impact가 모두 evidence table에 연결되어 있다.
- Allowed claim과 blocked claim이 분리되어 있다.
- Ablation 결과가 main result처럼 쓰이지 않는다.
- `results.md`에 `Gate status: PASS_MAIN_CLAIM_READY` 또는 `PASS_NEGATIVE_MAIN_READY`가 있다.

## Failure Return

Evidence가 downstream 개선을 지지하지 않으면 positive claim을 낮춘다. 특정 metric 누락이 claim 판단을 막으면 Stage 06으로 돌아가 평가를 보강한다.
