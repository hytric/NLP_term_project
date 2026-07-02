# Building A Coptic-Syriac Neural Machine Translator

Source: `docs/survey/termProjectGuideLine.pdf`

## 핵심 내용

- 원 과제 가이드는 Coptic ↔ Syriac NMT 시스템 구축을 목표로 한다.
- 산출물은 작동 모델, held-out test 평가, BLEU/chrF++/정성 분석, report, reproducible code를 요구한다.
- 모델 선택지는 Glot500 encoder + decoder 또는 NLLB-200 fine-tuning 등이다.
- low-resource ancient language에서 tokenizer extension, embedding initialization, data split, leakage 방지가 중요하다고 본다.

## Second_try에서 달라지는 점

- 사용자 결정에 따라 번역/NMT는 제외한다.
- XLM-R-base는 encoder-only 모델이므로 decoder 학습 대신 encoder-only downstream proxy task를 사용한다.
- BLEU/chrF++ 대신 classification/retrieval metric을 중심으로 둔다.

## 가져올 요구사항

- held-out test split을 명확히 둔다.
- train/dev/test leakage를 방지한다.
- 정량 평가와 정성 sample을 모두 남긴다.
- report에 data source, preprocessing, model config, compute, seed, metric을 명시한다.
- failure case 분석을 포함한다.

## Plan 반영

- Book-level split: train/dev/test를 book 기준으로 나눈다.
- Stage별 `results.md`, TSV, sample markdown을 남긴다.
- 최종 분석에 qualitative examples와 limitations를 포함한다.
- Downstream task는 `book/genre classification`, `verse retrieval/ranking`, `parallel verse matching`으로 재정의한다.
