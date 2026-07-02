# Stage 03 Plan: Glot500-Style Tokenizer Extension

## Goal

XLM-R 기존 vocab id를 100% 보존하면서 target10 + high-resource mixture에서 auxiliary tokenizer를 학습하고, 새 piece만 append한다. Byte fallback과 character fallback/coverage 비교는 ablation으로 분리한다.

## Inputs

- `../01_data/split_manifest.tsv`
- `../01_data/mlm_mixture_manifest.tsv`
- `../02_baseline/tokenization_metrics.tsv`
- `xlm-roberta-base` tokenizer

## Required Work

1. Target10 low-resource와 high-resource replay/control이 함께 들어간 corpus에서 SentencePiece unigram auxiliary tokenizer를 학습한다.
2. language-script별 multinomial sampling alpha `0.3` 또는 Stage 00 mixture contract의 sampling rule을 적용한다.
3. high-resource sample cap을 target10을 압도하지 않도록 적용한다.
4. Auxiliary vocab에서 XLM-R 기존 piece를 제거한다.
5. 새 piece만 XLM-R vocab 뒤에 append한다.
6. special token id와 기존 token id 보존 여부를 audit한다.
7. Main tokenizer와 fallback ablation tokenizer를 분리해서 만든다.
8. before/after tokenization metrics와 sample을 작성한다.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `file_results.tsv`
- `merge_report.json`
- `id_preservation_audit.tsv`
- `tokenization_before_after.tsv`
- `fallback_ablation.tsv`
- `tokenization_samples.md`
- `selected_main_tokenizer.md`

## Score Table Contract

`score_table.tsv`는 아래 항목을 포함한다.

| Metric | Expected |
| --- | --- |
| changed existing token ids | 0 |
| changed special token ids | 0 |
| appended token id violations | 0 |
| fallback ablation separated from main | yes |
| selected main tokenizer recorded | yes |

## Exit Criteria

- 기존 XLM-R token id와 special token id가 100% 보존되어 있다.
- 새 token은 모두 base vocab size 이후 id를 가진다.
- Main tokenizer 선택과 fallback ablation 결과가 섞이지 않는다.
- Tokenization 개선/악화가 target10 language별로 기록되어 있다.
- `results.md`에 `Gate status: PASS`가 있다.

## Failure Return

Id 보존이 깨지면 Stage 03 안에서 merge 절차를 고친다. Auxiliary vocab size나 corpus sampling이 부적절하면 deviation을 기록하고, 필요한 경우 Stage 01 또는 Stage 00으로 돌아간다.
