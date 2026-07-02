# 04 Method Draft

## 목적

Tokenizer extension, embedding initialization, continued MLM pretraining을 순서대로 설명한다. 모든 단계에서 "왜 이 방식을 썼는가"와 "어느 코드가 구현하는가"를 붙인다.

## 4.1 Tokenizer Extension

### 핵심 절차

1. XLM-R-base tokenizer의 `sentencepiece.bpe.model`을 복사한다.
2. v5.2 mixed corpus에서 SentencePiece unigram auxiliary model을 학습한다.
3. 기존 XLM-R SPM에 없는 piece만 append한다.
4. HuggingFace `add_tokens()`가 아니라 SentencePiece protobuf append를 사용한다.

### 코드 근거

- `tokenization/train_v52_glot5007.sh`
- `tokenization/run.py`

### 설정값과 이유

| Setting | Value | 이유 |
| --- | --- | --- |
| `model_type` | `unigram` | Glot500/XLM-R 계열과 tokenizer family를 맞춘다. |
| `byte_fallback` | `true` | OOV 문자와 rare character를 byte piece로 안전하게 처리한다. |
| `character_coverage` | `1.0` | target7 Latin-script 문자를 손실 없이 보존한다. |
| `input_sentence_size` | `20000000` | 전체 corpus를 scan하되 SPM memory와 training time을 통제한다. |

## 4.2 Embedding Initialization

### 공통 규칙

- Existing token string이 source tokenizer에 있으면 source row를 그대로 복사한다.
- 새 token row만 method별로 초기화한다.
- `<mask>`는 id가 이동할 수 있으므로 token identity 기준으로 remap한다.
- input embedding과 LM head weight tying을 확인한다.

### 코드 근거

- `scripts/build_v5_initialized_checkpoint.py`.

### Method Definitions

| Method | 정의 | 초기화 근거 |
| --- | --- | --- |
| `random` | 새 row를 model init distribution에서 sample한다. | 가장 단순한 resize baseline. |
| `mean` | 기존 lexical embedding의 global mean을 새 row에 넣는다. | 새 embedding을 기존 embedding cloud 중심에 둔다. |
| `FVT` | 새 token surface를 source tokenizer로 재분해하고 source subtoken embedding 평균을 쓴다. | source subword morphology/orthography 정보를 재사용한다. |
| `weighted FVT` | FVT subtoken 평균에 surface length weight를 둔다. | 긴 source subtoken이 더 구체적인 lexical signal일 수 있다는 가설. |
| `family-aware mean` | token provenance를 language family로 mapping하고 family별 frequency-weighted source-token mean을 쓴다. | surface decomposition보다 typology/family prior가 도움이 되는지 확인한다. |

### Audit Counts

나중에 보고서에 넣을 수 있는 구현 검증 숫자:

- Source tokenizer length: 250002.
- Target tokenizer length: 366666.
- New rows: 116664.
- `<mask>` source id: 250001.
- `<mask>` target id: 366665.
- `<mask>` copy diff: 0.0.
- LM head tied: true.

## 4.3 Continued MLM Pretraining

### 코드 근거

- `modeling/train_v52_glot5007_mlm.sh`
- `modeling/run.py`

### 설정값

| Item | Value |
| --- | --- |
| base model | `xlm-roberta-base` |
| objective | MLM |
| learning rate | `5e-5` |
| Adam betas | `(0.9, 0.999)` |
| max length | 512 |
| MLM probability | 0.15 |
| checkpoint interval | 1000 steps |
| main convergence budget | 50K steps |

## 꼭 설명할 위험

SPM protobuf append 이후 token id prefix가 유지된다고 가정하면 위험하다. `<mask>` id가 이동할 수 있으므로 반드시 token string identity로 source row를 복사했다고 설명한다.

