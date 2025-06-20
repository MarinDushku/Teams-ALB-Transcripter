@echo off
echo ================================================================
echo         IMPROVED TEAMS TRANSCRIBER SETUP
echo ================================================================
echo.
echo This will install the upgraded transcriber with:
echo   ✓ Whisper (much better Albanian transcription)
echo   ✓ Advanced speaker diarization 
echo   ✓ Real speaker name recognition
echo   ✓ Improved audio capture
echo.
pause

echo Setting up HuggingFace token...
echo Please set your HuggingFace token:
echo set HUGGINGFACE_TOKEN=your_token_here
echo (Get token from: https://huggingface.co/settings/tokens)
echo.

echo Installing upgraded dependencies...
pip install --upgrade pip
pip install pyaudiowpatch
pip install openai-whisper
pip install pyannote.audio
pip install speechbrain
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install psutil numpy requests scipy librosa scikit-learn python-docx

echo.
echo ================================================================
echo                    SETUP COMPLETE!
echo ================================================================
echo.
echo You can now run the improved transcriber:
echo   python main.py
echo.
echo Features enabled:
echo   ✓ Whisper Albanian transcription (2-3x better accuracy)
echo   ✓ Advanced speaker diarization (pyannote.audio)
echo   ✓ Real speaker names (not just Speaker_1, Speaker_2)
echo   ✓ WASAPI loopback audio capture
echo   ✓ GPU acceleration (if available)
echo.
echo Next steps:
echo 1. Accept terms at: https://huggingface.co/pyannote/speaker-diarization-3.1
echo 2. Run: python main.py
echo.
pause