# 15Palle Raspberry Pi

Headless QR scanner (`scanner.py`) and optional fullscreen **kiosk browser** for the check-in display.

## 1. Configuration

Copy `.env.example` to `.env` and fill in:

| Variable | Used by | Purpose |
|----------|---------|---------|
| `API_URL` | `scanner.py` | `POST` check-in endpoint |
| `API_KEY` | `scanner.py` | `x-api-key` for the API |
| `KIOSK_URL` | `kiosk-display.sh` | Full URL to open in Chromium kiosk mode |

Set permissions so secrets are not world-readable:

```bash
chmod 600 .env
```

### Website: `KIOSK_ACCESS_SECRET`

On the Next.js deployment (e.g. AWS Amplify), set **`KIOSK_ACCESS_SECRET`** to a long random string (same value you put in `KIOSK_URL` as the `token` query parameter).

- First visit with `?token=...` exchanges the token for an **HttpOnly** cookie (valid 1 year).
- After that, the Pi can use `https://15palle.com/kiosk` **without** the token in the URL if the browser profile still has the cookie (e.g. after reboot).

**Security:** anyone who can read the Pi’s `.env` or the Chromium command line can see the token. Lock down the Pi (no untrusted shell access), and avoid logging `KIOSK_URL` in plain text.

## 2. QR scanner (headless)

`launcher.sh` waits for the network, updates git, installs `requirements.txt`, and runs `scanner.py`.

Autostart (example with systemd — adjust paths):

```ini
[Unit]
Description=15Palle QR scanner
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=raspberry
WorkingDirectory=/home/raspberry/scanner/15PalleRaspberry
ExecStart=/home/raspberry/scanner/15PalleRaspberry/launcher.sh
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable: `sudo systemctl enable --now 15palle-scanner.service` (after copying the unit to `/etc/systemd/system/`).

## 3. Fullscreen kiosk (HDMI display)

Use a **desktop** Raspberry Pi OS image (or Lite + X11 / Wayland + desktop) so Chromium can run fullscreen.

1. Install Chromium if needed: `sudo apt install chromium-browser`
2. Copy `.env.example` → `.env` and set **`KIOSK_URL`** (and scanner keys).
3. **Automatic kiosk after every reboot (recommended)** — run **once** in the repo folder, as the same user that auto-logs into the desktop (often `raspberry`):
   ```bash
   cd /home/raspberry/scanner/15PalleRaspberry   # your path
   chmod +x install-kiosk-autostart.sh kiosk-display.sh
   ./install-kiosk-autostart.sh
   ```
   This installs `~/.config/autostart/15palle-kiosk.desktop`, so **`kiosk-display.sh` starts when the graphical session starts** (after login). Enable **desktop auto-login** in Raspberry Pi OS settings if the machine should open the session without a password after boot.

4. Reboot: the browser should open fullscreen on the kiosk URL after network is ready (`kiosk-display.sh` waits for ping before launching Chromium).

Manual test without autostart: `./kiosk-display.sh`

### Why autostart instead of systemd for the browser?

Chromium needs your **logged-in graphical session** (X11/Wayland). A system-wide systemd unit often starts **before** the desktop or without the right `DISPLAY`/Xauthority, so the kiosk is unreliable. The **desktop autostart** entry runs in the user session, which matches how Raspberry Pi OS is meant to run a fullscreen browser.

Optional: if you prefer systemd, use a **user** service (`systemctl --user`) with `loginctl enable-linger` — not included here; autostart is the usual Pi pattern.

Example systemd unit (system level — only if you know your display stack):

```ini
[Unit]
Description=15Palle kiosk browser
After=network-online.target graphical-session.target
Wants=network-online.target

[Service]
Type=simple
User=raspberry
Environment=DISPLAY=:0
WorkingDirectory=/home/raspberry/scanner/15PalleRaspberry
ExecStart=/home/raspberry/scanner/15PalleRaspberry/kiosk-display.sh
Restart=on-failure
RestartSec=5

[Install]
WantedBy=graphical.target
```

Ensure the Pi boots to desktop (auto-login optional) and `DISPLAY=:0` matches your setup.

### Plug / unplug monitor

- **Power / boot:** both `launcher.sh` (scanner) and `kiosk-display.sh` wait for **ping to the internet** before starting, so short network delays after boot are handled.
- **HDMI:** if the screen stays black when you plug the cable after boot, enable **HDMI force hotplug** in `/boot/firmware/config.txt` (`hdmi_force_hotplug=1`) on Raspberry Pi OS, then reboot once.

## 4. Same Pi: scanner + kiosk

Run **two** services: one for `launcher.sh`, one for `kiosk-display.sh`. They share the same `.env` but do not block each other.
