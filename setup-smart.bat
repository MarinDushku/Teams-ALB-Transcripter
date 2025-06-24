@echo off
echo ========================================
echo Albanian Teams Transcriber - Smart Setup
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

echo [1/3] Checking dependencies and versions...

REM Create a Python script to check versions
echo import sys > check_deps.py
echo try: >> check_deps.py
echo     import pyaudiowpatch; print("✓ pyaudiowpatch:", pyaudiowpatch.__version__) >> check_deps.py
echo except: print("✗ pyaudiowpatch: missing") >> check_deps.py
echo try: >> check_deps.py
echo     import torch; print("✓ torch:", torch.__version__) >> check_deps.py
echo except: print("✗ torch: missing") >> check_deps.py
echo try: >> check_deps.py
echo     import numpy; print("✓ numpy:", numpy.__version__) >> check_deps.py
echo except: print("✗ numpy: missing") >> check_deps.py
echo try: >> check_deps.py
echo     import scipy; print("✓ scipy:", scipy.__version__) >> check_deps.py
echo except: print("✗ scipy: missing") >> check_deps.py
echo try: >> check_deps.py
echo     import requests; print("✓ requests:", requests.__version__) >> check_deps.py
echo except: print("✗ requests: missing") >> check_deps.py
echo try: >> check_deps.py
echo     import psutil; print("✓ psutil:", psutil.__version__) >> check_deps.py
echo except: print("✗ psutil: missing") >> check_deps.py
echo try: >> check_deps.py
echo     import docx; print("✓ python-docx: installed") >> check_deps.py
echo except: print("✗ python-docx: missing") >> check_deps.py
echo. >> check_deps.py
echo missing = [] >> check_deps.py
echo try: >> check_deps.py
echo     import pyaudiowpatch >> check_deps.py
echo except: missing.append("pyaudiowpatch") >> check_deps.py
echo try: >> check_deps.py
echo     import torch >> check_deps.py
echo     if torch.__version__ ^< "2.0.0": missing.append("torch^>=2.0.0") >> check_deps.py
echo except: missing.append("torch^>=2.0.0") >> check_deps.py
echo try: >> check_deps.py
echo     import requests >> check_deps.py
echo except: missing.append("requests") >> check_deps.py
echo try: >> check_deps.py
echo     import psutil >> check_deps.py
echo except: missing.append("psutil") >> check_deps.py
echo try: >> check_deps.py
echo     import docx >> check_deps.py
echo except: missing.append("python-docx") >> check_deps.py
echo print("MISSING:" + " ".join(missing) if missing else "MISSING:") >> check_deps.py

python check_deps.py > dep_check_result.txt
type dep_check_result.txt

REM Extract missing packages
for /f "tokens=2*" %%a in ('findstr "MISSING:" dep_check_result.txt') do set missing_packages=%%a %%b

if "%missing_packages%"==" " (
    echo.
    echo ✓ All required dependencies are already installed with compatible versions!
    goto cleanup_and_continue
)

echo.
echo Installing only missing packages: %missing_packages%
pip install %missing_packages% --user --quiet
if %errorlevel% neq 0 (
    echo WARNING: Some packages failed to install, but continuing...
)

:cleanup_and_continue
del check_deps.py dep_check_result.txt

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

echo.
echo Installing Albanian ASR dependencies...
cd Albanian-ASR
pip install -r requirements.txt --user --quiet
if %errorlevel% neq 0 (
    echo WARNING: Some Albanian ASR dependencies may have failed
)
cd ..

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