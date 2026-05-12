#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTOMATION_DIR="$SCRIPT_DIR"
JOBS_DIR="$AUTOMATION_DIR/jobs"
LOG_DIR="$AUTOMATION_DIR/logs"

mkdir -p "$LOG_DIR"
AUTOMATION_LOG="$LOG_DIR/automation.log"

now() {
  date '+%Y-%m-%d %H:%M:%S%z'
}

resolve_job_file() {
  local input="$1"

  if [[ -f "$JOBS_DIR/$input" ]]; then
    basename "$input"
    return 0
  fi

  if [[ "$input" != *.bash ]] && [[ -f "$JOBS_DIR/${input}.bash" ]]; then
    basename "${input}.bash"
    return 0
  fi

  if [[ "$input" != *.sh ]] && [[ -f "$JOBS_DIR/${input}.sh" ]]; then
    basename "${input}.sh"
    return 0
  fi

  return 1
}

if [[ $# -lt 1 ]]; then
  echo "Uso: $0 <job_name>"
  exit 1
fi

JOB_INPUT="$1"
if ! JOB_FILE="$(resolve_job_file "$JOB_INPUT")"; then
  echo "Job no encontrado: $JOB_INPUT"
  exit 1
fi

JOB_NAME="${JOB_FILE%.*}"
JOB_LOG="$LOG_DIR/${JOB_NAME}.log"

START_TS="$(now)"
echo "[$START_TS] RUN_JOB START job=$JOB_FILE" | tee -a "$AUTOMATION_LOG" >> "$JOB_LOG"

set +e
"$JOBS_DIR/$JOB_FILE" >> "$JOB_LOG" 2>&1
EXIT_CODE=$?
set -e

END_TS="$(now)"
if [[ $EXIT_CODE -eq 0 ]]; then
  echo "[$END_TS] RUN_JOB OK job=$JOB_FILE exit_code=$EXIT_CODE" | tee -a "$AUTOMATION_LOG" >> "$JOB_LOG"
else
  echo "[$END_TS] RUN_JOB FAIL job=$JOB_FILE exit_code=$EXIT_CODE" | tee -a "$AUTOMATION_LOG" >> "$JOB_LOG"
fi

exit $EXIT_CODE
