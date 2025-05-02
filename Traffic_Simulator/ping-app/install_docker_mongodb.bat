@echo off
cd /d %~dp0

set CONTAINER_NAME=ping-app-mongo

echo ==================================================
echo   Step 1: Create and Activate Python Environment
echo ==================================================

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo ==================================================
echo   Step 2: Install Dependencies
echo ==================================================
echo Installing backend dependencies...
pip install -r backend\requirements.txt

echo Installing GUI dependencies...
pip install -r gui\requirements.txt

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

echo Setting default Mongo URI...
set MONGO_URI=mongodb://localhost:27017

echo Stopping existing MongoDB container if running...
docker stop %CONTAINER_NAME%

echo Removing existing MongoDB container if it exists...
docker rm %CONTAINER_NAME%

echo Starting MongoDB container with fixed name: %CONTAINER_NAME% ...
docker run -d --name %CONTAINER_NAME% -p 27017:27017 mongo

echo.
echo ==================================================
echo   Step 4: Docker Services Started Successfully
echo ==================================================
echo MongoDB  : mongodb://localhost:27017
echo docker ps

echo.
echo ==================================================
echo   Step 5: Running Tests and Code Coverage
echo ==================================================
echo     set PYTHONPATH=. && pytest tests

@echo off
echo.
echo ==================================================
echo   Step 6: Run GUI and Tests Manually
echo ==================================================
echo.
echo [1] Activate the virtual environment:
echo     venv\Scripts\activate
echo.
echo [2] Run the backend:
echo     python -m backend.app
echo.
echo [3] Run the GUI:
echo     python gui\ping_gui.py
echo.
echo [4] Run the tests:
echo     set PYTHONPATH=.
echo     pytest tests
echo.
echo ==================================================
echo           You're all set. Happy Testing!
echo ==================================================