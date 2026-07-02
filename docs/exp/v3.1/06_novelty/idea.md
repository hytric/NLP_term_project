현재 문제를 이렇게 정의하면 됩니다.

Glot500/MLM-only encoder에서 Coptic–Syriac 문장 embedding의 raw cosine similarity가 positive/negative 모두 과하게 높게 나와, 절대 cosine threshold로는 “같은 문장/다른 문장”을 안정적으로 구분하기 어렵다.

따라서 실험 목표는 cosine 값을 낮추는 것이 아니라, positive pair가 negative pair보다 일관되게 높은 순위에 오르도록 만드는 것입니다.

⸻

1. 전체 실험 구조

실험 질문

Q1. Raw cosine similarity는 Coptic–Syriac sentence equivalence를 잘 구분하는가?
Q2. <s> pooling과 mean pooling 중 어떤 것이 더 나은가?
Q3. Centering / PCA removal / Whitening / CSLS가 과도하게 높은 cosine 문제를 완화하는가?
Q4. Downstream task score에서 representation 개선이 실제로 확인되는가?

Glot500은 XLM-R 기반 encoder에 vocabulary extension을 적용하고 MLM continued pretraining을 수행한 모델입니다. 즉, NSP나 sentence similarity objective로 학습된 모델이 아닙니다. 따라서 sentence retrieval, roundtrip alignment, NER, POS, text classification 같은 task는 학습 objective가 아니라 representation 평가용 downstream evaluation으로 봐야 합니다.  

⸻

2. 실험 단계 요약

Step 0. Dataset 구축
Step 1. Baseline cosine 분포 확인
Step 2. Pooling ablation
Step 3. Layer ablation
Step 4. Representation debiasing
Step 5. Similarity metric 비교
Step 6. Retrieval score 측정
Step 7. Downstream task score 측정
Step 8. 선택적으로 contrastive adaptation

⸻

3. Step 0 — 데이터 구성

3.1 Positive pair

Coptic–Syriac direct parallel이 거의 없으므로, Bible verse alignment나 Greek/English pivot을 활용합니다.

Positive:
Coptic_i ↔ Syriac_i

예:

Coptic verse 001
Syriac verse 001
Label = positive

프로젝트 가이드라인에서도 Coptic–Syriac direct parallel data는 매우 적고, Coptic–Greek, Syriac–Greek, Coptic–English, Syriac–English 같은 auxiliary parallel data를 활용해야 한다고 설명합니다.  

3.2 Negative pair

negative는 최소 3종류로 나눠야 합니다.

Negative type	구성	목적
Random negative	Coptic_i ↔ Syriac_j, 랜덤 j	쉬운 오답
Same-chapter negative	같은 장 안의 다른 verse	hard negative
Length-matched negative	길이가 비슷한 다른 verse	길이 bias 제거
Lexical-overlap negative	고유명사/반복어가 겹치는 오답	도메인/단어 overlap bias 확인
Nearest-neighbor negative	현재 embedding 기준 가장 가까운 오답	가장 어려운 hard negative

핵심은 random negative만 쓰면 안 됩니다.
Bible/종교 문헌은 문체와 도메인이 비슷해서, random negative도 cosine이 높게 나올 수 있습니다.

⸻

4. Step 1 — Baseline cosine 분포 확인

먼저 raw cosine 분포를 확인합니다.

측정값

positive cosine 평균
random negative cosine 평균
hard negative cosine 평균
positive - random negative margin
positive - hard negative margin

예시 표

Pair type	Mean cosine	Std	Min	Max
Positive	0.94	0.03	0.81	0.99
Random negative	0.89	0.04	0.76	0.98
Hard negative	0.92	0.03	0.80	0.99

이런 식으로 나오면 문제는 명확합니다.

cosine 절대값은 모두 높다.
따라서 threshold 기반 same/different classification은 부적절하다.
ranking/margin 기반 평가가 필요하다.

⸻

5. Step 2 — Pooling ablation

Glot500/XLM-R는 MLM-only encoder이므로 <s>가 sentence embedding으로 최적이라고 가정하면 안 됩니다. Glot500의 sentence retrieval 평가도 layer 8의 average word embedding을 사용합니다.  

비교할 pooling

Pooling	방식	설명
<s> pooling	첫 token hidden state	CLS-style 후보
Mean pooling	content token 평균	MLM encoder에서 일반적으로 안정적
Mean without special tokens	<s>, </s>, <pad> 제외	추천 baseline
Last-4 mean	마지막 4 layer 평균 후 pooling	layer noise 완화
Max pooling	token별 max	보조 실험

추천 기본값

Baseline 1: layer 8 + mean pooling
Baseline 2: last layer + mean pooling
Baseline 3: layer 8 + <s> pooling
Baseline 4: last layer + <s> pooling

⸻

6. Step 3 — Layer ablation

Transformer layer마다 정보 성격이 다릅니다.

lower layer: surface/script/token 정보
middle layer: syntactic/semantic 정보
upper layer: MLM objective에 가까운 정보

Glot500 논문은 sentence retrieval과 alignment에서 layer 8 representation을 사용합니다.  
따라서 layer 8은 반드시 포함하는 게 좋습니다.

비교할 layer

Layer 4
Layer 8
Layer 12 / last layer
Average last 4 layers

결과 표

Layer	Pooling	Pos cos	Hard neg cos	Margin	Top-1	Top-10	MRR
4	mean						
8	mean						
12	mean						
last4	mean						

⸻

7. Step 4 — Representation debiasing

cosine이 과하게 높으면 embedding anisotropy 또는 language/domain common component가 강한 상태일 가능성이 큽니다.

7.1 Raw

아무 보정 없이 사용합니다.

h_i

7.2 Global centering

전체 sentence embedding 평균을 제거합니다.

z_i = h_i - μ_global

목적:

모든 문장에 공통적으로 깔린 방향 제거

7.3 Language centering

언어별 평균을 따로 제거합니다.

z_cop = h_cop - μ_cop
z_syr = h_syr - μ_syr

목적:

Coptic/Syriac script-language bias 제거

현재 상황에서는 이게 가장 중요합니다.

7.4 Domain/chapter centering

Bible chapter 단위 평균을 제거합니다.

z_i = h_i - μ_chapter

주의:

너무 강하게 제거하면 실제 의미 정보도 사라질 수 있음.
보조 ablation으로만 사용.

7.5 PCA removal

상위 principal component를 제거합니다.

z'_i = z_i - Σ_k (z_i · u_k)u_k

비교:

remove top 1 PC
remove top 2 PCs
remove top 3 PCs
remove top 5 PCs

7.6 Whitening

covariance를 정규화해서 embedding space를 더 고르게 만듭니다.

z_i = W(h_i - μ)

추천 비교:

Raw
Global centering
Language centering
Language centering + PCA-1
Language centering + PCA-3
Whitening

⸻

8. Step 5 — Similarity metric 비교

8.1 Cosine

기본 baseline입니다.

sim(x, y) = cos(x, y)

8.2 Centered cosine

centering/PCA removal 후 cosine을 계산합니다.

8.3 CSLS

cross-lingual retrieval에서는 hubness 문제가 자주 발생하므로 CSLS를 비교해야 합니다.

CSLS(x, y) = 2cos(x, y) - r_x - r_y

여기서 r_x, r_y는 각 embedding이 주변 이웃들과 평균적으로 얼마나 가까운지입니다.

의미:

모두와 가까운 hub sentence에 penalty를 줌

추천

Main metric:
CSLS ranking
Baseline:
raw cosine ranking

⸻

9. Step 6 — Sentence retrieval score 측정

이게 현재 문제를 가장 직접적으로 해결하는 downstream score입니다.

9.1 Task 정의

각 Coptic 문장에 대해 모든 Syriac 후보 중 정답을 찾습니다.

Query: Coptic_i
Candidates: Syriac_1 ... Syriac_N
Correct: Syriac_i

반대 방향도 평가합니다.

Syriac → Coptic
Coptic → Syriac

9.2 Score

Metric	의미
Top-1 Accuracy	정답이 1등인가
Top-5 Accuracy	정답이 5등 안인가
Top-10 Accuracy	정답이 10등 안인가
MRR	정답 rank의 reciprocal 평균
Mean Rank	정답이 평균 몇 등인가
Positive-Hard Negative Margin	정답 similarity가 hard negative보다 얼마나 높은가

9.3 Margin

margin_i = sim(cop_i, syr_i) - max_{j≠i} sim(cop_i, syr_j)

해석:

margin > 0이면 정답이 가장 가까움
margin ≤ 0이면 오답이 정답보다 가까움

결과 표

Method	Pooling	Similarity	Top-1	Top-5	Top-10	MRR	Margin
Raw	mean	cosine					
Global centered	mean	cosine					
Language centered	mean	cosine					
Lang center + PCA-1	mean	cosine					
Lang center + PCA-3	mean	cosine					
Raw	mean	CSLS					
Lang center + PCA-3	mean	CSLS					

이 표가 메인 결과가 됩니다.

⸻

10. Step 7 — Binary classification score 측정

retrieval이 메인이고, binary classification은 보조 실험으로 두면 됩니다.

10.1 Fine-tuning 없는 threshold 방식

if sim(cop_i, syr_j) > threshold:
    Same
else:
    Different

하지만 cosine이 과하게 높으므로 raw cosine threshold는 약할 가능성이 큽니다.

10.2 Score

Metric	의미
Accuracy	전체 맞춘 비율
Precision	Same이라고 한 것 중 진짜 Same
Recall	진짜 Same 중 찾아낸 비율
F1	Precision/Recall 조화 평균
AUROC	threshold 전체 범위에서 분리 능력
AUPRC	positive가 적을 때 유용

추천

classification에서는 accuracy보다 AUROC / AUPRC를 더 중요하게 보세요.

왜냐하면 threshold 하나에 의존하지 않고 positive/negative 분리 능력을 보여주기 때문입니다.

결과 표

Method	Negative type	AUROC	AUPRC	F1	Best threshold
Raw cosine	random				
Raw cosine	hard				
Lang center + PCA	random				
Lang center + PCA	hard				
CSLS	hard				

⸻

11. Step 8 — Roundtrip alignment score

Sentence retrieval은 문장 단위 평가입니다.
Roundtrip alignment는 단어 단위 cross-lingual alignment 평가입니다.

Glot500도 Bible test set에서 SimAlign을 이용해 subword-level alignment를 수행하고, roundtrip 성공률을 측정했습니다.  

Task

Coptic word w
→ Syriac aligned word
→ Greek or English pivot aligned word
→ 다시 Coptic word

또는 단순화해서:

Coptic → Syriac → Coptic

Score

Roundtrip accuracy =
원래 token/word로 돌아온 비율

목적

sentence-level retrieval이 좋아졌을 때,
word-level alignment도 좋아졌는지 확인

결과 표

Method	Alignment direction	Roundtrip Acc
Raw layer 8 mean	Coptic→Syriac→Coptic	
Lang center + PCA	Coptic→Syriac→Coptic	
Raw layer 8 mean	Syriac→Coptic→Syriac	
Lang center + PCA	Syriac→Coptic→Syriac	

주의:

centering/PCA는 sentence embedding에는 잘 맞지만,
token-level alignment에는 효과가 다를 수 있음.

그래서 sentence-level과 token-level을 구분해서 해석해야 합니다.

⸻

12. Step 9 — Pseudoperplexity score

이건 cross-lingual similarity 문제가 아니라, Coptic/Syriac 자체를 모델이 잘 encode하는지 보는 intrinsic score입니다.

Glot500은 MLM 모델이므로 일반 perplexity 대신 pseudoperplexity를 씁니다. 논문에서도 pseudoperplexity를 low-resource language 평가에 사용합니다.  

방법

각 문장의 token을 하나씩 mask하고 원래 token 확률을 계산합니다.

Coptic sentence:
t1 t2 t3 ... tn
Step 1:
[MASK] t2 t3 ... tn → p(t1)
Step 2:
t1 [MASK] t3 ... tn → p(t2)

Score

Pseudo-log-likelihood
Pseudoperplexity

낮을수록 좋습니다.

비교할 모델

Original Glot500
+ Coptic/Syriac vocabulary extension
+ MLM continued pretraining
+ optional LoRA adaptation

결과 표

Model	Coptic PPPL ↓	Syriac PPPL ↓
Original Glot500		
Vocab extension only		
MLM continued pretraining		
MLM + contrastive adaptation		

⸻

13. Step 10 — NER/POS/Text Classification은 어떻게 할까

Coptic/Syriac에는 NER/POS/Text Classification gold label이 없을 가능성이 큽니다. 그래서 Glot500 방식 그대로는 어렵습니다.

Glot500은 NER/POS/Text Classification에서 English labeled data로 fine-tuning한 뒤 target language에 zero-shot 평가했습니다.  
하지만 Coptic/Syriac에는 WikiANN, UD, Taxi1500 같은 평가셋이 없을 수 있습니다.

따라서 네 프로젝트에서는 아래처럼 대체하는 게 현실적입니다.

⸻

13.1 POS 대체: projected POS 평가

방법

1. Greek/English 문장에 POS tag가 있는 데이터를 사용
2. Coptic/Syriac parallel sentence로 word alignment
3. POS tag를 Coptic/Syriac token에 projection
4. 소량 sample을 수동 검수
5. POS tagging 또는 POS retrieval 평가

Score

POS projection accuracy
POS F1

목적

representation이 syntax-level transfer에 도움이 되는지 확인

⸻

13.2 NER 대체: Bible named entity matching

성경에는 반복되는 인명/지명이 많습니다.

Jesus
Moses
David
Jerusalem
Galilee
Egypt

방법

1. English/Greek named entity list 구축
2. Coptic/Syriac verse alignment에서 해당 entity가 등장하는 문장 추출
3. string dictionary 또는 manual lexicon으로 Coptic/Syriac entity span 구축
4. embedding similarity로 entity alignment 확인

Score

Entity retrieval Top-1 / Top-5
Entity alignment accuracy

목적

token/entity-level semantic alignment 확인

⸻

13.3 Text classification 대체: book/chapter classification

Coptic/Syriac 문장이 어느 book 또는 chapter에 속하는지 분류합니다.

Task

Input: Coptic/Syriac sentence embedding
Label: Book ID 또는 Chapter ID

예:

Matthew
Mark
Luke
John
Genesis
Exodus

방식

1. Coptic에서 classifier 학습
2. Syriac에서 zero-shot 평가
또는
1. English/Greek에서 classifier 학습
2. Coptic/Syriac에서 zero-shot 평가

Score

Accuracy
Macro-F1

주의

이 task는 semantic보다 topic/domain cue가 강할 수 있습니다.
그래서 메인 결과보다는 보조 downstream task로 두는 게 좋습니다.

⸻

14. 선택 실험 — Contrastive adaptation

후처리로 부족하면 contrastive learning을 추가합니다.

14.1 Positive / negative

Positive:
Coptic_i ↔ Syriac_i
Hard negative:
Coptic_i ↔ Syriac_j
j ≠ i, same chapter or high cosine

14.2 Loss

Triplet margin loss

L = max(0, m - sim(c_i, s_i) + sim(c_i, s_j))

InfoNCE

L_i = -log exp(sim(c_i, s_i)/τ) / Σ_j exp(sim(c_i, s_j)/τ)

14.3 학습 방식

Encoder frozen + projection head만 학습
또는
Glot500 LoRA fine-tuning

추천은 먼저 projection head만 학습하는 것입니다.

Glot500 encoder frozen
sentence embedding
→ small MLP projection
→ contrastive loss

이러면 catastrophic forgetting 위험이 작습니다.

14.4 Score

contrastive adaptation 전후로 비교합니다.

Model	Top-1	Top-10	MRR	Hard margin
Raw Glot500				
Debiased retrieval				
Contrastive projection				
LoRA contrastive				

⸻

15. 최종 실험 우선순위

반드시 해야 하는 것

1. raw cosine positive/negative 분포 확인
2. <s> vs mean pooling ablation
3. layer 8 vs last layer ablation
4. language centering + PCA removal
5. cosine vs CSLS retrieval
6. Top-1 / Top-10 / MRR / margin 제시

하면 좋은 것

7. pseudoperplexity 비교
8. binary classification AUROC/AUPRC
9. entity retrieval
10. book/chapter classification

시간이 남으면

11. contrastive projection head
12. LoRA contrastive adaptation

⸻

16. 최종 보고서용 실험 구성

Experiment 1. Tokenization and MLM quality

평가	목적
token per sentence	over-fragmentation 확인
<unk> ratio	tokenizer coverage 확인
pseudoperplexity	Coptic/Syriac language modeling quality

⸻

Experiment 2. Raw cosine calibration

평가	목적
positive cosine	정답쌍 유사도
random negative cosine	쉬운 오답과 분리
hard negative cosine	어려운 오답과 분리
margin	정답이 오답보다 얼마나 높은지

⸻

Experiment 3. Pooling/layer ablation

평가	목적
<s> vs mean	sentence embedding 방식 비교
layer 4/8/12	어떤 layer가 cross-lingual retrieval에 좋은지
last-4 average	안정성 확인

⸻

Experiment 4. Debiased retrieval

평가	목적
global centering	common direction 제거 효과
language centering	script/language bias 제거 효과
PCA removal	anisotropy 완화
whitening	embedding 분산 개선
CSLS	hubness 완화

⸻

Experiment 5. Downstream retrieval score

Score	목적
Top-1	정확한 parallel sentence를 1등으로 찾는가
Top-5/Top-10	상위 후보 안에 찾는가
MRR	평균 ranking 품질
hard-negative margin	실제 구분력

⸻

Experiment 6. Auxiliary downstream tasks

Task	Score	목적
Roundtrip alignment	roundtrip accuracy	word-level alignment
Entity retrieval	Top-k	named entity semantic alignment
Book/chapter classification	Accuracy / Macro-F1	sentence-level topic representation
Pair classification	AUROC / AUPRC / F1	same/different 분리 능력

⸻

17. 결론적으로 가져갈 방법론

현재 상황에서 가장 적절한 방법론 이름은:

Debiased Cross-Lingual Retrieval for Coptic–Syriac Alignment

핵심 구성은:

1. Glot500 sentence embedding 추출
2. pooling/layer ablation
3. language-common component removal
4. PCA/whitening으로 anisotropy 완화
5. CSLS로 hubness 보정
6. cosine threshold가 아니라 retrieval ranking과 hard-negative margin으로 평가

보고서용 문장은 이렇게 정리하면 됩니다.

Raw cosine similarities from the MLM-only Glot500 encoder were uniformly high for both parallel and non-parallel Coptic–Syriac sentence pairs, making absolute cosine thresholds unreliable. To address this, we evaluate sentence equivalence as a ranking problem rather than a binary thresholding problem. We compare pooling and layer choices, remove language-common components through centering and PCA-based debiasing, and apply CSLS to reduce hubness. The resulting representations are evaluated using Top-k retrieval accuracy, MRR, and hard-negative similarity margins, with pseudoperplexity and auxiliary token-level alignment tasks used as complementary downstream evaluations.

한국어 버전:

MLM-only Glot500 encoder에서 추출한 Coptic–Syriac sentence embedding은 parallel pair와 non-parallel pair 모두에서 cosine similarity가 과도하게 높게 나타났다. 따라서 절대 cosine threshold로 같은 문장 여부를 판단하는 방식은 신뢰하기 어렵다. 본 연구에서는 sentence equivalence를 binary thresholding 문제가 아니라 ranking 문제로 재정의한다. 이를 위해 pooling 및 layer 선택을 비교하고, language-common component removal과 PCA 기반 debiasing으로 anisotropy를 완화하며, CSLS를 적용해 hubness를 줄인다. 최종 평가는 Top-k retrieval accuracy, MRR, hard-negative margin을 중심으로 수행하고, pseudoperplexity 및 token-level alignment task를 보조 downstream 평가로 사용한다.