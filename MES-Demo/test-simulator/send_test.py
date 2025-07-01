import requests

# Simulate scan
requests.post("http://localhost:8000/scan", json={"serial_no": "ABC456"})

# Simulate test
requests.post("http://localhost:8000/test", json={
    "serial_no": "ABC456",
    "test_type": "WiFi_Power",
    "result": "FAILED"
})
