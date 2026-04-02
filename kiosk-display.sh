#!/bin/bash
set -euo pipefail

# Dynamic directory path
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR" || exit 1

if [ ! -f ".env" ]; then
  echo "[kiosk-display] Missing .env file!" >&2
  exit 1
fi

# Load .env variables
set -a
source ".env"
set +a

if [ -z "${KIOSK_URL:-}" ]; then
  echo "[kiosk-display] KIOSK_URL is not set in .env" >&2
  exit 1
fi

echo "[kiosk-display] Waiting for network (max 60s)..."
for i in {1..12}; do
  if ping -c 1 -W 2 google.com &> /dev/null; then
    break
  fi
  sleep 5
done

# Export DISPLAY if we are on X11, otherwise let Wayland handle it naturally
export DISPLAY="${DISPLAY:-:0}"

if command -v chromium-browser &>/dev/null; then
  CHROME=(chromium-browser)
elif command -v chromium &>/dev/null; then
  CHROME=(chromium)
else
  echo "[kiosk-display] Install Chromium first!" >&2
  exit 1
fi

echo "[kiosk-display] Starting fullscreen kiosk..."

exec "${CHROME[@]}" \
  --kiosk \
  --noerrdialogs \
  --disable-infobars \
  --disable-session-crashed-bubble \
  --disable-restore-session-state \
  --lang=it \
  --password-store=basic \
  --force-device-scale-factor=0.75 \
  "$KIOSK_URL"