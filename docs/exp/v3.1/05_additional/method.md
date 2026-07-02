아래 6개는 Glot500이 MLM으로 학습한 representation이 실제로 쓸 만한지 보기 위해 사용한 평가 방식입니다. Glot500은 NSP나 sentence similarity objective를 학습한 것이 아니라, XLM-R-base에 vocabulary extension을 하고 Glot500-c로 MLM continued pretraining한 뒤 여러 downstream task로 평가했습니다. Glot500 논문은 평가 task를 pseudoperplexity, sentence retrieval, text classification, NER, POS, roundtrip alignment로 정리합니다.  

1. Pseudoperplexity

Pseudoperplexity는 MLM encoder가 어떤 언어의 문장을 얼마나 자연스럽게 예측하는지 보는 지표입니다.

일반적인 GPT류 language model은 왼쪽에서 오른쪽으로 다음 token을 예측하므로 perplexity를 바로 계산할 수 있습니다.

I went to the library .
        ↓
다음 token 확률을 순서대로 계산

하지만 XLM-R/Glot500은 bidirectional MLM encoder입니다. 왼쪽에서 오른쪽으로 다음 token을 예측하는 모델이 아닙니다. 그래서 문장의 각 token을 하나씩 mask하고, 그 token을 얼마나 잘 맞히는지 봅니다.

예:

원문:
I went to the library .
Step 1:
<MASK> went to the library .  → I 확률 계산
Step 2:
I <MASK> to the library .  → went 확률 계산
Step 3:
I went <MASK> the library .  → to 확률 계산

이렇게 모든 token을 하나씩 mask해서 얻은 확률을 모아 계산한 것이 pseudoperplexity입니다. 낮을수록 좋습니다.

Glot500에서는 low-resource/tail language에서 XLM-R보다 pseudoperplexity가 크게 낮아졌습니다. 논문 표에서 tail language 평균은 XLM-R-base가 304.2, Glot500-m이 12.2입니다.  

의미:

이 언어의 문장을 모델이 내부적으로 더 잘 표현하고 예측한다.

단, 이것은 번역 성능이 아니라 monolingual language modeling quality에 가깝습니다.

⸻

2. Sentence Retrieval

Sentence Retrieval은 두 언어의 parallel sentence가 embedding 공간에서 가까운지 보는 평가입니다.

예를 들어 English–Syriac parallel sentence가 있다고 하면:

English sentence:
The Lord is my shepherd.
Syriac sentence candidates:
1. 정답 번역문
2. 다른 문장
3. 다른 문장
...

모델로 각 문장의 embedding을 만들고 cosine similarity를 계산합니다.

cos(English embedding, Syriac embedding)

정답 번역문이 cosine similarity 기준으로 top-1 또는 top-10 안에 들어가면 성공입니다.

Glot500은 Tatoeba와 Bible aligned sentence를 사용해 sentence retrieval을 평가했습니다. 논문은 layer 8의 average word embeddings를 사용하고 cosine similarity로 nearest neighbor를 찾은 뒤 top-10 accuracy를 계산했다고 설명합니다.  

의미:

두 언어의 같은 의미 문장이 embedding 공간에서 가까운가?

주의할 점:

Glot500이 sentence retrieval을 직접 학습한 것은 아님.
MLM으로 학습한 representation이 cross-lingual retrieval에도 쓸 만한지 평가한 것.

⸻

3. Roundtrip Alignment

Roundtrip Alignment는 word-level representation이 언어 간에 잘 정렬되어 있는지 보는 평가입니다.

아이디어는 이렇습니다.

언어 L1의 단어 w에서 시작
→ L2에서 가장 대응되는 단어로 align
→ L3로 align
→ L4로 align
→ 다시 L1으로 align

마지막에 원래 단어 w로 돌아오면 성공입니다.

예를 단순화하면:

English: God
→ Greek: Θεός
→ Syriac: ...
→ 다시 English: God

원래 단어로 돌아오면, 모델의 contextual embedding이 여러 언어에서 비슷한 의미의 단어를 어느 정도 같은 공간에 놓고 있다고 볼 수 있습니다.

Glot500은 SimAlign을 사용해 Bible test set에서 subword-level alignment를 수행하고, layer 8 representation을 사용했습니다. 평가지표는 roundtrip이 원래 단어로 돌아오는 비율입니다.  

의미:

문장 단위가 아니라 단어/토큰 단위 cross-lingual alignment가 잘 되는가?

Sentence Retrieval이 문장 embedding 평가라면, Roundtrip Alignment는 더 세밀한 word alignment 평가입니다.

⸻

4. NER

NER는 Named Entity Recognition입니다.

문장에서 사람, 장소, 기관 이름 같은 named entity를 찾는 task입니다.

예:

Barack Obama was born in Hawaii.

정답:

Barack Obama → PERSON
Hawaii → LOCATION

Glot500에서는 WikiANN dataset을 사용했습니다. 중요한 것은 대부분의 target language에 충분한 labeled data가 없기 때문에, English로 fine-tuning한 뒤 다른 언어에 zero-shot transfer합니다.  

구조:

1. English NER data로 fine-tune
2. tail language NER test set에 바로 적용
3. F1 score 측정

의미:

English에서 배운 entity recognition 능력이 low-resource language로 transfer되는가?

즉, NER는 Glot500 representation이 token-level semantic/syntactic 정보를 잘 담고 있는지 보는 평가입니다.

⸻

5. POS

POS tagging은 Part-of-Speech tagging입니다. 각 단어의 품사를 맞히는 task입니다.

예:

The dog runs fast.

정답:

The → DET
dog → NOUN
runs → VERB
fast → ADV

Glot500은 Universal Dependencies v2.11을 사용했고, NER와 마찬가지로 English에서 fine-tuning한 뒤 target language에서 zero-shot으로 평가했습니다.  

구조:

1. English POS data로 fine-tune
2. low-resource language POS test set에 평가
3. F1 score 측정

의미:

모델이 언어 간에 품사/문법 구조를 공유된 representation으로 잡고 있는가?

NER보다 더 문법적인 task입니다.

⸻

6. Text Classification

Text Classification은 문서나 문장을 특정 class로 분류하는 task입니다.

예:

문장: This movie was amazing.
label: positive

또는 주제 분류라면:

문장: The president announced a new policy.
label: politics

Glot500은 Taxi1500 dataset을 사용했습니다. 이 데이터는 여러 language-script에 대해 6개 class의 text classification gold data를 제공합니다. 평가 방식은 English로 fine-tuning한 뒤 target language-script test set에서 zero-shot으로 평가하는 방식입니다.  

구조:

1. English text classification data로 fine-tune
2. target low-resource language에 바로 적용
3. F1 score 측정

의미:

문장/문서 수준 의미가 언어 간에 잘 transfer되는가?

NER/POS가 token-level 평가라면, text classification은 더 sentence/document-level semantic representation 평가에 가깝습니다.

⸻

전체 정리

평가	보는 것	단위	필요 데이터	해석
Pseudoperplexity	문장을 얼마나 잘 예측하는가	token/language model	monolingual test	낮을수록 좋음
Sentence Retrieval	번역문끼리 가까운가	sentence	parallel sentence	top-k accuracy
Roundtrip Alignment	단어 alignment가 잘 되는가	word/subword	parallel Bible 등	원래 단어로 돌아오는 비율
NER	개체명 인식 transfer	token	WikiANN	F1
POS	품사 구조 transfer	token	UD	F1
Text Classification	문장/문서 의미 transfer	sentence/document	Taxi1500	F1

핵심은 이겁니다.

Glot500 학습 objective:
MLM
Glot500 평가:
MLM으로 생긴 representation이
언어 모델링, 문장 검색, 단어 정렬, NER, POS, 분류에 쓸 만한지 확인

즉, 학습은 MLM 하나지만, 평가는 representation의 여러 측면을 쪼개서 보는 방식입니다.




맞습니다. 전부 downstream evaluation task입니다.
다만 모두 fine-tuning 없이 하는 것은 아닙니다.

Glot500 평가는 크게 두 종류로 나뉩니다.

1. Fine-tuning 없이 바로 평가하는 것

이건 pretrained Glot500-m representation을 그대로 뽑아서 평가합니다.

Task	Fine-tuning 여부	설명
Pseudoperplexity	없음	test 문장의 token을 하나씩 mask해서 MLM 확률 계산
Sentence Retrieval	없음	문장 embedding 뽑고 cosine similarity로 정답 번역문 검색
Roundtrip Alignment	없음	SimAlign으로 word alignment 수행 후 원래 단어로 돌아오는지 평가

즉, 이 세 개는:

Glot500-m을 그대로 사용
→ representation 추출
→ metric 계산

입니다.

특히 sentence retrieval은 모델을 추가 학습하지 않고, layer 8의 average word embedding과 cosine similarity를 사용해 nearest neighbor를 찾습니다. Glot500 논문도 sentence retrieval과 roundtrip alignment를 representation quality 평가로 사용합니다.  

2. English에서 fine-tuning 후 zero-shot 평가하는 것

아래 task들은 fine-tuning을 합니다.
하지만 target low-resource language에서 fine-tuning하는 게 아니라, English labeled data로 fine-tuning한 뒤 target language에 zero-shot transfer합니다.

Task	Fine-tuning 여부	평가 방식
NER	English에서 fine-tuning	target language NER test에 zero-shot
POS	English에서 fine-tuning	target language POS test에 zero-shot
Text Classification	English에서 fine-tuning	target language classification test에 zero-shot

구조는 이렇게 됩니다.

Glot500-m
→ English task data로 fine-tuning
→ low-resource language test set에 바로 평가

예를 들어 POS라면:

English UD POS train set으로 fine-tune
→ Yoruba / Tatar / Chechen / 기타 tail language POS test에 평가

NER도 마찬가지입니다.

English WikiANN NER로 fine-tune
→ target language WikiANN NER test에 평가

Text classification도 English classification data로 fine-tune하고 target language-script에서 zero-shot 평가합니다. Glot500 논문은 NER/POS/Text Classification에서 English fine-tuning 후 target language zero-shot 평가를 사용합니다.  

정리

평가	Downstream task인가	Fine-tuning 하나?	목적
Pseudoperplexity	보조 평가/LM 평가	없음	monolingual modeling quality
Sentence Retrieval	downstream representation eval	없음	cross-lingual sentence alignment
Roundtrip Alignment	downstream representation eval	없음	word-level alignment
NER	downstream task	English fine-tuning	token-level transfer
POS	downstream task	English fine-tuning	syntactic transfer
Text Classification	downstream task	English fine-tuning	sentence/document-level transfer

핵심은 이겁니다.

Glot500 학습:
MLM continued pretraining
Glot500 평가:
1) fine-tuning 없는 representation 평가
2) English fine-tuning 후 target zero-shot 평가

그래서 “다 downstream task냐?”에 대한 답은 대체로 맞지만, 엄밀히는 pseudoperplexity는 downstream task라기보다 MLM 기반 intrinsic evaluation에 가깝고, 나머지는 downstream representation/transfer evaluation으로 보면 됩니다.