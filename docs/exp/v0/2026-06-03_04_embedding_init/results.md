# Results: Target10 Embedding Initialization

작성일: 2026-06-03

## Setup

Base model:

- `cis-lmu/glot500-base`

Merged tokenizer:

- `data/processed/target10/glot500_target10_spm16k`

Initialized model artifacts:

- `data/processed/target10/initialized_models/glot500_target10_random`
- `data/processed/target10/initialized_models/glot500_target10_mean`

GPU policy:

- All model initialization and training checks use physical GPU 3 only.
- Runtime command prefix: `CUDA_VISIBLE_DEVICES=3`

## Vocabulary Resize

| Item | Value |
| --- | ---: |
| Base model vocab size | 401,145 |
| Resized target10 vocab size | 415,139 |
| New tokens initialized | 13,994 |

The model and LM head were resized successfully for both initialization modes.

## Initialization Conditions

| Mode | New tokens | Initialized | Fallback global mean | Avg old subtokens per new token |
| --- | ---: | ---: | ---: | ---: |
| Random | 13,994 | 13,994 | 0 | n/a |
| Mean | 13,994 | 13,994 | 0 | 3.791 |

Mean initialization tokenizes each new target10 piece with the original Glot500 tokenizer and averages the old subtoken embeddings.

## 방법론 정리

이 실험의 핵심은 target10용 새 tokenizer를 Glot500에 붙인 뒤, 새로 생긴 13,994개 토큰 embedding만 초기화하는 것이다.

먼저 target10 Bible train text로 SentencePiece unigram 16k tokenizer를 학습했다. 그 vocabulary를 `cis-lmu/glot500-base` tokenizer에 merge했고, 기존 Glot500에 이미 있던 piece를 제외하면 실제로 새로 추가된 token은 13,994개다. 이후 `glot500-base` 모델을 로드하고 `resize_token_embeddings(415139)`로 embedding matrix와 LM head를 확장했다. 기존 401,145개 token row는 원래 Glot500 embedding을 유지하고, 뒤에 붙은 13,994개 row만 새로 초기화했다.

비교한 초기화 방식은 두 가지다.

- Random: `resize_token_embeddings()` 기본 동작으로 새 embedding row를 랜덤 초기화한 baseline이다. 코드상 별도 덮어쓰기 없이 resize 후 저장한다.
- Mean: 새 target10 token piece를 원래 Glot500 tokenizer로 다시 tokenize한다. 새 piece 하나가 기존 Glot500 subtoken 여러 개로 쪼개지면, 그 기존 subtoken embedding들을 평균내고 그 평균 vector를 새 token의 input embedding과 LM head row에 복사한다. old tokenizer로 못 쪼개는 경우에는 기존 embedding 전체 평균으로 fallback하게 되어 있지만, 이번 실험에서는 fallback이 0개였다.

따라서 Mean 초기화가 더 의미 있는 조건이다. 새 토큰 13,994개 전부가 기존 Glot500 embedding 공간 안의 평균 vector로 초기화됐고, 평균적으로 새 token 하나당 기존 subtoken 3.791개를 사용했다. 즉 랜덤하게 출발하는 것이 아니라, 기존 모델이 이미 알고 있는 조각들의 의미와 형태 정보를 빌려서 시작한 것이다.

보고서에는 다음처럼 요약할 수 있다.

> target10 tokenizer로 추가된 13,994개 token에 대해, Random baseline은 resize 시 기본 랜덤 초기화를 사용했고, Mean 조건은 각 새 token을 기존 Glot500 tokenizer로 재분절한 뒤 해당 기존 subtoken embedding들의 평균으로 input embedding과 LM head를 초기화했다. Mean 조건에서는 fallback 없이 모든 새 token이 기존 embedding geometry에 기반해 초기화되었다.

참고로 Align 초기화는 plan에는 있지만 이번 결과에는 아직 포함되지 않았다.

## Interpretation

Both checkpoints are loadable and ready for controlled MLM adaptation.

The mean condition has no fallback cases, so every added token received an initialization based on existing Glot500 embedding geometry. This is the preferred condition for the next larger run unless a later Align experiment beats it.

## Artifacts

- `data/processed/target10/initialized_models/glot500_target10_random/init_report.json`
- `data/processed/target10/initialized_models/glot500_target10_mean/init_report.json`
- `docs/exp/2026-06-03_04_embedding_init/embedding_init_metrics.tsv`
