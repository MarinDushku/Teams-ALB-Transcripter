@echo off
title Enhanced Albanian Teams Transcriber
color 0E

echo.
echo ================================================
echo    🚀 ENHANCED Albanian Teams Transcriber
echo    Advanced Real-time Meeting Transcription
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
    echo Creating virtual environment for enhanced features...
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

REM Install enhanced dependencies
echo.
echo ================================================
echo    INSTALLING ENHANCED DEPENDENCIES
echo ================================================
echo.
echo Installing enhanced packages for superior performance...
pip install --upgrade pip --quiet
pip install SpeechRecognition psutil numpy requests --quiet
pip install scipy librosa scikit-learn --quiet

echo.
echo Installing audio packages...
pip install pyaudio pyaudiowpatch --quiet
if errorlevel 1 (
    echo.
    echo Trying alternative audio installation...
    pip install pipwin --quiet
    pipwin install pyaudio --quiet
)

echo.
echo Installing remaining requirements...
pip install -r requirements.txt --quiet

echo.
echo ================================================
echo    🌟 ENHANCED FEATURES READY
echo ================================================
echo.
echo Starting Enhanced Albanian Teams Transcriber...
echo.
echo ✨ Enhanced Features Active:
echo   • Advanced noise reduction and echo cancellation
echo   • Superior speaker identification with voice analysis  
echo   • Multiple Albanian transcription engines
echo   • Real-time performance monitoring
echo   • Albanian language corrections and enhancements
echo.
echo The enhanced GUI will open shortly...
echo Press Ctrl+C to stop the application
echo.

REM Run the enhanced application
python enhanced_main.py auto

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ================================================
    echo    ENHANCED APPLICATION ERROR
    echo ================================================
    echo.
    echo The enhanced version encountered an error.
    echo.
    echo Possible solutions:
    echo   1. Run basic version: python main.py
    echo   2. Install missing packages: pip install scipy librosa scikit-learn
    echo   3. Check audio device configuration
    echo.
    echo Falling back to basic version...
    echo.
    python main.py auto
    if errorlevel 1 (
        echo.
        echo Both enhanced and basic versions failed.
        echo Please check the installation guide.
        echo.
        pause
    )
)

deactivate