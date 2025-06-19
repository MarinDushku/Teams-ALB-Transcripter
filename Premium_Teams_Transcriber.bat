@echo off
title 🌟 Premium Albanian Teams Transcriber
color 0D

echo.
echo ================================================
echo    🌟 PREMIUM Albanian Teams Transcriber
echo    AI-Powered Participant Recognition
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
    echo Creating virtual environment for premium features...
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

REM Install premium dependencies
echo.
echo ================================================
echo    🌟 INSTALLING PREMIUM DEPENDENCIES
echo ================================================
echo.
echo Installing premium packages for ultimate performance...
pip install --upgrade pip --quiet
pip install SpeechRecognition psutil numpy requests --quiet
pip install scipy librosa scikit-learn python-docx --quiet

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
echo    ✨ PREMIUM FEATURES ACTIVATED
echo ================================================
echo.
echo Starting Premium Albanian Teams Transcriber...
echo.
echo 🌟 Premium Features Active:
echo   • Real participant name detection and voice mapping
echo   • Modern beautiful UI with dark/light themes  
echo   • AI-powered speaker-to-participant matching
echo   • Professional audio processing and enhancement
echo   • Advanced voice analysis and characteristics
echo   • Persistent participant profiles across meetings
echo   • Real-time performance monitoring and analytics
echo   • Enhanced Albanian language processing
echo.
echo The premium GUI will open shortly...
echo Press Ctrl+C to stop the application
echo.

REM Run the premium application
python premium_main.py auto

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ================================================
    echo    PREMIUM APPLICATION ERROR
    echo ================================================
    echo.
    echo The premium version encountered an error.
    echo.
    echo Possible solutions:
    echo   1. Run enhanced version: python enhanced_main.py
    echo   2. Run basic version: python main.py
    echo   3. Install missing packages: pip install scipy librosa scikit-learn
    echo   4. Check audio device configuration
    echo.
    echo Falling back to enhanced version...
    echo.
    python enhanced_main.py auto
    if errorlevel 1 (
        echo.
        echo Falling back to basic version...
        echo.
        python main.py auto
        if errorlevel 1 (
            echo.
            echo All versions failed. Please check the installation guide.
            echo.
            pause
        )
    )
)

deactivate