#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTOMATION_DIR="$SCRIPT_DIR"
ENABLED_DIR="$AUTOMATION_DIR/enabled"
LOG_DIR="$AUTOMATION_DIR/logs"
RUN_JOB_SCRIPT="$AUTOMATION_DIR/run_job.bash"

mkdir -p "$LOG_DIR" "$ENABLED_DIR"
AUTOMATION_LOG="$LOG_DIR/automation.log"

now() {
  date '+%Y-%m-%d %H:%M:%S%z'
}

shopt -s nullglob
ENABLED_FLAGS=("$ENABLED_DIR"/*.enabled)
shopt -u nullglob

if [[ ${#ENABLED_FLAGS[@]} -eq 0 ]]; then
  MSG="[$(now)] RUN_ENABLED SKIP reason=no_enabled_jobs"
  echo "$MSG" | tee -a "$AUTOMATION_LOG"
  exit 0
fi

TOTAL=0
FAILED=0

for flag in "${ENABLED_FLAGS[@]}"; do
  job_name="$(basename "$flag" .enabled)"
  TOTAL=$((TOTAL + 1))

  set +e
  "$RUN_JOB_SCRIPT" "$job_name"
  EXIT_CODE=$?
  set -e

  if [[ $EXIT_CODE -ne 0 ]]; then
    FAILED=$((FAILED + 1))
  fi
done

MSG="[$(now)] RUN_ENABLED END total=$TOTAL failed=$FAILED"
echo "$MSG" | tee -a "$AUTOMATION_LOG"

if [[ $FAILED -gt 0 ]]; then
  exit 1
fi

exit 0
