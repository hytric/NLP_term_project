최종 발표를 기반으로 term report paper 를 최종 작성하여 제출한다.

논문형식에 기반하며, /home/axt/jongha/Glot500-py39-eval/docs/survey 형식을 참고하여 baseline을 작성한다.

이전 발표에 내용이며 여기에 추가되는 피드백을 적용한후 살을 채워 작성한다.

---

feadback

제목 변경 xlm based
init 방법론 비교 및 수렴 정도 비교

downstream task 의 정당성 확보
왜  이런 코드와 방법을 사용했는지 이전 논문들의 레퍼런스를 명시적으로 찾아서 증명해야함.
그리고 자세하게 어떤 방법, step으로 동작하는지 보고

언어 선택의 이유를 더 명시할 필요가 있음
나는 downsteamtask 를 3개 언어씩 포함하도록 정했는데 그거를 table을 따로 하나더 만들어서 설명하기

Sampling strategy training 에서도 적용했는지 확인하고 해당 부분 추가

Embedding Initialization 방법론 2개 더 추가.

최종 table 을 head, tail, all 3개로 만들기 기존 glot500 처럼

그리고 4k-step 이하의 짧은 continued pretraining 과정에서 initialization 방법별 PPPL 감소 추세
이거 실제 loss 그래프를 추가해서 정당성 입증

sentence representation space 안에서도 언어별·계통별 구조를 어느 정도 형성
이거를 1번으로 설명하고

step 별로 이게 어떻게 모이는지를 plot 해서 지역별로 먼저 분류가 되고 다음에 어려운 task 가 분류가 됨을 설명해야함.
그니까 지금 5개 방법중에 가장 잘되는거 step 별로 연속적으로 보여주면서 어떻게 값들이 모이는지를 보여주면 좋을 듯
그거를 5개 다 해보고 비교해보는 것도 좋을 듯

38개 언어 subset의 문장 임베딩 평균값을 2D PCA로 시각화
유지


---

발표내용

# Title

Term project : Glot500 based Low-resource language extension

# Contents

# Previous research

## scaling

Vertical scaling

* 문제를 더 잘 풀기 위해 파라미터 수, 학습 데이터 양, 모델 깊이, 연산량을 키우는 방식

  * Ex) Chatgpt, Claude, scaling-law

horizontal scaling

* 더 많은 언어·도메인·태스크를 포괄하는 방식

* “더 많은 대상을 지원할 수 있는가”

* 데이터가 적은 Low-resource language 지원

## Glot500

horizontal scaling 방식 사용

High-resouece language 의 기존 표현 지식을 기반으로 언어 간 전이를 확장

|                     |              |
| ------------------- | ------------ |
| **Domain**          | **예시**       |
| Religious texts     | 성경, 종교 번역문   |
| News articles       | 뉴스 기사        |
| Scientific papers   | 과학 논문        |
| Wikipedia/web crawl | 위키, 웹 크롤링 문서 |

### Corpus collection

* Low-resource Language는 고품질 데이터셋 확보가 어려움

* web crawling

* data cleaning

  * Language-Scripts

    * 언어만 보는 것이 아니라 language-script 단위로 분리

  * Ngram LMs and Language Divergence

    * 3-gram 모델 만들어서 perplexity 비교 잘못 라벨링된 corpus 를 찾는다.

    * language-script corpus 전체를 검사

  * Chunk-level filter

    * 반복 문자·반복 단어·특수문자·너무 짧은 텍스트·중복 데이터 제거

  * Corpus-level filter

* 30,000 sentence’ 이상 언어만 선별

  * sentence’ : 하나의 학습 단위(chunk) 완전한 한 문장일 수도 있고, 짧은 구절일 수도 있고, 여러 문장이 묶인 paragraph일 수도 있음.

    * 언어마다 특징이 매우 다르기 때문에 수집된 텍스트 단위를 그대로 처리 하기 위한 묶음

최종적으로 Glot500-c 학습 데이터 구축

### Tokenization

* BPE: Byte Pair Encoding

  * 자주 같이 등장하는 문자 쌍을 계속 합치는 방식

* Unigram Language Model

  * Unigram 방식은 처음부터 많은 subword 후보를 만들어두고, 그중 문장을 가장 잘 설명하는 token 조합을 남기는 방식

  * Glot500이 사용하는 방식

Character fallback : 미등록 subword를 Unicode character 단위로 분해, unknown token 발생 가능

Byte fallback : 미등록 문자를 UTF-8 byte 단위로 분해하는 방식

Masked Language Modeling

the multilingual model Glot500-m on a 600GB corpus

1. Vocabulary Extension : 기존 XLM-R tokenizer vocabulary 확장 (Random initialization)

2. Continued Pretraining : XLM-R-base를 Glot500-c로 추가 pretraining

Analysis

성능 = corpus size + script coverage + related language support + model capacity

주변의 유사 언어가 같이 학습될 때 representation이 더 좋아진다.

가까운 관련 언어가 없는 경우에는 continued pretraining한 Glot+1이 더 나은 경우도 있다.  

# Problem statement

Glot500 논문에서 충분히 좋은 결과를 보였지만 아래 세부 디테일 정보는 부족하다

vocabulary extension

Glot500

XLM 100 seen + 500 unseen (target) 같은 mixed corpus로 새 SentencePiece unigram tokenizer 학습

Yamaguchi et al.의 low-resource vocabulary expansion

아주 적은 target language text만으로 auxiliary tokenizer를 새로 학습 후 기존 vocab 뒤에 새 token을 append

Embedding Initialization

Random

Mean

FVT

# Novelty

Glot500의 Embedding Initialization 방법론 비교

Glot500 vocabulary extension

Embedding Initialization 3가지 방법

Random

Mean

FVT

Downstream-task로 확장

|                                |                                                     |                     |
| ------------------------------ | --------------------------------------------------- | ------------------- |
| **평가 항목**                      | **무엇을 평가하나**                                        | **해석**              |
| **Pseudoperplexity**           | MLM 모델이 해당 언어 문장을 얼마나 자연스럽게 예측하는지                   | 낮을수록 좋음             |
| **Sentence Retrieval Tatoeba** | 영어 문장과 같은 의미의 다른 언어 문장을 Tatoeba에서 찾는 능력             | Top-10 Acc. 높을수록 좋음 |
| **Sentence Retrieval Bible**   | Bible parallel corpus에서 의미가 같은 문장을 찾는 능력            | Top-10 Acc. 높을수록 좋음 |
| **Text Classification**        | 영어로 fine-tuning한 분류 모델이 다른 언어에도 zero-shot으로 잘 전이되는지 | F1 높을수록 좋음          |
| **NER**                        | 영어 NER 학습 후 다른 언어의 개체명 인식이 가능한지                     | F1 높을수록 좋음          |
| **POS**                        | 영어 POS tagging 학습 후 다른 언어의 품사 태깅이 가능한지              | F1 높을수록 좋음          |
| **Roundtrip Alignment**        | 여러 언어를 거쳐 단어 alignment를 돌렸을 때 원래 단어로 돌아오는지          | Accuracy 높을수록 좋음    |

# Method

## Data

99 language-script = 92 XLM-R-seen + 7 XLM-R-unseen target

|                     |                        |                    |                |                                                           |
| ------------------- | ---------------------- | ------------------ | -------------- | --------------------------------------------------------- |
| **language_script** | **language full name** | **region**         | **new_length** | **Covered tasks**                                         |
| dtp_Latn            | Kadazan Dusun          | Southeast Asia     | 48,468         | Tatoeba, Bible, Roundtrip, Taxi1500, Embedding similarity |
| xav_Latn            | Xavánte                | South America      | 31,765         | Bible, Roundtrip, POS, Taxi1500                           |
| bam_Latn            | Bambara                | West Africa        | 32,150         | Bible, Roundtrip, POS, Taxi1500                           |
| csb_Latn            | Kashubian              | Europe             | 33,743         | Tatoeba, NER, Embedding similarity                        |
| ile_Latn            | Interlingue            | Constructed/Europe | 40,984         | Tatoeba, Embedding similarity                             |
| lij_Latn            | Ligurian               | Europe             | 42,447         | NER, POS                                                  |
| fur_Latn            | Friulian               | Europe             | 30,052         | NER                                                       |

## Tokenization

SentencePiece + Unigram Language Model 사용

Byte Fallback

Sampling strategy: α = 0.3

Head language 를 많이넣으면 vocab size는 고정 되어있는 환경에서 high resource language 에 subtoken 들이 편항됨.

P_i = i번째 language-script가 샘플링될 확률

n_i = i번째 language-script의 데이터 양

α = 0.3

![c5ee9a4f-59f2-40af-bb95-f2c74603433d](/api/assets/v2/workspaces/iiplab/projects/03bc868f-9e88-46da-98fa-c91290e83b29/c5ee9a4f-59f2-40af-bb95-f2c74603433d/)

Head : 1,000,000

Tail : 1,000

α = 1

- P_1 : P_2 = 1000 : 1

α = 0.3

- P_1 : P_2 = 10,000,000^{0.3} : 10,000^{0.3}

- 대략 8 : 1

## Embedding Initialization

Random

N(0, 0.02) random vector

의미 정보 없이 새 token을 무작위 시작점에서 학습

Mean

기존 lexical token embedding들의 평균 vector

pretrained embedding space의 “중앙값” 근처에서 안정적으로 시작

FVT

새 token을 기존 tokenizer로 분해한 뒤 source subtoken embedding 평균

token 표면형/부분형 정보를 살려 의미 있는 위치에서 시작

# Experiments

|                 |                  |
| --------------- | ---------------- |
| Item            | Setting          |
| Base model      | xlm-roberta-base |
| Objective       | MLM              |
| LR              | 5e-5             |
| Adam betas      | (0.9, 0.999)     |
| Effective batch | 384              |
| Max length      | 512              |
| MLM prob        | 0.15             |

Glot500-style vocabulary expansion에서 새 token embedding row 초기화 방식이 XLM-R-unseen low-resource tail language adaptation에 영향을 주는지 확인한다

Target7 : dtp_Latn, xav_Latn, bam_Latn, csb_Latn, ile_Latn, lij_Latn, fur_Latn

MLM train set (samples)

seen/head : 4,147,176

target7 : 335,083

total : 4,482,259

Target evaluation set (samples)

PPPL : 700

Tatoeba : 2,253

Bible : 23,238

Roundtrip : 22,669

NER : 300

POS : 1,342

# Result

fvt가 PPPL, Tatoeba retrieval, Bible retrieval, Roundtrip Alignment에서 가장 좋은 값을 보이며, embedding initialization이 downstream retrieval 계열에도 영향을 준다는 점을 보여준다.

XLM-R-B, XLM-R-L, Glot500-m baseline과 v5.2 initialization ablation을 같은 target task setup에서 비교하기 위한 요약표

|                    |            |               |             |            |           |           |                 |
| ------------------ | ---------- | ------------- | ----------- | ---------- | --------- | --------- | --------------- |
| **Model / Method** | **PPPL ↓** | **Tatoeba ↑** | **Bible ↑** | **Text ↑** | **NER ↑** | **POS ↑** | **Roundtrip ↑** |
| XLM-R-B            | 98.2       | 20.5          | 0.5         | 59.3       | 45.7      | 53.9      | 2.5             |
| XLM-R-L            | 63.7       | 12.8          | 0.4         | 72.9       | 53.9      | 54.4      | 2.8             |
| Glot500-m          | 7.7        | 45.7          | 14.7        | 74.3       | 52.6      | 59.5      | 5.6             |
| random             | 119.6      | 24.9          | 0.6         | 69.7       | 37.7      | 10.9      | 2.0             |
| mean               | 128.3      | 24.6          | 0.6         | 77.8       | 40.5      | 3.9       | 2.2             |
| fvt                | 58.0       | 28.3          | 0.6         | 71.3       | 48.4      | 4.3       | 2.5             |

4k-step 이하의 짧은 continued pretraining 과정에서 initialization 방법별 PPPL 감소 추세

|            |             |              |              |              |              |
| ---------- | ----------- | ------------ | ------------ | ------------ | ------------ |
| **method** | **step500** | **step1000** | **step2000** | **step3000** | **step4000** |
| random     | 374.61      | 241.80       | 160.50       | 133.11       | 119.58       |
| mean       | 479.42      | 270.93       | 172.58       | 138.51       | 128.26       |
| fvt        | 161.88      | 108.60       | 75.26        | 61.60        | 58.03        |

Tokenizer Extension의 Target Languages 에 대한 Subword 분할 비율 감소

|           |                       |                      |               |
| --------- | --------------------- | -------------------- | ------------- |
| **Scope** | **XLM-R tokens/word** | **v5.2 tokens/word** | **Reduction** |
| target7   | 2.204                 | 1.592                | **27.75%**    |

sentence representation space 안에서도 언어별·계통별 구조를 어느 정도 형성

![e40a7ec2-a988-4ed8-bf25-7ff27cd3def6](/api/assets/v2/workspaces/iiplab/projects/03bc868f-9e88-46da-98fa-c91290e83b29/e40a7ec2-a988-4ed8-bf25-7ff27cd3def6/)

|                     |                        |                    |
| ------------------- | ---------------------- | ------------------ |
| **language_script** | **language full name** | **region**         |
| dtp_Latn            | Kadazan Dusun          | Southeast Asia     |
| xav_Latn            | Xavánte                | South America      |
| bam_Latn            | Bambara                | West Africa        |
| csb_Latn            | Kashubian              | Europe             |
| ile_Latn            | Interlingue            | Constructed/Europe |
| lij_Latn            | Ligurian               | Europe             |
| fur_Latn            | Friulian               | Europe             |

38개 언어 subset의 문장 임베딩 평균값을 2D PCA로 시각화

색은 language family를, 삼각형은 tail 언어를, 동그라미는 head/reference 언어를 나타낸다.

![7e097134-7f9a-4144-ae0d-b3bf1ba40b7e](/api/assets/v2/workspaces/iiplab/projects/03bc868f-9e88-46da-98fa-c91290e83b29/7e097134-7f9a-4144-ae0d-b3bf1ba40b7e/)

|             |              |                                       |                                                                      |
| ----------- | ------------ | ------------------------------------- | -------------------------------------------------------------------- |
| 색깔          | Family       | Region                                | 언어                                                                   |
| 파랑 #1f77b4  | Afro-Asiatic | West Africa                           | hau_Latn                                                             |
| 연파랑 #aec7e8 | Austronesian | Southeast Asia, East Africa           | dtp_Latn, ind_Latn, jav_Latn, mlg_Latn, msa_Latn, tgl_Latn           |
| 주황 #ff7f0e  | Bantu        | Southern Africa                       | xho_Latn                                                             |
| 연주황 #ffbb78 | Constructed  | Constructed/Europe                    | epo_Latn, ile_Latn                                                   |
| 초록 #2ca02c  | Germanic     | Europe                                | deu_Latn, eng_Latn, nld_Latn                                         |
| 연초록 #98df8a | Hellenic     | Europe                                | ell_Grek                                                             |
| 빨강 #d62728  | Indo-Aryan   | South Asia                            | mar_Deva                                                             |
| 연빨강 #ff9896 | Koreanic     | East Asia                             | kor_Hang                                                             |
| 보라 #9467bd  | Kra-Dai      | Southeast Asia                        | lao_Laoo                                                             |
| 연보라 #c5b0d5 | Macro-Je     | South America                         | xav_Latn                                                             |
| 갈색 #8c564b  | Mande        | West Africa                           | bam_Latn                                                             |
| 연갈색 #c49c94 | Romance      | Europe                                | cat_Latn, fra_Latn, fur_Latn, ita_Latn, lij_Latn, por_Latn, ron_Latn |
| 분홍 #e377c2  | Semitic      | Middle East, Middle East/North Africa | ara_Arab, heb_Hebr                                                   |
| 연분홍 #f7b6d2 | Sinitic      | East Asia                             | cmn_Hani                                                             |
| 회색 #7f7f7f  | Slavic       | Europe                                | ces_Latn, csb_Latn, hrv_Latn, pol_Latn, slk_Latn, slv_Latn           |
| 연회색 #c7c7c7 | Uralic       | Europe                                | est_Latn, fin_Latn, hun_Latn                                         |

# Conclusion and limitation

Glot500-style tokenizer extension이 tail language의 subword fragmentation을 줄인다

Vocabulary embedding initialization

FVT는 기존 XLM-R subtoken embedding을 재사용해 새 token을 더 좋은 위치에서 시작하게 만든다.

MLM, Downstream-task 에서 빠른 수렴한다.

Representation Analysis

Tail language identity와 family/typology 구조가 관찰

Limitation

학습이 수렴점에 도달하지 못함.

FVT가 모든 task에서 항상 best는 아님

family similarity plot은 전체 90/99개 언어가 아니라 38개 language subset에 대한 분석

# Reference

# Appendix

Sentence embedding 추출 방법

Glot500의 retrieval 방법에서 차용

각 raw sentence를 tokenizer로 인코딩

AutoModel로 forward

hidden states 중 layer index 7, 즉 0-index 기준 8번째 layer 선택

special token과 padding token을 제외하고 token hidden states를 mean pooling

pooling된 sentence vector를 L2 normalize

전체 sentence vector 평균을 빼서 centered normalize

언어별 centroid는 해당 언어 sentence vectors의 평균

![370f8ef1-f044-4c01-b7ae-369314743e42](/api/assets/v2/workspaces/iiplab/projects/03bc868f-9e88-46da-98fa-c91290e83b29/370f8ef1-f044-4c01-b7ae-369314743e42/)

다음 그림은 원래 glot600 score

#
