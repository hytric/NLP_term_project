# Experiment Presentation Walkthrough

작성일: 2026-06-05

목적: 현재 `docs/exp`에 흩어진 실험을 발표자가 순서대로 볼 수 있게 정리한다.
각 실험은 질문, 코드, 실행 예시, 결과, 발표 멘트 순서로 읽으면 된다.

## Core Message

한 문장 결론:

> target10 tokenizer extension과 mean embedding initialization은 representation-side 적응에서 강한 긍정 결과를 보였지만, Coptic/Syriac generation은 direct NMT, pivot, retrieval-augmented neural editing 모두 아직 source-grounded translation으로 보기 어렵다.

발표에서 강하게 말할 수 있는 것:

- Glot500 tokenizer는 Coptic/Syriac/Cherokee/Ojibwa를 심하게 잘게 쪼갠다.
- target10 SentencePiece를 Glot500에 merge하면 Coptic/Syriac tokens/word가 약 2/3 줄어든다.
- mean initialization은 pilot10k MLM stable eval에서 random보다 좋다.
- direct NMT와 Greek pivot/back-translation은 negative gate다.
- char n-gram retrieval과 top8 reranking은 현재 가장 강한 Coptic 기준선이다.
- 10C controls는 neural retrieval-editing이 아직 retrieved Coptic hint에 크게 의존함을 보여준다.

발표에서 피해야 할 주장:

- Coptic/Syriac neural translation을 해결했다고 말하지 않는다.
- Greek pivot/back-translation을 usable하다고 말하지 않는다.
- 현재 ByT5-small retrieval-editing을 source-grounded editing이라고 말하지 않는다.

## Slide Flow

| Slide | 제목 | 핵심 메시지 | 증거 |
| ---: | --- | --- | --- |
| 1 | Problem | unsupported script에서는 multilingual model도 representation/generation 병목이 있다 | target10 setup |
| 2 | Target10 Setup | 10개 저자원 언어 + Coptic/Syriac downstream | 76,972 verse rows, overlap 4,892 |
| 3 | Tokenizer Bottleneck | Glot500은 fragmentation, NLLB는 UNK collapse | tokenization audit |
| 4 | Vocabulary Extension | target10 SPM16K merge로 subword sequence가 짧아짐 | Coptic 66.3%, Syriac 68.5% reduction |
| 5 | Embedding Init | mean init이 random보다 안정적 | MLM stable eval loss 5.8343 vs 7.0169 |
| 6 | Direct NMT | 파이프라인은 통과하지만 generation collapse | full Syriac -> Coptic chrF++ 9.9340, max-length 반복 |
| 7 | Retrieval Baseline | retrieval은 강한 non-neural 기준선 | English -> Coptic chrF++ 22.3584 |
| 8 | Reranking | top8 oracle headroom이 있고 CPU selector는 소폭 개선 | pairwise selector chrF++ 24.7438 |
| 9 | Pivot Gate | Greek pivot은 synthetic data 생성에 부적합 | Greek -> Coptic chrF++ 0.0, Coptic 0/32 |
| 10 | 10C Controls | neural editing은 retrieval-sensitive지만 source-grounded 아님 | retrieved-only 18.6220 > source+retrieval 18.3574 |
| 11 | Claim Boundary | positive claim과 negative gate를 분리 | release audit |
| 12 | Next Steps | source-grounding objective, delta/edit target, copy-aware eval | limitations |

## 00. Goal And GPU Policy

질문: 이 프로젝트의 최종 목표와 실행 제약은 무엇인가?

설명:
target10 저자원 언어를 Glot500 계열 모델에 추가하는 multilingual adaptation 파일럿이다.
Coptic/Syriac은 downstream 번역 사례로 유지한다.
GPU 실험은 physical GPU 3만 사용한다.

코드:

- [../../scripts/gpu3_env.sh](../../scripts/gpu3_env.sh)
- [2026-06-03_00_final_goal/plan.md](2026-06-03_00_final_goal/plan.md)
- [README.md](README.md)

실행 예시:

```bash
source scripts/gpu3_env.sh
nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader
```

발표 멘트:

> 먼저 scope를 고정했습니다. broad multilingual pretraining이 아니라, 10개 저자원 언어에 대한 vocabulary/model adaptation 파일럿이고, 모든 GPU diagnostic은 physical GPU 3에서만 실행했습니다.

## 01. Target10 Data And Splits

질문: 어떤 언어와 데이터를 대상으로 실험하는가?

설명:
Bible corpus에서 10개 언어를 추출하고, book-level split을 사용했다.
John은 test, Mark는 dev, 나머지는 train이다.
random verse split보다 leakage 설명이 쉽고, 발표에서 재현 규칙을 간단히 말할 수 있다.

코드:

- [../../scripts/prepare_target10_bible.py](../../scripts/prepare_target10_bible.py)
- [2026-06-03_01_data_and_splits/results.md](2026-06-03_01_data_and_splits/results.md)

실행 예시:

```bash
python3 scripts/prepare_target10_bible.py \
  --bible-dir data/raw/bible-corpus/bibles \
  --out-dir data/processed/target10
```

주요 결과:

| 항목 | 값 |
| --- | ---: |
| target languages | 10 |
| total verse rows | 76,972 |
| tokenizer train lines | 61,930 |
| shared verse overlap | 4,892 |

발표 멘트:

> target10은 Coptic, Syriac, Cherokee, Ojibwa처럼 script bottleneck이 예상되는 언어와 몇 개 Latin-script 저자원 언어를 함께 넣은 controlled pilot입니다.

## 02. Tokenization Audit

질문: 기존 multilingual tokenizer가 target10을 잘 처리하는가?

설명:
XLM-R, Glot500, NLLB tokenizer를 10개 언어 train verse 500개씩에 적용해 tokens/word, single-char token 비율, UNK 비율을 비교했다.

코드:

- [../../scripts/tokenization_audit_target10.py](../../scripts/tokenization_audit_target10.py)
- [2026-06-03_02_tokenization_audit/results.md](2026-06-03_02_tokenization_audit/results.md)
- [2026-06-03_02_tokenization_audit/target10_tokenization_metrics.tsv](2026-06-03_02_tokenization_audit/target10_tokenization_metrics.tsv)

실행 예시:

```bash
python3 scripts/tokenization_audit_target10.py \
  --input data/processed/target10/target10_bible_verses.tsv \
  --split train \
  --limit-per-language 500 \
  --tokenizer xlm-r=xlm-roberta-base \
  --tokenizer glot500=cis-lmu/glot500-base \
  --tokenizer nllb=facebook/nllb-200-distilled-600M \
  --out docs/exp/2026-06-03_02_tokenization_audit/target10_tokenization_metrics.tsv
```

주요 결과:

| Model | Language | Failure |
| --- | --- | --- |
| Glot500 | Coptic | tokens/word 5.274, single-char 67.7% |
| Glot500 | Syriac | tokens/word 5.089, single-char 80.3% |
| NLLB | Coptic | UNK 48.6% |
| NLLB | Syriac | UNK 50.0% |

발표 멘트:

> 여기서 두 가지 failure mode가 갈립니다. Glot500은 문자를 지나치게 잘게 쪼개고, NLLB는 일부 script를 UNK로 뭉개버립니다. 그래서 vocabulary extension이 다음 실험으로 자연스럽게 이어집니다.

## 03. Vocabulary Extension

질문: target10만으로 새 subword vocabulary를 만들면 fragmentation이 줄어드는가?

설명:
target10 train text로 SentencePiece unigram 16k tokenizer를 학습하고, 그 vocabulary를 Glot500 tokenizer에 merge했다.
목표는 새 tokenizer 효과를 얻으면서 Glot500 model loading과 compatibility를 유지하는 것이다.

코드:

- [../../scripts/train_target10_spm.py](../../scripts/train_target10_spm.py)
- [../../scripts/merge_target10_with_glot500.py](../../scripts/merge_target10_with_glot500.py)
- [2026-06-03_03_vocab_extension/results.md](2026-06-03_03_vocab_extension/results.md)

주의:
이번 target10 실험은 [../../tokenization/run.py](../../tokenization/run.py)를 직접 실행한 것이 아니다.
방법은 비슷하지만, `scripts/` 아래 코드가 target10/Glot500-base 실험용으로 범위와 설정을 줄인 구현이다.

실행 예시:

```bash
python3 scripts/train_target10_spm.py

python3 scripts/merge_target10_with_glot500.py \
  --base-model cis-lmu/glot500-base \
  --target-spm data/processed/target10/spm_16k/target10_unigram_16k.model \
  --out-dir data/processed/target10/glot500_target10_spm16k
```

주요 결과:

| Language | Glot500 tokens/word | Merged tokens/word | Reduction |
| --- | ---: | ---: | ---: |
| Coptic | 5.274 | 1.779 | 66.3% |
| Syriac | 5.089 | 1.601 | 68.5% |
| Cherokee | 5.254 | 2.001 | 61.9% |
| Ojibwa | 5.021 | 2.205 | 56.1% |

발표 멘트:

> 이 단계가 representation-side에서 가장 명확한 positive result입니다. Unsupported-script 언어에서 sequence length가 크게 줄었고, 이 개선이 merged Glot500 tokenizer에서도 유지됩니다.

## 04. Embedding Initialization

질문: 새로 추가한 13,994개 token embedding을 어떻게 초기화할 것인가?

설명:
random init과 mean init을 비교했다.
mean init은 새 target10 piece를 기존 Glot500 tokenizer로 다시 tokenize한 뒤, 기존 subtoken embedding 평균으로 새 token embedding과 LM head row를 초기화한다.

코드:

- [../../scripts/init_target10_embeddings.py](../../scripts/init_target10_embeddings.py)
- [2026-06-03_04_embedding_init/results.md](2026-06-03_04_embedding_init/results.md)

실행 예시:

```bash
python3 scripts/init_target10_embeddings.py \
  --base-model cis-lmu/glot500-base \
  --merged-tokenizer data/processed/target10/glot500_target10_spm16k \
  --out-root data/processed/target10/initialized_models \
  --mode random

python3 scripts/init_target10_embeddings.py \
  --base-model cis-lmu/glot500-base \
  --merged-tokenizer data/processed/target10/glot500_target10_spm16k \
  --out-root data/processed/target10/initialized_models \
  --mode mean
```

주요 결과:

| Mode | New tokens | Fallback | Avg old subtokens |
| --- | ---: | ---: | ---: |
| Random | 13,994 | 0 | n/a |
| Mean | 13,994 | 0 | 3.791 |

발표 멘트:

> mean init은 모든 새 token에 대해 fallback 없이 기존 embedding geometry를 이용했습니다. 그래서 MLM adaptation 전에 random보다 더 안정적인 시작점을 기대할 수 있습니다.

## 05. MLM Adaptation

질문: extended tokenizer와 initialized model이 target10에서 실제로 더 잘 적응하는가?

설명:
target10 plain text를 MLM 파일로 만들고, random/mean initialized checkpoint를 같은 조건에서 continued pretraining했다.
pilot10k built-in eval은 batch size 2에서 NaN이 나왔기 때문에, 최종 판단은 fp32 batch size 16 stable re-evaluation으로 했다.

코드:

- [../../scripts/write_target10_mlm_files.py](../../scripts/write_target10_mlm_files.py)
- [../../modeling/run.py](../../modeling/run.py)
- [2026-06-03_05_mlm_adaptation/training_config.json](2026-06-03_05_mlm_adaptation/training_config.json)
- [2026-06-03_05_mlm_adaptation/results.md](2026-06-03_05_mlm_adaptation/results.md)

대표 실행 형태:

```bash
python3 scripts/write_target10_mlm_files.py \
  --input data/processed/target10/target10_bible_verses.tsv \
  --out-dir data/processed/target10/mlm

source scripts/gpu3_env.sh
python3 modeling/run.py \
  --model_name_or_path data/processed/target10/initialized_models/glot500_target10_mean \
  --tokenizer_name data/processed/target10/glot500_target10_spm16k \
  --train_file data/processed/target10/mlm/target10_train.txt \
  --validation_file data/processed/target10/mlm/target10_dev.txt \
  --output_dir docs/exp/2026-06-03_05_mlm_adaptation/pilot10k_mean \
  --line_by_line \
  --max_seq_length 128 \
  --per_device_train_batch_size 2 \
  --per_device_eval_batch_size 2 \
  --learning_rate 5e-5 \
  --max_train_samples 10000 \
  --max_eval_samples 1000 \
  --max_steps 5000 \
  --fp16 \
  --do_train --do_eval \
  --report_to none
```

주요 결과:

| Init | Stable eval loss | Stable perplexity |
| --- | ---: | ---: |
| Random | 7.0169 | 1,115.29 |
| Mean | 5.8343 | 341.84 |

발표 멘트:

> mean init은 pilot10k stable re-eval에서 random보다 명확히 좋았습니다. 이후 downstream NMT는 `pilot10k_mean`을 active checkpoint로 사용했습니다.

## 06. Direct NMT And Retrieval Baselines

질문: representation-side 개선이 Coptic/Syriac translation으로 이어지는가?

설명:
Glot500-style encoder-decoder로 Coptic -> Syriac, Syriac -> Coptic direct NMT를 돌렸다.
pipeline은 통과했지만 output은 반복 붕괴에 머물렀다.
그래서 non-neural char n-gram retrieval baseline을 추가해, 현재 neural run이 넘어야 할 기준을 세웠다.

코드:

- [../../scripts/prepare_cop_syr_nmt.py](../../scripts/prepare_cop_syr_nmt.py)
- [../../scripts/train_cop_syr_encoder_decoder.py](../../scripts/train_cop_syr_encoder_decoder.py)
- [../../scripts/evaluate_retrieval_baseline.py](../../scripts/evaluate_retrieval_baseline.py)
- [2026-06-03_06_nmt_baselines/results.md](2026-06-03_06_nmt_baselines/results.md)

Direct NMT 실행 예시:

```bash
source scripts/gpu3_env.sh
python3 scripts/train_cop_syr_encoder_decoder.py \
  --model_name_or_path docs/exp/2026-06-03_05_mlm_adaptation/pilot10k_mean \
  --tokenizer_name data/processed/target10/glot500_target10_spm16k \
  --train_file data/processed/nmt_cop_syr/syr_to_cop/train.jsonl \
  --validation_file data/processed/nmt_cop_syr/syr_to_cop/dev.jsonl \
  --test_file data/processed/nmt_cop_syr/syr_to_cop/test.jsonl \
  --output_dir docs/exp/2026-06-03_06_nmt_baselines/example_syr_to_cop \
  --max_source_length 128 \
  --max_target_length 64 \
  --max_train_samples 512 \
  --max_eval_samples 64 \
  --max_test_samples 64 \
  --no_repeat_ngram_size 2 \
  --repetition_penalty 1.2 \
  --do_train --do_eval --do_predict \
  --overwrite_output_dir \
  --report_to none \
  --skip_save_model
```

Retrieval baseline 실행 예시:

```bash
python3 scripts/evaluate_retrieval_baseline.py \
  --train-file data/processed/nmt_pivot/eng_to_cop/train.jsonl \
  --validation-file data/processed/nmt_pivot/eng_to_cop/dev.jsonl \
  --test-file data/processed/nmt_pivot/eng_to_cop/test.jsonl \
  --output-dir docs/exp/2026-06-03_06_nmt_baselines/retrieval_char345_eng_to_cop \
  --char-ngram-min 3 \
  --char-ngram-max 5
```

주요 결과:

| Experiment | Scope | chrF++ | 해석 |
| --- | --- | ---: | --- |
| full Coptic -> Syriac direct NMT | full test | 5.7982 | repetitive |
| full Syriac -> Coptic direct NMT | full test | 9.9340 | max-length Coptic repetition |
| English -> Coptic retrieval | full test | 22.3584 | strong non-neural baseline |
| Syriac -> Coptic retrieval | full test | 22.2083 | strong non-neural baseline |

발표 멘트:

> Direct NMT 결과는 조심해서 해석해야 합니다. chrF++가 올라가도 실제 출력은 formulaic repetition입니다. 반대로 retrieval baseline은 생성 모델은 아니지만 valid Coptic sentence를 만들기 때문에, 이후 neural 실험의 현실적인 비교 기준이 됩니다.

## 07. Pivot And Back-Translation Gate

질문: Greek pivot path를 back-translation 확대에 써도 되는가?

설명:
ByT5-small fp32로 Syriac -> Greek, Greek -> Coptic gate를 작게 돌렸다.
첫 leg는 Greek-looking output을 내지만 반복이며, 두 번째 leg는 Coptic script 전환에 실패했다.

코드:

- [../../scripts/prepare_pivot_nmt.py](../../scripts/prepare_pivot_nmt.py)
- [../../scripts/train_pretrained_seq2seq_baseline.py](../../scripts/train_pretrained_seq2seq_baseline.py)
- [2026-06-03_07_pivot_backtranslation/results.md](2026-06-03_07_pivot_backtranslation/results.md)

실행 예시:

```bash
source scripts/gpu3_env.sh
python3 scripts/train_pretrained_seq2seq_baseline.py \
  --model_name_or_path google/byt5-small \
  --train_file data/processed/nmt_pivot/grc_to_cop/train.jsonl \
  --validation_file data/processed/nmt_pivot/grc_to_cop/dev.jsonl \
  --test_file data/processed/nmt_pivot/grc_to_cop/test.jsonl \
  --output_dir docs/exp/2026-06-03_07_pivot_backtranslation/byt5_small_pivot_grc_to_cop_len320_128_pilot256_step50_fp32_nosave \
  --max_source_length 320 \
  --max_target_length 128 \
  --generation_max_length 128 \
  --use_language_tags \
  --max_train_samples 256 \
  --max_eval_samples 32 \
  --max_test_samples 32 \
  --learning_rate 5e-5 \
  --max_steps 50 \
  --do_train --do_eval --do_predict \
  --overwrite_output_dir \
  --report_to none \
  --skip_save_model
```

주요 결과:

| Direction | chrF++ | Gen len | Script check |
| --- | ---: | ---: | --- |
| Syriac -> Greek | 3.5930 | 127.0 | Greek 32/32 |
| Greek -> Coptic | 0.0000 | 127.0 | Coptic 0/32 |

발표 멘트:

> 이 실험의 결론은 negative gate입니다. 이 checkpoint로 synthetic back-translation을 만들면 noise를 증폭할 가능성이 큽니다.

## 08. Evaluation Analysis

질문: 어떤 수치를 논문/발표 claim으로 쓸 수 있는가?

설명:
08번은 새 학습보다 consolidation 단계다.
tokenization, MLM, NMT, retrieval, pivot, qualitative failure mode를 paper-ready table과 figure로 정리했다.

자료:

- [2026-06-03_08_evaluation_analysis/final_metrics.tsv](2026-06-03_08_evaluation_analysis/final_metrics.tsv)
- [2026-06-03_08_evaluation_analysis/paper_tables.md](2026-06-03_08_evaluation_analysis/paper_tables.md)
- [2026-06-03_08_evaluation_analysis/qualitative_analysis.md](2026-06-03_08_evaluation_analysis/qualitative_analysis.md)
- [2026-06-03_08_evaluation_analysis/error_taxonomy.md](2026-06-03_08_evaluation_analysis/error_taxonomy.md)

발표용 핵심 표:

| Category | Best current evidence | Interpretation |
| --- | --- | --- |
| Tokenization | Coptic 66.3%, Syriac 68.5% reduction | positive |
| MLM | mean eval loss 5.8343 vs random 7.0169 | positive |
| Direct NMT | full Syriac -> Coptic chrF++ 9.9340 | negative, repetition |
| Retrieval | English -> Coptic chrF++ 22.3584 | strong baseline |
| Pivot | Greek -> Coptic chrF++ 0.0 | negative gate |

발표 멘트:

> 08번에서는 positive result와 negative gate를 분리했습니다. 이 분리가 발표의 신뢰도를 지켜줍니다.

## 09. Report And Release Drafts

질문: 실험 결과를 보고서/논문/발표로 어떻게 옮길 것인가?

설명:
09번은 progress report, term paper outline, command examples, reproducibility checklist, claim-evidence map을 만든 단계다.
발표 자료를 만들 때는 command examples와 claim-evidence map을 같이 보면 좋다.

자료:

- [2026-06-03_09_report_release/progress_report.md](2026-06-03_09_report_release/progress_report.md)
- [2026-06-03_09_report_release/term_paper_outline.md](2026-06-03_09_report_release/term_paper_outline.md)
- [2026-06-03_09_report_release/command_examples.md](2026-06-03_09_report_release/command_examples.md)
- [2026-06-03_09_report_release/claim_evidence_map.md](2026-06-03_09_report_release/claim_evidence_map.md)
- [2026-06-03_09_report_release/final_presentation_outline.md](2026-06-03_09_report_release/final_presentation_outline.md)

발표 멘트:

> 모든 수치는 claim-evidence map으로 되돌아갈 수 있게 정리했습니다. 발표에서 말하는 claim마다 해당 evidence file이 있습니다.

## 10. Source-Grounding And Retrieval-Editing

질문: retrieval candidate를 더 잘 고르거나 편집하면 source-grounded Coptic translation으로 갈 수 있는가?

설명:
10A는 top8 retrieval candidate diagnostic, 10B는 CPU selector, 10C는 ByT5-small retrieval-editing gate다.
pairwise CPU selector는 현재 best CPU retrieval selector지만, neural editing gate는 negative다.

코드:

- [../../scripts/evaluate_retrieval_topk_pairwise_feature_selector.py](../../scripts/evaluate_retrieval_topk_pairwise_feature_selector.py)
- [../../scripts/prepare_feature_selected_retrieval_auto_aux_nmt.py](../../scripts/prepare_feature_selected_retrieval_auto_aux_nmt.py)
- [../../scripts/prepare_retrieval_eval_controls.py](../../scripts/prepare_retrieval_eval_controls.py)
- [../../scripts/train_pretrained_seq2seq_baseline.py](../../scripts/train_pretrained_seq2seq_baseline.py)
- [2026-06-04_10_source_grounding_editing/pairwise_selector_summary.md](2026-06-04_10_source_grounding_editing/pairwise_selector_summary.md)
- [2026-06-04_10_source_grounding_editing/retrieval_edit_controls.md](2026-06-04_10_source_grounding_editing/retrieval_edit_controls.md)

Pairwise selector 실행 예시:

```bash
python3 scripts/evaluate_retrieval_topk_pairwise_feature_selector.py \
  --validation-candidates docs/exp/2026-06-03_06_nmt_baselines/retrieval_topk_oracle_eng_to_cop_char345_k8/validation_top8_candidates.tsv \
  --test-candidates docs/exp/2026-06-03_06_nmt_baselines/retrieval_topk_oracle_eng_to_cop_char345_k8/test_top8_candidates.tsv \
  --existing-selected docs/exp/2026-06-03_06_nmt_baselines/retrieval_topk_feature_reranker_eng_to_cop_char345_k8/test_selected.tsv \
  --output-dir docs/exp/2026-06-04_10_source_grounding_editing \
  --models logistic_regression
```

10C same-checkpoint control 실행 형태:

```bash
source scripts/gpu3_env.sh
PAIRWISE_DIR=data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_pairwise_selected_top8
SOURCE_ONLY_DIR=data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_pairwise_selected_top8_control_source_only
RETRIEVED_ONLY_DIR=data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_pairwise_selected_top8_control_retrieved_only
WRONG_DIR=data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_pairwise_selected_top8_control_wrong_shift1
FEATURE_DIR=data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_feature_selected_top8

python3 scripts/train_pretrained_seq2seq_baseline.py \
  --model_name_or_path google/byt5-small \
  --train_file "${PAIRWISE_DIR}/train.jsonl" \
  --validation_file "${PAIRWISE_DIR}/validation.jsonl" \
  --test_file "${PAIRWISE_DIR}/test.jsonl" \
  --extra_test_file "source_only=${SOURCE_ONLY_DIR}/test.jsonl" \
  --extra_test_file "retrieved_only=${RETRIEVED_ONLY_DIR}/test.jsonl" \
  --extra_test_file "wrong_shift1=${WRONG_DIR}/test.jsonl" \
  --extra_test_file "feature_selected=${FEATURE_DIR}/test.jsonl" \
  --output_dir docs/exp/2026-06-04_10_source_grounding_editing/byt5_small_pairwise_selected_same_checkpoint_controls_train512_step120_fp32_nosave \
  --max_source_length 768 \
  --max_target_length 384 \
  --generation_max_length 192 \
  --num_beams 4 \
  --length_penalty 1.0 \
  --max_train_samples 512 \
  --max_eval_samples 64 \
  --max_test_samples 64 \
  --learning_rate 5e-5 \
  --max_steps 120 \
  --do_train --do_eval --do_predict \
  --overwrite_output_dir \
  --report_to none \
  --skip_save_model
```

주요 결과:

| Condition | chrF++ | Interpretation |
| --- | ---: | --- |
| top1 retrieval | 22.5362 | baseline |
| existing feature reranker | 24.5921 | positive |
| 10B pairwise logistic selector | 24.7438 | current best CPU selector |
| oracle@8 | 28.3327 | headroom remains |
| 10C source+retrieval edit | 18.3574 | negative neural gate |
| 10C source-only | 0.2729 | source alone collapses |
| 10C retrieved-only | 18.6220 | retrieved hint alone slightly better |
| 10C wrong-shift1 | 12.8253 | wrong retrieval hurts but still guides output |

발표 멘트:

> 10번은 가장 중요한 failure analysis입니다. CPU selector는 retrieval candidate selection에 의미 있는 신호가 있음을 보여주지만, small ByT5 editing은 source보다 retrieved Coptic hint에 더 기대고 있습니다.

## 11. Release Audit

질문: 현재 상태에서 무엇을 claim할 수 있고, 무엇은 release 전에 남아 있는가?

설명:
11번은 실험 목표 완료 여부, large artifact 위치, license/release risk를 정리한 audit이다.
실험 진행 목표는 만족하지만 public GitHub release는 worktree cleanup과 데이터 license 확인이 더 필요하다.

자료:

- [2026-06-04_11_release_audit/release_audit_summary.md](2026-06-04_11_release_audit/release_audit_summary.md)
- [2026-06-04_11_release_audit/completion_audit.md](2026-06-04_11_release_audit/completion_audit.md)
- [2026-06-04_11_release_audit/artifact_inventory.tsv](2026-06-04_11_release_audit/artifact_inventory.tsv)

발표 멘트:

> 현재 실험 story는 cautious paper draft로 충분하지만, public release claim은 별개입니다. full corpora와 checkpoint는 license와 storage 정책이 확정될 때까지 Git에 넣지 않는 쪽으로 정리했습니다.

## Final Takeaway

발표 마지막 문장:

> 이 프로젝트의 현재 기여는 translation solved claim이 아니라, unsupported low-resource scripts에서 tokenizer/embedding adaptation은 분명한 개선을 만들지만 generation 단계에서는 retrieval baseline과 copy-aware source-grounding evaluation이 필수라는 것을 체계적으로 보여준 데 있다.

## Where To Continue

다음 실험을 한다면 우선순위는 다음과 같다.

1. retrieval-editing을 plain target generation이 아니라 delta/edit target으로 바꾼다.
2. prediction-vs-retrieved chrF++, exact copy, wrong-retrieval control을 기본 metric으로 유지한다.
3. stronger candidate selector는 oracle@8 gap을 줄이는 방향으로 listwise/objective를 개선한다.
4. direct/pivot NMT는 단순 step 증가보다 EOS/coverage/source-grounding objective가 생긴 뒤 재시도한다.
