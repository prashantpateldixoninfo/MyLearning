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

echo ==================================================
echo   Step 2: Install Dependencies
echo ==================================================
echo.
echo Installing backend dependencies...
pip install -r backend\requirements.txt

echo.
echo Installing GUI dependencies...
pip install -r gui\requirements.txt

echo.
echo Installing test dependencies...
pip install -r tests\requirements.txt

@echo off
echo ==================================================
echo   Step 3: Checking if Docker is Running
echo ==================================================

REM Try to get Docker info
docker info >nul 2>&1

IF ERRORLEVEL 1 (
    echo.
    echo [ERROR] Docker Engine is not running!
    echo Please start Docker Desktop and try again.
    echo.
    pause
    exit /b 1
)

echo [OK] Docker is running.
echo.

echo.
echo ==================================================
echo   Step 4: Build and Launch Docker Services
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
echo   Step 5: Docker Services Started Successfully
echo ==================================================
echo Backend  : http://localhost:5000
echo MongoDB  : mongodb://localhost:27017
echo docker ps

echo.
echo ==================================================
echo   Step 6: Running Tests and Code Coverage
echo ==================================================
echo     set PYTHONPATH=. && pytest tests

echo.
echo ==================================================
echo   Step 7: Run GUI and Tests Manually
echo ==================================================
echo.
echo To activate the virtual environment:
echo     venv\Scripts\activate
echo.
echo To launch the GUI:
echo     python gui\ping_gui.py
echo.
echo To run tests:
echo     set PYTHONPATH=.
echo     pytest tests
echo.
echo ==================================================
echo           You're all set. Happy Testing!
echo ==================================================
