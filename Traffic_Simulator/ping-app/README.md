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

### 🖥 2️⃣ **Set Up Backend**

```sh
cd backend
python -m venv venv   # Create Virtual Environment for one time
venv\Scripts\activate  # Activate (Windows)
pip install -r requirements.txt  # Install Dependencies
deactivate   # Deactivate Environment
```

### 🎨 3️⃣ **Set Up GUI**export MONGO_URI="mongodb://localhost:27017"

```sh
cd gui
python -m venv venv   # Create Virtual Environment for one time
venv\Scripts\activate  # Activate (Windows)
pip install -r requirements.txt  # Install Dependencies
deactivate   # Deactivate Environment
```

---

## 🚀 **Running the Application**

### 🔹 1️⃣ **Start Backend Server**

```sh
python -m main
```

This will run the FastAPI backend on `http://127.0.0.1:8000`.

### 🔹 2️⃣ **Start GUI Application**

```sh
python -m main
```

---

## 🧪 **Running Tests**

```sh
cd tests
python -m unittest discover
```

---

## 📌 **Additional Notes**

-   The backend runs on **port 8000**.
-   The GUI interacts with the backend via API calls.
-   Ensure both environments (`gui/venv` and `backend/venv`) are activated while running respective parts.
-   Update dependencies using:
    ```sh
    pip install -r requirements.txt
    ```
