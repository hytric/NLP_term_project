# The UnigramLM Tokenization Algorithm

Source: `docs/survey/unigramLM.pdf`

## 핵심 내용

- SentencePiece는 library 이름이고, 알고리즘은 `bpe` 또는 `unigram` 등으로 선택된다.
- XLM-R, Glot500 계열은 SentencePiece unigram mode와 잘 맞는다.
- UnigramLM은 corpus likelihood를 최대화하는 token vocabulary를 확률 모델로 학습한다.

## 알고리즘 요약

- 입력 corpus를 whitespace 기반 pre-token과 frequency로 본다.
- 큰 seed vocabulary에서 시작한다.
- 각 token에 probability를 둔다.
- EM으로 token probability를 추정한다.
- likelihood 기여가 낮은 token을 pruning한다.
- 최종 vocab size까지 반복한다.

## Second_try에 가져올 것

- target10 tokenizer는 SentencePiece `model_type=unigram`으로 학습한다.
- vocab size는 모델 품질과 sequence length의 tradeoff를 조절하는 실험 변수로 둔다.
- `8k`, `16k`, `32k`를 비교해 fertility 감소가 꺾이는 지점을 찾는다.

## 주의점

- "SentencePiece를 썼다"만으로는 BPE인지 Unigram인지 불명확하다. 문서와 command에 `model_type=unigram`을 명시해야 한다.
- vocab이 작으면 sequence length가 길어지고, vocab이 크면 희귀 token embedding 학습이 어려워진다.
- character coverage와 byte fallback은 `<unk>`와 sequence length에 직접 영향을 준다.

## Plan 반영

- Stage 03에서 unigram tokenizer grid.
- tokenizer metrics에 tokens/word, tokens/char, sequence length percentile 포함.
- command/config를 stage별 결과에 기록.
