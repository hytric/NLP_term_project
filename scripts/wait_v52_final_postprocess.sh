#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/home/axt/jongha/Glot500-py39-eval}"
LOG_DIR="${LOG_DIR:-/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/final_postprocess}"
WATCH_PIDS="${WATCH_PIDS:-}"
SLEEP_SECONDS="${SLEEP_SECONDS:-300}"

mkdir -p "${LOG_DIR}"
cd "${ROOT}"

log_file="${LOG_DIR}/wait_and_render_$(date +%Y%m%d_%H%M%S).log"

any_alive() {
  local pid
  for pid in ${WATCH_PIDS}; do
    if kill -0 "${pid}" 2>/dev/null; then
      return 0
    fi
  done
  return 1
}

{
  echo "[start] $(date '+%F %T %Z') waiting for: ${WATCH_PIDS}"
  while any_alive; do
    echo "[wait] $(date '+%F %T %Z') launchers still active"
    sleep "${SLEEP_SECONDS}"
  done
  echo "[render] $(date '+%F %T %Z') rendering downstream tables"
  python3 scripts/render_v52_inference_tables.py \
    --tasks pppl,retrieval_tatoeba,retrieval_bible,roundtrip_alignment,text_classification,ner,pos
  echo "[render] $(date '+%F %T %Z') refreshing similarity map grids"
  python3 scripts/render_v52_similarity_map_grids.py
  echo "[done] $(date '+%F %T %Z')"
} >> "${log_file}" 2>&1
