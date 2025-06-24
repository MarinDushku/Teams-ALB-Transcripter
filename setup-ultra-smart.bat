@echo off
echo ========================================
echo Albanian Teams Transcriber - Ultra Smart Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [1/3] Smart dependency checking...
python check_requirements.py
if %errorlevel% neq 0 (
    echo.
    echo Some dependencies had issues, but continuing...
)

echo.
echo [2/3] Downloading Albanian ASR Model...
if exist "Albanian-ASR" (
    echo Albanian-ASR already exists, skipping download...
) else (
    git clone https://github.com/florijanqosja/Albanian-ASR
    if %errorlevel% neq 0 (
        echo ERROR: Failed to clone Albanian-ASR repository
        echo Make sure git is installed
        pause
        exit /b 1
    )
)

echo Installing Albanian ASR dependencies...
cd Albanian-ASR
python -c "import subprocess, sys; subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '--user', '--quiet'])"
cd ..

echo.
echo [3/3] Final verification...
python -c "
try:
    import torch, numpy, scipy, requests, psutil, pyaudiowpatch
    print('✓ All core dependencies verified!')
except ImportError as e:
    print(f'⚠ Missing: {e}')
    print('You may need to install some packages manually')
"

echo.
echo ✓ Setup complete!
echo.
echo IMPORTANT: For audio capture to work:
echo 1. Install Virtual Audio Cable: https://vac.muzychenko.net/en/
echo 2. Route Teams audio to the transcriber
echo.
set /p choice="Do you want to run the transcriber now? (y/n): "
if /i "%choice%"=="y" (
    echo.
    echo Starting Albanian Teams Transcriber...
    python main.py
) else (
    echo.
    echo To run later, use: python main.py
)

pause