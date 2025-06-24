@echo off
echo ========================================
echo Albanian Teams Transcriber - Basic Setup
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

echo [1/2] Checking core dependencies...
python -c "
import sys
missing = []
try: import pyaudiowpatch
except: missing.append('pyaudiowpatch')
try: import torch
except: missing.append('torch')
try: import numpy
except: missing.append('numpy')
try: import scipy
except: missing.append('scipy')
try: import requests
except: missing.append('requests')
try: import psutil
except: missing.append('psutil')
try: import docx
except: missing.append('python-docx')

if missing:
    print('Installing missing packages:', ' '.join(missing))
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing + ['--user'])
else:
    print('✓ All core dependencies already installed!')
"

echo.
echo [2/2] Setup complete!
echo.
echo NOTE: Albanian ASR model download skipped due to Python 3.13 compatibility issues.
echo The transcriber will work with OpenAI Whisper or other compatible models.
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