# 🚀 Albanian Teams Transcriber - Installation Guide

## 📋 Quick Start (5 Minutes)

### Prerequisites Check
✅ Windows 10/11 (64-bit)  
✅ Microsoft Teams desktop app installed  
✅ Python 3.8+ installed ([Download Python](https://python.org))  
✅ Administrator access (for some installations)  

### One-Command Installation

1. **Download and extract the project**
2. **Open Command Prompt in the project folder**
3. **Run the automated installer:**
   ```bash
   setup-final.bat
   ```
4. **Follow the on-screen prompts**
5. **Done! Skip to [Testing Your Installation](#testing-your-installation)**

---

## 🔧 Detailed Installation Steps

### Step 1: Download the Project

**Option A: Git Clone (Recommended)**
```bash
git clone https://github.com/MarinDushku/Teams-ALB-Transcripter.git
cd Teams-ALB-Transcripter
```

**Option B: Download ZIP**
1. Go to: https://github.com/MarinDushku/Teams-ALB-Transcripter
2. Click "Code" → "Download ZIP"
3. Extract to your desired folder
4. Open Command Prompt in that folder

### Step 2: Python Dependencies

**Automated (Recommended):**
```bash
setup-final.bat
```

**Manual Installation:**
```bash
# Core AI and audio
pip install openai-whisper torch pyaudiowpatch numpy scipy

# Participant detection
pip install pygetwindow pyautogui opencv-python pillow pytesseract

# Export and utilities
pip install python-docx psutil requests

# Windows-specific
pip install pywin32
```

### Step 3: Tesseract OCR (For Participant Names)

**Why needed:** To read participant names from Teams interface

1. **Download Tesseract:**
   - Go to: https://github.com/UB-Mannheim/tesseract/wiki
   - Download: `tesseract-ocr-w64-setup-v5.x.x.exe`

2. **Install Tesseract:**
   - Run the installer
   - Use default installation path: `C:\Program Files\Tesseract-OCR`
   - Add to Windows PATH when prompted

3. **Verify Installation:**
   ```bash
   tesseract --version
   ```

### Step 4: Audio Routing Setup

Choose **ONE** of these options:

#### Option A: VB-Cable (Recommended for Best Quality)

**Why:** Captures Teams audio directly without interference

1. **Download VB-Cable:**
   - Go to: https://vb-audio.com/Cable/
   - Download the free version

2. **Install VB-Cable:**
   - Extract and run `VBCABLE_Setup_x64.exe` **as Administrator**
   - Restart your computer when prompted

3. **Configure Teams:**
   - Open Teams → Settings → Devices
   - Set **Speaker** to "CABLE Input (VB-Audio Virtual Cable)"
   - Keep **Microphone** as your real microphone

4. **Test Audio:**
   - Join a test meeting
   - Verify you can hear others through your headphones/speakers
   - Others should hear you normally

#### Option B: Windows WASAPI Loopback (Built-in)

**Why:** No additional software needed, uses Windows built-in audio capture

**Pros:** Simple, no installation  
**Cons:** May capture system sounds, slightly lower quality

**Setup:** Nothing needed - works automatically with system audio

---

## 🧪 Testing Your Installation

### Basic Functionality Test

1. **Start the application:**
   ```bash
   python main.py
   ```

2. **Verify UI opens:**
   - Should see beautiful dark-themed interface
   - Title: "🎭 Albanian Teams Transcriber"
   - Buttons: Start Transcription, Export, Clear

3. **Test without Teams:**
   - Click "🎙️ Start Transcription"
   - Speak into your microphone
   - Should see some form of audio detection

### Teams Integration Test

1. **Join a Teams meeting** (or create a test meeting)

2. **Start transcription:**
   - Click "🎙️ Start Transcription" in the app
   - Should see: "🔍 Monitoring Teams participants..."
   - Should see: "🎤 Recording started - speak now!"

3. **Test participant detection:**
   - Verify participant names appear in the UI
   - Join/leave events should be detected

4. **Test transcription:**
   - Speak or have others speak
   - Should see real-time transcription with participant names

### Troubleshooting Failed Tests

**If UI doesn't open:**
```bash
# Check Python and tkinter
python -c "import tkinter; print('UI OK')"

# If error, install tkinter
# On Windows, reinstall Python with "tcl/tk" option checked
```

**If no audio detected:**
```bash
# Test audio packages
python -c "import pyaudiowpatch; print('Audio OK')"

# Check audio devices
python -c "
import pyaudiowpatch as pyaudio
p = pyaudio.PyAudio()
print('Audio devices:')
for i in range(p.get_device_count()):
    print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}')
"
```

**If Teams not detected:**
```bash
# Test screen capture
python -c "import pygetwindow, pyautogui; print('Screen capture OK')"

# Test OCR
python -c "import pytesseract; print('OCR OK')"
```

**If Whisper fails:**
```bash
# Test Whisper
python -c "import whisper; print('Whisper OK')"

# If error, try:
pip install --upgrade openai-whisper
```

---

## 🔧 Advanced Installation Options

### Custom Python Environment

**For developers or advanced users:**

```bash
# Create virtual environment
python -m venv teams_transcriber_env
teams_transcriber_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### GPU Acceleration (Optional)

**For faster AI processing:**

```bash
# Install CUDA-enabled PyTorch (if you have NVIDIA GPU)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify GPU detection
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

### Offline Installation

**For computers without internet:**

1. **On connected computer:**
   ```bash
   pip download -r requirements.txt -d packages/
   ```

2. **Copy `packages/` folder to offline computer**

3. **On offline computer:**
   ```bash
   pip install --find-links packages/ -r requirements.txt --no-index
   ```

---

## 🏗️ System Configuration

### Windows Audio Settings

1. **Sound Control Panel:**
   - Right-click sound icon → "Sound settings"
   - Ensure default devices are correct

2. **Teams Audio Test:**
   - Teams → Settings → Devices → "Test" buttons
   - Verify microphone and speaker work

3. **Application Permissions:**
   - Settings → Privacy → Microphone → Allow Python
   - Settings → Privacy → Camera → Allow Teams

### Firewall Configuration

**If prompted by Windows Firewall:**
- Allow Python through firewall
- Allow Teams through firewall  
- Allow pyaudio/audio capture

### Performance Optimization

**For better performance:**

1. **Close unnecessary applications**
2. **Set Windows power plan to "High Performance"**
3. **Disable Windows real-time protection temporarily during meetings**
4. **Use wired internet connection**

---

## 📱 Platform-Specific Notes

### Windows 10 vs Windows 11

**Windows 10:**
- Fully supported
- May need manual audio driver updates
- Use compatibility mode if issues occur

**Windows 11:**
- Preferred platform
- Better audio subsystem
- Enhanced security may require additional permissions

### Teams Versions

**Teams Desktop App (Recommended):**
- Full functionality
- Best participant detection
- Optimal audio capture

**Teams Web App:**
- Limited functionality
- Participant detection may be unreliable
- Audio capture works but with limitations

**Teams Mobile:**
- Not supported
- Use desktop version for transcription

---

## 🔍 Verification Checklist

After installation, verify these work:

### ✅ Core Functionality
- [ ] Python application starts
- [ ] UI displays correctly
- [ ] Start/Stop buttons work
- [ ] Export functionality works

### ✅ Audio Capture
- [ ] Microphone detected
- [ ] System audio captured (Teams audio)
- [ ] Audio levels visible in application
- [ ] Real-time transcription works

### ✅ Teams Integration
- [ ] Teams window detected
- [ ] Participant names extracted
- [ ] Join/leave events tracked
- [ ] Speaker identification works

### ✅ AI Processing
- [ ] Whisper model loads
- [ ] Albanian transcription works
- [ ] Confidence scores displayed
- [ ] Speaker differentiation works

### ✅ Export Features
- [ ] Text export works
- [ ] JSON export works
- [ ] Word document export works
- [ ] File saving successful

---

## 🆘 Installation Support

### Common Installation Errors

**"Python not found"**
- Install Python from python.org
- Ensure "Add to PATH" is checked during installation
- Restart Command Prompt after installation

**"pip not found"**
- Python installation issue
- Reinstall Python with pip included
- Or download get-pip.py and run: `python get-pip.py`

**"Module not found" errors**
- Run: `pip install --upgrade pip`
- Try: `pip install --user [package-name]`
- Check internet connection

**"Permission denied" errors**
- Run Command Prompt as Administrator
- Or use: `pip install --user [package-name]`
- Check antivirus settings

**"CUDA/GPU errors" (optional)**
- These are warnings, not critical errors
- Application will use CPU instead
- Install CUDA toolkit if you want GPU acceleration

### Getting Help

1. **Check this guide first**
2. **Try the troubleshooting steps**
3. **Run the automated installer again**
4. **Search GitHub issues for similar problems**
5. **Create a new GitHub issue with:**
   - Windows version
   - Python version
   - Full error message
   - Installation steps attempted

### Success Indicators

**Installation is successful when:**
```
🎭 Albanian Teams Transcriber - Production Version
====================================================
Real-time transcription with beautiful UI and AI-powered accuracy

🔍 Checking capabilities:
  Audio capture: ✓
  Whisper AI: ✓
  PyTorch: ✓

🚀 Starting Albanian Teams Transcriber...
📋 Instructions:
  1. Click 'Start Transcription' to begin
  2. Speak or play Teams audio
  3. See real-time transcription
  4. Use Export to save transcripts
```

---

*✨ Ready to start transcribing Albanian Teams meetings with professional quality!*