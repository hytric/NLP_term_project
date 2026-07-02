# Downstream Task Design

작성일: 2026-06-10

## Purpose

Second_try의 downstream task는 번역 품질을 보는 것이 아니라, `xlm-roberta-base`에 vocabulary extension과 MLM adaptation을 적용했을 때 encoder representation이 실제 task에서 좋아지는지 확인하기 위한 proxy evaluation이다.

핵심 질문:

- Tokenizer fragmentation이 줄어든 것이 downstream score 개선으로 이어지는가?
- 새 token embedding initialization 방법 차이가 downstream task에서도 남는가?
- 개선이 단순 language/script 식별처럼 쉬운 shortcut 때문이 아니라 retrieval/classification 성능 개선으로 나타나는가?

## Why Not Translation

`xlm-roberta-base`는 encoder-only 모델이다. 번역을 하려면 decoder를 새로 붙이거나 encoder-decoder 모델을 따로 학습해야 한다. 그러면 vocab extension 효과와 decoder 학습 실패가 섞여서 원인을 해석하기 어렵다.

따라서 second_try에서는 번역을 제외하고 encoder-only로 자연스럽게 수행할 수 있는 task를 사용한다.

## Final Task Set

최종 downstream task는 아래 3개로 둔다.

| Task | Type | Main Metric | Main Question |
| --- | --- | --- | --- |
| Book/genre classification | sequence classification | accuracy, macro-F1 | target text를 더 안정적으로 분류하는가? |
| Verse retrieval/ranking | embedding retrieval | Recall@1, Recall@5, MRR | verse representation이 좋아지는가? |
| Parallel verse matching | sentence-pair classification | accuracy, macro-F1, AUC | true parallel pair와 hard negative를 구분하는가? |

Language identification은 너무 쉬울 수 있으므로 final claim에는 쓰지 않고 sanity check로만 둔다.

## Task 1: Book/Genre Classification

### Goal

Target-language verse 또는 짧은 passage를 입력으로 넣고, 해당 text가 어떤 book 또는 genre에 속하는지 분류한다.

이 task는 adapted encoder가 target script와 target-language lexical pattern을 더 잘 표현하는지 확인하는 기본 classification task다.

### Data

Input:

- 한 target language의 verse text
- 필요하면 인접 verse를 concatenate한 short passage

Label options:

- Book id: `MAT`, `MRK`, `LUK`, `JOH`, ...
- Broad genre: gospel, epistle, prophecy 등

추천:

- 먼저 book id classification을 pilot한다.
- 너무 쉬우면 genre classification은 제외하고 retrieval/matching 중심으로 간다.
- 너무 어려우면 broad genre로 완화한다.

### Split

Book-level split과 task label이 충돌할 수 있다. 예를 들어 test book을 John으로 고정하면 book id classification의 test label이 train에 없을 수 있다.

따라서 classification task는 아래 중 하나를 사용한다.

- Option A: downstream classification만 stratified verse-level split을 사용하되, tokenizer/MLM test leakage와 분리해서 명시한다.
- Option B: broad genre label을 사용해 dev/test book의 genre가 train에도 존재하도록 만든다.
- Option C: train/dev/test book split은 유지하고, classification은 genre 또는 section-level label만 사용한다.

추천 기본값:

- `broad genre classification`을 기본으로 두고, book id classification은 pilot diagnostic으로 둔다.

### Model

- Encoder: original XLM-R 또는 adapted XLM-R
- Pooling: `<s>` representation 또는 mean pooling
- Head: linear classification head

### Metrics

- accuracy
- macro-F1
- per-language macro-F1
- confusion matrix

### Baselines

- majority label baseline
- original `xlm-roberta-base`
- vocab-only model if feasible
- best vocab+init+MLM model

### Success Interpretation

성공:

- adapted model이 original XLM-R보다 macro-F1을 개선한다.
- 특히 fragmentation이 심했던 Coptic/Syriac/Cherokee/Ojibwa에서 개선이 나타난다.

주의:

- genre/topic cue가 너무 쉬우면 task가 tokenizer bottleneck을 잘 검증하지 못한다.
- 이 task 단독 개선만으로 representation alignment가 좋아졌다고 주장하지 않는다.

## Task 2: Verse Retrieval/Ranking

### Goal

Query verse embedding으로 candidate pool에서 정답 verse를 찾는다.

이 task는 encoder representation의 quality를 직접 보는 task다. Classification head를 새로 학습하는 것보다 모델 embedding 자체의 변화가 더 잘 드러난다.

### Data

Input:

- query verse
- candidate verses

Positive:

- 같은 verse id의 parallel counterpart
- 또는 같은 언어 안에서 동일 verse id/passage id

Negative:

- random negative
- 같은 book negative
- 같은 chapter hard negative

추천:

- 쉬운 random retrieval만 쓰지 않는다.
- same book 또는 same chapter hard negative를 포함한다.

### Retrieval Settings

Setting 1: Monolingual retrieval

- 같은 언어 안에서 query verse와 matching target을 찾는다.
- 주로 representation stability와 tokenization quality를 본다.

Setting 2: Cross-lingual parallel retrieval

- 한 언어의 query verse로 다른 언어의 같은 verse id를 찾는다.
- cross-lingual alignment를 본다.

Setting 3: Hard candidate retrieval

- 같은 book/chapter 안에서 후보를 제한한다.
- random shortcut을 줄인다.

추천 기본값:

- cross-lingual retrieval + same book/chapter hard candidate pool.

### Embedding

- `<s>` pooling
- mean pooling
- optional: layer 8 mean pooling, Glot500-style representation check

각 pooling 방식은 고정된 baseline에서 먼저 비교하고, 가장 안정적인 것을 main metric으로 사용한다.

### Metrics

- Recall@1
- Recall@5
- Recall@10
- MRR
- per-language pair score

### Baselines

- random retrieval baseline
- BM25/char-ngram lexical baseline if feasible
- original XLM-R embedding
- best adapted embedding

### Success Interpretation

성공:

- adapted model이 original XLM-R보다 Recall@1/MRR을 개선한다.
- hard candidate setting에서도 개선이 유지된다.

주의:

- Bible verse는 parallel structure가 강하므로, lexical overlap 또는 verse length shortcut이 생길 수 있다.
- retrieval 개선이 특정 language pair에만 나타나는지 language별로 나눠 봐야 한다.

## Task 3: Parallel Verse Matching

### Goal

두 verse가 같은 verse id의 parallel pair인지 아닌지 binary classification한다.

이 task는 retrieval보다 학습 head가 들어가지만, hard negative를 잘 만들면 encoder가 source/target sentence relation을 얼마나 잘 표현하는지 볼 수 있다.

### Data

Input:

- sentence A
- sentence B

Positive:

- 같은 verse id의 서로 다른 언어 pair

Negative:

- random negative
- 같은 book 다른 verse
- 같은 chapter 다른 verse
- length-similar false pair

추천:

- random + same book + same chapter negative를 섞는다.
- 같은 chapter negative 비율을 높여 shortcut을 줄인다.

### Model

Option A: Bi-encoder

- A와 B를 따로 encode한다.
- cosine similarity 또는 small classifier로 match score를 낸다.
- retrieval task와 잘 연결된다.

Option B: Cross-encoder

- pair를 하나의 sequence로 넣고 classification head를 붙인다.
- 성능은 높을 수 있지만 representation retrieval과는 다르다.

추천 기본값:

- bi-encoder를 main으로 두고, cross-encoder는 optional diagnostic으로 둔다.

### Metrics

- accuracy
- macro-F1
- AUC
- precision/recall
- hard-negative-only F1

### Baselines

- random baseline
- lexical overlap baseline if feasible
- original XLM-R
- best adapted model

### Success Interpretation

성공:

- adapted model이 hard-negative setting에서 original XLM-R보다 macro-F1/AUC를 개선한다.
- retrieval improvement와 matching improvement가 같은 방향이면 representation 개선 근거가 강해진다.

주의:

- random negative에서만 성능이 높으면 task가 너무 쉽다.
- same chapter negative에서 성능이 유지되는지 반드시 따로 본다.

## Diagnostic Task: Language Identification

Language identification은 target text가 어떤 언어인지 맞히는 task다.

사용 목적:

- tokenizer가 blank/unk/character-level collapse를 줄였는지 sanity check
- adapted encoder가 target script를 구분할 수 있는지 확인

Final claim에서 제외하는 이유:

- script가 다른 언어가 많아 너무 쉬울 수 있다.
- language id 성능은 tokenizer bottleneck 완화의 충분한 downstream evidence가 아니다.

사용 방식:

- final table에는 diagnostic으로만 둔다.
- language ID만 좋아지고 retrieval/classification이 개선되지 않으면 downstream success로 주장하지 않는다.

## Evaluation Matrix

최소 비교:

| Model | Tokenizer | MLM Adapted | Downstream |
| --- | --- | --- | --- |
| original XLM-R | original | no | yes |
| vocab-only | extended | no | optional |
| best adapted | extended | yes | yes |

Pilot 비교:

- vocab size: 8k, 16k, 32k
- init: random, mean, fvt, align, focus where feasible
- fixed compute budget

Full comparison:

- original XLM-R: 3 seeds
- selected best checkpoint: 3 seeds
- optional best vocab-only: 3 seeds

## Reporting

Downstream 결과에는 다음을 포함한다.

- task별 dataset size
- label distribution
- negative sampling rule
- baseline score
- adapted score
- per-language score
- hard-negative-only score
- sample predictions
- failure cases

## Decision Rule

최종 downstream success는 아래 조건을 만족할 때만 주장한다.

1. Tokenization gate를 통과한다.
2. MLM dev loss가 개선된다.
3. Retrieval/ranking 또는 parallel matching 중 하나 이상에서 original XLM-R보다 개선된다.
4. Language identification만 개선된 경우는 success로 보지 않는다.

위 조건을 만족하지 못하면 tokenizer/MLM 개선은 보고하되, downstream transfer는 negative result로 정리한다.
