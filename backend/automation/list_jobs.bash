#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTOMATION_DIR="$SCRIPT_DIR"
JOBS_DIR="$AUTOMATION_DIR/jobs"
ENABLED_DIR="$AUTOMATION_DIR/enabled"
SCHEDULES_DIR="$AUTOMATION_DIR/schedules"

current_cron="$(crontab -l 2>/dev/null || true)"

read_schedule() {
  local job_name="$1"
  local schedule_file="$SCHEDULES_DIR/${job_name}.cron"

  if [[ ! -f "$schedule_file" ]]; then
    echo "N/A"
    return 0
  fi

  local expr
  expr="$(grep -v '^\s*#' "$schedule_file" | sed '/^\s*$/d' | head -n 1 | xargs)"
  if [[ -z "$expr" ]]; then
    echo "N/A"
  else
    echo "$expr"
  fi
}

shopt -s nullglob
jobs=("$JOBS_DIR"/*.bash "$JOBS_DIR"/*.sh)
shopt -u nullglob

if [[ ${#jobs[@]} -eq 0 ]]; then
  echo "No hay jobs registrados en $JOBS_DIR"
  exit 0
fi

echo "Jobs automáticos:"
for path in "${jobs[@]}"; do
  file="$(basename "$path")"
  name="${file%.*}"
  schedule="$(read_schedule "$name")"

  cron_state="NO"
  if grep -q "AUTO_JOB:${name}" <<< "$current_cron"; then
    cron_state="YES"
  fi

  if [[ -f "$ENABLED_DIR/${name}.enabled" ]]; then
    echo "- $name [ENABLED] schedule='$schedule' cron_installed=$cron_state"
  else
    echo "- $name [DISABLED] schedule='$schedule' cron_installed=$cron_state"
  fi
done
