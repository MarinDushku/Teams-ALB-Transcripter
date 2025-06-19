@echo off
title Albanian Teams Transcriber
color 0A

echo.
echo ================================================
echo    Albanian Teams Transcriber
echo    Real-time Teams Meeting Transcription
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo.
    pause
    exit /b 1
)

REM Change to the script directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install/update requirements
echo Checking dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo WARNING: Some dependencies may not have installed correctly
    echo This might affect functionality
    echo.
)

REM Clear screen and show startup info
cls
echo.
echo ================================================
echo    Albanian Teams Transcriber - STARTING
echo ================================================
echo.
echo Starting the application...
echo The GUI will open shortly.
echo.
echo Instructions:
echo - The app will automatically detect Teams meetings
echo - Click "Start Auto-Transcription" to begin
echo - Transcripts are saved automatically
echo - Use "Export Transcript" to save your transcript
echo.
echo Press Ctrl+C in this window to stop the application
echo.

REM Run the application
python main.py auto

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ================================================
    echo    APPLICATION STOPPED WITH ERROR
    echo ================================================
    echo.
    echo If you see import errors, try running:
    echo   pip install -r requirements.txt
    echo.
    echo For audio issues, make sure:
    echo   - Teams is running
    echo   - Audio devices are working
    echo   - Virtual Audio Cable is installed (if needed)
    echo.
    pause
)

deactivate