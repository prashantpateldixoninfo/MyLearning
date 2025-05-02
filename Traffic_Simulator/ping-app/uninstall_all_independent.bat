@echo off
cd /d %~dp0
setlocal enabledelayedexpansion

echo ==================================================
echo   UNINSTALLING ENVIRONMENT & SERVICES
echo ==================================================

echo [1] Stopping MongoDB service (requires Admin)...
net stop MongoDB >nul 2>&1
if %errorlevel%==0 (
    echo MongoDB stopped successfully.
) else (
    echo [WARNING] MongoDB may not be running or requires admin rights.
)

echo [2] Checking MongoDB service status...
sc query MongoDB | findstr /I "STATE"

echo [3] Removing virtual environment if exists...
if exist venv (
    rmdir /s /q venv
    echo Virtual environment 'venv' deleted.
) else (
    echo No virtual environment found.
)

echo.
echo ==================================================
echo   Cleanup Completed Successfully!
echo ==================================================
echo.

endlocal
