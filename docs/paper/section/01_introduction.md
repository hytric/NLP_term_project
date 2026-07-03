# 01 Introduction

## 1.1 Motivation: vertical scaling vs. horizontal scaling

대규모 언어모델의 발전은 크게 두 방향으로 나뉜다. **Vertical scaling**은 파라미터 수, 학습 데이터 양, 연산량을 키워 같은 대상을 더 잘 푸는 방향이다(scaling law 계열). **Horizontal scaling**은 더 많은 언어·도메인·태스크를 포괄하는 방향, 즉 "더 많은 대상을 지원할 수 있는가"를 묻는 방향이다. Low-resource language 지원은 전형적인 horizontal scaling 문제다.

XLM-R은 100개 언어를 하나의 MLM으로 학습한 강력한 multilingual encoder지만, 학습에 포함되지 않은 언어(XLM-R-unseen tail language)에서는 두 가지 약점이 남는다. (1) **Token fragmentation**: tokenizer가 해당 언어를 본 적이 없어 한 단어가 여러 subword로 과하게 쪼개진다. (2) **Representation mismatch**: 그 언어의 어휘·형태 정보가 embedding 공간에 정렬돼 있지 않다.

## 1.2 Prior solution: Glot500

Glot500은 horizontal scaling을 위해 두 단계를 결합한다. 먼저 500여 language-script의 mixed corpus로 SentencePiece unigram tokenizer를 다시 학습하여 XLM-R의 vocabulary를 확장하고(**vocabulary extension**), 확장된 모델을 그 corpus 위에서 MLM으로 이어 학습한다(**continued pretraining**). Glot500은 결과를 high-resource(head)와 low-resource(tail)로 나눠 보고하여, 두 그룹의 이득이 다르다는 점을 드러냈다. 본 보고서도 이 head/tail/all reporting 방식을 그대로 가져온다.

## 1.3 Gap: embedding initialization은 별도의 선택이다

Vocabulary를 확장하면 embedding matrix 뒤에 기존에 없던 새 token row가 추가된다. 이 새 row를 어떤 벡터로 시작할지는 tokenizer 설계와 독립적인 **modeling 선택**이다. Glot500 계열은 보통 이를 단순 random으로 처리하지만, 다음과 같은 대안이 가능하다.

- `random`: 정보 없이 무작위 시작.
- `mean`: 기존 embedding들의 중심(centroid)에서 시작.
- `FVT` 계열: 새 token의 표면형을 기존 tokenizer로 다시 쪼개, 그 source subtoken embedding을 재사용해 시작.

본 보고서는 여기에 두 가지 초기화를 **추가로 제안·비교**한다. `weighted FVT`는 FVT의 subtoken 평균을 균등 평균 대신 **표면 길이로 가중**한다 — 긴 source subtoken이 더 구체적인 lexical 신호를 담는다는 가정이다. `family-aware mean`은 표면형 분해 대신, 새 token의 corpus provenance가 가리키는 **language family의 source-token 평균**을 쓴다 — 철자보다 계통(typology) prior가 저자원 token에 더 좋은 출발점을 줄 수 있는지 확인하기 위함이다. 이로써 비교 축은 (무정보) `random` → (전역 centroid) `mean` → (표면형 재사용) `FVT` → (표면형+길이 가중) `weighted FVT` → (계통 prior) `family-aware mean`의 다섯 방법으로 확장된다.

이 선택은 값 하나의 차이처럼 보이지만, continued pretraining의 출발점을 바꾸므로 수렴 속도와 최종 표현에 영향을 줄 수 있다. 그럼에도 동일 조건에서 여러 초기화를 통제 비교한 보고는 드물다.

## 1.4 Our setup

본 보고서는 이 gap을 작은 controlled 설정으로 검증한다. `xlm-roberta-base`를 base로, 92개 XLM-R-seen replay language-script와 7개 XLM-R-unseen target(Target7)을 쓴다. tokenizer는 Glot500 방식(SentencePiece unigram + append-only 주입)으로 고정하고, **새 embedding row 초기화만** 다섯 방법으로 바꿔 continued MLM pretraining을 돌린다. 따라서 결과에서 보이는 method 간 차이는 tokenizer가 아니라 initialization과 그에 따른 training dynamics에서 온다.

## 1.5 Research questions & contributions

- **RQ1.** Glot500-style tokenizer extension이 Target7의 token fragmentation을 실제로 줄이는가?
- **RQ2.** 같은 tokenizer·corpus에서 embedding initialization이 50K-step MLM 수렴에 영향을 주는가?
- **RQ3.** 초기화 차이가 downstream(head/tail/all) 지표에서 나타나는가, 어느 task family에서 두드러지는가?
- **RQ4.** 학습 초반(10K) 순위와 수렴(50K) 순위가 일치하는가, 아니면 뒤바뀌는가?

**Contributions.**

1. **통제된 초기화 ablation 설계.** Glot500-style vocabulary extension에서 tokenizer·corpus·MLM objective·schedule·evaluation을 모두 고정하고 새 embedding row 초기화만 바꾸는, 재현 가능한 controlled ablation을 구성한다. 이로써 관측 차이를 tokenizer가 아니라 initialization으로 귀속할 수 있다.
2. **두 초기화 방법 제안.** 기존 `random`/`mean`/`FVT`에 더해 `weighted FVT`(표면 길이 가중 FVT)와 `family-aware mean`(language family prior)을 제안하고 5-way로 비교한다.
3. **50K 수렴까지의 증거.** 초기화가 50K-step MLM 수렴 loss를 유의하게 바꾸며(FVT 계열 최저, `mean`이 `random`보다도 높음), 이 이득이 학습 초반 noise로 사라지지 않고 수렴까지 유지됨을 보인다.
4. **수렴 시점 downstream 및 crossover 발견.** 50K downstream에서 제안한 두 refinement(`weighted FVT`, `family-aware mean`)가 PPPL·Tatoeba·NER·Roundtrip에서 plain FVT를 **추월**하며, `family-aware mean`은 **NER에서 full Glot500-m까지 능가**함을 보인다. plain FVT는 조기 포화하는 반면 refinement는 수렴 구간에서 계속 개선된다.
5. **표현 공간 진단.** Target7 문장 표현에서 script보다 language/family 구조가 더 강하게 나타남을 centered-cosine과 2D map으로 진단하고, 이 구조가 학습 조기에 형성되어 이후 평탄함을 함께 보고한다.
6. **task별 정당화와 coverage 투명성.** downstream task를 선행연구 근거와 함께 입력→처리→출력→해석으로 정의하고, 언어·task coverage를 명시해 과대해석을 방지한다.

**범위 제한.** "Glot500을 완전 재현했다", "모든 low-resource language에 일반화된다", "Target7이 script diversity를 대표한다"는 주장은 하지 않는다.
