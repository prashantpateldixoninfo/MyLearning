@echo off
cd /d %~dp0

echo Creating virtual environment (if not exists)...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing backend dependencies...
pip install -r backend\requirements.txt

echo Installing GUI dependencies...
pip install -r gui\requirements.txt

echo Installing test dependencies...
pip install pytest pytest-qt

echo Setting default Mongo URI...
set MONGO_URI=mongodb://localhost:27017

echo Checking version of MongoDB if present...
mongo --version

echo Stopping existing MongoDB if running...
net stop MongoDB

echo Starting MongoDB if not running...
net start MongoDB

echo Checking container status...
net status MongoDB

@echo off
echo.
echo ==================================================
echo        PRE-INSTALLATION COMPLETE! NEXT STEPS:
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
echo     pytest tests
echo     set PYTHONPATH=. && pytest tests
echo.
echo ==================================================
echo           You're all set. Happy Testing!
echo ==================================================