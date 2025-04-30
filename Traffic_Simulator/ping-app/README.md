# Ping APP

## 🚀 Overview

This project demonstrates how to run the `ping` command through a GUI using a Flask backend and MongoDB for data storage.

---

## 📂 Project Structure

```bash
ping-app/
├── gui/                     # Frontend (PyQt5-based GUI)
│   ├── ping_gui.py
│   ├── requirements.txt     # GUI Dependencies
├── backend/                 # Backend (FastAPI)
│   ├── app.py
│   ├── db.py                # MongoDB Connection
│   ├── ping_logic.py        # Ping Logic
│   ├── requirements.txt     # Backend Dependencies
├── tests/                   # Unit Tests
│   ├── test_api.py
│   ├── test_gui.py
├── pre_install.sh           # Pre-setup script (Ubuntu/macOS)
├── post_cleanup.sh          # Cleanup script (Ubuntu/macOS)
├── pre_install_windows.bat  # Pre-setup script (Windows)
├── post_cleanup_windows.bat # Cleanup script (Windows)
├── README.md                # Documentation
├── .gitignore
```

---

## 🧰 Pre-Installation

### 🐧 For Ubuntu/Linux/macOS

```bash
./pre_install.sh
```

This script performs:

-   Virtual environment creation
-   Dependency installation
-   MongoDB Docker container startup (`ping-app-mongo`)

> ⚠️ Ensure Docker is installed and the daemon is running.

---

### 🪟 For Windows (VS Code + Git Bash)

```bash
./pre_install_windows.bat
```

This script performs:

-   Python virtual environment setup using `venv`
-   Backend, GUI, and test dependencies installation
-   MongoDB Docker container startup (`ping-app-mongo`)

> ⚠️ Docker Desktop must be installed and running.

---

## 🚀 Running the Application

### ✅ 1️⃣ Start the Backend (in activated virtual environment)

```bash
python -m backend.app
```

Runs the backend on: `http://127.0.0.1:5000`

---

### ✅ 2️⃣ Start the GUI

```bash
python gui/ping_gui.py
```

A simple GUI will launch where you can enter a hostname or IP address to ping.

---

## 🧪 Running Tests

### 🐧 Linux/macOS

```bash
PYTHONPATH=. pytest tests
```

### 🪟 Windows (PowerShell or Git Bash)

```powershell
$env:PYTHONPATH="."; pytest tests
```

Runs API and GUI tests.

---

## 🧹 Post-Cleanup

### 🐧 Ubuntu/Linux/macOS

```bash
./post_cleanup.sh
```

### 🪟 Windows

```bash
./post_cleanup_windows.bat
```

This script:

-   Stops and removes the MongoDB Docker container (`ping-app-mongo`)
-   Leaves the virtual environment and project files intact

---

## 📝 Notes

-   MongoDB runs inside a Docker container named `ping-app-mongo`.
-   The application uses virtual environments to isolate dependencies.
-   Project is cross-platform: works on both Ubuntu/Linux and Windows systems with proper scripts.

---
