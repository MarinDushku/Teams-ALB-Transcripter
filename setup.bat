@echo off
echo ========================================
echo Albanian Teams Transcriber - Setup
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

echo [1/4] Installing Python dependencies...
echo Installing setuptools first...
pip install "setuptools<70.0.0"

echo Checking existing installations...
python -c "import torch, numpy, scipy, requests, psutil, pyaudiowpatch; print('Core packages already installed!')" 2>nul
if %errorlevel% equ 0 (
    echo All core dependencies are already installed!
    goto skip_install
)

echo Installing missing dependencies individually...
pip install pyaudiowpatch --quiet
pip install torch --quiet
pip install "numpy>=1.21.0" --only-binary=numpy --quiet
pip install scipy --only-binary=scipy --quiet
pip install requests --quiet
pip install psutil --quiet
pip install python-docx --quiet

:skip_install
echo Verifying installation...
python -c "import torch, numpy, scipy, requests, psutil, pyaudiowpatch; print('✓ All dependencies verified!')"
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Some packages may be missing, but continuing...
    echo You can install missing packages later with: pip install [package-name]
)

echo.
echo [2/4] Downloading Albanian ASR Model...
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
echo [3/4] Installing Albanian ASR dependencies...
cd Albanian-ASR
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Albanian ASR dependencies
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo [4/4] Audio Setup Instructions...
echo.
echo IMPORTANT: For audio capture to work, you need to:
echo 1. Install Virtual Audio Cable (free): https://vac.muzychenko.net/en/
echo 2. OR use Windows WASAPI loopback (built-in)
echo 3. Route Teams audio to the transcriber
echo.
echo Setup completed successfully!
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