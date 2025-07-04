import requests
import os
import time
import random
from datetime import datetime

API_URL = os.getenv("API_URL", "http://localhost:8000")

# Generate a unique serial number for each run
serial_no = f"SN-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(100, 999)}"

# Scan the product
try:
    r1 = requests.post(f"{API_URL}/scan", json={"serial_no": serial_no})
    print("🔍 Scan:", r1.status_code, r1.json())
except Exception as e:
    print("❌ Failed to scan:", e)

# Simulate tests
test_types = ["WiFi_Power", "Bluetooth", "Camera", "Battery", "Display", "Charging"]
result_options = ["PASS", "FAIL"]

for i in range(random.randint(3, 6)):
    payload = {
        "serial_no": serial_no,
        "test_type": random.choice(test_types),
        "result": random.choices(result_options, weights=[0.7, 0.3])[0]  # 70% pass rate
    }
    try:
        r2 = requests.post(f"{API_URL}/test", json=payload)
        print(f"📤 Test {i+1}:", r2.status_code, r2.json())
    except Exception as e:
        print(f"❌ Failed to send test {i+1}:", e)
    time.sleep(random.uniform(0.5, 1.5))  # randomized delay
