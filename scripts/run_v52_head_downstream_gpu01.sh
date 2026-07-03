#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/home/axt/jongha/Glot500-py39-eval}"
DOCS_EXP_ROOT="${DOCS_EXP_ROOT:-${ROOT}/docs/exp/v5.2}"
V52_ROOT="${V52_ROOT:-/home/axt/mnt2/jongha/v5.2_glot5007}"
EVAL_OUTPUT_ROOT="${EVAL_OUTPUT_ROOT:-${V52_ROOT}/evaluation}"
MODEL_MATRIX="${MODEL_MATRIX:-${DOCS_EXP_ROOT}/3_evaluation/model_matrix.tsv}"
FAIR_TARGETS_TSV="${FAIR_TARGETS_TSV:-${DOCS_EXP_ROOT}/3_evaluation/convergence_5way_fair_inference_targets.tsv}"
LOG_DIR="${LOG_DIR:-${V52_ROOT}/runs/logs/head_downstream_gpu01}"

PYTHON_BIN="${PYTHON_BIN:-python3}"
GPUS="${GPUS:-0 1}"
METHODS="${METHODS:-random mean fvt weighted_fvt family_mean}"
STEPS="${STEPS:-10000 20000 30000 40000 50000}"
TASKS="${TASKS:-retrieval_tatoeba retrieval_bible roundtrip_alignment}"

RETRIEVAL_DATA_ROOT="${RETRIEVAL_DATA_ROOT:-${ROOT}/evaluation/download_data/download}"
ROUNDTRIP_DATA_DIR="${ROUNDTRIP_DATA_DIR:-${ROOT}/evaluation/download_data/download/roundtrip_alignment}"
RETRIEVAL_BATCH_SIZE="${RETRIEVAL_BATCH_SIZE:-1024}"
RETRIEVAL_MAX_LENGTH="${RETRIEVAL_MAX_LENGTH:-512}"
RETRIEVAL_TOKEN_CACHE_ROOT="${RETRIEVAL_TOKEN_CACHE_ROOT:-${V52_ROOT}/runs/retrieval_token_cache}"
ROUNDTRIP_BATCH_SIZE="${ROUNDTRIP_BATCH_SIZE:-64}"
ROUNDTRIP_MAX_SAMPLES_PER_LANGUAGE="${ROUNDTRIP_MAX_SAMPLES_PER_LANGUAGE:-100}"

MODE="${1:-all}"

cd "${ROOT}"
mkdir -p "${LOG_DIR}" "${DOCS_EXP_ROOT}/3_evaluation"

if [[ "${REFRESH_MODEL_MATRIX:-1}" == "1" ]]; then
  "${PYTHON_BIN}" scripts/write_v52_eval_model_matrix.py --v52-root "${V52_ROOT}" --out-dir "${DOCS_EXP_ROOT}/3_evaluation" >/dev/null
fi

IFS=' ' read -r -a GPU_ARRAY <<< "${GPUS}"
GPU_COUNT="${#GPU_ARRAY[@]}"
if [[ "${GPU_COUNT}" -eq 0 ]]; then
  echo "GPUS must contain at least one GPU id." >&2
  exit 2
fi

lookup_field() {
  local model_key="$1"
  local field="$2"
  awk -F '\t' -v key="${model_key}" -v field="${field}" '
    NR == 1 {
      for (i = 1; i <= NF; i++) {
        if ($i == field) idx = i
      }
      next
    }
    $1 == key {
      if (!idx) exit 3
      print $idx
      found = 1
      exit
    }
    END {
      if (!found) exit 4
    }
  ' "${MODEL_MATRIX}"
}

model_available() {
  local model_key="$1"
  [[ -s "${MODEL_MATRIX}" ]] || return 1
  awk -F '\t' -v key="${model_key}" '
    NR > 1 && $1 == key {
      found = 1
      if ($10 == "yes") ready = 1
    }
    END {
      if (ready) exit 0
      if (found) exit 2
      exit 1
    }
  ' "${MODEL_MATRIX}"
}

resolved_model_key() {
  local method="$1"
  local step="$2"
  local default_key="v52_${method}_conv5way_step${step}"
  if [[ "${step}" == "50000" && -s "${FAIR_TARGETS_TSV}" ]]; then
    awk -F '\t' -v method="${method}" -v default_key="${default_key}" '
      NR > 1 && $1 == method && $2 == "exposure_aligned_50k" && $10 == "yes" {
        print $6
        found = 1
        exit
      }
      END {
        if (!found) print default_key
      }
    ' "${FAIR_TARGETS_TSV}"
    return
  fi
  echo "${default_key}"
}

head_languages() {
  local task="$1"
  local separator="$2"
  local path="${DOCS_EXP_ROOT}/3_evaluation/00_coverage/coverage_${task}.tsv"
  awk -F '\t' -v sep="${separator}" '
    NR == 1 {
      for (i = 1; i <= NF; i++) {
        col[$i] = i
      }
      next
    }
    $col["group"] == "head" && $col["in_task_list"] == "yes" && $col["has_data"] == "yes" {
      if (n++ > 0) {
        printf "%s", sep
      }
      printf "%s", $col["language_script"]
    }
    END {
      printf "\n"
    }
  ' "${path}"
}

expected_head_count() {
  local task="$1"
  local sep="${2:- }"
  local langs
  langs="$(head_languages "${task}" "${sep}")"
  if [[ -z "${langs}" ]]; then
    echo 0
    return
  fi
  if [[ "${sep}" == "," ]]; then
    tr ',' '\n' <<< "${langs}" | awk 'NF {n++} END {print n+0}'
  else
    wc -w <<< "${langs}" | tr -d ' '
  fi
}

result_language_count() {
  local path="$1"
  [[ -s "${path}" ]] || {
    echo 0
    return
  }
  grep -c '^language=' "${path}" || true
}

head_done() {
  local task="$1"
  local model_key="$2"
  case "${task}" in
    retrieval_tatoeba)
      local result expected found
      result="${EVAL_OUTPUT_ROOT}/retrieval_tatoeba_head/${model_key}/test_results.txt"
      expected="$(expected_head_count retrieval_tatoeba " ")"
      found="$(result_language_count "${result}")"
      [[ "${expected}" -gt 0 && "${found}" -ge "${expected}" ]]
      ;;
    retrieval_bible)
      local result expected found
      result="${EVAL_OUTPUT_ROOT}/retrieval_bible_head/${model_key}/test_results.txt"
      expected="$(expected_head_count retrieval_bible " ")"
      found="$(result_language_count "${result}")"
      [[ "${expected}" -gt 0 && "${found}" -ge "${expected}" ]]
      ;;
    roundtrip_alignment)
      local result expected found
      result="${EVAL_OUTPUT_ROOT}/roundtrip_alignment_head/${model_key}/summary.tsv"
      expected="$(expected_head_count roundtrip_alignment ",")"
      found=0
      if [[ -s "${result}" ]]; then
        found="$(tail -n +2 "${result}" | awk 'NF {n++} END {print n+0}')"
      fi
      [[ "${expected}" -gt 0 && "${found}" -ge "${expected}" ]]
      ;;
    *)
      return 1
      ;;
  esac
}

run_task() {
  local task="$1"
  local method="$2"
  local step="$3"
  local model_key="$4"
  local gpu="$5"

  if head_done "${task}" "${model_key}"; then
    echo "[skip] task=${task} model=${model_key} head already done"
    return 0
  fi

  local model_path
  model_path="$(lookup_field "${model_key}" model_path)"
  local started
  started="$(date +%F_%H%M%S)"
  echo "[start] task=${task} method=${method} step=${step} model=${model_key} gpu=${gpu} ${started}"

  case "${task}" in
    retrieval_tatoeba)
      local langs
      langs="$(head_languages retrieval_tatoeba " ")"
      if [[ -z "${langs}" ]]; then
        echo "[skip] no retrieval_tatoeba head languages"
        return 0
      fi
      local batch rc
      batch="${RETRIEVAL_BATCH_SIZE}"
      while true; do
        set +e
        CUDA_VISIBLE_DEVICES="${gpu}" "${PYTHON_BIN}" scripts/run_v52_retrieval_head_fast.py \
          --task retrieval_tatoeba \
          --model-name-or-path "${model_path}" \
          --data-dir "${RETRIEVAL_DATA_ROOT%/}/retrieval_tatoeba" \
          --output-dir "${EVAL_OUTPUT_ROOT}/retrieval_tatoeba_head/${model_key}" \
          --languages "${langs}" \
          --device cuda \
          --batch-size "${batch}" \
          --max-seq-length "${RETRIEVAL_MAX_LENGTH}" \
          --token-cache-dir "${RETRIEVAL_TOKEN_CACHE_ROOT}/retrieval_tatoeba_gpu${gpu}"
        rc=$?
        set -e
        if [[ "${rc}" -eq 0 ]] && head_done "${task}" "${model_key}"; then
          break
        fi
        if [[ "${batch}" -le 512 ]]; then
          echo "[fail] task=${task} model=${model_key} incomplete after batch=${batch} rc=${rc}" >&2
          return 1
        fi
        batch=$((batch / 2))
        echo "[retry] task=${task} model=${model_key} lowering batch to ${batch}"
      done
      ;;
    retrieval_bible)
      local langs
      langs="$(head_languages retrieval_bible " ")"
      if [[ -z "${langs}" ]]; then
        echo "[skip] no retrieval_bible head languages"
        return 0
      fi
      local batch rc
      batch="${RETRIEVAL_BATCH_SIZE}"
      while true; do
        set +e
        CUDA_VISIBLE_DEVICES="${gpu}" "${PYTHON_BIN}" scripts/run_v52_retrieval_head_fast.py \
          --task retrieval_bible \
          --model-name-or-path "${model_path}" \
          --data-dir "${RETRIEVAL_DATA_ROOT%/}/retrieval_bible" \
          --output-dir "${EVAL_OUTPUT_ROOT}/retrieval_bible_head/${model_key}" \
          --languages "${langs}" \
          --device cuda \
          --batch-size "${batch}" \
          --max-seq-length "${RETRIEVAL_MAX_LENGTH}" \
          --token-cache-dir "${RETRIEVAL_TOKEN_CACHE_ROOT}/retrieval_bible_gpu${gpu}"
        rc=$?
        set -e
        if [[ "${rc}" -eq 0 ]] && head_done "${task}" "${model_key}"; then
          break
        fi
        if [[ "${batch}" -le 512 ]]; then
          echo "[fail] task=${task} model=${model_key} incomplete after batch=${batch} rc=${rc}" >&2
          return 1
        fi
        batch=$((batch / 2))
        echo "[retry] task=${task} model=${model_key} lowering batch to ${batch}"
      done
      ;;
    roundtrip_alignment)
      local langs
      langs="$(head_languages roundtrip_alignment ",")"
      if [[ -z "${langs}" ]]; then
        echo "[skip] no roundtrip head languages"
        return 0
      fi
      CUDA_VISIBLE_DEVICES="${gpu}" "${PYTHON_BIN}" evaluation/round-trip/evaluate_roundtrip_v5.py \
        --model-name-or-path "${model_path}" \
        --data-dir "${ROUNDTRIP_DATA_DIR}" \
        --output-dir "${EVAL_OUTPUT_ROOT}/roundtrip_alignment_head/${model_key}" \
        --device cuda \
        --batch-size "${ROUNDTRIP_BATCH_SIZE}" \
        --max-samples-per-language "${ROUNDTRIP_MAX_SAMPLES_PER_LANGUAGE}" \
        --languages "${langs}"
      ;;
    *)
      echo "unknown task: ${task}" >&2
      exit 2
      ;;
  esac

  if ! head_done "${task}" "${model_key}"; then
    echo "[fail] task=${task} model=${model_key} did not produce expected head count" >&2
    return 1
  fi
  echo "[done] task=${task} model=${model_key} gpu=${gpu} $(date +%F_%H%M%S)"
}

build_queue() {
  local queue_file="${LOG_DIR}/queue.tsv"
  {
    echo -e "index\ttask\tmethod\tstep\tmodel_key\tstatus"
    local idx=0
    for task in ${TASKS}; do
      for method in ${METHODS}; do
        for step in ${STEPS}; do
          local model_key status
          model_key="$(resolved_model_key "${method}" "${step}")"
          status="pending"
          if ! model_available "${model_key}"; then
            status="missing_model"
          elif head_done "${task}" "${model_key}"; then
            status="done"
          fi
          echo -e "${idx}\t${task}\t${method}\t${step}\t${model_key}\t${status}"
          idx=$((idx + 1))
        done
      done
    done
  } > "${queue_file}"
  echo "${queue_file}"
}

run_queue_shard() {
  local shard="$1"
  local gpu="$2"
  local queue_file="$3"
  local status_file="${LOG_DIR}/status_shard${shard}.tsv"

  echo -e "index\ttask\tmodel_key\tgpu\tstatus\tstarted_at\tfinished_at" > "${status_file}"
  tail -n +2 "${queue_file}" | while IFS=$'\t' read -r idx task method step model_key status; do
    if (( idx % GPU_COUNT != shard )); then
      continue
    fi
    if [[ "${status}" == "done" || "${status}" == "missing_model" ]]; then
      echo -e "${idx}\t${task}\t${model_key}\t${gpu}\t${status}\t\t" >> "${status_file}"
      continue
    fi

    local started job_log
    started="$(date +%Y-%m-%dT%H:%M:%S)"
    job_log="${LOG_DIR}/${idx}_${task}_${model_key}_gpu${gpu}.log"
    echo -e "${idx}\t${task}\t${model_key}\t${gpu}\trunning\t${started}\t" >> "${status_file}"
    if run_task "${task}" "${method}" "${step}" "${model_key}" "${gpu}" > "${job_log}" 2>&1; then
      echo -e "${idx}\t${task}\t${model_key}\t${gpu}\tcomplete\t${started}\t$(date +%Y-%m-%dT%H:%M:%S)" >> "${status_file}"
    else
      echo -e "${idx}\t${task}\t${model_key}\t${gpu}\tfailed\t${started}\t$(date +%Y-%m-%dT%H:%M:%S)" >> "${status_file}"
      echo "failed task=${task} model=${model_key}; see ${job_log}" >&2
      return 1
    fi
  done
}

queue_file="$(build_queue)"

case "${MODE}" in
  dry-run)
    echo "Queue written to ${queue_file}"
    awk -F '\t' 'NR == 1 || $6 != "done"' "${queue_file}"
    ;;
  all)
    echo "Queue written to ${queue_file}"
    pids=()
    for shard in "${!GPU_ARRAY[@]}"; do
      gpu="${GPU_ARRAY[$shard]}"
      run_queue_shard "${shard}" "${gpu}" "${queue_file}" &
      pids+=("$!")
    done
    for pid in "${pids[@]}"; do
      wait "${pid}"
    done
    ;;
  shard)
    shard="${2:?Usage: bash scripts/run_v52_head_downstream_gpu01.sh shard <shard_index>}"
    gpu="${GPU_ARRAY[$shard]:?No GPU configured for shard ${shard}}"
    run_queue_shard "${shard}" "${gpu}" "${queue_file}"
    ;;
  *)
    echo "Usage: bash scripts/run_v52_head_downstream_gpu01.sh [dry-run|all|shard <idx>]" >&2
    exit 2
    ;;
esac
