# 04 Method

파이프라인은 (1) tokenizer extension, (2) embedding initialization, (3) continued MLM pretraining 세 단계다. 각 단계에서 "무엇을 했는가"와 "왜 그렇게 했는가", "어느 코드가 구현하는가"를 함께 적는다.

## 4.1 Tokenizer extension

**절차.** (1) `xlm-roberta-base`의 `sentencepiece.bpe.model`을 source로 복사한다. (2) v5.2 mixed corpus에서 SentencePiece unigram auxiliary model을 학습한다. (3) source SPM에 없는 piece만 뒤에 append한다. (4) HuggingFace `add_tokens()`가 아니라 **SPM protobuf에 직접 append**한다 — Glot500-style 구현과 맞추고, unigram score를 보존하기 위해서다.

**설정과 이유.**

| Setting | Value | 이유 |
| --- | --- | --- |
| `model_type` | `unigram` | XLM-R/Glot500 계열과 tokenizer family 일치 |
| `byte_fallback` | `true` | OOV·rare 문자를 byte piece로 안전 분해 |
| `character_coverage` | `1.0` | Target7 Latin 문자 손실 없이 보존 |
| `input_sentence_size` | `20,000,000` | 전체 corpus scan하되 SPM memory/시간 통제 |

**결과(감사 수치).** source vocab 250,002 → 확장 후 **366,666**, 새로 추가된 novel token **116,664**개. 근거 코드: `tokenization/train_v52_glot5007.sh`, `tokenization/run.py`.

**Fertility 효과.** 동일 Target7 문장 3,500개(7언어×500)에 대해 XLM-R tokenizer와 확장 tokenizer의 tokens/word를 비교하면 2.204 → 1.592로 약 **27.75%** 감소한다(언어별 12.4%~34.9%). 상세는 §6.1. 다만 모든 초기화 방법이 **같은 확장 tokenizer**를 쓰므로, method 간 차이는 fertility가 아니라 embedding initialization에서 온다.

## 4.2 Embedding initialization

**공통 규칙.** (1) source tokenizer에 이미 있는 token string은 source row를 그대로 복사한다. (2) 새 token row만 method별로 초기화한다. (3) `<mask>`는 append로 id가 이동하므로(250001 → 366665) **string identity로 remap**해 source row를 복사한다. (4) input embedding과 LM head의 weight tying을 확인한다.

**감사 수치.** source len 250,002 · target len 366,666 · new rows 116,664 · `<mask>` copy diff 0.0 · LM head tied = true. 근거 코드: `scripts/build_v5_initialized_checkpoint.py`, `docs/exp/v5.2/4_reporting/v52_initializer_core_code.py`.

**Table 3. 다섯 초기화 방법.**

| Method | 정의 | 직관 / 위치 |
| --- | --- | --- |
| `random` | 새 row를 model init 분포 $\mathcal{N}(0,0.02)$에서 sample | 정보 없는 가장 단순한 resize baseline |
| `mean` | 기존 lexical embedding의 global mean을 새 row에 복사 | embedding cloud 중심에서 안정적 시작, 표면형 정보 미사용 |
| `FVT` | 새 token 표면형을 source tokenizer로 재분해 → 구성 subtoken embedding **평균** | source subword 형태/철자 정보 재사용 (**main hypothesis**) |
| `weighted FVT` | FVT subtoken 평균에 **표면 길이 가중** | 긴 subtoken이 더 구체적 lexical signal이라는 가설 (local variant) |
| `family-aware mean` | token provenance가 가리키는 language family의 frequency-weighted source-token mean | 표면형 대신 계통(typology) prior 사용 (exploratory local variant) |

> 예시: 새 token이 확장 tokenizer에는 한 piece로 들어와도, source XLM-R tokenizer로는 여러 subtoken으로 분해될 수 있다. FVT는 그 source subtoken들의 embedding 평균을 새 row 초기값으로 써서, random보다 언어적·형태적 힌트를 가진 상태에서 MLM을 시작한다.

**`align`에 대한 주의.** 기존 `align` initializer는 FVT 실패 token에만 unicode-block mean fallback을 적용하는 방식인데, 이번 tokenizer에서는 FVT 실패 token이 거의 없어 `fvt`와 **byte-identical하게 collapse**됐다. 따라서 5-way 독립 ablation에서는 제외하고, 표 연속성을 위한 historical row로만 남긴다.

## 4.3 Continued MLM pretraining

확장·초기화된 모델을 §3.3 corpus 위에서 MLM으로 이어 학습한다. 근거 코드: `modeling/train_v52_glot5007_mlm.sh`, `modeling/run.py`(HuggingFace `run_mlm.py` 커스텀; `--tokenizer_name` 지정 시 `resize_token_embeddings` 호출).

| Item | Value |
| --- | --- |
| base model | `xlm-roberta-base` |
| objective | MLM (dynamic masking, mask probability 0.15) |
| learning rate | `5e-5` |
| Adam | betas `(0.9, 0.999)`, ε `1e-8` |
| LR schedule / warmup | linear decay, warmup 0 (HuggingFace Trainer default) |
| weight decay / grad-clip | `0.0` / `1.0` (Trainer default) |
| max sequence length | 512 |
| language sampling | α = 0.3 (§3.3) |
| effective global batch | exposure-aligned across 5 methods (§6.2); convergence queue log 기준 ≈ 36/step |
| checkpoint/log interval | 1,000 steps |
| convergence budget | 50,000 steps (5-way) |

> **effective batch 주의.** batch 관련 기록이 소스마다 다르다(설계 문서 target 384, base launcher 12×8=96, convergence queue log ≈ 36). 본 보고서는 다섯 방법을 **동일 exposure**로 맞춰 비교하므로 x축을 exposure-aligned step으로 두며(§6.2), 절대 batch 수치는 queue log 기준으로 기재한다. 제출 전 실제 v5.2 convergence 실행 batch를 한 번 더 확인해 확정할 것.

학습은 초기 구간과 continuation 구간을 이어붙여 다섯 방법 모두 **50K-step까지 동일 exposure 조건으로** 진행한다(prior + continuation). 모든 최종 수치는 50K checkpoint 기준으로 보고하며, 학습 진행은 10K→50K 궤적으로 제시한다(§6.4). 수렴 loss plot의 x축은 raw local step이 아니라 exposure-aligned step이다(§6.2).
