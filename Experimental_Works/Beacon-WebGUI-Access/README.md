# 📡 FWA Verification Tool with Logging

A Python-based desktop tool built using **Tkinter + Selenium** to verify device firmware and serial number via web UI and log results automatically.

---

## 🚀 Features

* Scan or enter **Device Serial Number**
* Automatically login to device web UI
* Fetch:

  * Serial Number (SN)
  * Software Version (SW)
* Compare with expected values
* Display result:

  * ✅ PASS
  * ❌ FAIL
  * ⚠️ Connection Error
* Save logs to CSV file with timestamp

---

## 🖥️ Tech Stack

* Python 3.x
* Tkinter (GUI)
* Selenium (Web automation)
* WebDriver Manager (Auto ChromeDriver setup)
* CSV (Logging)

---

## 📂 Project Structure

```
FWA-Tool/
│── main.py
│── device_logs.csv (auto-generated)
│── README.md
│── requirements.txt
```

---

## ⚙️ Configuration

Edit these variables in code:

```python
TARGET_IP = "192.168.1.1"
REQUIRED_SW = "V1.2.3_2026"
```

---

## ▶️ How to Run

### 1. Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run Application

```bash
python main.py
```

---

## 📊 Output Log (CSV)

A file `device_logs.csv` will be created automatically:

| Timestamp  | Scanned_SN | Detected_SW | Status |
| ---------- | ---------- | ----------- | ------ |
| 2026-03-22 | ABC123     | V1.2.3      | PASS   |

---

## ⚠️ Important Notes

* Ensure device is reachable at `TARGET_IP`
* Update login credentials if needed:

  ```python
  username = "admin"
  password = "Airtel@123"
  ```
* Update element IDs based on actual web UI:

  * `sn_val`
  * `sw_val`

---

## 🧠 Future Enhancements

* Dashboard integration (Grafana / Streamlit)
* Barcode scanner integration
* Multi-device batch testing
* Database logging (PostgreSQL)

---

## 👨‍💻 Author

Prashant Patel
(MES + Automation + AI Learning Project)

---
