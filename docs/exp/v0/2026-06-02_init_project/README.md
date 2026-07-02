# 2026-06-02 Init Project

이 폴더는 NLP 텀프로젝트를 논문화 가능한 실험 프로젝트로 발전시키기 위한 작업 노트이다.
현재 목표는 Coptic-Syriac NMT 과제 가이드라인과 서베이 PDF를 바탕으로, 단계별 실험 계획과 novelty 후보를 명확히 만드는 것이다.

## 문서 구조

- [00_project_guideline.md](./00_project_guideline.md): 전체 프로젝트 방향, 산출물, 단계별 로드맵
- [01_survey_synthesis.md](./01_survey_synthesis.md): 서베이 PDF별 핵심 내용과 실험적 함의
- [02_experiment_matrix.md](./02_experiment_matrix.md): baseline, ablation, novelty 후보를 관리하는 실험 매트릭스
- [03_data_inventory.md](./03_data_inventory.md): 데이터 소스 후보, 현재 근거, 검증해야 할 라이선스/품질 이슈
- [04_novelty_ranking.md](./04_novelty_ranking.md): 논문화 가능성이 높은 novelty 후보와 우선순위
- [05_progress_report_outline.md](./05_progress_report_outline.md): 2026-06-12 progress report와 최종 보고서 초안 구조

## 현재 판단

첫 번째 연구 질문은 "Coptic과 Syriac처럼 웹 중심 수집 파이프라인에서 빠진 고문헌 언어를, Glot500 계열 모델에 어떻게 안정적으로 추가할 수 있는가?"로 잡는다.

초기 실험 축은 다음 5개이다.

1. Tokenization audit: 기존 tokenizer가 Coptic/Syriac을 얼마나 과분절하는지 측정한다.
2. Vocabulary extension: SentencePiece unigram 기반 새 토큰을 추가한다.
3. Embedding initialization: random, mean, align 계열 초기화를 비교한다.
4. Continued pretraining: target-only와 Glot500-mixed 학습을 비교한다.
5. Translation transfer: pivot/multitask/back-translation으로 Coptic-Syriac NMT 성능을 끌어올린다.

## 다음 액션

- 데이터 소스별 수집 가능성, 라이선스, 예상 문장 수를 표로 확정한다.
- Coptic/Syriac 샘플 100-1000문장으로 tokenizer audit 스크립트를 먼저 만든다.
- 실험 결과가 생길 때마다 `02_experiment_matrix.md`의 표를 업데이트한다.
