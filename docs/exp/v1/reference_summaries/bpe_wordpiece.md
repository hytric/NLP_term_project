# BPE And WordPiece Tokenization

Source: `docs/survey/BEP_WordPiece.pdf`

## 핵심 내용

- BPE와 WordPiece는 bottom-up greedy merge 기반 subword algorithm이다.
- BPE는 adjacent pair frequency가 높은 pair를 merge한다.
- WordPiece는 PMI 성격의 score를 사용하며, word-internal token에 `##` marker를 둔다.
- SentencePiece는 library이며, BPE와 UnigramLM을 모두 지원한다.

## Second_try와의 관련성

- XLM-R/Glot500 계열 실험에서는 BPE/WordPiece보다 SentencePiece unigram이 더 자연스럽다.
- 이 자료는 왜 `SentencePiece`라는 말만으로는 tokenizer algorithm이 특정되지 않는지 설명하는 보조 reference다.
- second_try 문서에서는 `SentencePiece unigram`이라고 정확히 써야 한다.

## 주의점

- WordPiece의 `##` convention은 XLM-R SentencePiece의 `▁` whitespace marker와 다르다.
- BPE merge rule 방식과 UnigramLM probability/pruning 방식은 다르므로, BPE식 merge intuition을 그대로 적용하면 안 된다.
- HF tokenizer API가 같아 보여도 underlying model이 다르면 vocab merge 방식이 달라져야 한다.

## Plan 반영

- Plan의 tokenizer method를 `SentencePiece unigram`으로 고정.
- command/config에 `model_type=unigram` 기록.
- WordPiece/BPE 방식은 비교 대상이 아니라 background로만 사용.
