# Python GUI and Backend Project

## Overview

This project demonstrates how to create a simple Python GUI using Tkinter that interacts with a Flask backend.

## Project Structure

project/
├── gui/
│ ├── **init**.py
| ├── main.py
| ├── main_page.py
| ├── first_page.py
| ├── second_page.py
├── backend/
│ ├── api.py
├── shared/
│ ├── config.py
├── tests/
│ ├── test_backend.py
├── requirements.txt
├── README.md
├── .gitignore

### Installation

1. Clone the repository:
   git clone <https://github.com/prashantpateldixoninfo/MyLearning/tree/main/Traffic_Simulator/OLT-Configuration>
   cd OLT-Configuration

2. Create a virtual environment:
   python -m venv venv
   venv\Scripts\activate # On Linux use `source venv/bin/activate`

3. Install dependencies:
   pip install -r requirements.txt

### Running the Application

1. Start the backend server:
   python backend/api.py

2. Run the GUI application:
   python -m gui.main

### Running Tests

Run unit tests with:
python -m unittest discover tests
