@echo off
cd /d %~dp0
setlocal enabledelayedexpansion

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

echo ==================================================
echo   Step 3: Configure And Start MongoDB
echo ==================================================

echo Setting default Mongo URI...
set MONGO_URI=mongodb://localhost:27017

echo Checking MongoDB version (if installed)...
where mongo >nul 2>&1
if %errorlevel%==0 (
    mongo --version
) else (
    echo [WARNING] MongoDB not found in PATH.
)

echo Attempting to stop MongoDB service (requires Admin)...
net stop MongoDB >nul 2>&1

echo Attempting to start MongoDB service (requires Admin)...
net start MongoDB >nul 2>&1

echo ==================================================
echo   Step 4: Run Tests and Coverage
echo ==================================================
echo     set PYTHONPATH=. && pytest tests

echo ==================================================
echo   Step 5: Run GUI and Tests Manually
echo ==================================================
echo.
echo [1] Activate the virtual environment:
echo     venv\Scripts\activate
echo.
echo [2] Run the backend:
echo     python backend\app.py
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
endlocal