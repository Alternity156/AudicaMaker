@echo off
cd %~dp0

:: Only works on Python 2

:: Change this depending where you installed Python...
set PYTHON=C:\Python27

:: Don't change these...
set PATH=%PYTHON%;%PATH%

python source/main.py
pause