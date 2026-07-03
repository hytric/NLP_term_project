#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/home/axt/jongha/Glot500-py39-eval}"
DOCS_EXP_ROOT="${DOCS_EXP_ROOT:-${ROOT}/docs/exp/v5.2}"
V5_ROOT="${V5_ROOT:-/home/axt/mnt2/jongha/v5.2_glot5007}"
MODEL_MATRIX="${MODEL_MATRIX:-${DOCS_EXP_ROOT}/3_evaluation/model_matrix.tsv}"
PPPL_MANIFEST="${PPPL_MANIFEST:-${DOCS_EXP_ROOT}/0_tokenizer/merge/Glot500_v52_glot5007_xlmr100.manifest.tsv}"
LOG_DIR="${LOG_DIR:-${V5_ROOT}/runs/logs/pppl_head}"
GPU="${1:?usage: bash scripts/run_v52_pppl_head_queue.sh <gpu> <shard> <num_shards>}"
SHARD="${2:?usage: bash scripts/run_v52_pppl_head_queue.sh <gpu> <shard> <num_shards>}"
NUM_SHARDS="${3:?usage: bash scripts/run_v52_pppl_head_queue.sh <gpu> <shard> <num_shards>}"

mkdir -p "${LOG_DIR}"
cd "${ROOT}"

MODEL_KEYS=(
  xlmr_base
  xlmr_large
  v52_random_conv5way_step10000
  v52_random_conv5way_step20000
  v52_random_conv5way_step30000
  v52_random_conv5way_step40000
  v52_random_conv5way_step43000
  v52_mean_conv5way_step10000
  v52_mean_conv5way_step20000
  v52_mean_conv5way_step30000
  v52_mean_conv5way_step40000
  v52_mean_conv5way_step43000
  v52_fvt_conv5way_step10000
  v52_fvt_conv5way_step20000
  v52_fvt_conv5way_step30000
  v52_fvt_conv5way_step40000
  v52_fvt_conv5way_step43000
  v52_weighted_fvt_conv5way_step10000
  v52_weighted_fvt_conv5way_step20000
  v52_weighted_fvt_conv5way_step30000
  v52_weighted_fvt_conv5way_step40000
  v52_weighted_fvt_conv5way_step50000
  v52_family_mean_conv5way_step10000
  v52_family_mean_conv5way_step20000
  v52_family_mean_conv5way_step30000
  v52_family_mean_conv5way_step40000
  v52_family_mean_conv5way_step50000
)

rows_in_scores() {
  local model_key="$1"
  local score_file="${DOCS_EXP_ROOT}/3_evaluation/01_pseudoperplexity/${model_key}/scores.tsv"
  if [[ ! -s "${score_file}" ]]; then
    echo 0
    return 0
  fi
  awk 'END {print NR > 0 ? NR - 1 : 0}' "${score_file}"
}

wait_for_gpu() {
  local gpu="$1"
  local used util
  while true; do
    IFS=',' read -r used util < <(
      nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader,nounits -i "${gpu}" |
        awk -F',' '{gsub(/ /, "", $1); gsub(/ /, "", $2); print $1 "," $2}'
    )
    if [[ "${used:-999999}" -lt "${GPU_MAX_USED_MB:-2000}" && "${util:-100}" -lt "${GPU_MAX_UTIL:-20}" ]]; then
      return 0
    fi
    echo "[wait] gpu=${gpu} used_mb=${used:-?} util=${util:-?} $(date '+%F %T')"
    sleep "${POLL_SECONDS:-60}"
  done
}

mask_batch_size_for() {
  local model_key="$1"
  if [[ "${model_key}" == "xlmr_large" ]]; then
    echo "${MASK_BATCH_SIZE_LARGE:-128}"
  else
    echo "${MASK_BATCH_SIZE_BASE:-256}"
  fi
}

run_one() {
  local model_key="$1"
  local rows
  rows="$(rows_in_scores "${model_key}")"
  if [[ "${rows}" -ge 99 ]]; then
    echo "[skip] pppl_head ${model_key} already has ${rows}/99 rows $(date '+%F %T')"
    return 0
  fi
  wait_for_gpu "${GPU}"
  echo "[start] pppl_head ${model_key} gpu=${GPU} current_rows=${rows}/99 $(date '+%F %T')"
  ALLOW_TRAIN_SOURCE_PPPL=1 \
  PPPL_SPLIT=train \
  PPPL_EVAL_ROLE=train_source_diagnostic \
  INCLUDE_ALL_HEAD=1 \
  HEAD_LIMIT=20 \
  MAX_EXAMPLES_PER_LANGUAGE="${MAX_EXAMPLES_PER_LANGUAGE:-20}" \
  MAX_LENGTH="${MAX_LENGTH:-128}" \
  MASK_BATCH_SIZE="$(mask_batch_size_for "${model_key}")" \
  PPPL_EXAMPLES_CACHE="${V5_ROOT}/evaluation/cache/pppl_examples_train_ex${MAX_EXAMPLES_PER_LANGUAGE:-20}_allhead1_gpu${GPU}.json" \
  DOCS_EXP_ROOT="${DOCS_EXP_ROOT}" \
  V5_ROOT="${V5_ROOT}" \
  MODEL_MATRIX="${MODEL_MATRIX}" \
  PPPL_MANIFEST="${PPPL_MANIFEST}" \
  REFRESH_MODEL_MATRIX=0 \
  bash scripts/run_v5_eval_metric.sh pppl "${model_key}" "${GPU}"
  rows="$(rows_in_scores "${model_key}")"
  echo "[done] pppl_head ${model_key} rows=${rows}/99 $(date '+%F %T')"
}

for index in "${!MODEL_KEYS[@]}"; do
  if (( index % NUM_SHARDS != SHARD )); then
    continue
  fi
  run_one "${MODEL_KEYS[index]}" 2>&1 | tee -a "${LOG_DIR}/gpu${GPU}_shard${SHARD}.log"
done
