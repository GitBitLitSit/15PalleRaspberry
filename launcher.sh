#!/bin/bash

# 1. Get the directory dynamically (no hardcoded usernames!)
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_NAME="scanner.py"

cd "$REPO_DIR" || exit 1

# 2. Wait for Network with a Timeout (Max 60 seconds)
echo "[Launcher] Waiting for internet connection..."
for i in {1..12}; do
  if ping -c 1 -W 2 google.com &> /dev/null; then
    echo "[Launcher] Internet connected."
    break
  fi
  sleep 5
done

# 3. Update Code from Git (Fail gracefully if offline)
echo "[Launcher] Checking for updates..."
git reset --hard HEAD
git pull origin master || echo "[Launcher] Git pull failed, using local version."

# 4. Set up Virtual Environment (Fixes the Python crash)
echo "[Launcher] Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
# Activate the virtual environment
source venv/bin/activate

# Install requirements inside the venv
if [ -f "requirements.txt" ]; then
    echo "[Launcher] Installing/Verifying requirements..."
    pip install -r requirements.txt
fi

# 5. Run the Python Script
echo "[Launcher] Starting scanner..."
python "$SCRIPT_NAME"