지금 2. Embedding initialization 에서 모든 언어 및 문장의 유사도가 너무 높음. 

맞습니다. cosine 유사도가 전체적으로 과하게 높게 나오는 문제는 multilingual encoder에서 흔합니다. 이 경우 “positive pair가 높다” 자체는 별 의미가 없고, positive와 negative를 얼마나 분리하느냐가 핵심입니다.

1. 왜 cosine이 과하게 높게 나오나

Glot500/XLM-R 같은 encoder의 hidden state는 sentence embedding 전용으로 학습된 게 아닙니다. Glot500도 NSP나 contrastive sentence similarity가 아니라 MLM continued pretraining으로 학습했고, sentence retrieval 평가는 layer 8의 average word embedding과 cosine similarity를 사용한 downstream evaluation입니다.  

그래서 sentence embedding을 단순 mean pooling하면 이런 현상이 생길 수 있습니다.

positive pair cosine: 0.94
negative pair cosine: 0.89
random pair cosine:   0.86

겉으로 보면 전부 높습니다. 하지만 문제는 절대값이 아니라:

positive - negative margin이 충분한가?
ranking에서 정답이 위로 올라오는가?

입니다.

2. 주요 원인

A. Embedding anisotropy

BERT/XLM-R류 embedding은 모든 문장이 비슷한 방향으로 몰리는 경향이 있습니다.

즉, 문장 의미와 관계없이 embedding들이 공간의 좁은 cone 안에 모입니다.

대부분 문장쌍 cosine ≈ 0.8~0.95

이러면 cosine similarity가 과하게 높아지고, threshold classification이 어려워집니다.

B. Mean pooling이 공통 성분을 많이 포함함

Mean pooling은 모든 token hidden state를 평균냅니다.

sentence_embedding = mean(token_hidden_states)

그런데 모든 문장에 공통적으로 들어가는 feature가 있습니다.

문장 길이
script 정보
언어 ID 비슷한 신호
punctuation
frequent token pattern
layer-specific common direction

이 공통 성분이 크면, 서로 다른 문장도 cosine이 높게 나옵니다.

C. 같은 도메인 데이터면 더 심함

Coptic/Syriac에서 Bible verse나 종교 문헌을 쓰면 문장들이 원래 비슷합니다.

예를 들어 모든 문장이 이런 도메인에 있으면:

Lord
God
said
came
people
king
disciples

negative pair도 완전히 다른 의미가 아니라 비슷한 lexical/domain distribution을 가집니다. 그러면 random negative도 cosine이 높게 나옵니다.

D. Low-resource script adaptation이 의미보다 script/domain을 잡을 수 있음

Coptic/Syriac adaptation 초반에는 모델이 의미 정렬보다 먼저 다음을 학습할 수 있습니다.

이건 Coptic 문장이다
이건 Syriac 문장이다
이건 종교 텍스트다
이건 비슷한 길이의 verse다

이러면 같은 의미가 아니어도 representation이 가까워질 수 있습니다.

⸻

3. 그러면 cosine threshold classification은 위험함

예를 들어:

cos > 0.85이면 Same

같은 방식은 거의 쓸모가 없을 수 있습니다. 왜냐하면 negative도 0.85를 넘기기 때문입니다.

따라서 “same/different binary classification”보다 먼저 해야 할 것은 ranking evaluation입니다.

4. 더 나은 평가 방식

1. Top-k retrieval

각 Coptic 문장에 대해 모든 Syriac 후보와 cosine을 계산합니다.

Coptic_i vs Syriac_1
Coptic_i vs Syriac_2
...
Coptic_i vs Syriac_N

정답 Syriac_i가 몇 등인지 봅니다.

Top-1 accuracy
Top-5 accuracy
Top-10 accuracy
MRR

cosine 절대값이 전부 높아도, 정답이 항상 상위에 오르면 representation은 쓸 만합니다.

예:

positive cosine = 0.94
negative 평균 = 0.91

라도 정답이 항상 1등이면 괜찮습니다.

반대로:

positive cosine = 0.94
negative cosine = 0.95

가 자주 나오면 문제입니다.

⸻

2. Positive-negative margin

절대 cosine 대신 margin을 봅니다.

margin_i = cos(Coptic_i, Syriac_i)
         - max_j≠i cos(Coptic_i, Syriac_j)

좋은 경우:

margin > 0

나쁜 경우:

margin ≤ 0

보고서에는 평균 cosine보다 이게 더 설득력 있습니다.

Mean positive cosine
Mean random negative cosine
Mean hard negative cosine
Mean margin
Top-k retrieval accuracy

이렇게 같이 제시하면 됩니다.

⸻

5. 해결 방법

A. Centering

전체 sentence embedding 평균을 빼줍니다.

emb = emb - emb.mean(axis=0)

정확히는 train/dev 전체 sentence embedding의 global mean을 구하고, 각 embedding에서 빼는 방식입니다.

global_mean = all_embeddings.mean(axis=0)
emb_centered = emb - global_mean

이렇게 하면 모든 문장에 공통으로 깔린 방향을 제거할 수 있습니다.

⸻

B. Whitening / PCA 제거

가장 큰 principal component를 제거합니다.

embedding에서 공통 방향 PC1, PC2, ... 제거

간단한 방식:

# X: [num_sentences, hidden_dim]
X_centered = X - X.mean(axis=0)
# PCA 후 상위 k개 방향 제거
X_denoised = X_centered - X_centered @ PCs[:k].T @ PCs[:k]

보통 k=1~3 정도만 제거해도 cosine 분포가 넓어집니다.

⸻

C. CSLS 사용

Cross-lingual retrieval에서는 cosine보다 CSLS를 많이 씁니다.

CSLS는 hubness 문제를 줄입니다.

문제 상황:

어떤 Syriac 문장 하나가 모든 Coptic 문장과 다 높게 나옴

이런 문장을 hub라고 합니다. CSLS는 이런 hub를 벌점 줍니다.

개념적으로:

CSLS(x, y) = 2 cos(x, y)
             - average_neighborhood_similarity(x)
             - average_neighborhood_similarity(y)

즉, 그냥 가까운 게 아니라 상대적으로 특별히 가까운지를 봅니다.

Sentence retrieval에서는 cosine baseline과 CSLS를 같이 제시하면 좋습니다.

⸻

D. Hard negative 평가

random negative만 쓰면 쉽거나 왜곡될 수 있습니다. 아래 negative를 따로 만들어야 합니다.

Random negative:
완전히 랜덤한 다른 verse
Same-chapter negative:
같은 장 안의 다른 verse
Length-matched negative:
길이가 비슷한 다른 문장
Lexical-overlap negative:
공통 고유명사나 반복 단어가 있는 다른 문장
Nearest-neighbor negative:
현재 embedding 기준 cosine이 높은 오답

cosine이 과하게 높게 나오는 문제는 특히 hard negative에서 드러납니다.

⸻

6. 네 상황에서 추천 실험 세트

지금은 이렇게 가면 됩니다.

Pooling ablation:
1. <s> pooling
2. mean pooling
Layer ablation:
layer 8
last layer
average last 4 layers
Similarity:
1. raw cosine
2. centered cosine
3. PCA removal cosine
4. CSLS
Evaluation:
1. positive vs random negative cosine distribution
2. positive vs hard negative cosine distribution
3. Top-1 / Top-5 / Top-10 retrieval
4. MRR
5. margin

가장 중요한 것은 이 표입니다.

Setting	Pos cos	Rand neg cos	Hard neg cos	Margin	Top-1	Top-10	MRR
mean + raw cosine	0.94	0.89	0.92	낮음	?	?	?
mean + centered	낮아짐	더 낮아짐	분리 확인	개선 가능	?	?	?
<s> + raw cosine	?	?	?	?	?	?	?
mean + CSLS	-	-	-	-	?	?	?

CSLS는 similarity 값 자체보다 ranking 지표로 보는 게 좋습니다.

7. 결론

cosine이 과하게 높으면 문제는 두 가지입니다.

1. embedding anisotropy 때문에 cosine 절대값이 부풀려짐
2. 같은 도메인/같은 corpus라 negative도 의미적으로 가까움

그래서 지금은:

cosine threshold로 same/different 분류

보다

retrieval ranking + margin + centering/CSLS 보정

으로 가는 게 맞습니다.

보고서 문장은 이렇게 쓰면 됩니다.

Because raw cosine similarities were uniformly high across both positive and negative pairs, we do not interpret the absolute cosine value as a reliable indicator of semantic equivalence. Instead, we evaluate whether positive pairs are ranked above negative candidates using retrieval accuracy, MRR, and positive-negative similarity margins. We additionally apply centering/PCA removal and CSLS to mitigate embedding anisotropy and hubness.