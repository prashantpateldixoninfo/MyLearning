# 🏠 MES-Demo: Manufacturing Execution System (Local Simulation)

This project simulates a **basic Manufacturing Execution System (MES)** that:

* Accepts barcode scans from the shop floor.
* Simulates product test results (Pass/Fail).
* Displays real-time status via a simple dashboard.

Useful for learning, testing, or prototyping MES functionality on a laptop without any hardware dependencies.

---

## 📦 Features

* ✅ FastAPI backend for receiving scanned/tested data.
* ✅ Test Simulator to generate mock test results.
* ✅ Static HTML frontend dashboard to view pass/fail metrics.
* ✅ Streamlit dashboard for simple visual insights.
* ✅ Grafana integration for real-time analytics.
* ✅ Modular structure for easy expansion (e.g., PostgreSQL, Docker).

---

## 👤 Target Audience

* Automation engineers and developers learning MES integration.
* Factory IT/OT teams building proof-of-concept systems.
* Students and researchers interested in industrial systems simulation.

---

## 🗂️ Project Structure

```
MES-Demo/
├── backend/                # FastAPI server to receive barcode and test data
├── test-simulator/         # Simulates test result data
├── frontend_static/        # Static HTML dashboard
├── frontend_streamlit/     # Streamlit-based dashboard
├── frontedn_grafana/       # Grafana provisioning files
├── docker-compose.yml      # Container orchestration
└── README.md               
```

---

## ▶️ How to Run This Demo Locally

### 📅 Prerequisites

* Docker and Docker Compose installed

### 🌟 Start with Docker Compose

```bash
docker-compose up --build
```

### ⏹️ Stop and Clean Up

```bash
docker-compose down
```

> ⚠️ Ensure ports 8000 (FastAPI), 3000 (Grafana), and 8501 (Streamlit) are free before running.

---

## 📈 Frontend Dashboard Access

### 🌐 Static HTML Dashboard

Open in browser:

```
http://localhost:8080  (if served via local web server)
OR
Open ./frontend_static/index.html directly
```

Displays basic pre-rendered pass/fail results.

### 🌎 Streamlit Dashboard

Access via browser:

```
http://localhost:8501
```

Streamlit displays real-time or recent test results interactively.

### 📊 Grafana Dashboard

Access via browser:

```
http://localhost:3000
```

* Login: `admin / admin`
* Explore dashboards under `MES Metrics`

---
