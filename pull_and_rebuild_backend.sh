#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/home/asistentes/ProDus/ProDus_Registro_de_Horas_Backend"
APP_DIR="$REPO_DIR/backend"
VENV_DIR="/home/asistentes/ProDus/venv"

echo "[BACK] git pull..."
git -C "$REPO_DIR" pull --ff-only

echo "[BACK] activar venv e instalar dependencias..."
source "$VENV_DIR/bin/activate"
pip install -r "$APP_DIR/requirements.txt"

echo "[BACK] migraciones + static..."
cd "$APP_DIR"
python manage.py migrate
python manage.py collectstatic --noinput

echo "[BACK] reiniciar servicio..."
sudo systemctl restart produs-backend
sudo systemctl status produs-backend --no-pager