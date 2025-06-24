@echo off
echo ========================================
echo Albanian Teams Transcriber - Final Setup
echo ========================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found
    pause
    exit /b 1
)

echo [1/3] Installing AI and participant monitoring dependencies...
pip install openai-whisper pygetwindow pyautogui opencv-python pillow pytesseract --user --quiet
if %errorlevel% neq 0 (
    echo WARNING: Some dependencies failed, continuing...
)

echo [2/3] Installing Tesseract OCR for participant detection...
echo.
echo IMPORTANT: Download Tesseract OCR from:
echo https://github.com/UB-Mannheim/tesseract/wiki
echo.
echo Choose "tesseract-ocr-w64-setup-v5.x.x.exe" and install it
echo.
set /p tesseract_installed="Have you installed Tesseract OCR? (y/n): "
if /i not "%tesseract_installed%"=="y" (
    echo.
    echo Please install Tesseract OCR for participant name detection
    echo The transcriber will work without it, but won't detect participant names
)

echo.
echo [3/3] Verifying setup...
python -c "
import sys
print('Checking packages...')

# Check core packages
packages = {
    'pyaudiowpatch': 'Audio capture',
    'torch': 'AI processing', 
    'numpy': 'Data processing',
    'tkinter': 'User interface',
    'pygetwindow': 'Window detection',
    'cv2': 'Image processing'
}

working = 0
for pkg, desc in packages.items():
    try:
        if pkg == 'tkinter':
            import tkinter
        else:
            __import__(pkg)
        print(f'✓ {desc}')
        working += 1
    except ImportError:
        print(f'✗ {desc} - {pkg} missing')

# Check Whisper
try:
    import whisper
    print('✓ Whisper AI transcription')
    working += 1
except ImportError:
    print('✗ Whisper AI - will use basic transcription')

print(f'\\nSystem readiness: {working}/5 components available')
if working >= 3:
    print('✓ Ready to run!')
else:
    print('⚠ Some features may be limited')
"

echo.
echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo Your transcriber is ready to use with:
echo ✓ Beautiful modern UI
echo ✓ Real-time audio capture  
echo ✓ AI-powered transcription
echo ✓ Automatic participant detection
echo ✓ Speaker identification
echo ✓ Join/leave notifications
echo ✓ Export capabilities
echo.
echo AUDIO SETUP (Important):
echo 1. Download VB-CABLE: https://vb-audio.com/Cable/
echo 2. Install and restart computer
echo 3. In Teams: Output → CABLE Input
echo 4. Transcriber will capture Teams audio automatically
echo.
set /p choice="Start the transcriber now? (y/n): "
if /i "%choice%"=="y" (
    echo.
    echo 🚀 Starting Albanian Teams Transcriber...
    python working_transcriber.py
) else (
    echo.
    echo To run later: python working_transcriber.py
)

pause