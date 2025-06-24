@echo off
echo ========================================
echo Albanian Teams Transcriber - Simple Setup
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

echo [1/3] Checking dependencies...
python -c "import torch, numpy, scipy, requests, psutil, pyaudiowpatch, docx; print('✓ All dependencies found!')" 2>nul
if %errorlevel% equ 0 (
    echo All required packages are already installed!
    goto download_asr
)

echo Some packages are missing. Installing...
pip install pyaudiowpatch torch requests psutil python-docx --user --quiet

:download_asr
echo.
echo [2/3] Downloading Albanian ASR Model...
if exist "Albanian-ASR" (
    echo Albanian-ASR already exists, skipping download...
) else (
    git clone https://github.com/florijanqosja/Albanian-ASR
    if %errorlevel% neq 0 (
        echo ERROR: Failed to clone Albanian-ASR repository
        echo Make sure git is installed or download manually
        pause
        exit /b 1
    )
)

echo.
echo [3/3] Setup complete!
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