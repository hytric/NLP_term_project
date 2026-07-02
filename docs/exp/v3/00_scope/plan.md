# Stage 00 Plan: Scope Freeze

## Goal

Target10 low-resource main set과 high-resource replay/control set을 고정한다. 이 stage의 핵심은 Coptic/Syriac를 포함한 기존 target10을 main으로 유지하고, 동시에 사용할 high-resource data를 확정하는 것이다.

## Inputs

- `../scope_lock_20260612.md`
- `../idea.md`
- `../plan.md`
- `../ablation_study.md`
- `../decision_log.md`
- `docs/survey/2305.12182v2.pdf`
- `docs/survey/GLOT500_extension.pdf`

## Required Work

1. 기존 target10 inventory를 확정한다: `acu`, `ake`, `bsn`, `chr`, `cop`, `kbh`, `nhg`, `oji`, `syr`, `usp`.
2. Coptic/Syriac가 main target임을 명시한다.
3. High-resource replay/control 후보를 정한다: English, German, Japanese, Korean을 우선 검토한다.
4. Low-resource target과 high-resource replay가 동시에 들어가는 train mixture contract를 작성한다.
5. Target10 downstream task 가능 여부를 language별로 기록한다.
6. `xlm-roberta-large`는 사용하지 않는 것으로 고정한다.
7. Main run에서 사용하지 않는 prior experiment는 ablation mapping 대상으로 표시한다.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `file_results.tsv`
- `language_inventory.tsv`
- `high_resource_inventory.tsv`
- `head_tail_definition.tsv`
- `task_availability.tsv`
- `mixture_contract.tsv`
- `scope_decisions.tsv`

## Score Table Contract

`score_table.tsv`는 아래 항목을 포함한다.

| Metric | Expected |
| --- | --- |
| target10 missing language count | 0 |
| Coptic/Syriac main label present | yes |
| high-resource replay candidates recorded | yes |
| train mixture contract present | yes |
| task availability recorded | yes |
| XLM-R-large excluded | yes |

## Exit Criteria

- target10 전체가 main low-resource target으로 라벨링되어 있다.
- Coptic/Syriac가 main experiment에 포함되어 있다.
- high-resource replay/control set이 기록되어 있다.
- target10 downstream task 중 가능한 항목과 불가능한 항목이 기록되어 있다.
- `results.md`에 `Gate status: PASS` 또는 명확한 blocker가 있다.

## Failure Return

Scope가 흔들리면 Stage 01로 가지 않는다. target10 중 일부 data/task가 부족하면 제외가 아니라 "main included, evaluation unavailable reason recorded"를 우선 적용하고, 정말 불가능한 경우에만 사용자 확인 후 scope를 줄인다.
