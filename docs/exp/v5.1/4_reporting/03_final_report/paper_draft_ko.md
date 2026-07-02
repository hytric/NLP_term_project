# v5.1 보고서 초안

## 제목

Glot500-style Vocabulary Extension에서 New-token Embedding Initialization의 효과 분석

## 초록

본 연구는 Glot500의 다국어 평가 체계를 축소된 통제 환경에서 재현하고,
vocabulary extension 이후 새 token embedding initialization이 unseen-language
adaptation에 미치는 영향을 분석한다. 언어 범위는 XLM-R 학습에 포함된 92개
language-script와 새로 선택한 XLM-R-unseen target10으로 제한한다. 기존 v5의
train-source PPPL 문제를 보완하기 위해 v5.1에서는 각 language-script의 raw
corpus에서 dev/test를 먼저 제외한 뒤, train-only corpus로 tokenizer 확장과
continued MLM을 수행한다. 최종 PPPL은 Glot500 방식에 맞춰 held-out test에서만
측정한다. Novelty는 동일한 tokenizer, corpus, step, batch, schedule 아래에서
Random initialization과 FVT/source-token-decomposition initialization을 matched
pair로 비교하는 데 있다. 평가는 PPPL, Tatoeba/Bible retrieval, Taxi1500, NER,
POS, Roundtrip alignment를 유지하고, 추가로 sentence embedding similarity와 2D
map을 통해 representation-level 변화를 분석한다.

## 핵심 질문

XLM-R이 학습한 92개 언어와 새로 고른 XLM-R-unseen target10만 사용해
Glot500의 평가 방식을 최대한 충실히 재연한다. 이때 vocabulary extension 이후
새 token embedding을 어떻게 초기화하느냐가 held-out PPPL과 downstream metric에
영향을 주는지 확인한다.

## 기여

1. Glot500의 split discipline을 축소 실험 환경에서 재현한다. v5.1은 train/dev/test를 먼저 고정하고, tokenizer/MLM에는 train-only corpus만 사용한다.
2. Downstream-aware target10을 재선정해 target-side retrieval, tagging, alignment evidence를 만들 수 있도록 했다.
3. Vocabulary extension 이후 new-token embedding initialization을 Random vs FVT matched pair로 분리해 비교한다.
4. Glot500 7개 metric 외에 sentence embedding similarity와 2D map을 추가해 novelty 분석을 보강한다.

## 실험 설계

본 실험은 v5.1 strict line을 최종 실험으로 사용한다. 기존 v5는 train-source
PPPL과 downstream coverage 문제가 있었으므로 diagnostic/fallback으로만 둔다.
v5.1에서는 각 language-script raw corpus에서 dev/test를 먼저 제외하고,
tokenizer training과 continued MLM은 train-only corpus로 수행한다. PPPL은
Glot500 방식에 맞춰 held-out test set에서 측정한다.

## 데이터

언어 universe는 총 102개다. 이 중 92개는 XLM-R 학습 언어이고, target10은
XLM-R-unseen 언어로 구성된다. Target10은 downstream coverage와 지역/문자 다양성을
함께 고려해 선택했다.

Target10:

```text
guj_Gujr, asm_Beng, srp_Cyrl, sun_Latn, zsm_Latn,
aze_Latn, fil_Latn, bos_Latn, dzo_Tibt, sat_Olck
```

평가 coverage는 PPPL 102/102, Tatoeba 66/102, Bible 80/102, Taxi1500 1/102,
NER 84/102, POS 58/102, Roundtrip 80/102이다. Target10 기준으로는 PPPL 10/10,
Tatoeba 3/10, Bible 6/10, NER 6/10, Roundtrip 6/10이 가능하다.

| Metric / data | Total | Head | Target10 | Report use |
| --- | ---: | ---: | ---: | --- |
| PPPL raw text | 102 | 92 | 10 | final held-out intrinsic metric |
| Tatoeba retrieval | 66 | 63 | 3 | target-subset retrieval evidence |
| Bible retrieval | 80 | 74 | 6 | target-subset retrieval evidence |
| Taxi1500 classification | 1 | 1 | 0 | Glot500 replay only, no target claim |
| NER | 84 | 78 | 6 | target-subset tagging evidence |
| POS | 58 | 58 | 0 | Glot500 replay only, no target claim |
| Roundtrip alignment | 80 | 74 | 6 | target-subset alignment evidence |

여기서 `head`는 XLM-R 학습 언어 92개 중 해당 metric data가 있는 subset이고,
`target10`은 이번에 선택한 XLM-R-unseen 10개 중 해당 metric data가 있는 subset이다.
`all`은 v5.1의 102개 language-script universe 안에서 head와 target10을 합친 값이다.

## 방법

Tokenizer는 v5.1 strict 5% train-only corpus로 확장했다. Base vocab size는
250,002이고, 확장 후 vocab size는 370,051이다. 새 token은 120,049개다.
초기화 방법은 두 가지를 비교한다.

| Method | 설명 |
| --- | --- |
| Random | 새 token embedding을 random initialization으로 둔다. |
| FVT | 새 token을 기존 source token decomposition으로 표현해 embedding을 초기화한다. |

두 방법은 같은 corpus, tokenizer, step, batch, schedule로 continued MLM을 수행한다.
현재 first strict line은 5% corpus, 3K steps matched pair이다.

### 학습 설정

| Setting | Value |
| --- | --- |
| Train corpus | strict v5.1 5% train-only corpus |
| Lines | 8,130,401 |
| Model family | XLM-R / Glot500-compatible masked LM |
| Tokenizer | extended SentencePiece, vocab 370,051 |
| Optimizer | AdamW |
| Initial LR | 5e-5 |
| Effective batch | 384 |
| Per-device batch | 8 |
| GPUs | 3 GPUs, physical GPU 0/1/3 |
| Gradient accumulation | 16 |
| Max sequence length | 512 |
| Max steps | 3,000 per initializer |
| Precision | fp16 |

현재 `v51_random` run이 먼저 실행 중이고, launcher가 완료 후 `v51_fvt` run으로
넘어가도록 구성되어 있다. 최신 live 상태는 `docs/exp/v5.1/2_training/training_status.md`에
기록한다.

## 평가

Glot500의 7개 평가 축을 유지한다.

| 평가 | v5.1 실행 계획 | Final table grouping |
| --- | --- | --- |
| PPPL | held-out test split에서 mask-based pseudoperplexity | head / target10 / all |
| Tatoeba retrieval | layer 8 mean embedding, cosine Top-10 accuracy | head / target10 / all |
| Bible retrieval | materialized Bible test pairs, cosine Top-10 accuracy | head / target10 / all |
| Taxi1500 | fine-tune then test F1 | available/head only |
| NER | English fine-tune, target test zero-shot F1 | head / target10 / all |
| POS | documented training language fine-tune, test F1 | available/head only |
| Roundtrip alignment | Bible-based roundtrip alignment accuracy | head / target10 / all |

결과 표는 `head`, `target10`, `all`로 분리한다. POS와 Taxi1500은 target10 data가
없으므로 target-side improvement claim에 쓰지 않는다.

## 결과

실험 종료 시점에는 final checkpoint가 생성되지 않았다. 따라서 아래 결과 표는
metric 삽입 대상이자 pending table이며, 실제 종료 결과는
`docs/exp/v5.1/EXPERIMENT_END_SUMMARY_KO.md`에 정리한다.

```text
docs/exp/v5.1/3_evaluation/09_aggregation/main_head_tail_all.tsv
docs/exp/v5.1/3_evaluation/09_aggregation/v5_target_subset.tsv
docs/exp/v5.1/4_reporting/00_tables/table_03_main_metric_results.md
docs/exp/v5.1/4_reporting/00_tables/table_06_metric_completion.md
```

### Main Metric Table Template

| Metric | XLM-R Base head | Glot500 head | Random head | FVT head | XLM-R Base target10 | Glot500 target10 | Random target10 | FVT target10 | Random vs FVT interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| PPPL | pending | pending | pending | pending | pending | pending | pending | pending | lower is better |
| Tatoeba Top-10 Acc. | pending | pending | pending | pending | pending | pending | pending | pending | higher is better |
| Bible Top-10 Acc. | pending | pending | pending | pending | pending | pending | pending | pending | higher is better |
| Taxi1500 F1 | pending | pending | pending | pending | n/a | n/a | n/a | n/a | no target10 claim |
| NER F1 | pending | pending | pending | pending | pending | pending | pending | pending | higher is better |
| POS F1 | pending | pending | pending | pending | n/a | n/a | n/a | n/a | no target10 claim |
| Roundtrip Acc. | pending | pending | pending | pending | pending | pending | pending | pending | higher is better |

### Training Curve

학습 loss는 final metric이 아니라 optimization trace로만 사용한다. 종료 시점 기준
`v51_random`은 `1869/3000` step까지 진행한 뒤 멈췄으며, 로그에 기록된 최신 loss row는
step 1800의 loss `4.0544`, LR `2.01e-05`이다.

Figure source:

```text
docs/exp/v5.1/4_reporting/01_figures/training_loss_lr.svg
```

![v5.1 random MLM training loss and LR trace](../01_figures/training_loss_lr.svg)

최종 보고서에는 이 curve를 partial optimization trace로만 제시한다. FVT run,
held-out PPPL, downstream 결과가 없으므로 Random vs FVT 성능 claim은 하지 않는다.

## Novelty

본 실험의 novelty는 vocabulary extension 자체가 아니라, 확장된 vocabulary의
새 token embedding initialization이 low-resource / unseen-language adaptation에
주는 영향을 matched pair로 분리해 보는 데 있다. 추가로 sentence-vector similarity와
2D map을 통해 같은 의미 문장과 같은 언어 문장이 layer 8 embedding space에서
어떻게 모이는지 분석한다.

현재 similarity 입력은 Tatoeba, Bible, Roundtrip에서 만든 22,600개 sentence
pair이다. 결과 파일은 `docs/exp/v5.1/3_evaluation/08_embedding_similarity/`에
`similarity_scores.tsv`, `similarity_summary.tsv`, `embedding_map_2d.tsv`,
`embedding_map_2d.png`로 저장한다.

Similarity 분석은 세 가지 질문으로 정리한다.

| Question | Pair source | Expected evidence |
| --- | --- | --- |
| 같은 언어의 문장들이 더 잘 모이는가 | same-language pairs | cosine distribution, 2D clusters |
| 같은 의미의 cross-lingual pair가 가까워지는가 | Tatoeba/Bible aligned pairs | aligned pair cosine |
| roundtrip intermediate language가 alignment를 보존하는가 | Bible roundtrip pairs | source-English and source-pivot cosine |

FVT가 Random보다 target10에서 PPPL을 낮추거나 retrieval/tagging/alignment를 개선하면서
similarity space에서도 aligned pair를 더 가깝게 만든다면, embedding initialization이
vocabulary extension 이후의 semantic transfer에 기여했다는 제한적 주장을 할 수 있다.

## Limitations

v5.1은 Glot500 전체 500개 언어를 재현하지 않고, 92 seen + target10으로 제한한
controlled reproduction이다. Downstream target coverage는 metric별로 다르며,
POS와 Taxi1500은 target10 claim을 제공하지 못한다. 기존 v5의 train-source PPPL은
최종 Glot500-style PPPL로 사용하지 않는다.

## 결론 초안

v5.1은 기존 v5의 핵심 문제였던 train-source PPPL과 target10 downstream coverage
부족을 보완한 strict rerun 설계다. 데이터 split, tokenizer 확장, initialization
pair, evaluation coverage, post-checkpoint execution path는 준비되었다. 다만 실험
종료 시점에 `v51_random`이 `1869/3000` step에서 중단되었고 `v51_fvt`는 시작되지
않았으므로, Random과 FVT의 matched comparison 및 Glot500-style final metric
claim은 제시하지 않는다. 이번 산출물은 strict rerun 설계, 재현 가능한 평가 경로,
partial random MLM optimization trace로 보고한다.
