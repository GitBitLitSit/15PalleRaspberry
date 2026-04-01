#!/bin/bash

# --- CONFIGURATION ---
REPO_DIR="/home/raspberry/scanner/15PalleRaspberry"
SCRIPT_NAME="scanner.py"

# 1. Navigate to the directory
cd "$REPO_DIR" || exit 1

# 2. Wait for Network (Critical for Git Pull & API)
echo "[Launcher] Waiting for internet connection..."
until ping -c 1 google.com &> /dev/null
do
  sleep 5
done
echo "[Launcher] Internet connected."

# 3. Update Code from Git
echo "[Launcher] Checking for updates..."
git reset --hard HEAD
git pull origin master

# 4. Install Dependencies INTO SYSTEM PYTHON (no venv)
if [ -f "requirements.txt" ]; then
    echo "[Launcher] Installing requirements..."
    pip3 install -r requirements.txt
fi

# 5. Run the Python Script with system Python
echo "[Launcher] Starting scanner..."
python3 "$SCRIPT_NAME"