가능합니다. 지금 문제를 novelty로 잡으려면 단순히 “cosine이 높아서 centering/whitening 했다”가 아니라, low-resource cross-lingual encoder에서 embedding anisotropy를 완화하면서 parallel sentence retrieval을 개선하는 방법론으로 포장해야 합니다.

핵심 novelty 문장은 이렇게 잡을 수 있습니다.

MLM-only multilingual encoders produce overly concentrated sentence embeddings for low-resource languages, making raw cosine similarity unreliable. We propose a representation dispersion procedure that spreads sentence embeddings by removing language/domain-common components and evaluates cross-lingual equivalence using margin-based retrieval rather than absolute cosine similarity.

1. 관련 논문 흐름

1) BERT-flow 계열: anisotropy 문제를 직접 다룸

BERT-flow 논문은 fine-tuning 없는 BERT sentence embedding이 semantic similarity를 잘 못 잡는 이유 중 하나로 anisotropic sentence embedding space를 지적합니다. 즉, sentence embedding들이 한쪽 방향으로 몰려 있어서 cosine similarity가 과하게 높게 나오는 문제입니다. 이 논문은 normalizing flow로 embedding distribution을 더 smooth/isotropic한 Gaussian space로 변환합니다.  

너의 문제와 연결:

문제:
Coptic/Syriac sentence embedding cosine이 전반적으로 너무 높음
해석:
MLM-only encoder representation이 anisotropic하고,
sentence embedding들이 같은 방향으로 몰림
기존 방법:
BERT-flow는 normalizing flow로 embedding space를 isotropic하게 변환

하지만 BERT-flow는 보통 monolingual STS 중심입니다. 너는 이걸 low-resource cross-lingual retrieval로 가져올 수 있습니다.

⸻

2) Whitening Sentence Representations

Whitening 논문은 BERT류 sentence representation의 anisotropy를 완화하기 위해 whitening operation을 사용합니다. whitening은 embedding 평균을 빼고 covariance를 정규화해서 각 차원이 더 고르게 퍼지도록 만드는 방식입니다. 논문은 이 방법이 semantic representation과 retrieval efficiency를 개선할 수 있다고 주장합니다.  

너의 프로젝트에는 BERT-flow보다 whitening이 더 실용적입니다.

장점:
- 학습이 거의 필요 없음
- low-resource setting에 적합
- embedding 후처리만으로 가능
- Coptic/Syriac 데이터가 작아도 적용 가능

⸻

3) SimCSE 계열: contrastive learning으로 uniformity 개선

SimCSE는 sentence embedding 학습에서 contrastive learning을 사용합니다. unsupervised SimCSE는 같은 문장을 dropout noise만 다르게 두 번 넣어 positive pair를 만들고, supervised SimCSE는 NLI entailment를 positive, contradiction을 hard negative로 사용합니다. 중요한 점은 SimCSE가 contrastive objective를 통해 embedding space의 uniformity를 개선한다고 설명한다는 것입니다.  

너의 프로젝트에 연결하면:

기존 SimCSE:
same sentence + dropout = positive
너의 변형:
Coptic-Syriac aligned verse = positive
same chapter wrong verse = hard negative

즉, cross-lingual SimCSE-style contrastive alignment로 확장 가능.

⸻

4) CSLS: hubness 문제 완화

Cross-lingual retrieval에서는 어떤 vector가 너무 많은 query의 nearest neighbor가 되는 hubness 문제가 자주 발생합니다. CSLS는 cosine similarity에서 주변 이웃 평균 similarity를 빼서, 단순히 모두와 가까운 hub vector를 벌점 줍니다. Cross-lingual word translation 연구에서 이 문제를 다루기 위해 제안된 방식입니다.  

너의 문제와 연결:

문제:
일부 Syriac sentence가 많은 Coptic sentence와 다 cosine이 높음
해결:
CSLS로 hub sentence를 penalty

⸻

2. Novelty로 가져갈 수 있는 방법론 3개

방법론 A: Cross-lingual Centered Whitening Retrieval

가장 안전하고 구현 쉬운 방법입니다.

아이디어

raw sentence embedding을 그대로 쓰지 않고, common direction을 제거해서 embedding을 퍼뜨립니다.

1. Coptic/Syriac sentence embedding 추출
2. 전체 평균 vector 제거
3. PCA 또는 whitening 적용
4. cosine / CSLS로 sentence retrieval
5. raw cosine 대비 Top-k, MRR, margin 개선 확인

수식 수준 설명

문장 embedding을 h_i라고 하면:

centered:
z_i = h_i - μ

여기서 μ는 전체 sentence embedding 평균입니다.

PCA removal은:

z'_i = z_i - Σ_k (z_i · u_k) u_k

여기서 u_k는 상위 principal component입니다.

Whitening은:

z_i = W(h_i - μ)

여기서 W는 covariance를 identity에 가깝게 만드는 transformation입니다.

Novelty 포인트

기존 whitening은 일반 sentence embedding/STS에서 쓰였지만, 너는:

MLM-only Glot500 representation
+ unseen/ancient low-resource languages
+ Coptic-Syriac cross-lingual retrieval

에 적용하는 것이라 프로젝트 novelty로 충분히 잡을 수 있습니다.

보고서 제목 후보

Anisotropy-Aware Cross-Lingual Sentence Retrieval for Low-Resource Ancient Languages

⸻

방법론 B: Language-Common Component Removal

조금 더 네 프로젝트에 특화된 novelty입니다.

문제의식

Coptic과 Syriac embedding에는 의미 정보 외에 다음 성분이 섞입니다.

language identity
script identity
domain identity
religious corpus style
length signal

이 성분 때문에 모든 문장이 비슷하게 보입니다.

방법

언어별 평균 vector를 따로 구합니다.

μ_cop = mean(Coptic embeddings)
μ_syr = mean(Syriac embeddings)

각 문장에서 해당 언어 평균을 제거합니다.

z_cop = h_cop - μ_cop
z_syr = h_syr - μ_syr

그 다음 retrieval을 합니다.

왜 좋은가

global mean removal은 전체 공통 성분만 제거합니다.
language-specific mean removal은 각 언어의 script/style bias를 따로 제거합니다.

raw embedding:
semantic + language/script/domain common component
after language centering:
semantic component가 상대적으로 강조됨

추가 확장

도메인/장/chapter 평균도 제거할 수 있습니다.

z = h - μ_language - μ_chapter

하지만 너무 많이 제거하면 실제 의미 정보도 같이 사라질 수 있으므로 ablation으로 제시해야 합니다.

Novelty 포인트

이건 Coptic/Syriac Bible/patristic corpus처럼 도메인과 언어 신호가 강하게 얽힌 low-resource setting에 잘 맞는 방법입니다.

이름을 붙이면:

Language-Common Component Removal, LCCR

또는

Script-Domain Debiased Retrieval, SDDR

⸻

방법론 C: Margin-Calibrated Contrastive Adaptation

가장 연구적으로 그럴듯하지만, 추가 학습이 필요합니다.

아이디어

cosine 절대값이 높으면, positive를 단순히 높이는 것이 아니라 positive가 hard negative보다 더 높게 나오도록 margin을 학습합니다.

Positive:

Coptic_i ↔ Syriac_i

Hard negative:

Coptic_i ↔ Syriac_j
j ≠ i, but same chapter / similar length / high lexical overlap

Loss:

L = max(0, m - sim(cop_i, syr_i) + sim(cop_i, syr_j))

또는 InfoNCE:

L_i = -log exp(sim(c_i, s_i)/τ) / Σ_j exp(sim(c_i, s_j)/τ)

왜 좋은가

이 방법은 “cosine을 높여라”가 아니라:

정답 pair를 후보들 중 상대적으로 위로 올려라

를 학습합니다.

따라서 cosine이 전반적으로 높은 상황에서도 ranking 성능이 개선될 수 있습니다.

Novelty 포인트

기존 SimCSE-style contrastive learning은 sentence embedding을 잘 만들기 위한 일반 방법입니다. 너는 여기에:

low-resource ancient languages
parallel verse alignment
hard negative from same chapter
MLM-only Glot500 encoder adaptation

을 결합하는 방식으로 novelty를 잡을 수 있습니다.

이름 후보:

Margin-Calibrated Cross-Lingual Alignment, MC-CLA

또는

Hard-Negative Verse Contrastive Alignment, HNVCA

⸻

3. 가장 추천하는 프로젝트용 방법론

텀프로젝트라면 너무 큰 contrastive training까지 가기보다, 아래 조합이 가장 현실적입니다.

Proposed Method: Debiased Cross-Lingual Retrieval, DCLR

Step 1. Sentence embedding extraction

Glot500 encoder에서 여러 pooling을 비교합니다.

<s> pooling
mean pooling
last-layer mean
layer-8 mean
last-4-layer mean

Glot500 논문도 sentence retrieval에서 layer 8의 average word embeddings와 cosine similarity를 사용합니다. 그러므로 너도 layer/pooling ablation을 자연스럽게 제시할 수 있습니다.

Step 2. Representation dispersion

raw embedding에 대해 세 가지 보정을 적용합니다.

Raw
Global centering
Language centering
Whitening / PCA removal

Step 3. Similarity calibration

cosine만 쓰지 않고 CSLS도 비교합니다.

cosine
centered cosine
CSLS

Step 4. Evaluation

절대 cosine이 아니라 ranking metric으로 평가합니다.

Top-1 accuracy
Top-5 accuracy
Top-10 accuracy
MRR
positive-hard negative margin

Step 5. Optional contrastive fine-tuning

시간이 남으면 LoRA로 contrastive adaptation을 추가합니다.

Glot500 frozen or LoRA
positive = aligned Coptic-Syriac verse
hard negative = same chapter wrong verse
loss = InfoNCE or triplet margin loss

⸻

4. 논문식 contribution으로 쓰면

Contribution 1.
We identify that raw cosine similarity from MLM-only multilingual encoders is poorly calibrated for Coptic-Syriac sentence equivalence, producing uniformly high similarities even for non-parallel pairs.
Contribution 2.
We propose Debiased Cross-Lingual Retrieval, a lightweight post-processing method that removes language- and domain-common components from sentence embeddings before retrieval.
Contribution 3.
We evaluate sentence equivalence using ranking-based metrics and hard-negative margins rather than absolute cosine thresholds, showing a more reliable evaluation protocol for low-resource ancient language alignment.

한국어로는:

1. MLM-only multilingual encoder에서 얻은 Coptic/Syriac sentence embedding은 positive와 negative 모두 cosine similarity가 높게 나타나는 calibration 문제를 보인다.
2. 이를 해결하기 위해 sentence embedding에서 language/script/domain 공통 성분을 제거하는 Debiased Cross-Lingual Retrieval 방법을 제안한다.
3. 절대 cosine threshold 대신 Top-k retrieval, MRR, hard-negative margin을 사용하여 low-resource ancient language alignment를 더 안정적으로 평가한다.

⸻

5. 실험 설계 표

Method	Training 필요	목적	Novelty 강도	구현 난이도
Raw cosine	없음	baseline	낮음	낮음
Global centering	없음	common direction 제거	낮음~중간	낮음
Language centering	없음	language/script bias 제거	중간	낮음
PCA removal	없음	anisotropy 완화	중간	낮음
Whitening	없음	isotropic space 변환	중간	중간
CSLS	없음	hubness 완화	중간	중간
Contrastive LoRA	있음	positive/hard negative 분리	높음	높음

텀프로젝트 기준 추천 조합:

Main method:
Language centering + PCA removal + CSLS
Optional extension:
Hard-negative contrastive LoRA

⸻

6. 최종 방법론 이름 제안

가장 무난한 이름

Anisotropy-Aware Cross-Lingual Sentence Retrieval

조금 더 novelty 있어 보이는 이름

Debiased Cross-Lingual Retrieval for Low-Resource Ancient Languages

Coptic/Syriac 프로젝트에 맞춘 이름

Script-Domain Debiased Retrieval for Coptic-Syriac Alignment

contrastive까지 포함할 경우

Hard-Negative Contrastive Alignment for Coptic-Syriac Sentence Retrieval

⸻

결론

가장 현실적인 novelty는 이것입니다.

Glot500 같은 MLM-only encoder에서 raw cosine similarity가 low-resource cross-lingual sentence equivalence를 과대평가하는 문제를 보이고, 이를 language/script/domain common component removal + CSLS + margin-based retrieval evaluation으로 보정하는 방법론을 제안한다.

이건 단순 후처리 같지만, 프로젝트 프레임에서는 충분히 novelty가 됩니다. 핵심은 cosine을 낮추는 것이 아니라, positive와 hard negative를 더 잘 분리하도록 embedding space를 퍼뜨리는 것입니다.