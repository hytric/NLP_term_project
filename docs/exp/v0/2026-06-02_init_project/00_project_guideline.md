# Coptic-Syriac NMT Term Project Guideline

## 0. 프로젝트 한 줄 정의

Glot500/NLLB가 직접 지원하지 않는 Coptic과 Syriac에 대해 tokenizer extension, embedding initialization, multilingual transfer를 단계적으로 검증하고, 최종적으로 Coptic <-> Syriac 양방향 번역 시스템과 논문화 가능한 ablation 결과를 만든다.

## 1. 과제 요구사항 정리

출처: `docs/survey/termProjectGuideLine.pdf`

필수 산출물:

- Coptic -> Syriac, Syriac -> Coptic 양방향 번역 모델
- held-out test set 기준 BLEU, chrF++, 정성 분석
- design choice, data collection, training pipeline, results, ablation을 포함한 10페이지 보고서
- GitHub 코드와 재현성 문서

권장 평가:

- 500-1000개의 고품질 Bible-aligned Coptic/Syriac 평가 문장
- 50-100개 샘플 수동 alignment 검증
- sacrebleu 기반 BLEU, chrF++, 20-50개 예문 정성 분석

수업 일정:

- 2026-06-12: Progress report
- 2026-06-19: Final presentation
- 2026-07-03: Term paper + GitHub link submission

## 2. 연구 문제

### Main Question

저자원 고문헌 언어가 기존 multilingual model의 vocabulary와 웹 중심 수집 파이프라인에서 빠졌을 때, 어떤 tokenizer extension과 embedding initialization 전략이 실제 번역 품질과 representation quality를 가장 안정적으로 개선하는가?

### Sub Questions

- Coptic/Syriac은 기존 Glot500-m 또는 NLLB tokenizer에서 얼마나 과분절되는가?
- 새 subword vocabulary를 추가하면 sequence length, fertility, UNK/byte fallback 비율이 얼마나 개선되는가?
- 제한된 데이터에서 random initialization이 실패하고 mean/align initialization이 더 안정적인가?
- Coptic/Syriac target-only continued pretraining과 Glot500 mixed continued pretraining 중 어느 쪽이 target 성능과 catastrophic forgetting 사이에서 나은가?
- 직접 Coptic-Syriac 데이터가 적을 때 Greek/English/Arabic pivot 및 back-translation이 얼마나 도움이 되는가?

## 3. 현재 추천 방향

### Base Model

1순위: Glot500-m encoder 기반 실험

- 장점: XLM-R 기반, 약 395M 규모, low-resource representation 연구에 적합, 이 저장소의 tokenizer/pretraining/evaluation 코드와 잘 맞음
- 단점: decoder가 없어서 NMT 단계에서 별도 decoder 초기화 또는 seq2seq 구성이 필요함

2순위 baseline: NLLB-200 distilled 모델

- 장점: encoder-decoder와 cross-attention이 이미 translation에 학습되어 있음
- 단점: Coptic/Syriac 자체는 지원하지 않아 vocabulary extension은 여전히 필요하고, 반복 실험 비용이 큼

초기 판단:

- 논문화 목표에는 Glot500-m 기반이 더 선명하다. "Glot500의 automatic collection pipeline이 놓친 고문헌 언어를 학술 소스 기반으로 추가한다"는 contribution이 자연스럽다.
- 단, 최종 NMT 성능 비교를 위해 작은 NLLB baseline은 유지한다.

## 4. 단계별 로드맵

### Phase 0. Corpus Inventory

목표: 수집 가능한 데이터와 라이선스, split 가능성을 확정한다.

할 일:

- Coptic: Coptic Scriptorium, Coptic Bible, Sahidica, Nag Hammadi, Shenoute corpus 후보 조사
- Syriac: Peshitta, Beth Mardutho/SEDRA, CAL, Syriaca.org 후보 조사
- Parallel: Coptic-English, Syriac-English, Coptic-Greek, Syriac-Greek, Bible verse alignment
- 각 소스별 `language`, `domain`, `sentence_count`, `parallel_target`, `license`, `redistributable`, `notes` 기록

성공 조건:

- Coptic/Syriac 각각 최소 30K sentence 목표 가능성 판단
- 평가용 500-1000 aligned sentence 후보 확보

### Phase 1. Tokenization Audit

목표: vocabulary extension이 필요한 이유를 수치로 증명한다.

측정값:

- average tokens per sentence
- character/token fertility
- percentage of single-character tokens
- byte fallback 또는 unknown-like fragmentation 비율
- script purity: Coptic block U+2C80-U+2CFF, Syriac block U+0700-U+074F

비교 tokenizer:

- Glot500-m tokenizer
- XLM-R tokenizer
- NLLB tokenizer
- 새로 학습한 Coptic/Syriac SentencePiece unigram tokenizer

성공 조건:

- "기존 tokenizer는 Coptic/Syriac을 과분절한다"는 표와 예시 확보
- 이후 vocab extension의 motivation으로 바로 사용 가능

### Phase 2. Vocabulary Extension

목표: Coptic/Syriac 새 subword token을 추가하고 tokenizer 품질 개선을 확인한다.

기본 설정:

- SentencePiece unigram
- character_coverage=1.0
- initial vocab 후보: 8K, 16K, 32K 중 데이터 규모에 따라 선택
- 기존 Glot500 tokenizer와 merge하여 genuinely new token만 추가

Ablation:

- no extension
- Coptic-only extension
- Syriac-only extension
- joint Coptic+Syriac extension
- joint + pivot language anchors, 예: Greek/English/Arabic 일부 포함

성공 조건:

- sequence length 감소
- single-character token 비율 감소
- target script coverage 개선

### Phase 3. Embedding Initialization

목표: 새 token embedding 초기화 방법을 비교한다.

비교군:

- Random: 가장 약한 baseline
- Mean: 새 token을 기존 tokenizer로 다시 분해하고 constituent embedding 평균 사용
- Align: 새 tokenizer와 기존 tokenizer의 character span alignment를 통해 corpus occurrence 기반 평균 사용

초기 가설:

- 제한된 Coptic/Syriac 데이터에서는 random initialization이 불안정하다.
- Mean은 구현이 쉽고 강한 첫 baseline이다.
- Align은 character-span 구현이 필요하지만 저자원 조건에서 가장 설득력 있는 novelty 후보가 될 수 있다.

성공 조건:

- MLM validation loss 또는 pseudo-perplexity 비교
- downstream tokenization/NMT 결과와 연결
- 학습 초기 gradient 안정성, loss curve 차이 기록

### Phase 4. Continued Pretraining

목표: Glot500-m encoder를 Coptic/Syriac에 적응시킨다.

비교군:

- target-only full fine-tuning
- target + Glot500 sample full fine-tuning
- target-only LoRA/hybrid
- target + Glot500 sample LoRA/hybrid

권장 기본값:

- mixed sampling alpha=0.3 계열을 우선 검토
- target language oversampling
- catastrophic forgetting 측정을 위해 기존 Glot500 평가 일부 유지

성공 조건:

- Coptic/Syriac pseudo-perplexity 또는 MLM loss 개선
- 기존 언어 성능 손실이 과도하지 않음
- NMT encoder로 사용할 체크포인트 선정

### Phase 5. NMT Baselines

목표: Coptic <-> Syriac 번역 baseline을 만든다.

Baseline ladder:

- B0: pivot-only, Coptic -> Greek/English -> Syriac
- B1: no vocabulary extension seq2seq baseline
- B2: vocabulary extension + random init
- B3: vocabulary extension + mean init
- B4: vocabulary extension + align init
- B5: B4 + multitask auxiliary pairs
- B6: B5 + back-translation round 1
- B7: B5 + back-translation round 2

데이터 믹스:

- direct Coptic-Syriac if available
- Coptic-Greek, Greek-Syriac
- Coptic-English, English-Syriac
- Coptic-Arabic, Syriac-Arabic if available

성공 조건:

- BLEU, chrF++ reporting 가능
- qualitative examples 20-50개 수집
- baseline 대비 개선 원인을 tokenizer/embedding/data mix 중 하나로 설명 가능

## 5. Novelty 후보

### N1. Academic-source recovery for missed ancient languages

Glot500은 511개 언어를 다루지만 Coptic/Syriac은 빠져 있다. 이 프로젝트는 "데이터가 없어서"가 아니라 "웹 중심 수집 파이프라인이 못 찾는 학술/고문헌 데이터라서" 빠진 사례로 framing할 수 있다.

검증:

- 각 언어별 30K sentence threshold 충족 가능성
- 수집 소스의 도메인/라이선스/품질 분석
- Glot500 pipeline limitation에 대한 case study

### N2. Span-aligned embedding initialization for unseen scripts

Mean initialization보다 더 corpus-aware한 Align initialization을 Coptic/Syriac에 적용한다.

검증:

- initialization별 MLM loss curve
- token fertility 개선 이후 NMT 성능 차이
- 저자원 데이터량별 sensitivity, 예: 5K/10K/30K sentence

### N3. Tokenization quality as a predictor of ancient-language NMT

번역 성능만 보고 끝내지 않고, tokenizer metrics와 chrF++/BLEU의 상관을 분석한다.

검증:

- fertility, single-char ratio, sequence length reduction
- chrF++ improvement와의 correlation
- 언어별 Coptic/Syriac 차이 분석

### N4. Pivot-consistency training

직접 Coptic-Syriac data가 부족한 조건에서 Greek/English pivot 경로의 consistency를 regularization 또는 synthetic data selection 기준으로 사용한다.

검증:

- pivot-only baseline
- direct fine-tuning
- pivot consistency filtering 후 synthetic pair 학습
- back-translation round별 성능 변화

### N5. Forgetting-aware low-resource extension

target language 성능만 보지 않고 Glot500 기존 언어 일부의 representation 성능 저하를 같이 측정한다.

검증:

- target-only vs mixed continued pretraining
- full fine-tuning vs LoRA/hybrid
- 기존 Glot500 retrieval/roundtrip subset 성능

## 6. Progress Report용 최소 결과 세트

2026-06-12까지 현실적인 최소 패키지:

- survey synthesis 1장
- 데이터 소스 inventory 초안
- tokenizer audit 표
- baseline experiment matrix
- novelty 후보 2개와 실험 설계
- 실패/리스크 목록

## 7. Final Presentation용 최소 결과 세트

2026-06-19까지 목표:

- tokenizer extension 완료
- random vs mean 또는 mean vs align 중 최소 1개 비교
- MLM adaptation loss curve
- 작은 NMT baseline 또는 pivot baseline
- BLEU/chrF++ 초기 결과
- qualitative examples

## 8. Term Paper 구조 초안

1. Introduction
2. Related Work: Glot500, vocabulary extension, tokenizer algorithms, low-resource NMT
3. Data: Coptic/Syriac sources, preprocessing, split, evaluation set
4. Method: tokenizer extension, embedding initialization, continued pretraining, NMT
5. Experiments: baselines and ablations
6. Results: tokenization, MLM, NMT metrics, qualitative analysis
7. Discussion: novelty, failure modes, limitations
8. Conclusion

## 9. 현재 repo에서 바로 이어질 구현 TODO

- `scripts` 또는 `analysis` 폴더에 tokenizer audit 스크립트 추가
- `data_inventory.tsv` 작성
- Coptic/Syriac 샘플 데이터 위치 확정
- `tokenization/run.py`가 `XLMRobertaTokenizer` import 없이 사용되는지 확인하고 필요하면 수정
- NMT용 seq2seq training scaffold는 별도 폴더로 분리

## 10. 리스크

- 직접 Coptic-Syriac parallel data가 거의 없을 수 있음
- Bible verse alignment는 문장 단위 의미 대응이 거칠 수 있음
- 고문헌 데이터 라이선스 때문에 공개 가능한 데이터와 학습 가능한 데이터가 다를 수 있음
- Coptic은 Greek look-alike 문자 정규화가 성능에 큰 영향을 줄 수 있음
- BLEU가 낮게 나와도 chrF++와 정성 분석에서 의미 있는 개선을 보여야 함
