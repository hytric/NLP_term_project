#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/home/axt/jongha/Glot500-py39-eval}"
GPU_RANDOM="${GPU_RANDOM:-0}"
GPU_FVT="${GPU_FVT:-1}"
WITH_PLOTS="${WITH_PLOTS:-1}"
SKIP_MEASURED="${SKIP_MEASURED:-1}"
DRY_RUN="${DRY_RUN:-0}"
FINAL_PACKET_REQUIRED="${FINAL_PACKET_REQUIRED:-1}"
LOG_DIR="${LOG_DIR:-/home/axt/mnt2/jongha/v5_glot50010/runs/finalization_logs}"

cd "${ROOT}"
mkdir -p "${LOG_DIR}"
LOG_FILE="${LOG_FILE:-${LOG_DIR}/run_v5_ready_to_final_package_$(date +%Y%m%d_%H%M%S).log}"
STATUS_CAPTURE="$(mktemp)"
trap 'rm -f "${STATUS_CAPTURE}"' EXIT

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')" "$*" | tee -a "${LOG_FILE}"
}

verdict_line() {
  local path="$1"
  printf '%s: ' "${path}" | tee -a "${LOG_FILE}"
  grep -m1 '^Verdict:' "${path}" 2>/dev/null | tee -a "${LOG_FILE}" || true
}

log "starting v5 ready-to-final-package launcher"
log "GPU_RANDOM=${GPU_RANDOM}; GPU_FVT=${GPU_FVT}; WITH_PLOTS=${WITH_PLOTS}; SKIP_MEASURED=${SKIP_MEASURED}; DRY_RUN=${DRY_RUN}; FINAL_PACKET_REQUIRED=${FINAL_PACKET_REQUIRED}"

log "checking post-checkpoint status gate"
bash scripts/run_v5_post_checkpoint_evals.sh status 2>&1 | tee "${STATUS_CAPTURE}" | tee -a "${LOG_FILE}"

if ! grep -q '^READY_TO_LAUNCH=yes$' "${STATUS_CAPTURE}"; then
  log "READY_TO_LAUNCH is not yes; refusing evaluation"
  grep '^READY_TO_LAUNCH' "${STATUS_CAPTURE}" | tee -a "${LOG_FILE}" || true
  grep '^NEXT_COMMAND=' "${STATUS_CAPTURE}" | tee -a "${LOG_FILE}" || true
  exit 2
fi

if [[ "${DRY_RUN}" == "1" ]]; then
  log "DRY_RUN=1; would launch guarded post-checkpoint evaluation and final refresh now"
  grep '^NEXT_COMMAND=' "${STATUS_CAPTURE}" | tee -a "${LOG_FILE}" || true
  exit 0
fi

log "status gate passed; launching guarded post-checkpoint evaluation"
SKIP_MEASURED="${SKIP_MEASURED}" WITH_PLOTS="${WITH_PLOTS}" GPU_RANDOM="${GPU_RANDOM}" GPU_FVT="${GPU_FVT}" \
  bash scripts/run_v5_post_checkpoint_evals.sh all 2>&1 | tee -a "${LOG_FILE}"

log "running final reporting refresh"
if [[ "${WITH_PLOTS}" == "1" ]]; then
  python3 scripts/refresh_v5_reporting.py --with-plots 2>&1 | tee -a "${LOG_FILE}"
else
  python3 scripts/refresh_v5_reporting.py 2>&1 | tee -a "${LOG_FILE}"
fi

log "final verdict summary"
verdict_line docs/exp/v5/4_reporting/final_evidence_packet_audit.md
verdict_line docs/exp/v5/4_reporting/final_deliverable_audit.md
verdict_line docs/exp/v5/4_reporting/reporting_package_audit.md
verdict_line docs/exp/v5/4_reporting/final_submission_smoke_audit.md
verdict_line docs/exp/v5/4_reporting/release_bundle_audit.md

if grep -q 'Verdict: `final_evidence_packet_ready`' docs/exp/v5/4_reporting/final_evidence_packet_audit.md; then
  log "FINAL_PACKET_READY=yes"
  exit 0
fi

log "FINAL_PACKET_READY=no"
if [[ "${FINAL_PACKET_REQUIRED}" == "1" ]]; then
  log "final evidence packet is not ready; leaving measured rows unpromoted"
  exit 3
fi

exit 0
