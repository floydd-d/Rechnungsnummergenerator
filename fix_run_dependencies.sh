#!/usr/bin/env bash
set -euo pipefail

# This helper rebuilds the virtual environment with the fixed dependency versions
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"

if [ -d "$VENV_DIR" ]; then
    echo "Removing existing virtual environment at $VENV_DIR"
    rm -rf "$VENV_DIR"
fi

echo "Creating a fresh virtual environment with the best available Python..."
if command -v python3.6 &> /dev/null; then
    PYTHON_CMD=python3.6
elif command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    echo "Error: python3 not found"
    exit 1
fi

$PYTHON_CMD -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r "$PROJECT_DIR/requirements.txt"
echo "Finished rebuilding venv. Run ./run.sh 5000 to start the app."
