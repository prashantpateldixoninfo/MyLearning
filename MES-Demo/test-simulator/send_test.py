import requests
import os
import time
import random

# Use env variable (Docker will inject this)
BASE_URL = os.getenv("API_URL", "http://localhost:8000")
SERIAL_NO = "ABC123"

# Scan product
r1 = requests.post(f"{BASE_URL}/scan", json={"serial_no": SERIAL_NO})
print("Scan:", r1.json())

# Simulate multiple test cases
test_types = ["WiFi_Power", "Bluetooth", "Camera", "Battery"]

for i in range(5):
    payload = {
        "serial_no": SERIAL_NO,
        "test_type": random.choice(test_types),
        "result": random.choice(["PASS", "FAIL"])
    }
    r2 = requests.post(f"{BASE_URL}/test", json=payload)
    print(f"Test {i+1}:", r2.json())
    time.sleep(1)
