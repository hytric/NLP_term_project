# Second Try Reference Summary

작성일: 2026-06-10

## Purpose

이 문서는 `docs/exp/second_try/reference_summaries/`에 먼저 작성한 개별 레퍼런스 요약을 종합한 second_try 방법론 요약본이다.

사용자 결정사항:

- Base model은 `xlm-roberta-base`.
- first_try 흐름을 처음부터 다시 재현하되, Glot500 대신 XLM-R에 language adaptation을 적용한다.
- 번역은 제외하고 encoder-only downstream task를 사용한다.
- Bible 기반 proxy task는 허용하되, 쉬운 task라는 한계를 명시한다.
- 핵심 주장은 저자원/미지원 언어의 tokenizer bottleneck과 해결 조건, 그리고 vocab extension이 downstream 개선으로 이어지는지 검증하는 것이다.

## Individual Summaries

개별 요약은 아래 파일에 분리했다.

- `docs/exp/second_try/reference_summaries/2305.12182v2_glot500.md`
- `docs/exp/second_try/reference_summaries/2406.11477v3_low_resource_vocab_expansion.md`
- `docs/exp/second_try/reference_summaries/glot500_extension_tutorial.md`
- `docs/exp/second_try/reference_summaries/vocab_extension_tutorial.md`
- `docs/exp/second_try/reference_summaries/unigram_lm.md`
- `docs/exp/second_try/reference_summaries/bpe_wordpiece.md`
- `docs/exp/second_try/reference_summaries/term_project_guideline.md`

## Synthesis

개별 요약을 종합하면 second_try는 다음 방식으로 설계한다.

1. Glot500 논문과 tutorial에서 가져올 핵심은 `xlm-roberta-base`의 기존 token id를 보존한 append-style vocabulary extension이다.
2. UnigramLM/BPE/WordPiece 자료를 기준으로, XLM-R 계열에는 SentencePiece `model_type=unigram`을 명시해 target tokenizer를 학습한다.
3. Low-resource vocab expansion 자료와 feedback tutorial을 기준으로, random init은 baseline으로 두고 Mean/FVT/Align/Focus를 주요 비교 조건으로 둔다.
4. Term project guideline의 leakage 방지와 reporting 요구사항은 유지하되, NMT/translation 목표는 encoder-only downstream proxy task로 치환한다.

## Glot500-Style Vocabulary Extension

Glot500-m은 `xlm-roberta-base`를 기반으로 계속 사전학습한 encoder 모델이다. 모델 구조는 XLM-R-base와 같고, 핵심 차이는 tokenizer/vocabulary 확장과 continued pretraining이다.

가져와야 할 방법:

- 새 tokenizer로 완전히 교체하지 않는다.
- 기존 XLM-R vocabulary와 token id를 보존한다.
- target corpus로 auxiliary SentencePiece unigram tokenizer를 학습한다.
- auxiliary tokenizer에서 찾은 새 piece 중 기존 XLM-R vocab에 없는 것만 append한다.
- model embedding matrix와 MLM head를 확장하고, 기존 row는 그대로 유지한다.

주의할 점:

- 전체 tokenizer를 새로 학습해서 id를 재배치하면 XLM-R의 기존 embedding 지식이 깨진다.
- Glot500처럼 151K 수준으로 새 token을 추가하는 것은 second_try 규모에는 과하다.
- 작은 vocab grid를 비교하면서 tokenization 개선과 downstream 개선이 함께 나타나는 지점을 찾아야 한다.

## Tokenizer Choice

XLM-R/Glot500 계열에는 SentencePiece `unigram` 방식이 가장 자연스럽다.

UnigramLM의 핵심:

- 큰 seed vocabulary에서 시작한다.
- EM으로 token probability를 추정한다.
- likelihood 기여가 낮은 token을 pruning한다.
- vocab size가 sequence length와 embedding 학습 난이도를 조절하는 주요 knob이다.

Second_try 적용:

- `model_type=unigram`을 명시한다.
- `8k`, `16k`, `32k` vocab size grid를 비교한다.
- 기존 XLM-R SentencePiece model에 새 piece를 append하는 merge 방식을 사용한다.
- `byte_fallback`은 `<unk>`를 줄일 수 있지만 sequence가 길어질 수 있으므로 별도 지표로 기록한다.

## Embedding Initialization

새 token embedding 초기화는 second_try의 핵심 비교 조건이다. 레퍼런스는 random init만으로는 저자원 설정에서 불안정하다고 본다.

필수 비교 후보:

| Init | 요약 | 역할 |
| --- | --- | --- |
| Random / TransInner | `resize_token_embeddings()` 기반 랜덤 초기화 | 하한선 baseline |
| Mean / Gaussian Mean | 기존 embedding 분포 평균 또는 평균/분산 기반 초기화 | 단순 baseline |
| FVT / avg-subwords | 새 token을 기존 XLM-R tokenizer로 다시 쪼갠 뒤 기존 subtoken embedding 평균 | first_try mean 방식과 가장 유사 |
| Align | corpus에서 old/new tokenizer span alignment를 잡아 빈도 가중 평균 | 문맥 기반 강한 후보 |
| Focus | overlap token을 anchor로 삼고 target fastText similarity로 새 embedding 구성 | multilingual XLM-R에 적합한 후보 |

선택적 후보:

- `Ofa`: multilingual large-scale extension에는 후보지만 외부 aligned vector 의존성이 크다.
- `Wechsel`: monolingual transfer에 더 적합해서 XLM-R-base second_try의 주력 후보로는 우선순위가 낮다.

구현 주의:

- `encode(..., add_special_tokens=False)`를 사용한다.
- SentencePiece whitespace marker `▁`를 보존한다.
- `<unk>` 또는 byte token만 나오는 경우 fallback을 명확히 기록한다.
- input embedding과 MLM head weight tying이 깨지지 않았는지 확인한다.
- 새 vocab id와 embedding row 순서가 1:1로 맞는지 검증한다.
- Align은 Unicode normalization과 character span tracking 테스트가 필요하다.

## Data And Language Selection

first_try target10은 다음 언어를 사용했다.

| ISO | Language | Script |
| --- | --- | --- |
| acu | Achuar-Shiwiar | Latin |
| ake | Akawaio | Latin |
| bsn | Barasana-Eduria | Latin |
| chr | Cherokee | Cherokee |
| cop | Coptic | Coptic |
| kbh | Camsa | Latin |
| nhg | Nahuatl (Tetelcingo) | Latin |
| oji | Ojibwa | Aboriginal Syllabics |
| syr | Syriac | Syriac |
| usp | Uspanteco | Latin |

사용자 결정은 first_try target10을 최대한 유지하고, downstream은 가능한 subset으로 평가하는 것이다.

언어/데이터 해석:

- Coptic, Syriac, Cherokee, Ojibwa는 non-Latin script bottleneck을 보여주는 핵심 사례다.
- Latin-script 저자원 언어는 script 문제가 약해도 vocabulary 희소성과 형태론적 fragmentation이 남는지 보는 대조군이다.
- Bible corpus만 쓰면 domain-specific result가 될 수 있으므로 final report에서 한계를 명시한다.

## Evaluation Gates

Tokenization gate:

- tokens/word 감소
- tokens/char 감소
- single-character token 비율 감소
- `<unk>` 비율 또는 byte fallback 비율 감소
- sequence length percentile 감소
- 새 token 사용률
- encode/decode round-trip check

MLM gate:

- zero-step MLM loss
- fixed-step MLM loss
- dev loss / pseudo-perplexity
- embedding norm distribution
- 새 token nearest neighbors

Downstream gate:

- original XLM-R baseline 대비 accuracy/F1/MRR/Recall 개선
- task별 majority/random baseline보다 충분히 어려운지 확인
- language identification은 sanity check로만 사용
- 최종 주장은 retrieval/classification 중심으로 둔다

Forgetting/domain caveat:

- target-only MLM은 XLM-R의 기존 언어 능력을 잊게 할 수 있다.
- second_try의 우선 목표는 target10 개선이므로 full forgetting benchmark는 optional로 두되, report에는 limitation으로 적는다.

## Downstream Task Recommendation

번역은 제외한다. XLM-R-base는 encoder-only이므로 다음 task가 적합하다.

Detailed task definitions are in `docs/exp/second_try/downstream_tasks.md`.

최종 추천 task 3개:

1. Book/genre classification
    - 입력: target-language verse text
    - label: book 또는 broader genre
    - metric: accuracy, macro-F1
    - 장점: encoder classification으로 바로 구현 가능

2. Verse retrieval/ranking
    - 입력: query verse와 candidate pool
    - 목표: 같은 verse id의 parallel counterpart 또는 같은 book/chapter 위치 후보를 top-k에서 찾기
    - metric: Recall@1, Recall@5, MRR
    - 장점: representation quality를 직접 평가할 수 있음

3. Parallel verse matching
    - 입력: sentence pair
    - label: same verse id vs negative pair
    - metric: accuracy, macro-F1, AUC
    - 장점: sentence-pair classification으로 cross-lingual alignment를 평가할 수 있음

Language identification은 쉬우므로 tokenization sanity check와 diagnostic으로만 사용한다.

## Reporting Requirements

각 stage마다 다음 산출물을 남긴다.

- `plan.md`
- `results.md`
- TSV metric file
- sample markdown
- 실행 command 또는 config
- gate decision

최종 보고서에는 다음을 포함한다.

- data source와 split
- tokenizer before/after examples
- vocab size별 tokenization metric
- init method별 MLM metric
- downstream task별 baseline/adapted score
- 실패 사례 10개 이상
- limitation: Bible proxy task, domain leakage risk, translation 미수행, target-only adaptation forgetting risk
