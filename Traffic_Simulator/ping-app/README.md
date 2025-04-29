# Ping APP

## 🚀 Overview

This project demonstrates how to run ping command through GUI.

---

## 📂 Project Structure

```bash
OLT-Configuration/
├── gui/                     # Frontend (QtPy-based GUI)
│   ├── ping_gui.py
│   ├── requirements.txt     # Frontend Dependencies
├── backend/                 # Backend (FastAPI)
│   ├── app.py
│   ├── db.py                # MongoDB
│   ├── ping_logic.py        # ping command
│   ├── requirements.txt     # Backend Dependencies
├── tests/                   # Test Cases
│   ├── test_api.py
│   ├── test_gui.py
├── README.md                # Documentation
├── .gitignore               # Ignore Unwanted Files
```

## 🔧 **Installation**

### 🛠 1️⃣ **Clone the Repository**

```sh
git clone https://github.com/prashantpateldixoninfo/MyLearning.git
cd MyLearning/Traffic_Simulator/ping-app
```

### 🖥 2️⃣ **Install the libraries**

```sh
cd ping-app
python3 -m venv venv                # Create Virtual Environment for one time
source venv/bin/activate            # Activate (Linux)
pip install --upgrade pip
pip install -r backend/requirements.txt
pip install -r gui/requirements.txt
pip install pytest pytest-qt
export MONGO_URI="mongodb://localhost:27017"
sudo systemctl stop mongod          # Stop the docker if already running
docker-compose up -d mongo          # Run the mongo-db
docker ps                           # Check the mongo-db status
```

## 🚀 **Running the Application**

### 🔹 1️⃣ **Start Backend Server**

```sh
python3 -m backend.app
```

This will run the Flask backend on `http://127.0.0.1:5000`.

### 🔹 2️⃣ **Start GUI Application**

```sh
python3 gui/ping_gui.py
```

---

## 🧪 **Running Tests**

```sh
PYTHONPATH=. pytest tests           # For Linux
$env:PYTHONPATH="."; pytest tests   # For Windows
```

---
