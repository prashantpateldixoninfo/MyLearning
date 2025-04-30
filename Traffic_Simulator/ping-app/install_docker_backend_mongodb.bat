@echo off
cd /d %~dp0

echo ==================================================
echo   Step 1: Create and Activate Python Environment
echo ==================================================

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing backend dependencies...
pip install -r backend\requirements.txt

echo.
echo Installing GUI dependencies...
pip install -r gui\requirements.txt

echo.
echo Installing test dependencies...
pip install pytest pytest-qt

echo.
echo ==================================================
echo        Step 2: Build & Launch Docker Services
echo ==================================================

echo Stopping any running containers...
docker-compose down

echo.
echo Building containers...
docker-compose build

echo.
echo Starting containers (MongoDB + Backend)...
docker-compose up -d

echo.
echo ==================================================
echo       Docker Services Started Successfully
echo ==================================================
echo Backend  : http://localhost:5000
echo MongoDB  : mongodb://localhost:27017

echo.
echo ==================================================
echo      Step 3: Run GUI and Tests Manually
echo ==================================================
echo.
echo To activate the virtual environment:
echo     venv\Scripts\activate
echo.
echo To launch the GUI:
echo     python gui\ping_gui.py
echo.
echo To run tests:
echo     pytest tests
echo     set PYTHONPATH=. && pytest tests
echo.
echo ==================================================
echo           You're all set. Happy Testing!
echo ==================================================
