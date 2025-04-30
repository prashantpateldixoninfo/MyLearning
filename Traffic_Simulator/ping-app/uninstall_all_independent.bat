@echo off
cd /d %~dp0

echo Stopping MongoDB ...
net stop MongoDB

echo Checking MongoDB Status...
net status MongoDB

echo Cleanup complete!