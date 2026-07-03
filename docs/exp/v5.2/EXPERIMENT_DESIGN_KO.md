# v5.2 실험 설계

작성일: 2026-06-28

## 한 줄 설계

```text
v5.2 = Glot500-style 92 XLM-R-seen replay + 7 XLM-R-unseen downstream-capable tail targets
```

v5.2는 실제 재시작 run이다. 기본 방법은 Glot500 논문을 따른다. 즉 mixed corpus로
SentencePiece unigram tokenizer를 다시 학습하고, XLM-R SentencePiece vocabulary 뒤에
새 piece를 append하는 Glot500식 vocab injection을 사용한다. main ablation은 tokenizer가
아니라 새 embedding row initialization이다.

## 확정 사항

| Item | Decision |
| --- | --- |
| corpus | `92` XLM-R-seen/head + `7` XLM-R-unseen/tail target |
| target definition | XLM-R-unseen tail + downstream 가능한 최소 corpus band |
| target language count | 7 |
| tokenizer | Glot500-style SentencePiece unigram + append-only vocab injection |
| sampling | language sampling `alpha = 0.3` |
| Yamaguchi vocabulary method | main에서 제외, 추가 실험/appendix로 이동 |
| main comparison axis | same corpus, same tokenizer, same MLM schedule, different initialization |
| checkpoint policy | 8h run 동안 약 5-8개 checkpoint 생성 |
| downstream policy | 중간 checkpoint마다 가능한 task를 평가하고 table/log 갱신 |

## Target7

task overlap을 최대화한 최종 target7이다.

| language_script | language full name | region | new_length | Covered tasks |
| --- | --- | --- | ---: | --- |
| `dtp_Latn` | Kadazan Dusun | Southeast Asia | 48,468 | Tatoeba, Bible, Roundtrip, Taxi1500, Embedding similarity |
| `xav_Latn` | Xavánte | South America | 31,765 | Bible, Roundtrip, POS, Taxi1500 |
| `bam_Latn` | Bambara | West Africa | 32,150 | Bible, Roundtrip, POS, Taxi1500 |
| `csb_Latn` | Kashubian | Europe | 33,743 | Tatoeba, NER, Embedding similarity |
| `ile_Latn` | Interlingue | Constructed/Europe | 40,984 | Tatoeba, Embedding similarity |
| `lij_Latn` | Ligurian | Europe | 42,447 | NER, POS |
| `fur_Latn` | Friulian | Europe | 30,052 | NER |

총 21개 task slot을 unique 7개 언어로 압축한다. strict `<=10k` corpus 언어에는
downstream membership이 없으므로, 논문/발표에서는 아래처럼 설명한다.

```text
We define the target set as XLM-R-unseen tail languages in the smallest corpus
band that still supports downstream evaluation.
```

## Initialization Ablation

모든 run은 같은 tokenizer와 같은 MLM corpus를 사용한다.

| model_key | Initialization | Role |
| --- | --- | --- |
| `v52_random` | HF-style random row initialization | Glot500-style baseline |
| `v52_mean` | lexical source embedding global mean | stable simple baseline |
| `v52_fvt` | target token surface를 XLM-R tokenizer로 재분해한 source subtoken mean | main candidate |
| `v52_weighted_fvt` | FVT source subtoken mean을 subtoken surface length로 가중 평균 | FVT refinement ablation |
| `v52_family_mean` | 새 token의 corpus provenance가 가리키는 language family의 source-token 평균 | family-aware prior ablation |

기대하는 핵심 table은 `fvt`가 가장 좋은지 확인하는 것이다. 단, 문서에서는 결과가 나오기
전까지 `fvt should be best`가 아니라 `fvt is the primary hypothesis`로 쓴다. 기존
`align`은 v5.2에서 FVT와 byte-identical하게 collapse되었으므로 5-way 독립 ablation에서는
제외하고 historical continuity row로만 취급한다.

## Training/Evaluation Contract

| Phase | Output |
| --- | --- |
| target preparation | `docs/exp/v5.2/0_tokenizer/miscellaneous/glot5007_selected_manifest.tsv` |
| corpus merge | `docs/exp/v5.2/0_tokenizer/merge/Glot500_v52_glot5007_xlmr100.manifest.tsv` |
| tokenizer training | `/home/axt/mnt2/jongha/v5.2_glot5007/tokenization/output/Glot500_extended_spm` |
| initializer build | `/home/axt/mnt2/jongha/v5.2_glot5007/initialized_models/v5_{random,mean,fvt,weighted_fvt,family_mean}` |
| MLM run | `/home/axt/mnt2/jongha/v5.2_glot5007/runs/v52_{method}_mlm_8h` |
| checkpoint eval | PPPL, retrieval, NER/POS where materialized, Roundtrip/Taxi where generated |
| logging | table cells are updated per checkpoint, final claim only after paired rows exist |

## Glot500 Hyperparameter Alignment

v5.2는 full 480K-step reproduction이 아니라 8시간 initialization ablation이다. 그래도
core MLM recipe는 Glot500 논문에 맞춘다.

| Item | v5.2 |
| --- | --- |
| base model | `xlm-roberta-base` |
| objective | MLM |
| initial learning rate | `5e-5` |
| Adam betas | `(0.9, 0.999)` |
| effective batch per method step | `384` |
| max sequence length | `512` |
| language sampling | `alpha = 0.3` |
| checkpoint interval | `1000` steps, scaled down from paper's `10K` for 8h run |

## Main Result Tables

### Table A. Data And Coverage

| task | target languages | status |
| --- | --- | --- |
| Tatoeba retrieval | `csb_Latn`, `dtp_Latn`, `ile_Latn` | ready |
| Bible retrieval | `dtp_Latn`, `xav_Latn`, `bam_Latn` | materializable |
| Roundtrip alignment | `dtp_Latn`, `xav_Latn`, `bam_Latn` | after Bible materialization |
| NER | `csb_Latn`, `lij_Latn`, `fur_Latn` | ready |
| POS | `xav_Latn`, `bam_Latn`, `lij_Latn` | UD split/materialization needed |
| Taxi1500 | `dtp_Latn`, `xav_Latn`, `bam_Latn` | generation needed |
| Embedding similarity | `csb_Latn`, `dtp_Latn`, `ile_Latn` | ready |

### Table B. Initialization Comparison

| method | zero-step MLM/PPPL | checkpoint PPPL | Tatoeba | Bible | NER | POS | note |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| random |  |  |  |  |  |  | baseline |
| mean |  |  |  |  |  |  | simple init |
| fvt |  |  |  |  |  |  | main hypothesis |
| weighted_fvt |  |  |  |  |  |  | length-weighted FVT refinement |
| family_mean |  |  |  |  |  |  | family-aware prior |

### Table C. Checkpoint Log

| checkpoint | method | step | elapsed | train_loss | PPPL | downstream_done | promoted_claim |
| --- | --- | ---: | --- | ---: | ---: | --- | --- |

## Yamaguchi Position

Yamaguchi-style low-resource vocabulary expansion은 main axis에서 뺀다. v5.2 main은
Glot500식 vocab injection을 고정한 뒤 initialization만 비교한다. Yamaguchi는 같은
target7에 대해 별도 appendix/추가 실험으로 작은 table만 만든다.
