@echo off
title Albanian Teams Transcriber - Dependency Installer
color 0B

echo.
echo ================================================
echo    DEPENDENCY INSTALLER
echo    Albanian Teams Transcriber
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found! Proceeding with installation...
echo.

REM Change to the script directory
cd /d "%~dp0"

echo ================================================
echo    STEP 1: Upgrading pip
echo ================================================
python -m pip install --upgrade pip
echo.

echo ================================================
echo    STEP 2: Installing basic packages
echo ================================================
pip install speech-recognition
pip install psutil 
pip install numpy
pip install requests
echo.

echo ================================================
echo    STEP 3: Installing PyAudio (Audio Capture)
echo ================================================
echo This step may take a few minutes...
echo.

REM Try multiple methods to install PyAudio
echo Method 1: Using pipwin...
pip install pipwin
pipwin install pyaudio
if not errorlevel 1 (
    echo ✓ PyAudio installed successfully with pipwin!
    goto :pyaudio_success
)

echo.
echo Method 2: Direct pip install...
pip install pyaudio
if not errorlevel 1 (
    echo ✓ PyAudio installed successfully with pip!
    goto :pyaudio_success
)

echo.
echo Method 3: Trying precompiled wheel...
pip install PyAudio --find-links https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
if not errorlevel 1 (
    echo ✓ PyAudio installed successfully with wheel!
    goto :pyaudio_success
)

echo.
echo ⚠️  WARNING: PyAudio installation failed!
echo.
echo This usually happens because:
echo   - Visual Studio Build Tools are missing
echo   - You're using an unsupported Python version
echo.
echo SOLUTIONS:
echo   1. Install Visual Studio Build Tools
echo   2. Or manually download PyAudio wheel from:
echo      https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
echo.
echo The app may still work with limited functionality...
echo.

:pyaudio_success

echo ================================================
echo    STEP 4: Installing remaining packages
echo ================================================
pip install -r requirements.txt
echo.

echo ================================================
echo    STEP 5: Testing installation
echo ================================================
python -c "import pyaudio; print('✓ PyAudio OK')" 2>nul || echo "✗ PyAudio failed"
python -c "import speech_recognition; print('✓ SpeechRecognition OK')" 2>nul || echo "✗ SpeechRecognition failed"
python -c "import psutil; print('✓ psutil OK')" 2>nul || echo "✗ psutil failed"
python -c "import tkinter; print('✓ tkinter OK')" 2>nul || echo "✗ tkinter failed"
echo.

echo ================================================
echo    INSTALLATION COMPLETE!
echo ================================================
echo.
echo You can now run the application by:
echo   1. Double-clicking Albanian_Teams_Transcriber.bat
echo   2. Or running: python main.py
echo.
echo If you see any ✗ errors above, some features may not work.
echo.
pause