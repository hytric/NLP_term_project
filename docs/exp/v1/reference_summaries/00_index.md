# Reference Summaries Index

작성일: 2026-06-10

이 폴더는 second_try 실험 계획을 세우기 전에 각 reference를 개별로 요약한 기록이다.
종합본은 상위 폴더의 `reference_summary.md`에 있다.

## Files

| Summary | Source PDF | Role |
| --- | --- | --- |
| `2305.12182v2_glot500.md` | `docs/survey/2305.12182v2.pdf` | Glot500 논문 방법론 |
| `2406.11477v3_low_resource_vocab_expansion.md` | `docs/survey/2406.11477v3.pdf` | 저자원 vocab expansion 전략 |
| `glot500_extension_tutorial.md` | `docs/survey/GLOT500_extension.pdf` | Glot500-style extension tutorial |
| `vocab_extension_tutorial.md` | `docs/exp/second_try/feedback/vocab_extension_tutorial.pdf` | embedding init 방법 비교 |
| `unigram_lm.md` | `docs/survey/unigramLM.pdf` | SentencePiece unigram 원리 |
| `bpe_wordpiece.md` | `docs/survey/BEP_WordPiece.pdf` | BPE/WordPiece와 unigram 비교 |
| `term_project_guideline.md` | `docs/survey/termProjectGuideLine.pdf` | 과제 산출물/평가 요구사항 |

## Synthesis Target

개별 요약을 종합해 second_try에서는 다음 방향으로 정리한다.

- `xlm-roberta-base`를 base encoder로 사용한다.
- 기존 XLM-R vocabulary/token id는 보존하고 새 target token만 append한다.
- target10 Bible corpus로 SentencePiece unigram tokenizer를 학습한다.
- vocab size는 `8k`, `16k`, `32k` grid로 비교한다.
- embedding initialization은 tutorial 기준 가능한 방법을 비교한다.
- 번역은 제외하고 encoder-only downstream task를 사용한다.
- 최종 주장은 tokenizer bottleneck 완화와 downstream proxy task 개선 여부로 잡는다.
