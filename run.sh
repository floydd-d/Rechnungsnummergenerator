#!/bin/bash

# Rechnungsnummergenerator - Run Script
# This script installs dependencies and starts the Flask application

set -e

echo "================================"
echo "Rechnungsnummergenerator für Atchen"
echo "================================"
echo ""

# Choose the best available Python interpreter
if command -v python3.6 &> /dev/null; then
    PYTHON_CMD=python3.6
elif command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    echo "Error: Python 3.6+ is not installed"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "Found Python: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade packaging tools and install requirements
echo ""
echo "Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip setuptools wheel

echo ""
echo "Installing dependencies..."
python -m pip install -r requirements.txt

# Get port from command line argument, default to 5000
PORT=${1:-5000}

echo ""
echo "================================"
echo "Starting application on port $PORT"
echo "Open your browser to: http://localhost:$PORT"
echo "================================"
echo ""

# Run the application
python3 app.py $PORT
