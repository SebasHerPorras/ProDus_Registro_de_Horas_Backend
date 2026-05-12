#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTOMATION_DIR="$SCRIPT_DIR"
ENABLED_DIR="$AUTOMATION_DIR/enabled"
LOG_DIR="$AUTOMATION_DIR/logs"

mkdir -p "$ENABLED_DIR" "$LOG_DIR"
AUTOMATION_LOG="$LOG_DIR/automation.log"

now() {
  date '+%Y-%m-%d %H:%M:%S%z'
}

disable_one() {
  local job_name="$1"
  local marker="AUTO_JOB:${job_name}"

  rm -f "$ENABLED_DIR/${job_name}.enabled"

  local current_cron
  current_cron="$(crontab -l 2>/dev/null || true)"
  local cleaned_cron
  cleaned_cron="$(printf "%s\n" "$current_cron" | grep -v "$marker" || true)"

  if [[ -n "$cleaned_cron" ]]; then
    printf "%s\n" "$cleaned_cron" | crontab -
  else
    crontab -r >/dev/null 2>&1 || true
  fi

  echo "[$(now)] DISABLE job=${job_name}" | tee -a "$AUTOMATION_LOG"
}

if [[ $# -lt 1 ]]; then
  echo "Uso: $0 <job_name|--all>"
  exit 1
fi

if [[ "$1" == "--all" ]]; then
  shopt -s nullglob
  flags=("$ENABLED_DIR"/*.enabled)
  shopt -u nullglob

  for path in "${flags[@]}"; do
    disable_one "$(basename "$path" .enabled)"
  done

  exit 0
fi

INPUT="$1"
INPUT="${INPUT%.bash}"
INPUT="${INPUT%.sh}"

disable_one "$INPUT"
