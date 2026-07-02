# Survey Synthesis

이 문서는 `docs/survey` 아래 PDF들을 프로젝트 의사결정에 직접 연결하기 위한 요약이다.

## 1. PDF별 핵심

| File | 핵심 내용 | 프로젝트에 주는 의미 |
| --- | --- | --- |
| `termProjectGuideLine.pdf` | Coptic <-> Syriac NMT 과제 요구사항. Glot500+decoder와 NLLB extension 중 선택, vocab extension, embedding initialization, multi-task, back-translation, BLEU/chrF++/정성 분석 요구. | 과제의 최소 성공은 번역 모델이지만, 논문화하려면 ablation으로 "왜 좋아졌는지"를 보여야 한다. |
| `2305.12182v2.pdf` | Glot500 논문. XLM-R를 511개 언어로 확장, SentencePiece unigram vocab extension, 151K new token, 401K vocab, 30K sentence threshold, MLM continued pretraining. | Coptic/Syriac을 Glot500 방식으로 추가하는 것이 자연스러운 baseline. mixed data는 forgetting 방지 논리로 중요하다. |
| `GLOT500_extension.pdf` | Coptic/Syriac case study 튜토리얼. Glot500에 Coptic/Syriac이 빠진 이유를 웹 중심 수집 파이프라인 한계로 해석. Mean/Align initialization 추천, full vs LoRA/hybrid 비교 제안. | 논문화 framing의 핵심. "데이터 부재"가 아니라 "수집 파이프라인 부재"라는 contribution을 세울 수 있다. |
| `2406.11477v3.pdf` | 저자원 vocabulary expansion 연구. 30K sentences 또는 약 0.01GB 조건에서 random/full CLM이 항상 최적이 아니며, Mean/Align 같은 heuristic initialization과 제한적 layer update/MTP/short sequence 전략을 추천. | 작은 Coptic/Syriac 데이터에서 random init을 약한 baseline으로 두고, Mean/Align을 강한 baseline 또는 novelty 축으로 삼는다. |
| `unigramLM.pdf` | SentencePiece unigram의 EM 기반 segmentation 학습 설명. XLM-R, NLLB, Glot500 계열과 관련. | 새 tokenizer를 SentencePiece unigram으로 학습해야 하는 이유와 vocab size 선택 논리를 보고서에 설명할 수 있다. |
| `BEP_WordPiece.pdf` | BPE와 WordPiece의 merge criterion, word-position handling, 모델별 tokenizer 차이 설명. | tokenizer audit에서 BPE/WordPiece/UnigramLM 차이를 개념적으로 정리하는 배경 자료. |

## 2. Survey에서 나온 프로젝트 제약

### Data

- Coptic과 Syriac 직접 parallel data는 극히 적을 가능성이 높다.
- Bible, Greek, English, Arabic pivot이 사실상 필수다.
- evaluation set은 학습 데이터와 분리된 500-1000개 aligned sentence가 필요하다.
- Coptic은 Greek look-alike 문자와 Unicode normalization 문제가 중요하다.
- Syriac은 script block 검증과 punctuation/sentence segmentation 문제가 중요하다.

### Model

- Glot500-m은 encoder-only라 NMT를 위해 decoder가 필요하다.
- NLLB는 pretrained decoder/cross-attention이 있으나 Coptic/Syriac knowledge가 없어서 vocab extension은 여전히 필요하다.
- 첫 연구 단계는 NMT보다 encoder/tokenizer adaptation이 선명하다.

### Evaluation

- BLEU만으로는 부족하다.
- chrF++를 primary-ish metric으로 보고, BLEU는 표준 비교로 유지한다.
- qualitative analysis가 필수다.
- tokenizer metrics와 NMT metrics를 연결하면 novelty가 강해진다.

## 3. 핵심 가설

### H1. Tokenizer bottleneck

기존 Glot500/NLLB tokenizer는 Coptic/Syriac을 지나치게 character-level로 분해한다.

Evidence plan:

- 기존 tokenizer와 새 tokenizer의 fertility, sequence length, single-character token ratio 비교
- 실제 Coptic/Syriac 예문 tokenization 시각화

### H2. Initialization bottleneck

저자원 조건에서는 새 token embedding random initialization이 불안정하고, mean/align initialization이 더 안정적인 학습을 만든다.

Evidence plan:

- initialization별 MLM loss curve
- validation pseudo-perplexity
- NMT chrF++/BLEU 차이

### H3. Data-pipeline novelty

Coptic/Syriac은 실제 텍스트 전통이 있는데도 웹 중심 multilingual corpus 수집에서 누락된다.

Evidence plan:

- 수집 가능한 academic/religious source inventory
- 30K sentence threshold 충족 여부
- Glot500/NLLB coverage gap 정리

### H4. Pivot transfer necessity

Direct pair만으로는 부족하고, Greek/English/Arabic auxiliary pair와 back-translation이 성능을 결정한다.

Evidence plan:

- direct-only vs multitask auxiliary vs pivot synthetic vs back-translation 비교

## 4. 논문 contribution 후보 문장

초안:

> We study the adaptation of multilingual pretrained models to Coptic and Classical Syriac, two historically important but unsupported ancient languages. We show that their omission from web-derived multilingual corpora is better understood as a data discovery failure than a true data scarcity problem, and evaluate vocabulary extension, span-aware embedding initialization, and pivot-based NMT training for Coptic-Syriac translation.

한국어 해석:

> 본 연구는 Glot500/NLLB가 지원하지 않는 Coptic과 Classical Syriac을 대상으로 multilingual pretrained model 확장 방법을 분석한다. 이 언어들의 누락은 데이터 부재라기보다 웹 중심 수집 파이프라인의 한계로 볼 수 있으며, vocabulary extension, span-aware embedding initialization, pivot 기반 NMT 학습을 통해 Coptic-Syriac 번역 성능을 평가한다.

## 5. Related Work 정리 방향

### Glot500

- horizontal scaling: 더 큰 모델보다 더 많은 언어를 포괄
- XLM-R continued pretraining
- SentencePiece unigram으로 새 vocab 학습 후 기존 vocab과 merge
- 30K sentence threshold
- mixed training으로 catastrophic forgetting 완화

### Vocabulary Expansion in Low Resource

- high-resource 방식인 random init + full continual pretraining은 저자원에서 불안정할 수 있음
- Mean/Align/FOCUS 계열 initialization이 중요
- 데이터가 작으면 short sequence, 더 많은 update, 제한적 layer update가 유리할 수 있음

### Tokenizer Algorithms

- BPE: frequent pair merge
- WordPiece: PMI-like criterion, word-initial/internal distinction
- UnigramLM: 가능한 segmentation을 latent variable로 두고 EM으로 token probability 추정
- XLM-R/NLLB/Glot500 계열은 SentencePiece unigram과 연결됨

## 6. 아직 확인해야 할 질문

- Coptic/Syriac이 실제 Glot500 tokenizer에서 어떤 fallback 패턴을 보이는가?
- `cis-lmu/glot500-base` tokenizer 파일을 로컬/온라인에서 어떻게 확보할 것인가?
- Coptic/Syriac corpus를 재배포 가능한 형태로 공개할 수 있는가?
- Align initialization 구현 시 byte span과 Unicode character span 중 무엇을 기준으로 삼을 것인가?
- NMT 단계에서 Glot500 encoder + decoder를 직접 구성할지, NLLB baseline을 먼저 만들지 결정해야 한다.
