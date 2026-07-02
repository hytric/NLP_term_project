# Third Try Plan: Target10 Performance Model

작성일: 2026-06-12

## Objective

기존 target10 low-resource 언어에 대해 실제 downstream 성능이 개선되는 XLM-R-base adaptation model을 만든다. 목표는 "새 token을 붙이면 tokenizer가 좋아진다"가 아니라, **high-resource replay와 low-resource target을 동시에 사용한 id-preserving vocabulary extension + multi-init continued pretraining이 target10 downstream 성능을 seed-stable하게 개선하는가**를 검증하는 것이다.

## Non-Negotiable Rules

1. XLM-R의 기존 vocab id와 special token id를 보존한다.
2. 새 token은 항상 뒤에 append한다.
3. Main run은 full fine-tuning MLM이다. LoRA는 ablation이다.
4. Main run은 high-resource replay/control + target10 low-resource mixture를 쓴다. target-only는 ablation이다.
5. Main matrix는 여러 embedding initialization method를 포함한다. random init은 required baseline이다.
6. Model-dependent 비교는 3개 이상 seed를 사용한다.
7. Evaluation은 target10 downstream 개선까지 포함해야 한다.
8. 최종 주장은 target10 성능 개선, seed stability, high-resource control을 분리해서 쓴다.

## Stage 00: Scope Freeze

상태: 완료.

확정한 것:

- Base: `xlm-roberta-base`
- Scale baseline: 사용하지 않음
- Main target set: target10 전체 (`acu`, `ake`, `bsn`, `chr`, `cop`, `kbh`, `nhg`, `oji`, `syr`, `usp`)
- Coptic/Syriac: main experiment 포함
- True high-resource web replay: GlotCC-V1 `eng-Latn`, `deu-Latn`, `jpn-Jpan`, `kor-Hang`
- Domain-matched high-resource control: Bible English, German, Japanese, Korean
- Reference model: `cis-lmu/glot500-base`는 직접 baseline이 아니라 related-work/reference로 사용

Output:

- `00_scope/current_dataset_inventory.md`
- `00_scope/high_resource_inventory.tsv`
- `00_scope/high_resource_dataset_check.md`
- `01_data/high_resource_web_corpus_plan.md`
- `/home/axt/mnt2/jongha/third_try/high_resource/glotcc/high_resource_glotcc_manifest.tsv`

Gate:

- target10 전체가 main low-resource target으로 표시되어야 한다.
- Coptic/Syriac가 main experiment로 표시되어야 한다.
- high-resource replay/control set과 mixture rule이 명확해야 한다.

## Stage 01: Data Collection And Split

상태: 진행 중.

Glot500과 같은 split 원칙을 사용한다.

- 각 language-script에서 dev/test 각각 1000 sentence-prime reserve.
- Bible parallel verse가 있으면 dev/test 각각 500 verse reserve.
- Train에는 dev/test/final test를 절대 넣지 않는다.
- 각 language-script의 sentence count와 license/source를 기록한다.
- Target10 V2 clean split을 기본 low-resource source로 사용한다.
- High-resource web replay는 materialized GlotCC-V1 sample을 사용한다.
- Bible high-resource는 domain-matched replay/control로만 사용한다.

Materialized high-resource web replay:

| Config | Lines | Docs | Status |
| --- | ---: | ---: | --- |
| `eng-Latn` | 200000 | 11274 | PASS |
| `deu-Latn` | 200000 | 9573 | PASS |
| `jpn-Jpan` | 200000 | 20555 | PASS |
| `kor-Hang` | 200000 | 14732 | PASS |

Output:

- `01_data/results.md`
- `01_data/corpus_manifest.tsv`
- `01_data/split_manifest.tsv`
- `01_data/bible_parallel_manifest.tsv`
- `01_data/high_resource_manifest.tsv`
- `01_data/mlm_mixture_manifest.tsv`
- `01_data/leakage_audit.tsv`

Gate:

- tail language별 train/dev/test 수가 명확해야 한다.
- high-resource web replay와 target10 low-resource가 같은 MLM mixture manifest에 있어야 한다.
- 30,000 sentence-prime 미만인 language는 main run 포함 여부를 별도 표시해야 한다.

## Stage 02: XLM-R Baseline Audit

Main run 전에 XLM-R-B만 측정한다.

Metrics:

- tokens/word
- tokens/character
- single-character token ratio
- unk rate
- PPPL on held-out test
- sentence retrieval Bible/Tatoeba where available
- roundtrip alignment where parallel data allows
- zero-shot text classification/NER/POS where datasets exist

Output:

- `02_baseline/results.md`
- `02_baseline/tokenization_metrics.tsv`
- `02_baseline/baseline_eval.tsv`
- `02_baseline/tokenization_samples.md`

Gate:

- target10별 baseline table이 있어야 한다.

## Stage 03: Glot500-Style Tokenizer Extension

Glot500 절차:

1. Multilingual train corpus에서 SentencePiece unigram auxiliary tokenizer를 학습한다.
2. Sampling은 language-script별 multinomial distribution, alpha `0.3`을 사용한다.
3. Head language는 tail minimum 수준으로 cap한다.
4. Auxiliary vocab에서 XLM-R에 이미 있는 piece를 제거한다.
5. 진짜 new piece만 XLM-R vocabulary 뒤에 append한다.
6. XLM-R special token id와 기존 token id가 동일한지 audit한다.

Main run의 auxiliary vocab size는 1 GPU 며칠 예산과 target10 downstream 성능을 기준으로 선택한다. `8k/16k/32k`는 기존 evidence를 활용한 후보 grid이며, Glot500의 `250k`는 원 논문 reference/deviation으로만 기록한다.

Fallback ablation을 별도로 추가한다.

| Variant | SentencePiece setting | 목적 |
| --- | --- | --- |
| `char_fallback_or_coverage` | `byte_fallback=false`, high `character_coverage` | 학습 corpus에 등장한 문자를 직접 vocab/char 단위로 커버할 때의 fertility와 `<unk>` 위험 확인 |
| `byte_fallback` | `byte_fallback=true`, `character_coverage<1` | unseen character를 `<unk>`로 잃지 않는 대신 byte token 증가가 생기는지 확인 |

이 비교는 main selected tokenizer를 대체하는 claim이 아니라 tokenizer ablation이다. 같은 train split, 같은 vocab budget, 같은 sampling으로 학습하고 아래 지표를 비교한다.

- tokens/word
- tokens/character
- single-character token ratio
- byte-fallback token ratio
- `<unk>` rate
- exact string recoverability
- held-out script coverage

Output:

- `03_tokenizer/results.md`
- `03_tokenizer/merge_report.json`
- `03_tokenizer/id_preservation_audit.tsv`
- `03_tokenizer/tokenization_before_after.tsv`
- `03_tokenizer/fallback_ablation.tsv`
- `03_tokenizer/tokenization_samples.md`

Gate:

- 기존 XLM-R token id가 100% 보존되어야 한다.
- 새 token은 모두 base vocab size 이후 id를 가져야 한다.
- Fallback ablation은 main tokenizer 선택과 분리해서 보고해야 한다.

## Stage 04: Multi-Method Model Initialization

Main run:

- XLM-R-B model을 load한다.
- tokenizer vocab size에 맞게 input embedding과 LM head를 resize한다.
- 기존 rows는 그대로 copy한다.
- 새 rows는 random, mean, fvt, align, focus 등 여러 방법으로 초기화한다.
- model architecture는 XLM-R-base와 동일하고 embedding/vocab rows만 증가해야 한다.

Required init candidates:

- random
- mean
- fvt/source-tokenizer mean
- align
- focus, feasible if implementation is stable

Output:

- `04_init/results.md`
- `04_init/init_candidate_summary.tsv`
- `04_init/row_copy_audit.tsv`
- `04_init/init_method_reports/`

Gate:

- Base rows drift가 0이어야 한다.
- New row count가 tokenizer append count와 같아야 한다.
- Random plus at least one non-random init candidate가 준비되어야 한다.

## Stage 05: Multilingual Continued Pretraining

Target10 main training config:

| Item | Value |
| --- | --- |
| Objective | MLM |
| Optimizer | Adam |
| Betas | `(0.9, 0.999)` |
| Initial LR | `5e-5` |
| Batch | 384 samples per step, or gradient-accumulated equivalent |
| Sequence length | 512 tokens |
| Sampling | high-resource + low-resource mixture, alpha `0.3` or Stage 00 contract |
| Fine-tuning | full model |
| Checkpointing | every 10k steps |
| Selection | dev downstream/representation average early stopping |
| Seeds | at least 3 for final model-dependent comparisons |
| GPU | use GPU 3 only via `CUDA_VISIBLE_DEVICES=3` |

Compute가 부족하면 exact batch/step을 gradient accumulation 또는 scaled-down budget으로 바꿀 수 있지만, 반드시 deviation table에 남긴다.

Output:

- `05_mlm/results.md`
- `05_mlm/training_config.json`
- `05_mlm/checkpoint_metrics.tsv`
- `05_mlm/deviation_from_protocol.tsv`
- `05_mlm/seed_summary.tsv`
- `05_mlm/init_method_mlm_summary.tsv`

Gate:

- Main model은 full fine-tuning이어야 한다.
- High-resource와 low-resource가 동시에 mixture에 있어야 한다.
- Final candidate는 3개 이상 seed로 평가해야 한다.
- Target-only run은 main이 아니라 ablation으로만 기록한다.

## Stage 06: Target10 Evaluation Suite

Target10 downstream 개선을 최종 기준으로 둔다. Glot500-style PPPL/retrieval/alignment는 representation evidence로 함께 쓴다.

| Task | Metric | Protocol |
| --- | --- | --- |
| PPPL | pseudo-perplexity | held-out test, mask tokens one by one |
| Roundtrip Alignment | accuracy | SimAlign, layer 8, Bible parallel test, 5 intermediate-language samples |
| Sentence Retrieval Tatoeba | top10 accuracy | avg word embeddings, layer 8, cosine |
| Sentence Retrieval Bible | top10 accuracy | 500 English-aligned Bible test sentences |
| Text Classification | F1 | Taxi1500, train English, zero-shot target |
| NER | F1 | WikiANN, train English, zero-shot target |
| POS | F1 | UD v2.11, train English, zero-shot target |

Output:

- `06_eval/results.md`
- `06_eval/pppl.tsv`
- `06_eval/roundtrip.tsv`
- `06_eval/sentence_retrieval.tsv`
- `06_eval/text_classification.tsv`
- `06_eval/ner.tsv`
- `06_eval/pos.tsv`
- `06_eval/target10_downstream.tsv`
- `06_eval/target10_seed_summary.tsv`
- `06_eval/target10_summary.tsv`
- `06_eval/high_resource_control_summary.tsv`

Gate:

- XLM-R-B vs third_try model의 target10 평균과 language별 score가 있어야 한다.
- Seed 3개 이상 평균/분산이 있어야 한다.
- Task별 available language count를 반드시 표시한다.

## Stage 07: Main Claim Synthesis

Main result는 아래 형식으로만 쓴다.

- Target10에서는 어떤 downstream task에서 XLM-R-B를 이겼는가.
- 3개 이상 seed에서 개선이 안정적인가.
- High-resource replay/control 성능은 어느 정도 보존되는가.
- Tokenization 개선과 downstream 개선이 같은 방향인가.
- Embedding initialization method별 차이가 downstream까지 이어지는가.

Output:

- `07_main_claim/results.md`
- `07_main_claim/evidence_table.tsv`
- `07_main_claim/allowed_claims.md`
- `07_main_claim/blocked_claims.md`

Gate:

- tokenizer-only claim과 downstream claim을 분리해야 한다.
- seed-1 pilot 결과를 final model claim처럼 쓰면 안 된다.
- ablation 결과를 main result처럼 쓰면 안 된다.

## Stage 08: Ablation Study Packaging

기존 `first_try`와 `second_try` 결과를 여기로 재배치한다.

Ablation axes:

- CPT-only vs vocab extension
- vocab size: 8k/16k/32k and optional Glot500-style 250k reference
- fallback: character fallback/coverage vs byte fallback
- init: random/mean/fvt/align/focus
- training: full MLM vs LoRA
- data: multilingual replay vs target-only
- objective/repair: added-token curriculum, new-row-only, KL/replay
- downstream proxy vs target10 final downstream task

Output:

- `08_ablation/results.md`
- `08_ablation/ablation_matrix.tsv`
- `08_ablation/second_try_mapping.tsv`
- `08_ablation/negative_diagnostic_summary.md`

Gate:

- 기존 실험은 "target10 final model result"가 아니라 "ablation / failure analysis"로 표시되어야 한다.

## Stage 09: Extension Case Packaging

Target10 main run이 끝난 뒤 같은 protocol을 target10 밖 추가 언어에 적용할지 결정한다.

이 단계의 역할은 main result가 아니라 optional protocol transfer이다. Coptic/Syriac와 target10은 이미 main에 포함되어 있으므로 이 stage의 extension 대상이 아니다.

Output:

- `09_extension_case/results.md`
- `09_extension_case/extension_target_decision.tsv`
- `09_extension_case/extension_vs_main_deviation.tsv`

Gate:

- Main run과 다른 점을 모두 deviation으로 기록해야 한다.
- Extension case 결과를 target10 main result처럼 쓰면 안 된다.

## Final Report Structure

1. Problem: XLM-R target10 low-resource tokenizer/representation bottleneck
2. Method: id-preserving vocabulary extension, high-resource replay, multi-init continued pretraining
3. Main experiment: target10 performance model with Coptic/Syriac included
4. Evaluation: target10 downstream plus PPPL/retrieval/alignment diagnostics
5. Ablation: current/previous experiments
6. Optional extension case: target10 밖 언어 under the frozen protocol
7. Discussion: when vocab extension helps and when appended-token learning fails
8. Limitations: data scale, official dataset coverage, compute deviations
