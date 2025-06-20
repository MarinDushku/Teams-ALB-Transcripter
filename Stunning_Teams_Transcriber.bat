@echo off
title ✨ Ultra Premium Albanian Teams Transcriber
color 0F

echo.
echo ================================================
echo    ✨ ULTRA PREMIUM Albanian Teams Transcriber
echo    Stunning Visual Design ^& AI Beauty
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
    echo Creating virtual environment for ultra premium features...
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

REM Install ultra premium dependencies
echo.
echo ================================================
echo    ✨ INSTALLING ULTRA PREMIUM FEATURES
echo ================================================
echo.
echo Installing packages for the most beautiful transcription experience...
pip install --upgrade pip --quiet
pip install SpeechRecognition psutil numpy requests --quiet
pip install scipy librosa scikit-learn python-docx --quiet

echo.
echo Installing audio packages for crystal-clear capture...
pip install pyaudio pyaudiowpatch --quiet
if errorlevel 1 (
    echo.
    echo Trying alternative audio installation...
    pip install pipwin --quiet
    pipwin install pyaudio --quiet
)

echo.
echo Installing remaining ultra premium requirements...
pip install -r requirements.txt --quiet

echo.
echo ================================================
echo    🌟 ULTRA PREMIUM EXPERIENCE READY
echo ================================================
echo.
echo Starting Ultra Premium Albanian Teams Transcriber...
echo.
echo ✨ Ultra Premium Features Active:
echo   • Stunning animated gradient backgrounds
echo   • Glassmorphism effects with blur and transparency  
echo   • Floating particle systems for ambient beauty
echo   • Advanced voice signature learning and matching
echo   • Real-time participant detection with AI algorithms
echo   • Professional multi-band audio processing
echo   • Beautiful typography and modern iconography
echo   • Smooth animations and micro-interactions
echo.
echo The most beautiful transcription GUI will open shortly...
echo Press Ctrl+C to stop the ultra premium experience
echo.

REM Run the ultra premium application
python ultra_premium_main.py auto

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ================================================
    echo    ULTRA PREMIUM ERROR HANDLING
    echo ================================================
    echo.
    echo The ultra premium version encountered an issue.
    echo.
    echo Graceful fallback options:
    echo   1. Run premium version: python premium_main.py
    echo   2. Run enhanced version: python enhanced_main.py
    echo   3. Run basic version: python main.py
    echo   4. Install missing packages: pip install scipy librosa scikit-learn
    echo.
    echo Falling back to premium version...
    echo.
    python premium_main.py auto
    if errorlevel 1 (
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
)

deactivate