0bi
obi5295
Im Sprachchat

0bi — 07.02.2026 15:44
sounds intresting
MSA Nav

 — 07.02.2026 15:50
You got your pc ?
0bi — 07.02.2026 15:53
yes bro i have it
now it is time to shine
but not right
now i have to write some applications
MSA Nav

 — 07.02.2026 15:59
Noo
It's done with aws
They said hard no
We need to go the Google way
Disc ?
MSA Nav

 — 07.02.2026 16:38
Wait if you got the pc
Clash with the boys today?
At about 7
Or 8
0bi — 07.02.2026 17:27
hell nah sry bro
MSA Nav

 — 07.02.2026 17:27
Oki😭
MSA Nav

 — 08.02.2026 19:26
yoyooyoyoyo
less gooo cityyyyyyyyyyyyyyyyy
we did itttt
0bi — 08.02.2026 20:21
noway
peace at work at last xD
MSA Nav

 — gestern um 11:04 Uhr
yo bro when are you free so we can get a solution for the site
0bi — gestern um 11:09 Uhr
we can discuss that today
MSA Nav

 — gestern um 11:09 Uhr
yes sirrrrr
0bi — gestern um 21:43 Uhr
yo bro you got time after?
MSA Nav

 — gestern um 21:43 Uhr
yes sirr
0bi — gestern um 21:43 Uhr
i will pull up un 10-20 min
MSA Nav

 — gestern um 21:49 Uhr
so in 1 league game
MSA Nav

 — gestern um 22:34 Uhr
yoo
MSA Nav

 — gestern um 22:47 Uhr
https://www.flames.blue/?utm_source=sp_auto_dm&utm_referrer=sp_auto_dm
Flames.blue - AI App Builder
Build, deploy & monetize your app by chatting with AI
0bi — gestern um 22:53 Uhr
Raspberry
QwErTzUiOp!
Raspberry Pi ID 
Email: intify.dev@protonmail.com
Password: wu8@HbAPzm8pgZ]
MSA Nav

 — gestern um 23:04 Uhr
Bild
0bi — gestern um 23:14 Uhr
https://github.com/GitBitLitSit/15PalleRaspberry.git
GitHub
GitHub - GitBitLitSit/15PalleRaspberry: Repo for raspberry scanner
Repo for raspberry scanner. Contribute to GitBitLitSit/15PalleRaspberry development by creating an account on GitHub.
Repo for raspberry scanner. Contribute to GitBitLitSit/15PalleRaspberry development by creating an account on GitHub.
0bi — gestern um 23:38 Uhr
https://gemini.google.com/share/560bd76e0609
MSA Nav

 — gestern um 23:40 Uhr
ssh-keygen -t ed25519 -C "raspberry-pi-deploy-key"
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKK0MD0Zl/FDHhvcGh5ONCLy4VnfFAWSc4YAMFxEV55A raspberry-pi-deploy-key
0bi — gestern um 23:55 Uhr
nano ~/.ssh/config
Host github.com
  IdentityFile ~/.ssh/id_ed25519
0bi — 00:04
python-dotenv
requests
opencv-python-headless
pyzbar
numpy
API_KEY=kUhJU8azQQpbhAiKsiLXMqZW6zmoiQ2e1ZqGnQ4ZmugDw2XliuTUIeaouYgJw68
API_URL=https://nlgzpbv8nf.execute-api.eu-west-1.amazonaws.com/check-in
echo ".env" >> .gitignore
import time
import requests
import cv2
import numpy as np
import threading
import os

message.txt
4 kB
0bi — 00:13
/etc/systemd/system/qr-reader.service
[Unit]
Description=QR Scanner Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi
IMPORTANT: Use the folder where your .env file is located
WorkingDirectory=/home/pi/your-repo-name
Run the launcher script (which pulls git and runs python)
ExecStart=/bin/bash /home/pi/your-repo-name/launcher.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
Here is the complete launcher.sh script.

This script is the "glue" that makes your system robust. It handles the network check, the Git update, the dependency installation, and finally launches your Python scanner.
Create the launcher.sh file

Run this command inside your repository folder:
Bash

nano launcher.sh

Paste the following code into it:
Bash

#!/bin/bash

--- CONFIGURATION ---
REPO_DIR="/home/pi/your-repo-name"  # CHANGE THIS to your actual folder name
SCRIPT_NAME="scanner.py"            # Name of your python script
VENV_DIR="$REPO_DIR/venv"           # Virtual environment directory
---------------------
Navigate to the directory
cd "$REPO_DIR" || exit 1

Wait for Network (Critical for Git Pull & API)
This loops until it can ping google.com, ensuring internet is ready
echo "[Launcher] Waiting for internet connection..."
until ping -c 1 google.com &> /dev/null
do
  sleep 5
done
echo "[Launcher] Internet connected."

Update Code from Git
echo "[Launcher] Checking for updates..."
Reset local changes to avoid conflicts (force overwrite local files with remote)
git reset --hard HEAD
git pull origin main

Setup/Update Virtual Environment
if [ ! -d "$VENV_DIR" ]; then
    echo "[Launcher] Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

Activate the environment
source "$VENV_DIR/bin/activate"

Install Dependencies
This ensures new libraries (like python-dotenv) are installed automatically
if [ -f "requirements.txt" ]; then
    echo "[Launcher] Installing requirements..."
    pip install -r requirements.txt
fi

Run the Python Script
echo "[Launcher] Starting scanner..."
python "$SCRIPT_NAME"
Here is the complete launcher.sh script.

This script is the "glue" that makes your system robust. It handles the network check, the Git update, the dependency installation, and finally launches your Python scanner.
Create the launcher.sh file

Run this command inside your repository folder:
Bash

nano launcher.sh

Paste the following code into it:
Bash

#!/bin/bash

--- CONFIGURATION ---
REPO_DIR="/home/pi/your-repo-name"  # CHANGE THIS to your actual folder name
SCRIPT_NAME="scanner.py"            # Name of your python script
VENV_DIR="$REPO_DIR/venv"           # Virtual environment directory
---------------------
Navigate to the directory
cd "$REPO_DIR" || exit 1

Wait for Network (Critical for Git Pull & API)
This loops until it can ping google.com, ensuring internet is ready
echo "[Launcher] Waiting for internet connection..."
until ping -c 1 google.com &> /dev/null
do
  sleep 5
done
echo "[Launcher] Internet connected."

Update Code from Git
echo "[Launcher] Checking for updates..."
Reset local changes to avoid conflicts (force overwrite local files with remote)
git reset --hard HEAD
git pull origin main

Setup/Update Virtual Environment
if [ ! -d "$VENV_DIR" ]; then
    echo "[Launcher] Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

Activate the environment
source "$VENV_DIR/bin/activate"

Install Dependencies
This ensures new libraries (like python-dotenv) are installed automatically
if [ -f "requirements.txt" ]; then
    echo "[Launcher] Installing requirements..."
    pip install -r requirements.txt
fi

Run the Python Script
echo "[Launcher] Starting scanner..."
python "$SCRIPT_NAME"
0bi — 00:22
https://gemini.google.com/share/4233e065a955
/etc/systemd/system/qr-reader.service
sudo systemctl daemon-reload
sudo systemctl restart qr-reader.service
0bi — 00:29
journalctl -u qr-reader.service -f
sudo systemctl enable qr-reader.service
systemctl is-enabled qr-reader.service
systemctl status qr-reader.service
0bi — 00:54
import time
import requests
import cv2
import numpy as np
import threading
import os

message.txt
4 kB
sudo systemctl status qr-reader.service
﻿
MSA Nav
msanav
They Don't Know Me Son

 
 
 
 
 
 
import time
import requests
import cv2
import numpy as np
import threading
import os
from pyzbar.pyzbar import decode
from picamera2 import Picamera2
from dotenv import load_dotenv

# 1. Load the secret variables from the .env file
load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

if not API_KEY or not API_URL:
    print("[!!] Error: API_KEY or API_URL not found in .env file")
    exit(1)

COOLDOWN_SECONDS = 3.0
last_scan_time = 0
last_scanned_data = ""

def send_to_server(qr_uuid):
    # Strip whitespace to prevent errors
    qr_clean = qr_uuid.strip()
    print(f"[>>] Sending QR: {qr_clean}...")

    try:
        headers = {
            "Content-Type": "application/json",
            "x-api-key": API_KEY
        }
        # Ensure key matches your API expectation (camelCase vs snake_case)
        payload = { "qrUuid": qr_clean }

        response = requests.post(API_URL, json=payload, headers=headers, timeout=5)

        if response.status_code == 200:
            print(f"[OK] Check-in successful for {qr_clean}")
        else:
            print(f"[!!] Server Error ({response.status_code}): {response.text}")

    except Exception as e:
        print(f"[XX] Network Error: {e}")

def main():
    global last_scan_time, last_scanned_data

    print("[**] Initializing Camera (Headless Mode)...")

    try:
        picam2 = Picamera2()
        # Adjusted config for speed/reliability
        config = picam2.create_video_configuration(
            main={"size": (640, 480), "format": "BGR888"}
        )
        picam2.configure(config)
        picam2.start()
        print("[**] Scanner is running! (Background mode)")

    except Exception as e:
        print(f"[XX] Camera Failed to Start: {e}")
        return

    try:
        while True:
            # Capture frame
            frame = picam2.capture_array()

            # 2. REMOVED: cv2.imshow and cv2.waitKey (Requires Monitor)
            # We only decode, we don't display.
            
            decoded_objects = decode(frame)

            for obj in decoded_objects:
                try:
                    qr_uuid = obj.data.decode("utf-8")
                    current_time = time.time()

                    # Simple cooldown logic
                    if qr_uuid != last_scanned_data or (current_time - last_scan_time) > COOLDOWN_SECONDS:
                        print(f"[++] QR Detected: {qr_uuid}")
                        
                        last_scanned_data = qr_uuid
                        last_scan_time = current_time

                        # Threading is good here to keep camera loop fast
                        t = threading.Thread(target=send_to_server, args=(qr_uuid,))
                        t.start()
                except Exception as decode_error:
                    print(f"[!!] Error processing QR data: {decode_error}")

            # 3. Small sleep to prevent 100% CPU usage
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n[**] Stopping scanner...")
    finally:
        # REMOVED: cv2.destroyAllWindows()
        picam2.stop()

if __name__ == "__main__":
    main()