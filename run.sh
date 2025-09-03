#!/bin/bash

# Exit on any error
set -e

# Check for .env file
if [ ! -f ".env" ]; then
    echo "Error: .env file not found."
    exit 1
fi

# Check for required variables in .env file
if ! grep -q "REPO_PATH=" .env || ! grep -q "DEMISTO_CONTENT_PACK_DIR_PATH=" .env; then
    echo "Error: REPO_PATH and DEMISTO_CONTENT_PACK_DIR_PATH must be defined in .env file."
    exit 1
fi

# Source the .env file
source .env

# Activate the virtual environment
source venv/bin/activate

# Run the python scripts in order
echo "Running python scripts..."
python dependency_finder.py
echo "Run complete."