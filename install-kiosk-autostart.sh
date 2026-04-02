#!/bin/bash
# Run once on the Pi (desktop image, logged in as the user that should see the kiosk).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/autostart"
DESKTOP_FILE="$DESKTOP_DIR/15palle-kiosk.desktop"

if [ ! -x "$SCRIPT_DIR/kiosk-display.sh" ]; then
  chmod +x "$SCRIPT_DIR/kiosk-display.sh"
fi

mkdir -p "$DESKTOP_DIR"

cat >"$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=15 Palle Kiosk
Comment=Fullscreen check-in display (Chromium kiosk)
Exec=$SCRIPT_DIR/kiosk-display.sh
Path=$SCRIPT_DIR
Terminal=false
X-GNOME-Autostart-enabled=true
StartupNotify=false
EOF

echo "Installed autostart: $DESKTOP_FILE"
echo "It runs after you log into the desktop. Reboot or log out/in to test."
echo "Requires: .env with KIOSK_URL, and Raspberry Pi OS Desktop (or any DE that reads ~/.config/autostart)."
