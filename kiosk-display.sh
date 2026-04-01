#!/bin/bash
set -euo pipefail

# Full path to this repo on the Pi (match launcher.sh)
REPO_DIR="${REPO_DIR:-/home/raspberry/scanner/15PalleRaspberry}"

cd "$REPO_DIR" || exit 1

if [ ! -f ".env" ]; then
  echo "[kiosk-display] Missing .env — copy .env.example and set KIOSK_URL (and API_* for the scanner)." >&2
  exit 1
fi

# shellcheck disable=SC1091
set -a
source ".env"
set +a

if [ -z "${KIOSK_URL:-}" ]; then
  echo "[kiosk-display] KIOSK_URL is not set in .env" >&2
  echo "  Example: KIOSK_URL=https://15palle.com/kiosk?token=YOUR_KIOSK_ACCESS_SECRET" >&2
  exit 1
fi

echo "[kiosk-display] Waiting for network..."
until ping -c 1 -W 3 google.com &>/dev/null; do
  sleep 3
done

export DISPLAY="${DISPLAY:-:0}"

# Raspberry Pi OS: chromium or chromium-browser
if command -v chromium-browser &>/dev/null; then
  CHROME=(chromium-browser)
elif command -v chromium &>/dev/null; then
  CHROME=(chromium)
else
  echo "[kiosk-display] Install Chromium: sudo apt install chromium-browser" >&2
  exit 1
fi

echo "[kiosk-display] Starting fullscreen kiosk (${CHROME[*]})..."

exec "${CHROME[@]}" \
  --kiosk \
  --noerrdialogs \
  --disable-infobars \
  --disable-session-crashed-bubble \
  --disable-restore-session-state \
  --check-for-update-interval=31536000 \
  --password-store=basic \
  "$KIOSK_URL"
