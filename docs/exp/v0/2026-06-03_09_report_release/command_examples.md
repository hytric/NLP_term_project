# Command Examples

작성일: 2026-06-04

These commands are examples for reproducing the main stages from the current workspace.
Run them from:

```bash
cd /home/axt/jongha/Glot500-py39-eval
```

## Always Start Here

```bash
git pull --ff-only
df -h . /disk1
readlink -f data download docs/exp/2026-06-03_05_mlm_adaptation docs/exp/2026-06-03_06_nmt_baselines
```

For GPU runs:

```bash
source scripts/gpu3_env.sh
nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader
```

## Target10 Data

```bash
python3 scripts/prepare_target10_bible.py \
  --bible-dir data/raw/bible-corpus/bibles \
  --out-dir data/processed/target10
```

Expected evidence:

- `data/processed/target10/target_languages.tsv`
- `data/processed/target10/target10_stats.tsv`

## Tokenization Audit

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

## Vocabulary Merge

```bash
python3 scripts/train_target10_spm.py

python3 scripts/merge_target10_with_glot500.py \
  --base-model cis-lmu/glot500-base \
  --target-spm data/processed/target10/spm_16k/target10_unigram_16k.model \
  --out-dir data/processed/target10/glot500_target10_spm16k
```

Audit merged tokenizer:

```bash
python3 scripts/tokenization_audit_target10.py \
  --input data/processed/target10/target10_bible_verses.tsv \
  --split train \
  --limit-per-language 500 \
  --tokenizer glot500_target10=data/processed/target10/glot500_target10_spm16k \
  --out docs/exp/2026-06-03_03_vocab_extension/glot500_target10_merged_metrics.tsv
```

## Embedding Initialization

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

## MLM Adaptation

The completed pilot10k checkpoints are stored under:

```text
docs/exp/2026-06-03_05_mlm_adaptation/
```

Use GPU 3 only:

```bash
source scripts/gpu3_env.sh
```

Evidence:

- `docs/exp/2026-06-03_05_mlm_adaptation/mlm_pilot10k_results.tsv`
- `docs/exp/2026-06-03_05_mlm_adaptation/results.md`

## Direct NMT Baseline Pattern

Example direct Syriac -> Coptic diagnostic:

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

## Retrieval Baselines

```bash
python3 scripts/evaluate_retrieval_baseline.py \
  --train-file data/processed/nmt_pivot/eng_to_cop/train.jsonl \
  --validation-file data/processed/nmt_pivot/eng_to_cop/dev.jsonl \
  --test-file data/processed/nmt_pivot/eng_to_cop/test.jsonl \
  --output-dir docs/exp/2026-06-03_06_nmt_baselines/retrieval_char345_eng_to_cop \
  --char-ngram-min 3 \
  --char-ngram-max 5
```

Top-k oracle:

```bash
python3 scripts/evaluate_retrieval_topk_oracle.py \
  --train-file data/processed/nmt_pivot/eng_to_cop/train.jsonl \
  --validation-file data/processed/nmt_pivot/eng_to_cop/dev.jsonl \
  --test-file data/processed/nmt_pivot/eng_to_cop/test.jsonl \
  --output-dir docs/exp/2026-06-03_06_nmt_baselines/retrieval_topk_oracle_eng_to_cop_char345_k8 \
  --top-k 8
```

## Source-Grounding Diagnostics

10A/10B are CPU-only document/analysis stages. They use the top8 candidate files already produced by the retrieval oracle and feature-reranker runs.

Evidence:

- `docs/exp/2026-06-04_10_source_grounding_editing/source_candidate_summary.md`
- `docs/exp/2026-06-04_10_source_grounding_editing/candidate_decision_method.md`
- `docs/exp/2026-06-04_10_source_grounding_editing/candidate_decision_summary.md`

Current 10B result:

- top1 retrieval chrF++ 22.5362
- existing feature reranker chrF++ 24.5921
- 10B candidate decision selector chrF++ 24.6862
- 10B pairwise logistic selector chrF++ 24.7438
- oracle@8 chrF++ 28.3327

Pairwise selector command:

```bash
python3 scripts/evaluate_retrieval_topk_pairwise_feature_selector.py \
  --validation-candidates docs/exp/2026-06-03_06_nmt_baselines/retrieval_topk_oracle_eng_to_cop_char345_k8/validation_top8_candidates.tsv \
  --test-candidates docs/exp/2026-06-03_06_nmt_baselines/retrieval_topk_oracle_eng_to_cop_char345_k8/test_top8_candidates.tsv \
  --existing-selected docs/exp/2026-06-03_06_nmt_baselines/retrieval_topk_feature_reranker_eng_to_cop_char345_k8/test_selected.tsv \
  --output-dir docs/exp/2026-06-04_10_source_grounding_editing \
  --models logistic_regression
```

Pairwise-selected 10C data preparation:

```bash
python3 scripts/prepare_feature_selected_retrieval_auto_aux_nmt.py \
  --base-dir data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024 \
  --validation-selected-tsv docs/exp/2026-06-04_10_source_grounding_editing/pairwise_selector_validation_selected.tsv \
  --test-selected-tsv docs/exp/2026-06-04_10_source_grounding_editing/pairwise_selector_test_selected.tsv \
  --out-dir data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_pairwise_selected_top8 \
  --task-name eng_pairwise_selected_retrieval_to_cop
```

Pairwise-selected 10C edit gate:

```bash
source scripts/gpu3_env.sh
python3 scripts/train_pretrained_seq2seq_baseline.py \
  --model_name_or_path google/byt5-small \
  --train_file data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_pairwise_selected_top8/train.jsonl \
  --validation_file data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_pairwise_selected_top8/validation.jsonl \
  --test_file data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_pairwise_selected_top8/test.jsonl \
  --output_dir docs/exp/2026-06-04_10_source_grounding_editing/byt5_small_pairwise_selected_edit_gate_train512_step120_fp32_nosave \
  --max_source_length 768 \
  --max_target_length 384 \
  --generation_max_length 192 \
  --num_beams 4 \
  --length_penalty 1.0 \
  --max_train_samples 512 \
  --max_eval_samples 64 \
  --max_test_samples 64 \
  --per_device_train_batch_size 1 \
  --per_device_eval_batch_size 1 \
  --gradient_accumulation_steps 4 \
  --learning_rate 5e-5 \
  --max_steps 120 \
  --logging_steps 20 \
  --eval_steps 60 \
  --save_steps 100000 \
  --seed 42 \
  --do_train --do_eval --do_predict \
  --overwrite_output_dir \
  --report_to none \
  --skip_save_model
```

Pairwise-selected 10C control data:

```bash
python3 scripts/prepare_retrieval_eval_controls.py \
  --base-dir data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_pairwise_selected_top8 \
  --mode source_only \
  --out-dir data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_pairwise_selected_top8_control_source_only

python3 scripts/prepare_retrieval_eval_controls.py \
  --base-dir data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_pairwise_selected_top8 \
  --mode retrieved_only \
  --out-dir data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_pairwise_selected_top8_control_retrieved_only

python3 scripts/prepare_retrieval_eval_controls.py \
  --base-dir data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_pairwise_selected_top8 \
  --mode wrong_shift \
  --shift 1 \
  --out-dir data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_pairwise_selected_top8_control_wrong_shift1
```

10C same-checkpoint control gate template:

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
  --per_device_train_batch_size 1 \
  --per_device_eval_batch_size 1 \
  --gradient_accumulation_steps 4 \
  --learning_rate 5e-5 \
  --max_steps 120 \
  --logging_steps 20 \
  --eval_steps 60 \
  --save_steps 100000 \
  --seed 42 \
  --do_train --do_eval --do_predict \
  --overwrite_output_dir \
  --report_to none \
  --skip_save_model
```

## Pivot Gate Pattern

Example Greek -> Coptic gate:

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
  --per_device_train_batch_size 1 \
  --per_device_eval_batch_size 1 \
  --gradient_accumulation_steps 4 \
  --learning_rate 5e-5 \
  --max_steps 50 \
  --do_train --do_eval --do_predict \
  --overwrite_output_dir \
  --report_to none \
  --skip_save_model
```

## Notes

- Prefer `--skip_save_model` for diagnostics.
- Keep large artifacts off the root filesystem.
- For final paper claims, use evidence files in `docs/exp`, not terminal memory.
