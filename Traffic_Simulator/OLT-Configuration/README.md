# Python GUI and Backend Project

## Overview

This project demonstrates how to create a simple Python GUI using qtpy that interacts with a fastAPI backend.

## Project Structure

project/
├── gui/
│ ├── **init**.py
| ├── main.py
| ├── main_page.py
| ├── olt_page.py
| ├── ont_page.py
| ├── requirements.txt
├── backend/
│ ├── **init**.py
| ├── main.py
| ├── olt_telnet.py
| ├── olt_config.py
| ├── ont_config.py
| ├── requirements.txt
├── shared/
│ ├── config.py
├── tests/
│ ├── test_backend.py
├── README.md
├── .gitignore

### Installation

1. Clone the repository:
   git clone <https://github.com/prashantpateldixoninfo/MyLearning/tree/main/Traffic_Simulator/OLT-Configuration>
   cd OLT-Configuration

2. Create a virtual environment for backend(One Time):
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt # Do for any library update

3. Create a virtual environment for gui(One Time):
   cd gui
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt # Do for any library update

### Running the Application

1. Start the backend server from OLT-Configuration\backend:
   python -m main

2. Run the GUI application from OLT-Configuration\gui:
   python -m main

### Running Tests

Run unit tests with:
python -m unittest discover tests
