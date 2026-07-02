# 05 Additional Task별 결과 정리

작성일: 2026-06-19

이 폴더는 `method.md`의 Glot500-style evaluation task 구분에 맞춰 `05_additional` 결과를 task별로 정리한다.

각 task 문서는 같은 형식을 따른다.

> Task 정의 -> 데이터/설정 -> 결과 -> 해석 -> 주장 가능 범위 -> 산출물

## Task Index

| Task | File | 상태 | 현재 주장 |
| --- | --- | --- | --- |
| Pseudoperplexity / MLM Intrinsic Evaluation | `01_pseudoperplexity_mlm_intrinsic.md` | sampled pseudoPPL + gold-prob/content-token 진단 추가 완료 | `align/fvt/focus`가 상대적으로 덜 나쁘지만 내용 token MLM은 실질적으로 약함 |
| Sentence Retrieval | `02_sentence_retrieval.md` | target10 CSLS + `mlm200` report filter 추가 완료 | `xlmr_base` 비교는 제외, `mlm200` 내부 retrieval signal도 여전히 약함 |
| Roundtrip Alignment | `03_roundtrip_alignment.md` | 미실행 | future work |
| NER | `04_ner.md` | gold label 없음 | claim 없음 |
| POS Tagging | `05_pos_tagging.md` | Coptic supervised POS pilot 재집계 | token accuracy는 약하게 개선, zero-shot POS는 아님 |
| Text Classification | `06_text_classification.md` | Coptic-Syriac proxy 완료 | shallow pair-classification 개선 |
| Project-Specific Translation Diagnostic | `07_translation_diagnostic.md` | 완료 | collapse는 개선, 번역 품질은 여전히 약함 |

## 공통 배경

- Base model: `xlm-roberta-base`
- Candidate: replay-safe third_try checkpoints 및 `mlm200` initialization variants
- Tokenizer protocol: append-only vocabulary extension
- Tokenizer audit: 기존 XLM-R token id 변경 `0`, appended tokens `30,849`
- 핵심 주의점: v3.1은 Glot500-scale 재현이 아니라 small controlled diagnostic이다.

## 주요 참조 파일

| File | 용도 |
| --- | --- |
| `../method.md` | Glot500-style task 설명 |
| `../method_task_results.md` | 전체 task 통합 결과 |
| `../pseudoperplexity_summary.tsv` | raw sampled pseudoPPL 요약, degenerate `xlmr_base` row 포함 |
| `../pseudoperplexity_summary_expanded_only.tsv` | 보고서용 sampled pseudoPPL 요약, `xlmr_base` 제외 |
| `../pseudoperplexity_tokenization_diagnostics.tsv` | pseudoPPL sample tokenization diagnostic |
| `../pseudoperplexity_accuracy_summary.tsv` | pseudoPPL top-k/content-token diagnostic 요약 |
| `../pseudoperplexity_gold_probability_scores.tsv` | 평균 정답 token 확률 score 요약 |
| `../pseudoperplexity_prediction_samples.tsv` | 실제 content-token 예측 샘플 |
| `../target10_sentence_retrieval_csls_summary.tsv` | raw target10 CSLS sentence retrieval 요약 |
| `../target10_sentence_retrieval_csls_summary_mlm200_only.tsv` | 보고서용 target10 CSLS 요약, `xlmr_base` 제외 |
| `../coptic_pos_summary_replay_safe.tsv` | Coptic POS pilot 요약 |
| `../../02_embedding_downstream/results.md` | pair-classification proxy 결과 |
| `../../03_decoder_translation/results.md` | decoder translation/collapse diagnostic 결과 |
