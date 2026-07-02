# Stage 04 Plan: Glot500-Style Model Initialization

## Goal

Stage 03 tokenizer vocab size에 맞춰 XLM-R-base model을 resize하고, 기존 rows는 그대로 복사한다. 새 rows는 여러 embedding initialization 방법으로 초기화하며, random init은 required baseline으로 포함한다.

## Inputs

- `../03_tokenizer/selected_main_tokenizer.md`
- `../03_tokenizer/id_preservation_audit.tsv`
- `xlm-roberta-base`

## Required Work

1. XLM-R-base model과 tokenizer를 load한다.
2. Input embedding과 LM head를 tokenizer vocab size에 맞게 resize한다.
3. 기존 embedding/LM head rows가 그대로 복사되었는지 검증한다.
4. 새 rows가 tokenizer append count와 같은지 확인한다.
5. Random, mean, fvt, align, focus 등 가능한 initialization checkpoint를 만든다.
6. 각 init method의 source-token coverage, `<unk>` contamination, row norm, nearest-neighbor diagnostic을 기록한다.
7. Compute상 모든 method를 끝까지 학습할 수 없으면 Stage 05 pilot/dev 기준으로 축소할 candidate rule을 기록한다.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `file_results.tsv`
- `init_method_reports/`
- `row_copy_audit.tsv`
- `new_row_stats.tsv`
- `init_candidate_summary.tsv`

## Score Table Contract

`score_table.tsv`는 아래 항목을 포함한다.

| Metric | Expected |
| --- | --- |
| base embedding row drift | 0 |
| base LM head row drift | 0 |
| new row count mismatch | 0 |
| random init present | yes |
| non-random init methods present | >=1 |
| init candidate summary present | yes |

## Exit Criteria

- Base rows drift가 0이다.
- New row count가 appended token count와 같다.
- Random init과 하나 이상의 non-random init candidate가 준비되어 있다.
- 각 init method의 diagnostic이 기록되어 있다.
- `results.md`에 `Gate status: PASS`가 있다.

## Failure Return

Row copy audit이 실패하면 Stage 04 resize/init 코드를 수정한다. Tokenizer append count가 불일치하면 Stage 03으로 돌아가 vocab merge를 다시 확인한다.
