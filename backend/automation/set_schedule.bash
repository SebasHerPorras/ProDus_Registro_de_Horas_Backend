#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTOMATION_DIR="$SCRIPT_DIR"
JOBS_DIR="$AUTOMATION_DIR/jobs"
SCHEDULES_DIR="$AUTOMATION_DIR/schedules"
LOG_DIR="$AUTOMATION_DIR/logs"

mkdir -p "$SCHEDULES_DIR" "$LOG_DIR"
AUTOMATION_LOG="$LOG_DIR/automation.log"

now() {
  date '+%Y-%m-%d %H:%M:%S%z'
}

resolve_job_name() {
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

if [[ $# -lt 2 ]]; then
  echo "Uso: $0 <job_name> \"<cron_expr>\""
  echo "Ejemplo: $0 close_open_time_logs \"0 0 * * *\""
  echo "Ejemplo: $0 close_open_time_logs \"0 7 * * 3\""
  exit 1
fi

JOB_INPUT="$1"
CRON_EXPR="$2"

if ! JOB_FILE="$(resolve_job_name "$JOB_INPUT")"; then
  echo "Job no encontrado: $JOB_INPUT"
  exit 1
fi

if [[ "$(awk '{print NF}' <<< "$CRON_EXPR")" -ne 5 ]]; then
  echo "Expresión cron inválida. Debe tener 5 campos (min hora día mes día_semana)."
  exit 1
fi

JOB_NAME="${JOB_FILE%.*}"
SCHEDULE_FILE="$SCHEDULES_DIR/${JOB_NAME}.cron"
printf "%s\n" "$CRON_EXPR" > "$SCHEDULE_FILE"

echo "[$(now)] SET_SCHEDULE job=$JOB_FILE expr=\"$CRON_EXPR\"" | tee -a "$AUTOMATION_LOG"
echo "Horario actualizado para $JOB_NAME: $CRON_EXPR"
