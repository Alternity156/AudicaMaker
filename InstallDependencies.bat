@echo off
cd %~dp0

:: Only works on Python 2

:: Change this depending where you installed Python...
set PYTHON=C:\Python27

:: Don't change these...
set PATH=%PYTHON%;%PATH%

python -m pip install --upgrade pip wheel setuptools
python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
python -m pip install kivy.deps.angle
python -m pip install kivy
python -m pip install python-midi
python -m pip install mutagen
pause