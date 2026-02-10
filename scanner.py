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