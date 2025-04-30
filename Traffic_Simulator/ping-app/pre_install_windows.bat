@echo off
cd /d %~dp0

set CONTAINER_NAME=ping-app-mongo

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

echo Stopping existing MongoDB container if running...
docker stop %CONTAINER_NAME%

echo Removing existing MongoDB container if it exists...
docker rm %CONTAINER_NAME%

echo Starting MongoDB container with fixed name: %CONTAINER_NAME% ...
docker run -d --name %CONTAINER_NAME% -p 27017:27017 mongo

echo Checking container status...
docker ps

echo Pre-installation complete!