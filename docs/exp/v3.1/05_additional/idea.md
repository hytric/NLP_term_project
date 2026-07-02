Glot500에서 low-resource language를 테스트하는 방식은 “번역 성능”만 보는 게 아니라, 그 언어의 representation이 잘 학습됐는지를 여러 downstream task로 확인하는 방식입니다.

1. 먼저 low-resource / tail language를 어떻게 정의하나

Glot500 논문에서는 XLM-R이 원래 커버하던 약 100개 언어를 head language, 그 외 추가된 언어들을 tail language로 봅니다. 즉, Glot500의 low-resource language 테스트는 대부분 XLM-R에는 없었지만 Glot500-c에 포함된 tail language-script를 대상으로 합니다. Glot500-c는 511개 언어, 534개 language-script를 포함하고, 각 language-script는 최소 30,000 sentence’ 이상 있을 때 학습에 포함됩니다.  

2. 테스트셋 구성

각 언어별 corpus를 다음처럼 나눕니다.

train / dev / test

Glot500은 각 language-script마다 **dev 1000개, test 1000개 sentence’**를 따로 빼고 나머지를 학습에 사용합니다. Bible parallel verse가 있으면 dev/test에 각각 500개씩 추가해서 cross-lingual evaluation에 활용합니다.  

즉, low-resource language라도 최소한 다음 두 종류의 평가가 가능하게 만듭니다.

1. monolingual held-out test set
2. English-aligned / Bible-aligned parallel test set

3. 실제 평가 task

Glot500은 low-resource language를 다음 task들로 평가합니다.

평가 방식	무엇을 보는가	데이터 필요성
Pseudoperplexity	해당 언어 문장을 모델이 얼마나 자연스럽게 예측하는지	monolingual test만 필요
Sentence Retrieval	영어 문장과 해당 언어 문장이 embedding 공간에서 잘 매칭되는지	parallel sentence 필요
Roundtrip Alignment	여러 언어를 거쳐 word alignment를 했을 때 원래 단어로 돌아오는지	parallel Bible 등 필요
NER	영어로 fine-tuning 후 low-resource 언어에 zero-shot 적용	WikiANN 등 gold label 필요
POS tagging	영어 POS로 학습 후 low-resource 언어에 zero-shot 적용	UD 데이터 필요
Text Classification	영어 classification 학습 후 target language zero-shot	Taxi1500 등 필요

논문 표에서는 이 평가들을 Sentence Retrieval Tatoeba, Sentence Retrieval Bible, Text Classification, NER, POS, Roundtrip Alignment로 정리하고, 각각 head/tail language 수를 나눠서 비교합니다.  

4. 핵심은 “zero-shot transfer”

Glot500의 low-resource 테스트는 대부분 이렇게 합니다.

English에서 task fine-tuning
→ low-resource language test set에 바로 평가

예를 들어 POS tagging이면:

1. English UD POS 데이터로 fine-tune
2. Yoruba, Tatar, Chechen 같은 tail language의 POS test set에 평가
3. XLM-R vs Glot500-m 비교

이게 중요한 이유는, low-resource language에는 task-specific labeled data가 거의 없기 때문입니다. 그래서 “그 언어 자체로 supervised training을 잘하냐”보다, multilingual representation이 cross-lingual transfer를 잘하냐를 봅니다.

5. Glot500이 실제로 비교한 기준

기본 비교는 다음입니다.

XLM-R-base
XLM-R-large
Glot500-m

Glot500-m은 XLM-R-base에서 vocabulary를 확장하고 Glot500-c로 continued pretraining한 모델입니다. 평가 결과, tail language에서 Glot500-m이 XLM-R보다 대부분 크게 좋아졌습니다. 예를 들어 논문 표에서 tail language 평균은 다음처럼 나옵니다.  

Task	XLM-R-base	Glot500-m
Pseudoperplexity	304.2	12.2
Sentence Retrieval Tatoeba	32.6	59.8
Sentence Retrieval Bible	7.4	43.2
Text Classification	13.7	46.6
NER	47.5	60.7
POS	41.7	62.3

즉, low-resource language 테스트의 기본 질문은:

XLM-R가 못 보던 tail language에서
Glot500 continued pretraining이 representation을 개선했는가?

입니다.

6. 우리 Coptic/Syriac 프로젝트에 적용하면

Coptic/Syriac은 Glot500에 포함되지 않은 언어이므로, 테스트 구조는 Glot500 방식을 그대로 가져오되 번역 프로젝트에 맞게 바꾸면 됩니다.

A. tokenizer coverage 테스트

먼저 기존 Glot500 tokenizer가 Coptic/Syriac을 어떻게 쪼개는지 확인합니다.

tokenizer.tokenize(coptic_sample)
tokenizer.tokenize(syriac_sample)

확인할 것:

<unk> 비율
평균 token 수
character-level fragmentation 여부

프로젝트 가이드라인도 먼저 Coptic/Syriac text를 tokenization해보고, character 단위 fragment나 <unk>가 많으면 vocabulary extension이 필요하다고 설명합니다.  

B. language modeling 평가

Coptic/Syriac monolingual test set을 따로 빼서:

MLM loss / pseudoperplexity

를 비교합니다.

Glot500 original
vs
Glot500 + Coptic/Syriac vocab extension
vs
Glot500 + continued pretraining

C. translation 평가

텀프로젝트 기준으로는 최종적으로:

Coptic → Syriac
Syriac → Coptic

번역 결과를 평가해야 합니다. 가이드라인은 held-out test set에 대해 BLEU, chrF++, 그리고 qualitative analysis를 요구합니다.  

직접 Coptic–Syriac parallel data가 거의 없으면:

Coptic ↔ English
Syriac ↔ English
Coptic ↔ Greek
Syriac ↔ Greek

같은 pivot/pseudo-parallel 평가를 같이 써야 합니다.

정리

Glot500에서 low-resource language를 테스트하는 핵심 구조는 이겁니다.

1. 각 low-resource language의 held-out test set 확보
2. XLM-R vs Glot500-m 비교
3. monolingual quality: pseudoperplexity
4. cross-lingual quality: sentence retrieval / roundtrip alignment
5. downstream transfer: NER / POS / text classification zero-shot
6. low-resource language에서는 labeled data가 부족하므로 English fine-tune → target zero-shot 평가를 많이 사용

우리 프로젝트에서는 여기에 번역 평가를 추가해서:

tokenization 개선 → MLM/pseudoperplexity 개선 → translation BLEU/chrF++ 개선

순서로 보여주면 됩니다.