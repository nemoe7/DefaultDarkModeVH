@echo off
REM Drag-and-drop images onto this batch file to apply LUT

REM Path to Python interpreter
set PYTHON=python

REM Folder where this batch file is located
set SCRIPT_DIR=%~dp0

REM Change working directory to the batch file location
cd /d "%SCRIPT_DIR%"

REM Path to your Python script
set SCRIPT=lut_apply.py

REM Pass all dropped files at once and feed empty input to use default LUT
"%PYTHON%" "%SCRIPT%" %*

pause
