# v5 Report Draft

작성 상태: execution draft, 2026-06-28 기준  
실험 버전: v5 `Glot500_v5_glot50010_xlmr100`

## Abstract

본 연구는 Glot500의 multilingual vocabulary expansion 및 continued pretraining
흐름을 작은 규모에서 재현하고, vocabulary extension 이후 새 token embedding
row 초기화가 low-resource language adaptation에 미치는 영향을 분석한다. v5는
XLM-R seen Glot500 language-script `92`개와 Glot500 내부 raw dataset에서 고른
diverse target language-script `10`개를 사용한다. target `10`개는 모두 XLM-R
seen이 아니며 Glot500의 30,000 sentence 이상 inclusion threshold를 만족한다.
방법론적으로는 Glot500식 SentencePiece model append 방식과 Yamaguchi et al.의
low-resource vocabulary expansion 계열에서 동기를 얻은 embedding initialization
방법을 비교한다. 평가는 Glot500에서 사용한 모든 metric을 head/tail/all 관점으로
수행한다. 단, 현재 v5의 PPPL은 local raw dataset의 `train` split에서 추출한
train-source intrinsic diagnostic이므로 Glot500 논문의 held-out test PPPL과
동일한 final test metric으로 승격하지 않는다. strict held-out PPPL 재현은 v5.1
correction line에서 수행한다.

현재 문서는 실행 중 보고서 초안이다. 데이터 구성, tokenizer, embedding
initialization, zero-step 결과는 측정 산출물 기준으로 채웠고, continued MLM 이후
downstream 결과는 `waiting for checkpoint`, `running`, `blocked-data`,
`coverage-limited` 같은 explicit status label로 남긴다.

Claim boundary and allowed wording are tracked in:

```text
docs/exp/v5/4_reporting/03_final_report/claim_ledger.md
```

MLM/PPPL held-out policy is tracked in:

```text
docs/exp/v5/MLM_HELDOUT_POLICY_KO.md
```

Downstream metric-to-runner mapping is tracked in:

```text
docs/exp/v5/3_evaluation/metric_mapping.md
```

## 1. Introduction

XLM-R 계열 multilingual model은 많은 언어를 지원하지만, 실제로는 자료가 많고
tokenizer coverage가 좋은 언어에 성능이 집중되는 경향이 있다. Glot500은 더 많은
language-script corpus를 수집하고 vocabulary와 representation을 확장하는 방향을
제안한다.

본 프로젝트는 Glot500 전체를 재학습하는 것이 아니라, 계산 가능한 범위에서 핵심
구조를 재현하고 vocabulary extension에서 자주 간과되는 질문을 다룬다.

> 새 vocabulary token을 추가했을 때, 해당 token의 embedding row를 random으로
> 둘 것인가, 아니면 기존 tokenizer와 embedding을 이용해 의미 있는 초기값을
> 줄 것인가?

이 질문은 low-resource 언어에서 특히 중요하다. 추가 token이 충분히 학습되지
않으면 random initialization의 영향이 오래 남을 수 있고, source tokenizer 기반
초기화가 early-step 안정성과 downstream transfer에 도움을 줄 수 있다.

## 2. Related Work

### Glot500

Glot500은 `Glot500-c` corpus와 continued pretraining을 통해 511개의 주로
low-resource 언어를 다루는 multilingual model을 만든다. 원 논문은 XLM-R 대비
high-resource와 low-resource 양쪽에서 향상을 보고하며, 품질을 설명하는 단일
요인보다 corpus size, script, related language support, model capacity 등이 함께
작동한다고 분석한다.

v5는 Glot500을 full-scale로 재현하지 않는다. 대신 vocabulary expansion,
continued MLM pretraining, head/tail/all 평가 구도를 보존한다.

### Yamaguchi-Style Vocabulary Expansion

Yamaguchi et al.은 약 `0.01GB` 수준의 target language text만으로 LLM vocabulary를
확장하는 방법을 연구한다. 이 계열의 방법은 target language corpus에서 새 token을
선정하고, 기존 tokenizer/model에 token을 추가한 뒤, embedding initialization과
continued training을 비교한다.

본 프로젝트에서 `Yamaguchi 방법`은 V3에서 사용한 `add_tokens()` 기반 vocabulary
expansion 방식을 설명하기 위한 methodological label이다. V3는 기존 XLM-R tokenizer
id와 special token id를 보존하면서 새 token만 뒤에 붙이는 방식이었고, V4/V5는
Glot500에 더 가까운 SentencePiece model append 방식이다.

## 3. Research Questions

1. Glot500식 tokenizer expansion과 continued MLM pretraining을 102-language
   setting에서 재현하면 XLM-R-base 대비 head/tail/all 성능이 개선되는가?
2. 새 vocabulary embedding row를 source tokenizer 기반으로 초기화하면 random
   initialization보다 zero-step 및 after-training 성능이 개선되는가?
3. MLM proxy 개선이 sentence retrieval, NER, POS, text classification,
   roundtrip alignment 같은 downstream task로 이어지는가?

## 4. Data

### Head/Seen Languages

Head group은 v4와 동일하게 XLM-R seen Glot500 language-script 중 로컬 raw dataset이
존재하는 `92`개를 사용한다. 원래 XLM-R seen 후보 `100`개 중 다음 `8`개는 local
raw와 public snapshot에서 찾지 못해 제외했다.

```text
ben_Beng
rus_Cyrl
lao_Latn
tel_Telu
ori_Latn
lav_Latn
jpn_Latn
kir_Latn
```

### Tail/Target Languages

Tail group은 Glot500 내부 raw dataset에서 선택한 `10`개 language-script이다.
선정 조건은 `XLM-R != True`, `new_length >= 30000`, raw directory 존재, 그리고
지역/문자/어족 다양성이다.

| rank | language_script | name | region | script | new_length |
| ---: | --- | --- | --- | --- | ---: |
| 1 | `fur_Latn` | Friulian | Europe | Latin | 30,052 |
| 2 | `krc_Cyrl` | Karachay-Balkar | North Caucasus | Cyrillic | 30,353 |
| 3 | `acm_Arab` | Mesopotamian Arabic | West Asia | Arabic | 44,505 |
| 4 | `dzo_Tibt` | Dzongkha | Himalaya | Tibetan | 52,732 |
| 5 | `sat_Olck` | Santali | South Asia | Ol Chiki | 39,614 |
| 6 | `mad_Latn` | Madurese | Southeast Asia | Latin | 38,993 |
| 7 | `bam_Latn` | Bambara | West Africa | Latin | 32,150 |
| 8 | `kjb_Latn` | Q'anjob'al | Mesoamerica | Latin | 31,471 |
| 9 | `quw_Latn` | Tena Lowland Quichua | Andean South America | Latin | 33,449 |
| 10 | `rap_Latn` | Rapanui | Polynesia | Latin | 30,102 |

Target source rows 합계는 `363,421`이다.

### Corpus Construction

v5 raw root:

```text
/home/axt/mnt2/jongha/v5_glot50010/raw
```

Main merge result:

| Item | Value |
| --- | ---: |
| seen languages | 92 |
| target languages | 10 |
| source seen sentences | 1,025,635,434 |
| source target sentences | 363,421 |
| planned seen samples | 82,943,520 |
| planned target samples | 9,508,731 |
| planned total samples | 92,452,251 |
| actual total samples | 92,452,251 |
| missing language dirs | 0 |
| output size | 19G |

Main merge artifacts:

- corpus:
  `/home/axt/mnt2/jongha/v5_glot50010/data/Glot500_v5_glot50010_xlmr100.txt`
- manifest:
  `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.manifest.tsv`
- report:
  `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.report.json`
- command log:
  `/home/axt/mnt2/jongha/v5_glot50010/logs/full_merge_20260626_230847.log`

### Held-Out Boundary For MLM/PPPL

Glot500 splits each language-script corpus into train/dev/test and pretrains
only on train. PPPL is then computed on held-out test. The local v5 raw
datasets used here expose `train` splits, and the completed v5 merge/tokenizer
and MLM runs were built from those train-source rows. Therefore current v5 PPPL
values are reported as `train-source MLM/PPPL diagnostic`.

This does not invalidate v5. The controlled 102-language setup, tokenizer
extension, embedding initialization audits, zero-step comparison, matched 10K
checkpoints, and downstream benchmark rows remain useful. It only narrows the
PPPL claim: strict held-out PPPL is deferred to v5.1, where dev/test rows are
held out before merge/tokenizer/MLM.

## 5. Method

### Tokenization: Glot500 vs Yamaguchi-Style

| Item | Glot500-style | Yamaguchi-style |
| --- | --- | --- |
| 우리 실험 버전 | V4/V5 | V3 |
| 핵심 구현 | XLM-R SentencePiece model 자체에 auxiliary SPM piece append | 기존 tokenizer에 새 token을 `add_tokens()` 계열로 추가 |
| 장점 | Glot500 reproduction에 가까움, SPM score/type 보존 가능 | 기존 token id와 special token id 보존이 쉬움 |
| 주의점 | `<mask>` id가 target tokenizer에서 이동할 수 있음 | SentencePiece byte fallback을 faithful하게 실행하기 어려움 |
| 보고서 표현 | reproduction method | vocabulary expansion inspiration/ablation |

V5 main tokenizer는 Glot500-style이다. mixed corpus에서 auxiliary SentencePiece
tokenizer를 학습하고, auxiliary vocab 중 XLM-R 기존 SPM에 없는 piece를 XLM-R SPM
뒤에 append한다.

Pilot result: `Glot500_v5_glot50010_xlmr100_pilot10k` produced a `1,020,000`
line corpus and a `VOCAB_SIZE=50000` pilot tokenizer. The pilot tokenizer
appended `7,591` tokens, including `256` byte fallback tokens. The `<mask>` id
moved from XLM-R `250001` to pilot tokenizer `257592`, confirming that v5
initialization must copy rows by token identity rather than id prefix.

Pilot tokenization audit on `20` head languages and `10` targets showed
tokens/word improvement for `9/10` target languages. `dzo_Tibt` was the
exception, worsening from `4.223938` to `8.859717` tokens/word. This is a useful
failure case to analyze before making the final tokenizer claim.

Follow-up example analysis on `500` `dzo_Tibt` sentences showed that the
regression is not driven by `<unk>` or byte fallback. The v5 pilot tokenizer used
only `3` byte tokens and `0` `<unk>` tokens, but `83.432%` of its output tokens
were newly appended pieces. The likely issue is score calibration: newly appended
short Tibetan pieces can outcompete useful original XLM-R Tibetan pieces and
increase fertility.

Main tokenizer training on the full `92,452,251`-line corpus completed with
`VOCAB_SIZE=250000`. SentencePiece sampled `20,000,000` sentences from
`92,309,510` valid lines and skipped `142,722` too-long lines. The final extended
tokenizer has `368,687` HF tokens, adding `118,685` token strings over
XLM-R-base. It includes `256` byte fallback tokens, and `<mask>` moved from
source id `250001` to target id `368686`.

The main tokenizer audit on `20` head languages and `10` targets had `0`
failures. `29/30` audited languages reduced tokens/word. For target10, `9/10`
improved, with average delta `-0.390862`; excluding `dzo_Tibt`, target average
delta was `-0.581867`. The head sample improved for `20/20` languages, average
delta `-0.211765`.

`dzo_Tibt` remains the documented tokenizer-risk case. The main tokenizer
reduced the pilot regression substantially but still worsened `dzo_Tibt` from
`4.223938` to `5.552124` tokens/word on the audit sample. A `500`-example
sentence-level analysis shows average delta `+1.115844`, `0` byte tokens,
`0` `<unk>` tokens, and `86.981%` newly appended-token share. Therefore the
main tokenizer claim is `pass with documented risk`, not a clean win for every
target language.

### Embedding Initialization

| Method | Description | Role |
| --- | --- | --- |
| `random` | `resize_token_embeddings()` 기본 random row 사용 | Glot500-style baseline |
| `mean` | 새 lexical row를 source/global mean으로 초기화 | simple baseline |
| `fvt` | target token surface를 source tokenizer로 다시 tokenize하고 source subtoken embedding 평균 사용 | main proposed method |
| `align` | character/script-aware fallback | exploratory ablation |

Non-random 방법은 source row를 token identity 기준으로 복사하고, source `<mask>` row를
target `<mask>` id에 명시적으로 복사해야 한다. byte fallback row는 lexical row와
따로 집계한다.

Pilot FVT initialization smoke test on the pilot tokenizer passed:

- copied source identity rows: `250,002`
- initialized FVT rows: `7,334`
- byte/global-mean rows: `256`
- global-mean fallback rows: `1`
- `<mask>` remap: source `250001` -> target `257592`
- `<mask>` max absolute difference after copy: `0.0`
- LM head tied after init: `true`

Pilot zero-step MLM proxy on `5` head languages and `10` v5 target languages
provides the first positive evidence for the initialization novelty. On the v5
target group, `v5_fvt` reduced weighted NLL by `9.448385` versus `v5_random` and
by `3.423689` versus `v5_mean`. This is not a final result because the sample is
small and uses the pilot tokenizer, but it supports carrying FVT forward as the
main initialization candidate.

Main initialized checkpoints were then built on the full v5 tokenizer:

- `v5_random`: `118,685` new rows initialized by random resize.
- `v5_mean`: `118,685` new rows initialized by global/source mean.
- `v5_fvt`: `118,427` new rows initialized by source-token decomposition,
  `256` byte rows by global mean, and `2` lexical fallback rows by global mean.

All three main checkpoints preserve `250,002` source identity rows, remap
`<mask>` from `250001` to `368686` with max absolute difference `0.0`, and have
LM head tying verified as `true`.

Main zero-step MLM proxy with the full tokenizer again supports the novelty.
On the v5-target group, `v5_fvt` reduces weighted NLL by `9.626238` versus
`v5_random` and by `3.167624` versus `v5_mean`. On the head sample, `v5_fvt`
reduces weighted NLL by `6.273844` versus `v5_random` and by `1.415560` versus
`v5_mean`. The central FVT-vs-random comparison is summarized in
`docs/exp/v5/4_reporting/method_comparison_summary.md`: relative to random,
FVT reduces weighted NLL by `52.28%` on v5 target, `48.65%` on the head sample,
and `51.31%` on all measured zero-step rows. This result is an intrinsic
pre-MLM diagnostic; final claims still require matched MLM training and
downstream evaluation.

### Continued MLM

| Item | Value |
| --- | --- |
| base model | `xlm-roberta-base` |
| tokenizer | v5 extended tokenizer |
| objective | MLM |
| max length | 512 |
| learning rate | `5e-5` |
| effective batch | 384 if GPU allows |
| checkpoints | 10K step interval |
| primary comparison | `v5_random` vs `v5_fvt` |

Current paired MLM run:

- launcher: `modeling/launch_v5_random_fvt_10k.sh`
- run order: `v5_random_mlm_10k` then `v5_fvt_mlm_10k`
- GPUs: `2,3`
- max steps: `10,000`
- save steps: `10,000`
- status: `v5_random_mlm_10k` has a selected 10K checkpoint and
  `v5_fvt_mlm_10k` is running; current live snapshot is generated in
  `docs/exp/v5/3_evaluation/running_status.md` and
  `docs/exp/v5/2_training/mlm_progress_eta.md`
- launch log:
  `/home/axt/mnt2/jongha/v5_glot50010/runs/launch_logs/launch_random_fvt_10k_setsid_20260627_005616.log`

Execution note: the inherited `modeling/run.py` performs full dataset
tokenization and grouping before Trainer optimization starts. Therefore the 10K
run can spend a long time with low GPU utilization while the cache is being
materialized. This is a reproducibility cost of using the full v5 corpus rather
than a sampled debugging corpus.

## 6. Evaluation And Result Plan

Glot500에서 측정한 값들은 v5에서도 모두 측정한다. downstream metric은 선택
항목이 아니라 필수 산출물이다. 다만 selected target `10`개가 모든 downstream
dataset에 존재하지 않을 수 있으므로, 점수와 함께 task별 coverage를 반드시
보고한다.

### Required Glot500 Metrics

| ID | Metric | Score | v5 status |
| --- | --- | --- | --- |
| `pppl` | Pseudoperplexity | PPPL / MLM proxy loss | required |
| `retrieval_tatoeba` | Sentence Retrieval Tatoeba | Top-10 accuracy | required |
| `retrieval_bible` | Sentence Retrieval Bible | Top-10 accuracy | required |
| `text_classification` | Text Classification | F1 | required |
| `ner` | NER | F1 | required |
| `pos` | POS | F1 | required |
| `roundtrip_alignment` | Roundtrip Alignment | accuracy | required |

Metric-family fidelity is tracked explicitly in:

```text
docs/exp/v5/4_reporting/00_tables/table_13_metric_fidelity_matrix.md
```

This table is the report/PPT defense artifact for the claim that v5 retained
the Glot500 evaluation surface while separating measured rows,
checkpoint-pending rows, coverage-limited rows, and blocked-data rows.

PPPL fidelity note: v5 keeps the metric family but labels `PPPL_SPLIT=train`
rows as intrinsic diagnostics. The final Glot500-style held-out PPPL row is a
v5.1 requirement, not a v5 final claim.

### Current Execution Readiness

Artifact-based audit:

```text
docs/exp/v5/goal_readiness.md
```

Current verdict: main execution is underway, but final result claims are not
ready. The controlled Glot500-style subset setup, full merge, main tokenizer,
main initialization checkpoints, baseline PPPL rows, Tatoeba baseline/reference
rows, Bible baseline/reference rows, Taxi1500 baseline/reference rows, NER
`xlmr_base`/`glot500_base`, POS `xlmr_base`/`glot500_base`, and `v5_random`
available-language metric rows including POS are now measured. Main paired FVT
checkpoint rows and full downstream method comparisons remain.

Reproduction boundary: v5 is ready to execute and report a faithful
Glot500-style replay on a controlled `102` language-script subset. It is not a
full `511`-language Glot500 reproduction, and this distinction must stay visible
in the final abstract, title, and limitations.

Evaluation execution files:

- model matrix: `docs/exp/v5/3_evaluation/model_matrix.tsv`
- metric wrapper: `scripts/run_v5_eval_metric.sh`
- aggregation output:
  `docs/exp/v5/3_evaluation/09_aggregation/metric_completion.tsv`

Current tagging note: Glot500-base NER/POS and v5-random NER/POS are complete
and parsed by aggregation. Local POS uses `TRAIN_LANGS=tur_Latn` because the
materialized POS data has no `train-eng_Latn.tsv`; keep this condition visible
when comparing tagging rows.

Current local coverage snapshot:

| Task | Local materialized data / 102 | Local materialized target data / 10 | Current status |
| --- | ---: | ---: | --- |
| Pseudoperplexity | 102 | 10 | XLM-R, Glot500-base, and v5-random rows measured; v5-FVT waits for checkpoint |
| Tatoeba retrieval | 63 | 0 | locally materialized for available task languages; `xlmr_base`, `glot500_base`, and `v5_random` rows measured |
| Bible retrieval | 74 | 0 | materialized for available Glot500 Bible task languages in the current local files; local task-list membership includes 7 v5 targets and needs tail materialization repair |
| Text classification | 1 | 0 | partial local Taxi1500 only; XLM-R, Glot500-base, and v5-random rows measured |
| NER | 78 | 0 | materialized coverage audit is head-only; `xlmr_base` baseline is measured with all F1 `0.549858`, head F1 `0.621207`; `glot500_base` reference is measured with all F1 `0.627108`, head F1 `0.645915`; `v5_random` is measured with all F1 `0.544628`, head F1 `0.608020`; the actual runner also evaluated `fur_Latn`, producing one-language v5-target rows `0.459364` for XLM-R, `0.553191` for Glot500-base, and `0.560554` for v5-random |
| POS | 58 | 0 | locally materialized for available head languages; local task-list membership includes `bam_Latn` and needs tail materialization repair; `xlmr_base`, `glot500_base`, and `v5_random` measured with `TRAIN_LANGS=tur_Latn` because local POS has no `train-eng_Latn.tsv`; Glot500-base POS all F1 `0.567542`, head F1 `0.573832`; v5-random POS all F1 `0.481102`, head F1 `0.587430` |
| Roundtrip alignment | 74 | 0 | Bible-derived JSONL inputs and v5 runner are materialized; `xlmr_base`, `glot500_base`, and `v5_random` rows are measured; `v5_fvt` waits for checkpoint |

Important coverage boundary: the selected target10 has raw text for
pseudoperplexity. After correcting the task-list flag interpretation, official
Glot500 local task-list membership is partial rather than zero: Bible includes
`rap_Latn`, `krc_Cyrl`, `kjb_Latn`, `bam_Latn`, `quw_Latn`, `mad_Latn`, and
`dzo_Tibt`; NER includes `fur_Latn`; POS includes `bam_Latn`. The existing local
coverage/materialization files undercount these tail rows because they treated
the task-list head/tail flag as availability. Therefore target10 downstream
improvement should not be used as a main claim until tail materialization/eval
is repaired; downstream evidence should be reported for available languages with
explicit head/all and coverage-limited target notes.

Bible and roundtrip are retained as required Glot500 metric families, but their
current status is explicit rather than omitted. Bible retrieval has an
inherited evaluator and now has local Bible-style parallel files for `74/102`
available language-scripts under
`evaluation/download_data/download/retrieval_bible`; `xlmr_base` and
`glot500_base` rows are measured, and `v5_random` is also measured after the
10K random checkpoint; `v5_fvt` still waits for its matched checkpoint.
Tatoeba retrieval is likewise measured for `v5_random` over the available
language set, with `v5_fvt` still checkpoint-gated.
Roundtrip now has Bible-derived JSONL inputs for `74/102`
available language-scripts under
`evaluation/download_data/download/roundtrip_alignment` and a v5 runner at
`evaluation/round-trip/evaluate_roundtrip_v5.py`; `xlmr_base` and
`glot500_base` rows are measured, and `v5_random` is also measured; `v5_fvt`
still waits for its matched checkpoint.

Currently measured baseline rows:

| Metric | Model | Group | Score | Value | Source |
| --- | --- | --- | --- | ---: | --- |
| PPPL | `xlmr_base` | v5 target / tail | weighted PPPL | 61.980216 | `09_aggregation/main_head_tail_all.tsv` |
| PPPL | `xlmr_base` | head | weighted PPPL | 8.117338 | `09_aggregation/main_head_tail_all.tsv` |
| PPPL | `xlmr_base` | all | weighted PPPL | 9.986271 | `09_aggregation/main_head_tail_all.tsv` |
| PPPL | `glot500_base` | v5 target / tail | weighted PPPL | 15.102934 | `09_aggregation/main_head_tail_all.tsv` |
| PPPL | `glot500_base` | head | weighted PPPL | 10.213100 | `09_aggregation/main_head_tail_all.tsv` |
| PPPL | `glot500_base` | all | weighted PPPL | 10.640353 | `09_aggregation/main_head_tail_all.tsv` |
| Tatoeba retrieval | `xlmr_base` | head | Top-10 accuracy | 0.656309 | `09_aggregation/main_head_tail_all.tsv` |
| Tatoeba retrieval | `xlmr_base` | all available | Top-10 accuracy | 0.566067 | `09_aggregation/main_head_tail_all.tsv` |
| Tatoeba retrieval | `glot500_base` | head | Top-10 accuracy | 0.743755 | `09_aggregation/main_head_tail_all.tsv` |
| Tatoeba retrieval | `glot500_base` | all available | Top-10 accuracy | 0.706649 | `09_aggregation/main_head_tail_all.tsv` |
| Tatoeba retrieval | `v5_random` | head | Top-10 accuracy | 0.700285 | `09_aggregation/main_head_tail_all.tsv` |
| Tatoeba retrieval | `v5_random` | all available | Top-10 accuracy | 0.610353 | `09_aggregation/main_head_tail_all.tsv` |
| Bible retrieval | `xlmr_base` | head / all available | Top-10 accuracy | 0.381153 | `09_aggregation/main_head_tail_all.tsv` |
| Bible retrieval | `glot500_base` | head / all available | Top-10 accuracy | 0.509356 | `09_aggregation/main_head_tail_all.tsv` |
| Bible retrieval | `v5_random` | head / all available | Top-10 accuracy | 0.328019 | `09_aggregation/main_head_tail_all.tsv` |
| Text classification | `xlmr_base` | head / all available | macro-F1 | 0.592876 | `09_aggregation/main_head_tail_all.tsv` |
| Text classification | `glot500_base` | head / all available | macro-F1 | 0.743338 | `09_aggregation/main_head_tail_all.tsv` |
| Text classification | `v5_random` | head / all available | macro-F1 | 0.702956 | `09_aggregation/main_head_tail_all.tsv` |
| NER | `xlmr_base` | all available | F1 | 0.549858 | `09_aggregation/main_head_tail_all.tsv` |
| NER | `xlmr_base` | head | F1 | 0.621207 | `09_aggregation/main_head_tail_all.tsv` |
| NER | `xlmr_base` | v5-target actual intersection | F1 | 0.459364 | `09_aggregation/main_head_tail_all.tsv` |
| NER | `glot500_base` | all available | F1 | 0.627108 | `09_aggregation/main_head_tail_all.tsv` |
| NER | `glot500_base` | head | F1 | 0.645915 | `09_aggregation/main_head_tail_all.tsv` |
| NER | `glot500_base` | v5-target actual intersection | F1 | 0.553191 | `09_aggregation/main_head_tail_all.tsv` |
| NER | `v5_random` | all available | F1 | 0.544628 | `09_aggregation/main_head_tail_all.tsv` |
| NER | `v5_random` | head | F1 | 0.608020 | `09_aggregation/main_head_tail_all.tsv` |
| NER | `v5_random` | v5-target actual intersection | F1 | 0.560554 | `09_aggregation/main_head_tail_all.tsv` |
| POS | `xlmr_base` | all available | F1 | 0.481336 | `09_aggregation/main_head_tail_all.tsv` |
| POS | `xlmr_base` | head | F1 | 0.571446 | `09_aggregation/main_head_tail_all.tsv` |
| POS | `glot500_base` | all available | F1 | 0.567542 | `09_aggregation/main_head_tail_all.tsv` |
| POS | `glot500_base` | head | F1 | 0.573832 | `09_aggregation/main_head_tail_all.tsv` |
| POS | `v5_random` | all available | F1 | 0.481102 | `09_aggregation/main_head_tail_all.tsv` |
| POS | `v5_random` | head | F1 | 0.587430 | `09_aggregation/main_head_tail_all.tsv` |
| Roundtrip alignment | `xlmr_base` | head / all available | accuracy | 0.185300 | `09_aggregation/main_head_tail_all.tsv` |
| Roundtrip alignment | `glot500_base` | head / all available | accuracy | 0.205189 | `09_aggregation/main_head_tail_all.tsv` |
| Roundtrip alignment | `v5_random` | head / all available | accuracy | 0.190300 | `09_aggregation/main_head_tail_all.tsv` |

### Main Result Table Template

| Metric | XLM-R-base tail | Glot500-base tail | v5-random tail | v5-fvt tail | XLM-R-base head | Glot500-base head | v5-random head | v5-fvt head | XLM-R-base all | Glot500-base all | v5-random all | v5-fvt all |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Pseudoperplexity diagnostic | 61.980216 | 15.102934 | 39.222875 | waiting or explicit diagnostic | 8.117338 | 10.213100 | 18.726452 | waiting or explicit diagnostic | 9.986271 | 10.640353 | 20.138927 | waiting or explicit diagnostic |
| Tatoeba Retrieval Top-10 | N/A, 0/10 coverage | N/A, 0/10 coverage | N/A, 0/10 coverage | N/A, 0/10 coverage | 0.656309 | 0.743755 | 0.700285 | waiting checkpoint | 0.566067 | 0.706649 | 0.610353 | waiting checkpoint |
| Bible Retrieval Top-10 | pending tail repair | pending tail repair | pending tail repair | pending tail repair | 0.381153 | 0.509356 | 0.328019 | waiting checkpoint | 0.381153 | 0.509356 | 0.328019 | waiting checkpoint |
| Text Classification F1 | N/A, 0/10 coverage | N/A, 0/10 coverage | N/A, 0/10 coverage | N/A, 0/10 coverage | 0.592876 | 0.743338 | 0.702956 | waiting checkpoint | 0.592876 | 0.743338 | 0.702956 | waiting checkpoint |
| NER F1 | 0.459364, `fur_Latn` only | 0.553191, `fur_Latn` only | 0.560554, `fur_Latn` only | waiting checkpoint | 0.621207 | 0.645915 | 0.608020 | waiting checkpoint | 0.549858 | 0.627108 | 0.544628 | waiting checkpoint |
| POS F1 | pending tail repair | pending tail repair | pending tail repair | pending tail repair | 0.571446 | 0.573832 | 0.587430 | waiting checkpoint | 0.481336 | 0.567542 | 0.481102 | waiting checkpoint |
| Roundtrip Alignment Acc. | N/A, 0/10 coverage | N/A, 0/10 coverage | N/A, 0/10 coverage | N/A, 0/10 coverage | 0.185300 | 0.205189 | 0.190300 | waiting checkpoint | 0.185300 | 0.205189 | 0.190300 | waiting checkpoint |

Interim random-checkpoint interpretation: `v5_random` is useful as a sanity
row, not as the final method claim. On target10 PPPL it improves over XLM-R
(`39.222875` vs. `61.980216`) but remains far behind the external
Glot500-base reference (`15.102934`). On head/all PPPL it is worse than both
XLM-R and Glot500-base. Downstream is mixed: `v5_random` is above XLM-R but
below Glot500-base on Tatoeba and Taxi1500, below both references on Bible
retrieval, close to XLM-R on all-language POS, above both references on head
POS, and between XLM-R and Glot500-base on Roundtrip. This pattern is exactly
why the matched `v5_fvt` checkpoint is the decisive test: random initialization
plus short continued MLM does not by itself establish the vocabulary-extension
method claim.

### Metric Completion Checklist

| Metric | XLM-R-base | Glot500-base | v5-random | v5-fvt | Coverage file | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Pseudoperplexity | measured | measured | measured | waiting for checkpoint | `00_coverage/coverage_pseudoperplexity.tsv` | partial; XLM-R, Glot500-base, and v5-random values copied from `09_aggregation/main_head_tail_all.tsv`; FVT waits for checkpoint |
| Tatoeba Retrieval Top-10 | measured | measured | measured | waiting for checkpoint | `00_coverage/coverage_retrieval_tatoeba.tsv` | partial; baseline/reference and v5-random rows measured, no local v5 target membership found |
| Bible Retrieval Top-10 | measured | measured | measured | waiting for checkpoint | `00_coverage/coverage_retrieval_bible.tsv` | partial; baseline/reference and v5-random rows measured over 74/102 local materialized rows; local v5 target membership exists but needs tail materialization repair; FVT waits for checkpoint |
| Text Classification F1 | measured | measured | measured | waiting for checkpoint | `00_coverage/coverage_text_classification.tsv` | partial; local coverage is English-only head data |
| NER F1 | measured | measured | measured | waiting for checkpoint | `00_coverage/coverage_ner.tsv` | partial; local coverage audit is `78/102`; local v5 target membership includes `fur_Latn`, and the actual runner produced one-target rows for XLM-R, Glot500-base, and v5-random |
| POS F1 | measured | measured | measured | waiting for checkpoint | `00_coverage/coverage_pos.tsv` | partial; local coverage is `58/102`; local v5 target membership includes `bam_Latn` but local tail materialization needs repair; local POS rows use `TRAIN_LANGS=tur_Latn` |
| Roundtrip Alignment Acc. | measured | measured | measured | waiting for checkpoint | `00_coverage/coverage_roundtrip_alignment.tsv` | partial; baseline/reference and v5-random rows measured over 74/102; current local target materialization needs repair/audit; FVT waits for checkpoint |

### Pending Result Registry

This registry distinguishes unresolved result slots from explicit blockers.

| Label | Meaning | Promotion gate | Final-report wording |
| --- | --- | --- | --- |
| `waiting for checkpoint` | metric cannot run because the paired v5 model path for that row does not exist yet | the missing selected checkpoint is written under `2_training/05_checkpoint_selection/` and preflight is ready | pending execution, not a result |
| `running` | job is active but final metric file is not parseable yet | completed raw output exists and `scripts/aggregate_v5_metrics.py` parses it | live status only |
| `blocked-data` | metric family is retained, but local data or runner artifact is missing | coverage audit changes from `0` and a runnable evaluator command exists | explicit limitation row |
| `N/A, 0/10 coverage` | the selected target10 is absent from the materialized task data | coverage file shows at least one selected target language with data | coverage-limited, not negative performance |
| `pending tail repair` | local task-list membership exists but current local materialization undercounted tail rows | repaired materialization/eval produces target-language rows | not yet a measured downstream result |
| unresolved value | value is expected from a future measured artifact | replaced by aggregation output or one of the labels above | do not use in final numeric claim |

### Initialization Result Table Template

The required final method gate is the matched 10K `v5_random`/`v5_fvt`
comparison. Longer-budget checkpoints can be reported only as optional
ablation evidence if they are trained later; they are not required for the v5
final report/PPT package.

| Method | zero-step tail MLM | zero-step head MLM | matched 10K tail PPPL/MLM | optional longer-budget PPPL | new-row init | byte rows | status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| random | main target NLL 18.411756 | main head NLL 12.895301 | target PPPL 39.222875 | optional ablation | 118,685 random | 256 | main zero-step done; 10K selected; diagnostic PPPL/downstream rows parsed |
| mean | main target NLL 11.953142 | main head NLL 8.037017 | optional ablation | optional ablation | 118,685 mean | 256 | main zero-step done |
| fvt | main target NLL 8.785518 | main head NLL 6.621457 | waiting checkpoint | optional ablation | 118,427 FVT + 2 fallback | 256 | main zero-step done; 10K MLM running |
| align | optional | optional | optional ablation | optional ablation | optional | optional | exploratory ablation |

### V5 Target Subset Coverage Table

This table must be regenerated from local coverage after downstream data
download/materialization. The current local audit shows no selected-target
downstream materialization outside raw-text PPPL.

| Task | Current local selected-target coverage | Missing selected targets | Note |
| --- | --- | --- | --- |
| Pseudoperplexity | 10/10 | none | raw Glot500 text exists |
| Bible retrieval | 0/10 Glot500 task coverage | target languages outside Bible task flags | optional target-only auxiliary Bible eval must be labeled separately |
| NER | 0/10 local materialized; 1 actual evaluated target in `xlmr_base` output | materialized target coverage missing; actual output includes only `fur_Latn` | coverage-limited; do not generalize to target10 |
| POS | 0/10 local | all target languages locally missing | coverage-limited after data materialization |
| Tatoeba retrieval | 0/10 local | all target languages locally missing | verify upstream after download |
| Taxi1500 | 0/10 local | all target languages locally missing | local data currently English only |
| Roundtrip alignment | 0/10 local | all target languages locally missing | baseline/reference rows measured for available non-target languages; target10 parallel data still missing |

### Additional Diagnostic Figures

- sentence vector similarity across parallel/related sentences
- same-language clustering
- UMAP/t-SNE by head/tail/target group
- embedding row norm distribution
- training curves by initialization method

Currently generated measured figures:

- tokenizer fertility delta:
  `docs/exp/v5/4_reporting/01_figures/generated/figure_02_tokenizer_fertility_delta.png`
- zero-step initialization comparison:
  `docs/exp/v5/4_reporting/01_figures/generated/figure_03_zero_step_initialization.png`
- evaluation coverage boundary:
  `docs/exp/v5/4_reporting/01_figures/generated/figure_05_evaluation_coverage.png`

## 7. Report Composition

Final report sections:

1. Introduction
2. Related Work and Positioning
3. Scope and Reproduction Boundary
4. Data and v5 Language Selection
5. Tokenizer Extension Method
6. Embedding Initialization Methods
7. MLM Continued Pretraining
8. Evaluation Setup
9. Results
10. Analysis
11. Limitations
12. Conclusion

Presentation flow:

1. Motivation
2. Reproduction setup
3. Tokenizer and initialization method
4. Experiment matrix
5. Required Glot500 metric results
6. Initialization analysis
7. Coverage and limitations
8. Conclusion

## 8. Claims

Allowed if measured results support them:

- We reproduce the main Glot500 training/evaluation pattern in a controlled
  subset.
- FVT/source-token decomposition initialization improves zero-step target MLM
  proxy compared with random resize.
- If matched 10K train-source PPPL diagnostic supports it, the initialization
  advantage survives continued MLM as an intrinsic diagnostic under the
  controlled v5 budget. Held-out PPPL remains a v5.1 correction requirement.
- If available downstream rows support it, the initialization effect transfers
  beyond intrinsic MLM metrics; otherwise keep downstream transfer as mixed,
  coverage-limited, or negative.
- Some downstream tasks are coverage-limited, so results must distinguish
  head/tail/all from v5-target subset.

Avoid:

- Do not claim full 511-language Glot500 reproduction.
- Do not call v5 `PPPL_SPLIT=train` rows held-out test PPPL.
- Do not claim all downstream tasks cover all selected target languages.
- Do not claim embedding initialization alone explains all gains after long MLM.
- Do not compare against `cis-lmu/glot500-base` as if compute/data scale were equal.

## References

- Ayyoob Imani et al. 2023. [Glot500: Scaling Multilingual Corpora and Language
  Models to 500 Languages](https://aclanthology.org/2023.acl-long.61/). ACL 2023.
- Glot500 official code: <https://github.com/cisnlp/Glot500>
- Atsuki Yamaguchi, Aline Villavicencio, Nikolaos Aletras. 2026.
  [How Can We Effectively Expand the Vocabulary of LLMs with 0.01GB of Target
  Language Text?](https://aclanthology.org/2026.cl-1.9/). Computational
  Linguistics 52(1):295-330. DOI `10.1162/coli.a.581`. arXiv preprint:
  <https://arxiv.org/abs/2406.11477>.
- Yamaguchi et al. official code: <https://github.com/gucci-j/lowres-cve>

## Artifact Pointers

- Plan: `docs/exp/v5/Plan.md`
- Current status and folder map: `docs/exp/v5/README.md`
- data processing note: `docs/exp/v5/0_tokenizer/dataset_processing.md`
- selected target manifest:
  `docs/exp/v5/0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv`
- stats CSV:
  `docs/exp/v5/0_tokenizer/miscellaneous/languages_stats_glot50010_xlmr100.csv`
- merge dry-run report:
  `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.report.json`
- reporting table/figure source map:
  `docs/exp/v5/4_reporting/00_tables/source_map.md`
- generated figure manifest:
  `docs/exp/v5/4_reporting/01_figures/generated/figure_manifest.tsv`
- checkpoint selection plan:
  `docs/exp/v5/2_training/05_checkpoint_selection/selection_plan.md`
- next-run operational runbook:
  `docs/exp/v5/3_evaluation/next_runbook.md`
- standalone paper-style draft:
  `docs/exp/v5/4_reporting/03_final_report/paper_draft.md`
- contribution summary:
  `docs/exp/v5/4_reporting/03_final_report/contribution_summary.md`
