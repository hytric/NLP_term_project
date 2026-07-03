#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/home/axt/jongha/Glot500-py39-eval}"
V52_ROOT="${V52_ROOT:-/home/axt/mnt2/jongha/v5.2_glot5007}"
NER_DATA="${NER_DATA:-/home/axt/mnt2/jongha/v5_glot50010/eval_data_download/ner}"
COVERAGE="${COVERAGE:-${ROOT}/docs/exp/v5.2/3_evaluation/00_coverage/coverage_ner.tsv}"
MODEL_MATRIX="${MODEL_MATRIX:-${ROOT}/docs/exp/v5.2/3_evaluation/model_matrix.tsv}"
FAIR_TARGETS="${FAIR_TARGETS:-${ROOT}/docs/exp/v5.2/3_evaluation/convergence_5way_fair_inference_targets.tsv}"
LOG_DIR="${LOG_DIR:-${V52_ROOT}/runs/logs/ner_head_gpu23}"
LINK_DIR="${LINK_DIR:-${V52_ROOT}/runs/ner_head_model_links}"

cd "${ROOT}"
mkdir -p "${LOG_DIR}" "${LINK_DIR}" "${V52_ROOT}/evaluation/ner_head"

PYTHON_BIN="${PYTHON_BIN:-python3}"
GPUS="${GPUS:-2 3}"
EVAL_BATCH_SIZE="${EVAL_BATCH_SIZE:-1024}"
MAX_LENGTH="${MAX_LENGTH:-256}"
SEED="${SEED:-1}"
METHODS="${METHODS:-random mean fvt weighted_fvt family_mean}"
STEPS="${STEPS:-10000 20000 30000 40000 50000}"
DISABLE_FILE="${DISABLE_FILE:-${V52_ROOT}/runs/disable_v52_background_waiters}"

if [[ -e "${DISABLE_FILE}" && "${ALLOW_V52_BACKGROUND_QUEUE:-0}" != "1" && "${STEPS}" != "50000" ]]; then
  echo "[disabled] ${DISABLE_FILE} exists; refusing non-50k NER head queue STEPS='${STEPS}'."
  exit 0
fi

QUEUE_FILE="${LOG_DIR}/queue.tsv"
MISSING_FILE="${LOG_DIR}/missing_trained.tsv"
HEAD_LANGS_FILE="${LOG_DIR}/head_langs.txt"

export ROOT V52_ROOT NER_DATA COVERAGE MODEL_MATRIX FAIR_TARGETS LOG_DIR LINK_DIR
export QUEUE_FILE MISSING_FILE HEAD_LANGS_FILE METHODS STEPS

write_queue() {
  "${PYTHON_BIN}" - <<'PY' > "${QUEUE_FILE}.tmp"
import csv
import os
import re
from pathlib import Path

root = Path(os.environ["ROOT"])
v52_root = Path(os.environ["V52_ROOT"])
model_matrix = Path(os.environ["MODEL_MATRIX"])
fair_targets = Path(os.environ["FAIR_TARGETS"])
methods = os.environ["METHODS"].split()
steps = [int(item) for item in os.environ["STEPS"].split()]

matrix = {}
with model_matrix.open(newline="", encoding="utf-8") as handle:
    for row in csv.DictReader(handle, delimiter="\t"):
        key = row.get("model_key", "")
        if key:
            matrix[key] = row.get("model_path", "")

fair = {}
with fair_targets.open(newline="", encoding="utf-8") as handle:
    for row in csv.DictReader(handle, delimiter="\t"):
        if row.get("comparison_group") == "exposure_aligned_50k" and row.get("ready_for_inference") == "yes":
            fair[row["method"]] = (row["target_model_key"], row["checkpoint_dir"])

def model_key(method, step):
    if step == 50000 and method in fair:
        return fair[method]
    key = f"v52_{method}_conv5way_step{step}"
    return key, matrix.get(key, "")

def parse_best_checkpoint(source_dir):
    eval_results = source_dir / "eval_results.txt"
    if eval_results.exists():
        for line in reversed(eval_results.read_text(encoding="utf-8", errors="ignore").splitlines()):
            match = re.search(r"best checkpoint = ([^,]+)", line)
            if match:
                candidate = Path(match.group(1).strip())
                if (candidate / "pytorch_model.bin").exists():
                    return str(candidate)
    best = source_dir / "checkpoint-best"
    if (best / "pytorch_model.bin").exists():
        return str(best)
    if (source_dir / "pytorch_model.bin").exists():
        return str(source_dir)
    return ""

def source_for(key, model_path):
    basename = Path(model_path).name if model_path else ""
    if basename:
        direct = v52_root / "evaluation" / "ner" / key / basename
        if direct.exists():
            return direct
    base = v52_root / "evaluation" / "ner" / key
    candidates = sorted(base.glob("*/checkpoint-best/pytorch_model.bin"))
    if candidates:
        return candidates[0].parents[1]
    candidates = sorted(base.glob("*/pytorch_model.bin"))
    if candidates:
        return candidates[0].parent
    return direct if basename else base

print("index\tmethod\tstep\tmodel_key\tmodel_path\tsource_dir\tbest_checkpoint")
idx = 0
missing = []
for method in methods:
    for step in steps:
        key, model_path = model_key(method, step)
        source_dir = source_for(key, model_path)
        best_checkpoint = parse_best_checkpoint(source_dir)
        if not best_checkpoint:
            missing.append((method, step, key, model_path, str(source_dir)))
            continue
        print(f"{idx}\t{method}\t{step}\t{key}\t{model_path}\t{source_dir}\t{best_checkpoint}")
        idx += 1

missing_path = Path(os.environ["MISSING_FILE"])
missing_path.parent.mkdir(parents=True, exist_ok=True)
with missing_path.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(["method", "step", "model_key", "model_path", "expected_source_dir"])
    writer.writerows(missing)
PY
  mv "${QUEUE_FILE}.tmp" "${QUEUE_FILE}"
}

write_head_langs() {
  "${PYTHON_BIN}" - <<'PY' > "${HEAD_LANGS_FILE}.tmp"
import csv
import os
from pathlib import Path

coverage = Path(os.environ["COVERAGE"])
data = Path(os.environ["NER_DATA"])
langs = []
with coverage.open(newline="", encoding="utf-8") as handle:
    for row in csv.DictReader(handle, delimiter="\t"):
        lang = row.get("language_script") or row.get("language")
        if (
            lang
            and row.get("group") == "head"
            and row.get("in_task_list") == "yes"
            and row.get("has_data") == "yes"
            and (data / f"test-{lang}.tsv").exists()
        ):
            langs.append(lang)
print(" ".join(langs))
PY
  mv "${HEAD_LANGS_FILE}.tmp" "${HEAD_LANGS_FILE}"
}

head_count() {
  wc -w < "${HEAD_LANGS_FILE}" | tr -d ' '
}

result_count() {
  local key="$1"
  completed_languages "${key}" | awk 'NF {n++} END {print n+0}'
}

completed_languages() {
  local key="$1"
  local result_dir="${V52_ROOT}/evaluation/ner_head/${key}"
  [[ -d "${result_dir}" ]] || return 0
  find "${result_dir}" -name test_results.txt -type f -size +0c 2>/dev/null \
    | sort \
    | while IFS= read -r file; do
        awk -F '=' '/^language=/ {print $2}' "${file}"
      done \
    | awk 'NF && !seen[$0]++'
}

missing_languages() {
  local key="$1"
  local done_file
  done_file="$(mktemp "${LOG_DIR}/done_langs.XXXXXX")"
  completed_languages "${key}" > "${done_file}"
  awk -v done_file="${done_file}" '
    BEGIN {
      while ((getline line < done_file) > 0) {
        if (line != "") done[line] = 1
      }
      close(done_file)
    }
    {
      for (i = 1; i <= NF; i++) {
        if (!done[$i]) {
          if (n++ > 0) printf " "
          printf "%s", $i
        }
      }
    }
    END {printf "\n"}
  ' "${HEAD_LANGS_FILE}"
  rm -f "${done_file}"
}

archive_partial_results() {
  local current_result="$1" out_prefix="$2" gpu="$3"
  [[ -s "${current_result}" ]] || return 0
  local archive_dir
  archive_dir="${out_prefix}/partial_gpu${gpu}_$(date '+%Y%m%d_%H%M%S')_$$"
  mkdir -p "${archive_dir}"
  cp -f "${current_result}" "${archive_dir}/test_results.txt"
}

copy_tokenizer_files() {
  local source_dir="$1" out_dir="$2"
  mkdir -p "${out_dir}"
  local name
  for name in sentencepiece.bpe.model tokenizer_config.json special_tokens_map.json config.json; do
    if [[ -f "${source_dir}/${name}" ]]; then
      cp -f "${source_dir}/${name}" "${out_dir}/${name}"
    fi
  done
}

tokenizer_dir_for() {
  local source_dir="$1" model_path="$2" best_checkpoint="$3"
  local candidate
  for candidate in "${source_dir}" "${best_checkpoint}" "${model_path}"; do
    if [[ -n "${candidate}" && -f "${candidate}/sentencepiece.bpe.model" ]]; then
      printf '%s\n' "${candidate}"
      return 0
    fi
  done
  printf '%s\n' "${source_dir}"
}

run_one() {
  local index="$1" method="$2" step="$3" key="$4" model_path="$5" source_dir="$6" best_checkpoint="$7" gpu="$8"
  local expected out_prefix out_dir link_path log_file status_file count tokenizer_dir predict_langs current_result
  expected="$(head_count)"
  count="$(result_count "${key}" "${expected}")"
  if [[ "${count}" -ge "${expected}" && "${expected}" -gt 0 ]]; then
    printf '[skip] ner_head %s already complete %s/%s %s\n' "${key}" "${count}" "${expected}" "$(date '+%F %T')"
    return 0
  fi

  tokenizer_dir="$(tokenizer_dir_for "${source_dir}" "${model_path}" "${best_checkpoint}")"
  link_path="${LINK_DIR}/shared_tokenizer_gpu${gpu}"
  ln -sfn "${tokenizer_dir}" "${link_path}"
  out_prefix="${V52_ROOT}/evaluation/ner_head/${key}"
  out_dir="${out_prefix}/$(basename "${link_path}")"
  copy_tokenizer_files "${tokenizer_dir}" "${out_dir}"
  current_result="${out_dir}/test_results.txt"
  predict_langs="$(missing_languages "${key}")"
  if [[ -z "${predict_langs}" ]]; then
    printf '[fail] ner_head %s has no missing languages but count=%s/%s\n' "${key}" "${count}" "${expected}" >&2
    return 1
  fi
  archive_partial_results "${current_result}" "${out_prefix}" "${gpu}"

  log_file="${LOG_DIR}/${index}_ner_head_${key}_gpu${gpu}.log"
  status_file="${LOG_DIR}/status_gpu${gpu}.tsv"
  printf 'index\tmethod\tstep\tmodel_key\tgpu\tstatus\tstarted_at\tfinished_at\tlanguages\n' > "${status_file}"
  printf '%s\t%s\t%s\t%s\t%s\trunning\t%s\t\t%s\n' \
    "${index}" "${method}" "${step}" "${key}" "${gpu}" "$(date '+%FT%T')" "${count}/${expected}" >> "${status_file}"

  printf '[start] ner_head %s gpu=%s head_langs=%s %s\n' "${key}" "${gpu}" "${expected}" "$(date '+%F %T')"
  set +e
  (
    cd "${ROOT}/evaluation/tagging"
    CUDA_VISIBLE_DEVICES="${gpu}" \
    NER_PREDICT_LANGS="${predict_langs}" \
    "${PYTHON_BIN}" evaluate_ner.py \
      --model_type xlmr \
      --model_name_or_path "${link_path}" \
      --data_dir "${NER_DATA%/}/" \
      --labels "${NER_DATA%/}/labels.txt" \
      --output_dir "${out_prefix%/}/" \
      --max_seq_len "${MAX_LENGTH}" \
      --per_gpu_eval_batch_size "${EVAL_BATCH_SIZE}" \
      --seed "${SEED}" \
      --do_predict \
      --train_langs eng_Latn \
      --init_checkpoint "${best_checkpoint}" \
      --overwrite_output_dir
  ) > "${log_file}" 2>&1
  local rc=$?
  set -e
  count="$(result_count "${key}" "${expected}")"
  if [[ "${rc}" -eq 0 && "${count}" -ge "${expected}" ]]; then
    printf '%s\t%s\t%s\t%s\t%s\tcomplete\t\t%s\t%s/%s\n' \
      "${index}" "${method}" "${step}" "${key}" "${gpu}" "$(date '+%FT%T')" "${count}" "${expected}" >> "${status_file}"
    printf '[done] ner_head %s gpu=%s %s/%s %s\n' "${key}" "${gpu}" "${count}" "${expected}" "$(date '+%F %T')"
    return 0
  fi
  printf '%s\t%s\t%s\t%s\t%s\tfailed_rc%s\t\t%s\t%s/%s\n' \
    "${index}" "${method}" "${step}" "${key}" "${gpu}" "${rc}" "$(date '+%FT%T')" "${count}" "${expected}" >> "${status_file}"
  printf '[fail] ner_head %s gpu=%s rc=%s count=%s/%s log=%s\n' "${key}" "${gpu}" "${rc}" "${count}" "${expected}" "${log_file}" >&2
  return "${rc}"
}

run_shard() {
  local shard="${1:?missing shard}" gpu="${2:?missing gpu}" total="${3:?missing total}"
  if [[ "${REFRESH_QUEUE:-1}" == "1" || ! -s "${HEAD_LANGS_FILE}" || ! -s "${QUEUE_FILE}" ]]; then
    write_head_langs
    write_queue
  fi
  local expected
  expected="$(head_count)"
  if [[ "${expected}" -le 0 ]]; then
    printf '[fail] no NER head languages found from %s\n' "${COVERAGE}" >&2
    return 1
  fi
  tail -n +2 "${QUEUE_FILE}" | while IFS=$'\t' read -r index method step key model_path source_dir best_checkpoint; do
    if (( index % total != shard )); then
      continue
    fi
    run_one "${index}" "${method}" "${step}" "${key}" "${model_path}" "${source_dir}" "${best_checkpoint}" "${gpu}"
  done
}

wait_for_pids() {
  local pids="${WAIT_PIDS:-}"
  [[ -n "${pids}" ]] || return 0
  printf '[wait] waiting for pids: %s %s\n' "${pids}" "$(date '+%F %T')"
  local alive=1
  while [[ "${alive}" -eq 1 ]]; do
    alive=0
    local pid
    for pid in ${pids}; do
      if kill -0 "${pid}" 2>/dev/null; then
        alive=1
      fi
    done
    [[ "${alive}" -eq 1 ]] && sleep 20
  done
}

stop_pgid_if_requested() {
  local pgid="${KILL_AFTER_WAIT_PGID:-}"
  [[ -n "${pgid}" ]] || return 0
  printf '[stop] stopping previous process group %s before NER head %s\n' "${pgid}" "$(date '+%F %T')"
  kill -TERM "-${pgid}" 2>/dev/null || true
  sleep 3
}

run_all() {
  write_head_langs
  write_queue
  export REFRESH_QUEUE=0
  local gpu_list=(${GPUS})
  local total="${#gpu_list[@]}"
  local shard=0
  for gpu in "${gpu_list[@]}"; do
    bash "$0" shard "${shard}" "${gpu}" "${total}" &
    shard=$((shard + 1))
  done
  wait
}

mode="${1:-all}"
case "${mode}" in
  shard)
    run_shard "${2:?missing shard}" "${3:?missing gpu}" "${4:?missing total}"
    ;;
  all)
    run_all
    ;;
  after-wait)
    wait_for_pids
    stop_pgid_if_requested
    run_all
    ;;
  queue)
    write_head_langs
    write_queue
    printf 'head_langs=%s\n' "$(head_count)"
    printf 'queue=%s\n' "${QUEUE_FILE}"
    printf 'missing=%s\n' "${MISSING_FILE}"
    ;;
  *)
    printf 'usage: %s [all|after-wait|queue|shard SHARD GPU TOTAL]\n' "$0" >&2
    exit 2
    ;;
esac
