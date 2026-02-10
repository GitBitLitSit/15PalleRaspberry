






#!/bin/bash

# --- CONFIGURATION ---
REPO_DIR="/home/raspberry/scanner/15PalleRaspberry"  # CHANGE THIS to your actual folder name
SCRIPT_NAME="scanner.py"            # Name of your python script
VENV_DIR="$REPO_DIR/venv"           # Virtual environment directory
# ---------------------

# 1. Navigate to the directory
cd "$REPO_DIR" || exit 1

# 2. Wait for Network (Critical for Git Pull & API)
# This loops until it can ping google.com, ensuring internet is ready
echo "[Launcher] Waiting for internet connection..."
until ping -c 1 google.com &> /dev/null
do
  sleep 5
done
echo "[Launcher] Internet connected."

# 3. Update Code from Git
echo "[Launcher] Checking for updates..."
# Reset local changes to avoid conflicts (force overwrite local files with remote)
git reset --hard HEAD
git pull origin master	

# 4. Setup/Update Virtual Environment
if [ ! -d "$VENV_DIR" ]; then
    echo "[Launcher] Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate the environment
source "$VENV_DIR/bin/activate"

# 5. Install Dependencies
# This ensures new libraries (like python-dotenv) are installed automatically
if [ -f "requirements.txt" ]; then
    echo "[Launcher] Installing requirements..."
    pip install -r requirements.txt
fi

# 6. Run the Python Script
echo "[Launcher] Starting scanner..."
python "$SCRIPT_NAME"
