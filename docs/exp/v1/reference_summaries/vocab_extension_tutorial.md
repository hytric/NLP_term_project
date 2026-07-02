# Vocabulary Extension And Embedding Initialization For Fine-Tuning Foundational LLMs

Source: `docs/exp/second_try/feedback/vocab_extension_tutorial.pdf`

## 핵심 내용

- Foundational LLM을 새 언어/도메인에 맞출 때 tokenizer mismatch가 sequence length 증가, vocabulary 낭비, target text fragmentation을 만든다.
- 해결책은 vocabulary replacement 또는 extension이며, multilingual base model에서는 extension이 기존 능력 보존에 더 적합하다.
- 새 token을 추가하면 embedding row를 합리적으로 초기화해야 한다.
- Tutorial은 Mean, FVT, Wechsel, Focus, Ofa, random baseline 등을 다룬다.

## 필수 비교 방법

| Method | 요약 | second_try 역할 |
| --- | --- | --- |
| Random / TransInner | 새 token row를 random으로 초기화 | 하한선 baseline |
| Mean / Gaussian Mean | source embedding 평균/분포로 초기화 | 단순 baseline |
| FVT / avg-subwords | 새 token을 source tokenizer로 쪼개고 기존 subtoken embedding 평균 | first_try mean 방식 |
| Focus | overlap token anchor와 target fastText similarity를 사용 | XLM-R multilingual setting에서 강한 후보 |
| Align | corpus에서 old/new token span alignment를 잡아 빈도 가중 평균 | 문맥 기반 후보 |

선택적 방법:

- Ofa: multilingual large-scale extension 후보지만 구현과 외부 vector 의존성이 크다.
- Wechsel: monolingual model transfer에 더 적합하다.

## 구현 주의점

- `model_type=unigram`인지 명시한다.
- XLM-R special token id를 보존한다.
- HF `add_tokens`만 쓰면 SentencePiece unigram 확률/Viterbi 체계에 제대로 통합되지 않을 수 있다.
- 새 token이 실제 encode에 사용되는지 반드시 확인한다.
- `resize_token_embeddings` 후 input embedding과 LM head tying을 확인한다.
- FVT/Mean 구현 시 `encode(..., add_special_tokens=False)`를 사용한다.
- SentencePiece `▁` marker, Unicode normalization, `<unk>` fallback을 주의한다.

## 평가 지표

- fertility: tokens/word, tokens/char
- `<unk>` rate
- byte fallback rate
- meaningful overlap
- zero-step MLM loss
- fixed-step MLM loss
- embedding norm distribution
- nearest neighbors
- downstream F1/accuracy/MRR

## Plan 반영

- Required init: random, mean, fvt, align, focus.
- Optional init: ofa, wechsel.
- init 단계에서 zero-step MLM loss와 embedding diagnostics 기록.
- 모든 method를 downstream pilot까지 비교하되, full 3-seed는 best checkpoint만 수행.
