# Stage 05 Plan: Multilingual Continued Pretraining

## Goal

High-resource replay/control과 target10 low-resource를 동시에 사용해 full-model MLM continued pretraining을 수행한다. Model-dependent 비교는 3개 이상 seed를 원칙으로 하며, 1 GPU 며칠 예산에 맞춰 pilot와 final grid를 분리한다.

## Inputs

- `../04_init/init_candidate_summary.tsv`
- `../01_data/split_manifest.tsv`
- `../01_data/mlm_mixture_manifest.tsv`
- `../03_tokenizer/selected_main_tokenizer.md`

## Required Work

1. Full-model MLM training config를 작성한다.
2. High-resource와 low-resource가 동시에 들어가는 sampling config를 작성한다.
3. Adam, LR `5e-5`, sequence length 512, sampling alpha `0.3`을 기본값으로 두되, 1 GPU 예산 deviation을 기록한다.
4. Embedding init method별 pilot를 실행하고, final candidate는 3개 이상 seed로 반복한다.
5. Checkpointing interval과 downstream/dev selection metric을 고정한다.
6. Train/dev only로 checkpoint selection을 수행한다.
7. Glot500 설정 또는 scope lock에서 벗어난 항목을 `deviation_from_protocol.tsv`에 기록한다.
8. Target-only, LoRA, seed-1-only run은 ablation/diagnostic으로 분리한다.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `file_results.tsv`
- `training_config.json`
- `checkpoint_metrics.tsv`
- `seed_summary.tsv`
- `init_method_mlm_summary.tsv`
- `deviation_from_protocol.tsv`
- `checkpoint_selection.md`
- `training_command.md`

## Score Table Contract

`score_table.tsv`는 아래 항목을 포함한다.

| Metric | Expected |
| --- | --- |
| full-model training | yes |
| high-resource rows in mixture | >0 |
| low-resource rows in mixture | >0 |
| target-only main violation | 0 |
| LoRA main violation | 0 |
| final candidate seeds | >=3 |
| final test used for selection | 0 |
| deviations recorded | yes |

## Exit Criteria

- Main model은 full fine-tuning MLM이다.
- High-resource replay/control과 target10 low-resource가 training mixture에 모두 들어간다.
- Final candidate는 3개 이상 seed로 결과가 있다.
- Checkpoint selection이 dev/allowed validation 기준으로만 이루어졌다.
- 모든 compute/data/config deviation이 기록되어 있다.
- `results.md`에 `Gate status: PASS` 또는 `PASS_NEGATIVE_RESULT`가 있다.

## Failure Return

Training이 main 조건을 만족하지 않으면 Stage 05를 다시 실행한다. Loss 또는 validation이 비정상적으로 붕괴하면 Stage 03 tokenizer 또는 Stage 04 init으로 돌아가 원인을 진단한다.
