#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTOMATION_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKEND_DIR="$(cd "$AUTOMATION_DIR/.." && pwd)"

PYTHON_BIN="${PYTHON_BIN:-python3}"

cd "$BACKEND_DIR"
"$PYTHON_BIN" manage.py auto_close_open_time_logs
