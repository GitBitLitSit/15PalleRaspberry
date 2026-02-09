import time
import requests
import cv2
import numpy as np
import threading
from pyzbar.pyzbar import decode
from picamera2 import Picamera2

API_URL = "https://nlgzpbv8nf.execute-api.eu-west-1.amazonaws.com/check-in"
API_KEY = "kUhJU8azQQpbhAiKsiLXMqZW6zmoiQ2e1ZqGnQ4ZmugDw2XliuTUIeaouYgJw68"

COOLDOWN_SECONDS = 3.0

last_scan_time = 0
last_scanned_data = ""

def send_to_server(qr_uuid):
	print(f"[>>] Sending QR: {qr_uuid}...")

	try:
		headers = {
			"Content-Type": "application/json",
			"x-api-key": API_KEY
		}
		payload = { "qrUuid": qr_uuid }

		response = requests.post(API_URL, json=payload, headers=headers, timeout=3)

		if response.status_code == 200:
			print(f"[OK Check-in successful")
		else:
			print(f"[!! Server Error ({response.status_code}): {response.text}")


	except Exception as e:
		print(f"[XX Network Error: {e}")

def main():
	global last_scan_time, last_scanned_data

	print("[**] Initializing Camera Module 3...")

	try:
		picam2 = Picamera2()
		config = picam2.create_video_configuration(
			main={"size": (640, 480), "format": "BGR888"}
		)

		picam2.configure(config)
		picam2.start()
		print("[**] Scanner is running! Press Ctrl+C to stop.")

	except Exception as e:
		print(f"[XX] Camera Failed to Start: {e}")
		return

	try:
		while True:
			frame = picam2.capture_array()

			gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			cv2.imshow("Camera Preview", frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

			decoded_objects = decode(frame)

			for obj in decoded_objects:
				qr_uuid = obj.data.decode("utf-8")
				current_time = time.time()

				if qr_uuid != last_scanned_data or (current_time - last_scan_time) > COOLDOWN_SECONDS:
					print(f"[++] QR Detected: {qr_uuid}")

					last_scanned_data = qr_uuid
					last_scan_time = current_time

					t = threading.Thread(target=send_to_server, args=(qr_uuid,))
					t.start()

			time.sleep(0.05)
	except KeyboardInterrupt:
		print("\n[**] Stopping scanner...")
	finally:
		cv2.destroyAllWindows()
		picam2.stop()

if __name__ == "__main__":
	main()
