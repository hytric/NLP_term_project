# Third Try Branches

이 폴더는 main stage gate를 통과하지 못했을 때 원인 해결을 위한 제한적 branch 탐구를 기록한다.

Branch는 main result가 아니다. `return_decision.md`에서 `MERGE_TO_MAIN`으로 닫히기 전까지는 evidence 후보로만 취급한다.

## Required Files Per Branch

- `goal.md`
- `plan.md`
- `results.md`
- `score_table.tsv`
- `return_decision.md`

## Return Decision Values

| Value | Meaning |
| --- | --- |
| `MERGE_TO_MAIN` | main stage rule 또는 결과에 반영 |
| `RETRY_BRANCH` | 같은 branch를 조건 수정 후 반복 |
| `ABANDON_BRANCH` | main claim에는 쓰지 않고 appendix/diagnostic evidence로만 보관 |
