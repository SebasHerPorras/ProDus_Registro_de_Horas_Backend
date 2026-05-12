#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTOMATION_DIR="$SCRIPT_DIR"
JOBS_DIR="$AUTOMATION_DIR/jobs"
SCHEDULES_DIR="$AUTOMATION_DIR/schedules"
ENABLED_DIR="$AUTOMATION_DIR/enabled"
LOG_DIR="$AUTOMATION_DIR/logs"

mkdir -p "$ENABLED_DIR" "$LOG_DIR"
AUTOMATION_LOG="$LOG_DIR/automation.log"

now() {
  date '+%Y-%m-%d %H:%M:%S%z'
}

enable_one() {
  local job_file="$1"
  local job_name="${job_file%.*}"
  local schedule_file="$SCHEDULES_DIR/${job_name}.cron"
  local schedule_expr

  if [[ ! -f "$schedule_file" ]]; then
    echo "No hay horario para $job_name. Crea: $schedule_file" | tee -a "$AUTOMATION_LOG"
    return 1
  fi

  schedule_expr="$(grep -v '^\s*#' "$schedule_file" | sed '/^\s*$/d' | head -n 1 | xargs)"
  if [[ -z "$schedule_expr" ]]; then
    echo "Horario vacío para $job_name en $schedule_file" | tee -a "$AUTOMATION_LOG"
    return 1
  fi

  if [[ "$(awk '{print NF}' <<< "$schedule_expr")" -ne 5 ]]; then
    echo "Horario inválido para $job_name: '$schedule_expr'" | tee -a "$AUTOMATION_LOG"
    return 1
  fi

  touch "$ENABLED_DIR/${job_name}.enabled"

  local marker="# AUTO_JOB:${job_name}"
  local cron_cmd="cd $AUTOMATION_DIR && ./run_job.bash $job_name >> $LOG_DIR/cron.log 2>&1"
  local cron_line="$schedule_expr $cron_cmd $marker"

  local current_cron
  current_cron="$(crontab -l 2>/dev/null || true)"
  local cleaned_cron
  cleaned_cron="$(printf "%s\n" "$current_cron" | grep -v "AUTO_JOB:${job_name}" || true)"

  if [[ -n "$cleaned_cron" ]]; then
    printf "%s\n%s\n" "$cleaned_cron" "$cron_line" | crontab -
  else
    printf "%s\n" "$cron_line" | crontab -
  fi

  echo "[$(now)] ENABLE job=$job_file schedule='$schedule_expr'" | tee -a "$AUTOMATION_LOG"
  return 0
}

if [[ $# -lt 1 ]]; then
  echo "Uso: $0 <job_name|--all>"
  exit 1
fi

if [[ "$1" == "--all" ]]; then
  shopt -s nullglob
  jobs=("$JOBS_DIR"/*.bash "$JOBS_DIR"/*.sh)
  shopt -u nullglob

  if [[ ${#jobs[@]} -eq 0 ]]; then
    echo "No hay jobs para activar en $JOBS_DIR"
    exit 0
  fi

  failed=0
  for path in "${jobs[@]}"; do
    if ! enable_one "$(basename "$path")"; then
      failed=$((failed + 1))
    fi
  done

  if [[ $failed -gt 0 ]]; then
    echo "No se pudieron habilitar $failed jobs (revisa horario en schedules/)."
    exit 1
  fi

  exit 0
fi

INPUT="$1"
if [[ -f "$JOBS_DIR/$INPUT" ]]; then
  enable_one "$(basename "$INPUT")"
elif [[ -f "$JOBS_DIR/${INPUT}.bash" ]]; then
  enable_one "${INPUT}.bash"
elif [[ -f "$JOBS_DIR/${INPUT}.sh" ]]; then
  enable_one "${INPUT}.sh"
else
  echo "Job no encontrado: $INPUT"
  exit 1
fi
