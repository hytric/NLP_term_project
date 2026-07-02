# Stage 09 Plan: Extension Case Packaging

## Goal

Target10 main protocol이 닫힌 뒤 target10 밖의 추가 언어에 같은 protocol을 적용할지 결정한다. Coptic/Syriac와 target10은 이미 main이므로 extension case가 아니다.

## Inputs

- `../07_main_claim/main_result_summary.md`
- `../07_main_claim/limitation_and_deviation_summary.md`
- `../00_scope/scope_decisions.tsv`
- extension target data from Stage 01 or new extension inventory

## Required Work

1. Extension target이 필요한지 결정한다. 기본값은 `NOT_REQUIRED_FOR_MAIN`.
2. Extension target을 target10 밖 언어로만 확정한다.
3. Main protocol과 동일하게 적용 가능한 항목과 불가능한 항목을 나눈다.
4. 모든 차이를 deviation으로 기록한다.
5. Tokenizer/data/init/training/evaluation artifact를 main artifact와 분리한다.
6. Extension 결과를 target10 main result처럼 표현하지 않는다.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `file_results.tsv`
- `extension_target_decision.tsv`
- `extension_vs_main_deviation.tsv`
- `extension_result_summary.md`
- `blocked_extension_claims.md`

## Score Table Contract

`score_table.tsv`는 아래 항목을 포함한다.

| Metric | Expected |
| --- | --- |
| extension target decision recorded | yes |
| deviation rows missing | 0 |
| extension artifact mixed with main | 0 |
| extension overclaims | 0 |

## Exit Criteria

- Extension case와 target10 main result의 차이가 모두 기록되어 있다.
- Extension artifact가 main artifact와 분리되어 있다.
- Extension claim은 protocol transfer 또는 case study로만 쓰인다.
- `results.md`에 `Gate status: PASS_DEVIATION_DOCUMENTED` 또는 `PASS_EXTENSION_READY`가 있다.

## Failure Return

Main protocol과 차이가 기록되지 않으면 Stage 09를 닫지 않는다. Extension target data가 부족하면 extension scope를 줄이거나 Stage 00/01로 돌아가 inventory를 보강한다.
