@echo off
echo ========================================
echo Albanian Teams Transcriber - Working Setup
echo ========================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed
    pause
    exit /b 1
)

echo Verifying your existing packages...
python -c "
packages = ['pyaudiowpatch', 'torch', 'numpy', 'scipy', 'requests', 'psutil']
working = []
for pkg in packages:
    try:
        __import__(pkg)
        working.append(pkg)
    except ImportError:
        pass

print(f'✓ Working packages: {len(working)}/{len(packages)}')
for pkg in working:
    print(f'  ✓ {pkg}')

if len(working) >= 4:  # Need at least core packages
    print('\n✓ Sufficient packages for basic functionality!')
else:
    print('\n⚠ Need more packages for full functionality')
"

echo.
echo Your setup is ready to test!
echo.
echo AUDIO SETUP REQUIRED:
echo 1. Download Virtual Audio Cable: https://vac.muzychenko.net/en/download.html
echo 2. Install and restart your computer
echo 3. In Teams: Set Virtual Cable as output device
echo 4. Run transcriber and it will capture Teams audio
echo.
echo Alternative: Use Windows WASAPI loopback (built-in, no extra software)
echo.
set /p choice="Test the transcriber now? (y/n): "
if /i "%choice%"=="y" (
    echo.
    echo Starting transcriber...
    python main.py
) else (
    echo.
    echo To run: python main.py
)
pause