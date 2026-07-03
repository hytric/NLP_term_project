# Abstract

# Previous research

## vertical scaling vs horizontal scaling

Corpus collection

**30,000 sentence 이상에 대해서만 사용**

XLM-R의 기존 vocabulary는 250K인데, Glot500-c로 SentencePiece unigram tokenizer를 새로 학습한 뒤 기존 XLM-R vocab과 병합한다. 최종 Glot500-m vocabulary size는 **401K**

데이터 수집 방법

| **Domain**          | **예시**       |
| ------------------- | ------------ |
| Religious texts     | 성경, 종교 번역문   |
| News articles       | 뉴스 기사        |
| Scientific papers   | 과학 논문        |
| Wikipedia/web crawl | 위키, 웹 크롤링 문서 |

web crawling

data cleaning

* Language-Scripts

  * 언어만 보는 것이 아니라 language-script 단위로 분리

* **Ngram LMs and Language Divergence**

* **Chunk-level filter**

* **Corpus-level filter**

여기서 chunk는 문장일 수도 있고, 짧은 구간일 수도 있고, 여러 문장이 합쳐진 paragraph일 수도 있다.

논문에서는 이후 이 chunk를 **sentence’**&#xB77C;고 부른다.

**30,000 sentence’ 이상 언어만 선별**

## Masked Language Modeling

the multilingual model Glot500-m on a 600GB corpus

1. Vocabulary Extension : 기존 XLM-R tokenizer vocabulary 확장

2. Continued Pretraining : XLM-R-base를 Glot500-c로 추가 pretraining

논문의 핵심 분석

성능 = corpus size + script coverage + related language support + model capacity

특히 재미있는 점은 **related languages의 도움**이다. 어떤 언어는 자기 corpus만 많다고 좋은 게 아니라, 주변의 유사 언어가 같이 학습될 때 representation이 더 좋아진다.

논문에서는 corpus size와 Sentence Retrieval Bible 성능의 Pearson correlation이 **r = .34**였고, 해당 언어와 가까운 k개 언어의 corpus size까지 합치면 **r = .44**로 올라간다고 보고한다. 즉, 유사 언어의 데이터도 성능에 영향을 준다.  

하지만 반대로, 가까운 관련 언어가 없는 경우에는 511개 언어를 함께 학습한 Glot500-m보다 특정 언어 하나만 continued pretraining한 Glot+1이 더 나은 경우도 있다.  

# Problem statement

low resource language adaptation

이전 논문들에서 충분히 좋은 결과를 보였지만 아래 세부 디테일 정보는 부족하다.

vocabulary extension

* Glot500

  * `92 seen + 7 target` mixed corpus로 새 SentencePiece unigram tokenizer 학습

  * 새 tokenizer에만 있는 piece를 기존 XLM-R SentencePiece protobuf 뒤에 append

  * 새 vocab row embedding을 초기화

  * train-only corpus로 continued MLM pretraining

  * PPPL은 held-out test에서 측정

* Yamaguchi et al.의 low-resource vocabulary expansion은 main에서 제외하고 추가 실험으로 둔다.

  * 아주 적은 target language text로 auxiliary tokenizer를 새로 학습

  * 기존 source vocab에 없는 target token을 고름

  * 기존 vocab 뒤에 새 token을 append

  * 새 embedding row를 random, mean, FVT류, family-aware 방식으로 초기화

  * 짧은 continued pretraining으로 새 token을 적응시킴

Embedding Initialization

그래서 나는 이런 ablation study 를 해보려한다.

# Novelty

vocabulary extension

* Glot500 방식 vocab injection을 고정

* 야마구치 방식은 appendix/additional experiment

Embedding Initialization

* 동일 tokenizer, 동일 corpus, 동일 MLM schedule에서 `random`, `mean`, `fvt`, `weighted_fvt`, `family_mean` 비교
* 핵심 hypothesis는 `fvt` 계열이 새 token embedding row에 가장 좋은 출발점을 준다는 것

# Method

## Data

v5.2는 `target10`이 아니라 `Target7` 실험이다.

```text
Corpus universe = 99 language-script = 92 XLM-R-seen + 7 XLM-R-unseen target
Target7 = dtp_Latn, xav_Latn, bam_Latn, csb_Latn, ile_Latn, lij_Latn, fur_Latn
```

언어 선택 기준:

* 모두 `XLM-R training language = no`
* Glot500 raw corpus 존재
* `new_length >= 30,000`
* downstream task overlap을 최대화하는 30k 근처 low-resource band
* 지역은 Southeast Asia, South America, West Africa, Europe/Constructed로 분산
* 단, v5.2 Target7은 모두 `Latn` script라서 script-diversity claim은 하지 않는다.

Selected Target7:

| language_script | language | region | new_length | 역할 |
| --- | --- | --- | ---: | --- |
| `dtp_Latn` | Kadazan Dusun | Southeast Asia | 48,468 | Tatoeba/Bible/Roundtrip/Taxi/embedding overlap anchor |
| `xav_Latn` | Xavánte | South America | 31,765 | Bible/Roundtrip/POS/Taxi overlap anchor |
| `bam_Latn` | Bambara | West Africa | 32,150 | Bible/Roundtrip/POS/Taxi overlap anchor |
| `csb_Latn` | Kashubian | Europe | 33,743 | Tatoeba/NER/embedding overlap anchor |
| `ile_Latn` | Interlingue | Constructed/Europe | 40,984 | Tatoeba/embedding anchor |
| `lij_Latn` | Ligurian | Europe | 42,447 | NER/POS anchor |
| `fur_Latn` | Friulian | Europe | 30,052 | NER-ready minimum-band tail anchor |

raw corpus / PPPL / MLM 데이터 양:

| 항목 | 값 |
| --- | ---: |
| source raw sentences | 1,025,895,043 |
| source seen sentences | 1,025,635,434 |
| source target7 sentences | 259,609 |
| MLM train merge lines | 4,482,259 |
| MLM seen/head samples | 4,147,176 |
| MLM target7 samples | 335,083 |
| sampling_factor | 0.3 |
| scale | 1.5 |
| current PPPL diagnostic examples | 140 |
| current PPPL diagnostic masked tokens | 5,196 |

주의: 현재 v5.2 PPPL 산출물은 `held-out test`가 아니라
`target7_train_source_diagnostic`으로 기록되어 있다. 따라서 발표에서는
Glot500-style held-out PPPL 재연 결과가 아니라, checkpoint별 intrinsic diagnostic으로
설명한다.

downstream task별 실제 target7 coverage:

| task | target7 languages | 실제 데이터/상태 | 발표 해석 |
| --- | --- | --- | --- |
| Tatoeba retrieval | `dtp_Latn`, `ile_Latn`, `csb_Latn` | 3 target languages measured | target7 retrieval evidence |
| Bible retrieval | `dtp_Latn`, `xav_Latn`, `bam_Latn` | 23,238 aligned verse pairs materialized | target7 retrieval evidence |
| Roundtrip alignment | `dtp_Latn`, `xav_Latn`, `bam_Latn` | 22,669 JSONL samples materialized | target7 alignment evidence |
| NER | `csb_Latn`, `lij_Latn`, `fur_Latn` | 300 target test sentences measured for all table models | small target-subset diagnostic |
| POS | Table 3 POS 91 languages; target-relevant `xav_Latn`, `bam_Latn`, `lij_Latn` 포함 | recovered `pos_rebuilt` split measured for all table models | transfer evidence |
| Taxi1500 | target7 direct row 없음 | current result is English row | target7 evidence로 쓰지 않음 |

## Tokenization

tokenizer 방법론은 Glot500 방식으로 고정한다. 이번 main 비교는 tokenizer 자체가 아니라
embedding initialization 차이다.

BPE: Byte Pair Encoding → **자주 같이 등장하는 문자 쌍을 계속 합치는 방식**

Unigram Language Model → Unigram 방식은 처음부터 많은 subword 후보를 만들어두고, 그중 문장을 가장 잘 설명하는 token 조합을 남기는 방식

본 glot500에서는 SentencePiece + Unigram Language Model 사용

여기서 Head language 를 많이넣으면 **vocab size는 고정 되어있는 환경에서 high resource language 에 subtoken 들이 편항됨.**

Sampling strategy: α = 0.3

$$
P_i ∝ n_i^α
$$

* P_i = i번째 language-script가 샘플링될 확률

* n_i = i번째 language-script의 데이터 양

* α = 0.3

MLM v5.2 sampled train corpus:

* 실제 생성된 train corpus line 수: `4,482,259`

* `sampling_factor = 0.3`

* `scale = 1.5`

* seen/head samples: `4,147,176`

* target7 samples: `335,083`

## Embedding Initialization

vocabulary extension을 하면 기존 XLM-R에는 없던 새 token row가 embedding matrix 뒤에
추가된다. 이때 새 row를 어떤 벡터로 시작하느냐가 initialization ablation의 핵심이다.

이번 실험에서는 tokenizer, corpus, MLM schedule은 모두 고정하고, 새 token embedding row의
초기화 방법만 바꿔 비교한다.

| Method | 초기화 방식 | 직관 | 발표용 해석 |
| --- | --- | --- | --- |
| `random` | 새 row를 normal random으로 초기화 | 아무 정보 없이 시작하는 기본선 | Glot500-style vocab injection의 가장 단순한 baseline |
| `mean` | 기존 XLM-R lexical embedding의 global mean 사용 | 새 token을 평균적인 기존 단어 위치에서 시작 | 안정적이지만 token 표면형 정보는 쓰지 않음 |
| `fvt` | 새 token surface를 기존 XLM-R tokenizer로 다시 쪼갠 뒤, source subtoken embedding 평균 사용 | 새 token이 기존 subtoken 조합으로 설명될 수 있으면 그 의미/형태 정보를 재사용 | main hypothesis: 새 token에 가장 좋은 출발점을 제공 |
| `weighted_fvt` | FVT subtoken 평균에 surface length weight 적용 | 긴 subtoken이 더 많은 lexical 정보를 담는다는 가정 | FVT를 더 정교화한 ablation |
| `family_mean` | token provenance가 가리키는 language family의 source-token 평균 사용 | family/typology prior를 embedding 초기값에 반영 | 표면형이 아니라 계통 정보를 쓰는 stronger prior |

예시 설명:

```text
새 token이 target tokenizer에는 하나의 piece로 들어왔더라도, 기존 XLM-R tokenizer로는
여러 subtoken으로 분해될 수 있다. FVT는 그 기존 subtoken들의 embedding 평균을 새 token의
초기값으로 사용한다. 즉 random보다 언어적/형태적 힌트를 가진 상태에서 MLM을 시작한다.
```

공정성 포인트:

* 모든 방법은 같은 `92 seen + 7 target` corpus를 사용한다.
* tokenizer도 같은 Glot500-style append-only tokenizer를 사용한다.
* MLM hyperparameter도 같다.
* 따라서 표에서 보이는 차이는 주로 "새 embedding row를 어떻게 시작했는가"의 차이로 해석한다.

주의:

* 기존 `align`은 이름상 별도 방법처럼 보이지만, 이번 v5.2 tokenizer에서는 FVT 실패 token이
  거의 없어 `fvt`와 같은 artifact가 됐다.
* 따라서 새 5-way ablation은 `random`, `mean`, `fvt`, `weighted_fvt`, `family_mean`으로
  두고, `align`은 historical continuity row로만 설명한다.

### Current checkpoint diagnostic result

업데이트 기준: 2026-06-28 23:24 KST. 학습은 아직 진행 중이며, 아래는 중간 checkpoint
diagnostic 결과다.

| Step | Method | PPPL lower is better | Tatoeba Top10 higher is better |
| ---: | --- | ---: | ---: |
| 500 | random | 374.606977 | 0.209241 |
| 500 | mean | 479.424743 | 0.217194 |
| 500 | fvt | **161.877958** | **0.223194** |
| 500 | align | 161.877958 | 0.223194 |
| 1000 | random | 241.797413 | 0.222845 |
| 1000 | mean | 270.934481 | 0.214241 |
| 1000 | fvt | **108.603835** | **0.254813** |
| 1000 | align | 108.603835 | 0.254813 |
| 1500 | random | pending | pending |
| 1500 | mean | 208.204215 | 0.235511 |
| 1500 | fvt | **90.288642** | **0.265353** |
| 1500 | align | 90.288642 | 0.265353 |

발표용 한 줄 결론:

```text
Across the available paired checkpoints, FVT gives the strongest initialization
signal: it consistently lowers pseudoperplexity and improves Tatoeba retrieval
compared with random and mean initialization.
```

한국어 발표 문장:

```text
현재까지의 중간 checkpoint 결과에서는 FVT가 가장 강한 초기화 신호를 보인다.
PPPL은 random/mean보다 크게 낮고, Tatoeba retrieval top10 accuracy는 더 높다.
이는 새 token embedding을 완전히 새로 시작하기보다, 기존 XLM-R subtoken embedding을
조합해 시작하는 것이 low-resource target token adaptation에 유리할 수 있음을 보여준다.
```

claim 수위:

* 지금 말할 수 있는 것: `FVT is the strongest initialization signal in current checkpoint diagnostics`.
* 아직 말하면 안 되는 것: 모든 downstream task에서 최종적으로 FVT가 이겼다.
* `4000` step은 수렴 결과가 아니라 early diagnostic으로만 사용한다.
* 최종 결론은 최소 `8000` step 이후 loss/PPPL/downstream trajectory를 확인한 뒤 확정한다.

## Training

### 수렴 확인: MLM loss graph

**대표 plot**

`2_training/convergence_5way_loss_curve.png`

**PPT 한 줄**

```text
Training loss는 20k step 이후 random/mean/fvt에서 감소폭이 크게 둔화되지만, 아직 완전 수렴으로 단정하지 않는다.
```

**해석**

* 위 패널은 MLM training loss의 전체 감소 추세를 보여준다.
* 아래 패널은 직전 1000-step checkpoint 대비 loss 감소폭을 보여준다.
* 최근 loss drop이 작아지면 추가 학습 이득이 줄어드는 신호로 볼 수 있다.
* 현재 완료된 `random`, `mean`, `fvt`는 loss 감소폭이 둔화된 상태이지, 완전 수렴으로 단정하지 않는다.
* 단, `weighted_fvt`, `family_mean`은 아직 학습 중/대기 상태라 5-way 전체 수렴 결론은 보류한다.
* 완전 수렴 claim은 loss graph와 PPPL/downstream trajectory를 함께 확인한 뒤 제시한다.

### MLM task

setting

training plot

table작성

|                                          |          |          |                                                          |          |          |                                                          |         |         |                                                          |
| ---------------------------------------- | -------- | -------- | -------------------------------------------------------- | -------- | -------- | -------------------------------------------------------- | ------- | ------- | -------------------------------------------------------- |
|                                          | **tail** | **tail** | **tail**                                                 | **head** | **head** | **head**                                                 | **all** | **all** | **all**                                                  |
|                                          | XLM-R-B  | XLM-R-L  | [Glot500-m](https://huggingface.co/cis-lmu/glot500-base) | XLM-R-B  | XLM-R-L  | [Glot500-m](https://huggingface.co/cis-lmu/glot500-base) | XLM-R-B | XLM-R-L | [Glot500-m](https://huggingface.co/cis-lmu/glot500-base) |
| Pseudoperplexity                         |          |          |                                                          |          |          |                                                          |         |         |                                                          |
| Sentence Retrieval Tatoeba (Top 10 Acc.) |          |          |                                                          |          |          |                                                          |         |         |                                                          |
| Sentence Retrieval Bible (Top 10 Acc.)   |          |          |                                                          |          |          |                                                          |         |         |                                                          |
| Text Classification (F1)                 |          |          |                                                          |          |          |                                                          |         |         |                                                          |
| NER (F1)                                 |          |          |                                                          |          |          |                                                          |         |         |                                                          |
| POS (F1)                                 |          |          |                                                          |          |          |                                                          |         |         |                                                          |
| Roundtrip Alignment (Acc.)               |          |          |                                                          |          |          |                                                          |         |         |                                                          |

### sentence vector 끼리의 similarity 비교

**가능 여부: 가능.**

v5.2에서는 sentence embedding similarity를 novelty/diagnostic 분석으로 구성할 수 있다. 핵심 질문은 vocab extension과 embedding initialization이 PPPL 수치만 바꾸는 것이 아니라, 문장 벡터 공간에서 의미 정렬과 언어별 군집 구조도 바꾸는지 확인하는 것이다.

**비교 단위**

| 비교 | 목적 | 데이터 |
| --- | --- | --- |
| 같은 의미끼리 | target sentence와 English aligned sentence가 가까워지는지 확인 | Tatoeba, Bible |
| 같은 언어끼리 | 의미가 다른 target 문장들도 언어 identity 기준으로 모이는지 확인 | Tatoeba, Bible adjacent sentence |
| Roundtrip multi-way | source-English, source-pivot, English-pivot을 각각 비교 | Bible roundtrip |
| 2D point map | 모델별 embedding geometry를 시각적으로 비교 | PCA 2D map |

**현재 v5.2에서 바로 만들 수 있는 sampled diagnostic pair 수**

아래 300 단위는 embedding similarity/시각화용으로 고정한 샘플 수이다. Roundtrip
alignment 본 평가는 full materialized data인 22,669 samples로 갱신했다.

| Source | Pair type | Pairs |
| --- | --- | ---: |
| Bible | aligned_bible_src_eng | 300 |
| Bible | same_language_bible_adjacent | 300 |
| Roundtrip | roundtrip_src_eng | 300 |
| Roundtrip | roundtrip_src_pivot | 300 |
| Roundtrip | roundtrip_eng_pivot | 300 |
| Tatoeba | aligned_tatoeba_src_eng | 300 |
| Tatoeba | same_language_tatoeba_adjacent | 300 |
| **Total** |  | **2,100** |

**산출물**

| File | 내용 |
| --- | --- |
| `similarity_scores.tsv` | pair별 cosine / centered cosine |
| `similarity_summary.tsv` | model, pair type별 평균 similarity |
| `embedding_map_2d.tsv` | 문장별 2D 좌표 |
| `embedding_map_2d.png` | 2D point map |

**실행**

```bash
python3 scripts/build_v52_similarity_pairs.py
GPU=2 MODEL_KEYS=v52_random_step4000,v52_mean_step4000,v52_fvt_step4000 bash scripts/run_v52_similarity.sh
```

**해석 경계**

이 분석은 공식 Glot500 metric이 아니라 representation geometry를 설명하기 위한 추가 novelty 분석이다. 같은 의미 aligned pair의 similarity가 높아지면 semantic alignment 개선으로 해석할 수 있고, same-language adjacent pair의 similarity가 높아지면 언어 identity 또는 표면적 스타일 군집이 강해진 것으로 해석해야 한다. Roundtrip은 여러 intermediate comparison을 평균 하나로 뭉개기보다 `src-eng`, `src-pivot`, `eng-pivot`을 따로 보고 어느 축에서 alignment가 깨지는지 설명한다.

#### Family/script similarity diagnostic

**목적**

v5.2 target7은 모두 `Latn` script이므로, "같은 라틴 문자라서 가까운가"와 "언어 계통이 가까워서 가까운가"를 분리해서 볼 수 있다. 모든 pair는 최소 하나의 unseen tail language를 포함하도록 구성했다. head-head pair는 사용하지 않는다.

**실행 결과**

| 항목 | 값 |
| --- | ---: |
| sampled languages | 38 |
| sentence points | 3,708 |
| tail-anchored pair rows | 11,956 |
| samples per language | up to 100 |
| pair samples per language pair | up to 50 |
| models | random / mean / fvt step4000 |

**family / macro-family 판정 기준**

| 기준 | 규칙 | 발표용 예시 |
| --- | --- | --- |
| same language | `language_script`가 같음 | `dtp_Latn` - `dtp_Latn` |
| same family | `family`가 같음 | `fur_Latn` - `lij_Latn`: Romance |
| same macro-family | `macro_family`는 같지만 `family`는 다름 | `csb_Latn` - `fur_Latn`: Slavic/Romance, Indo-European |
| same script only | `script`는 같지만 `family`는 다름 | `bam_Latn` - `fra_Latn`: Latn, Mande/Romance |
| different script/family | `script`와 `family`가 모두 다름 | `bam_Latn` - `ara_Arab`: Latn/Arab, Mande/Semitic |

`same macro-family`는 `same family`와 겹치지 않도록 더 넓은 계통만 같은 경우로 둔다. 예를 들어 `fur_Latn` - `lij_Latn`은 둘 다 Romance라 same family이고, `csb_Latn` - `fur_Latn`은 Slavic/Romance라 family는 다르지만 Indo-European으로 same macro-family이다.

**실제 나뉜 language-pair bucket**

| tail | same family | same macro-family only |
| --- | --- | --- |
| `bam_Latn` | 없음 | `xho_Latn` = Niger-Congo |
| `csb_Latn` | `ces/hrv/pol/slk/slv` = Slavic | `cat/fra/ita/por/ron` = Romance; `deu/eng/nld` = Germanic; `ell`; `mar` = Indo-European |
| `dtp_Latn` | `ind/jav/mlg/msa/tgl` = Austronesian | 없음 |
| `fur_Latn` | `lij` 및 `cat/fra/ita/por/ron` = Romance | Slavic/Germanic/Hellenic/Indo-Aryan heads = Indo-European |
| `ile_Latn` | `epo_Latn` = Constructed | 없음 |
| `lij_Latn` | `fur` 및 `cat/fra/ita/por/ron` = Romance | Slavic/Germanic/Hellenic/Indo-Aryan heads = Indo-European |
| `xav_Latn` | 없음 | 없음 |

tail끼리는 `fur-lij`만 same family이고, `csb-fur`, `csb-lij`만 same macro-family이다. 나머지 tail-tail 조합 18개는 different family bucket이다.

**FVT step4000 기준 centered cosine**

| Relation type | Pairs | Mean centered cosine |
| --- | ---: | ---: |
| tail within language | 350 | 0.473229 |
| tail-tail same family | 50 | 0.306983 |
| tail-tail same macro-family | 100 | 0.181989 |
| tail-tail different family | 900 | 0.123785 |
| tail-head same family | 1,050 | 0.036947 |
| tail-head different family, same Latn script | 6,100 | -0.049819 |
| tail-head different family, different script | 1,856 | -0.078834 |

**발표용 해석**

raw cosine은 대부분 0.9 근처라 anisotropy 영향이 크므로 `centered_cosine`을 중심으로 말한다. 같은 Latn script만 공유하는 경우보다 같은 family를 공유하는 경우가 더 가깝다. 즉 v5.2 sentence vector 공간에서는 script 효과도 일부 있지만, family/typology 효과가 더 강한 설명력을 가진다. tail끼리만 봐도 `same family > same macro-family > different family` 순서가 나온다.

2D point map은 언어당 최대 100개 문장으로 다시 생성했다. centroid map은 비교적 잘 나뉘지만, sentence-level point는 완전한 cluster separation이 아니다. `dtp_Latn`, `bam_Latn`, `xav_Latn`은 비교적 뚜렷하고, `csb_Latn`, `fur_Latn`, `ile_Latn`, `lij_Latn`은 Latin script 기반 유럽권 언어라 많이 겹친다. 따라서 발표에서는 "완벽히 분리된다"가 아니라 "tail language identity와 family/typology 구조가 관찰된다"고 말한다.

**대표 plot**

| Plot | 용도 |
| --- | --- |
| `09_family_similarity/family_pair_boxplot_v52_fvt_step4000.png` | relation type별 similarity 분포 |
| `09_family_similarity/family_centroid_heatmap_v52_fvt_step4000.png` | 언어 centroid 간 heatmap |
| `09_family_similarity/family_point_map_tail_by_language_v52_fvt_step4000.png` | tail 언어별 2D point map |
| `09_family_similarity/family_point_map_all_tail_highlight_v52_fvt_step4000.png` | head 회색 + tail 강조 2D point map |
| `09_family_similarity/family_centroid_map_v52_fvt_step4000.png` | head/tail centroid geometry |

#### Tokenization effect : 변화율 확인하기

**Glot500-m의 성능 향상은 tokenizer 확장만으로 설명되지 않는다.**

**확인 질문**

1. v5.2 extended tokenizer가 target7에서 실제로 subword fertility를 줄였는가?
2. 줄였다면, 그 효과만으로 PPPL/downstream 차이를 설명할 수 있는가?

**Tokenization 변화율**

동일한 target7 raw sentence 3,500개에 대해 `xlm-roberta-base` tokenizer와 v5.2 extended tokenizer를 비교했다.

| 항목 | 값 |
| --- | ---: |
| XLM-R tokenizer length | 250,002 |
| v5.2 tokenizer length | 366,666 |
| appended/novel token strings | 116,664 |
| samples | 7 languages x 500 sentences |

| Scope | XLM-R tokens/word | v5.2 tokens/word | Reduction | XLM-R chars/token | v5.2 chars/token | New-token share |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| target7 | 2.204134 | 1.592392 | 27.754280% | 2.074479 | 2.871421 | 28.392427% |

**언어별 reduction**

| Language | Full name | Reduction |
| --- | --- | ---: |
| `xav_Latn` | Xavánte | 34.906811% |
| `csb_Latn` | Kashubian | 33.717290% |
| `bam_Latn` | Bambara | 32.677703% |
| `dtp_Latn` | Kadazan Dusun | 24.281085% |
| `fur_Latn` | Friulian | 20.331393% |
| `lij_Latn` | Ligurian | 16.914278% |
| `ile_Latn` | Interlingue | 12.426036% |

**해석**

Tokenizer extension은 target7에서 확실히 효과가 있다. 평균 tokens/word가 2.204134에서 1.592392로 줄어 약 27.75%의 fertility improvement가 나온다. 즉 Glot500-style vocabulary extension은 tail language를 더 짧고 안정적인 subword sequence로 표현하게 만든다.

하지만 이 효과만으로 v5.2 성능 차이를 설명할 수는 없다. v5.2 main ablation에서 `random`, `mean`, `fvt`는 모두 같은 extended tokenizer, 같은 corpus, 같은 MLM schedule을 사용한다. 그러므로 세 모델 사이의 PPPL/downstream 차이는 tokenizer 자체가 아니라 새 vocabulary row의 embedding initialization에서 온다.

| Metric | Random | FVT | 같은 tokenizer 조건에서의 차이 |
| --- | ---: | ---: | --- |
| PPPL | 119.581715 | 58.025602 | FVT가 훨씬 낮음 |
| Tatoeba Acc10 | 0.248908 | 0.282957 | FVT가 높음 |
| Roundtrip Acc. | 0.019533 | 0.025167 | FVT가 높음 |

**발표용 한 문장**

Tokenizer extension은 tail language의 subword fertility를 개선하지만, 같은 tokenizer를 공유하는 initialization variants 사이에서도 성능 차이가 유지된다. 따라서 v5.2의 novelty는 tokenizer 확장 자체가 아니라, 확장된 vocabulary row를 어떻게 initialize하느냐에 있다.

**산출물**

| File | 내용 |
| --- | --- |
| `0_tokenizer/03_tokenization_effect/results_ko.md` | 한국어 결과 요약 |
| `0_tokenizer/03_tokenization_effect/tokenization_effect_summary.tsv` | 언어별 변화율 |
| `0_tokenizer/03_tokenization_effect/tokenization_effect_change.png` | reduction bar plot |

## Downstream task

task 분석까지만 수행하고 마무리

시간관계상 하지 못했음을 정리

# Result

# Conclusion and limitation

대부분 tail language에는 human-labeled evaluation data가 없어서 mixed evaluation strategy를 쓴다

![e7c710c4-81fe-4cd1-8810-177fdff68aa7](/api/assets/v2/workspaces/iiplab/projects/03bc868f-9e88-46da-98fa-c91290e83b29/e7c710c4-81fe-4cd1-8810-177fdff68aa7/)

근데 실제 데이터를 까보면 실험 테이블에서 head/tail을 나누는 operational definition은 XLM-R coverage 기준

`tail`은 보통: XLM-R에 없던 언어에 가깝지,corpus size 30k~100k의 진짜 저자원 언어만 뜻하지 않습니다.

# Reference

Glot500

XLM-bert

야마구치

# Appendix

## 99-Language Compact Table
