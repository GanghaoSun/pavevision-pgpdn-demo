#!/usr/bin/env sh
set -eu

PROJECT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PYTHON_BIN="${PAVEVISION_PYTHON:-python3}"

cd "$PROJECT_DIR"

if ! "$PYTHON_BIN" -c "import flask" >/dev/null 2>&1; then
  "$PYTHON_BIN" -m pip install -r web_demo/requirements.txt
fi

echo "Starting PaveVision public web demo at http://localhost:5000"
cd "$PROJECT_DIR/web_demo"
"$PYTHON_BIN" app.py
