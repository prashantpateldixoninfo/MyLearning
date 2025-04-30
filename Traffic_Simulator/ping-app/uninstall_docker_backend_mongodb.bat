@echo off
cd /d %~dp0

echo ==================================================
echo          POST-CLEANUP: Shutting Down Project
echo ==================================================

echo.
echo Stopping and removing Docker containers...
docker-compose down

echo.
echo Docker containers cleaned up.

REM Optional: remove virtual environment (uncomment if desired)
REM echo.
REM echo Removing virtual environment...
REM rmdir /S /Q venv

REM Optional: remove __pycache__ and *.pyc files
echo.
echo Cleaning Python cache files...
for /r %%i in (__pycache__) do if exist "%%i" rmdir /s /q "%%i"
for /r %%i in (*.pyc) do del /q "%%i"

echo.
echo ==================================================
echo              Cleanup Completed Successfully!
echo ==================================================
echo.
