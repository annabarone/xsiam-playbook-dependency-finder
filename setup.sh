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

# Store the current directory
ORIGINAL_DIR=$(pwd)

# Change to the demisto content pack directory, fetch and pull latest
if [ -d "$DEMISTO_CONTENT_PACK_DIR_PATH" ]; then
    echo "Updating demisto content pack..."
    cd "$DEMISTO_CONTENT_PACK_DIR_PATH"
    git fetch
    git pull
    cd "$ORIGINAL_DIR"
else
    echo "Error: DEMISTO_CONTENT_PACK_DIR_PATH does not exist."
    exit 1
fi

# Check if the virtual environment directory exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install the required packages
echo "Installing requirements..."
pip install -r requirements.txt

# Run the python scripts in order
echo "Running python scripts..."
python content_pack_subdirs.py
python integration_commands.py
python scripts.py
python dependency_finder.py

echo "Setup complete."