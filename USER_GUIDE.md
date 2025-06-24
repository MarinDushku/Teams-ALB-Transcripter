# 🎭 Albanian Teams Transcriber - Complete User Guide

## 📖 Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Setup & Configuration](#setup--configuration)
4. [Using the Application](#using-the-application)
5. [Features](#features)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

---

## 🌟 Overview

The Albanian Teams Transcriber is a free, powerful Windows application that provides real-time transcription for Microsoft Teams meetings with advanced features:

### ✅ Key Features
- **Real-time Albanian transcription** using OpenAI Whisper AI
- **Automatic participant detection** from Teams interface
- **Speaker identification** with voice-to-name mapping
- **Join/leave tracking** with timestamps
- **Beautiful modern UI** with dark/light themes
- **Multiple export formats** (TXT, JSON, DOCX, CSV)
- **Session management** with auto-save
- **Privacy-focused** (all processing is local)

---

## 🚀 Installation

### System Requirements
- **Windows 10/11** (64-bit)
- **Python 3.8+** installed
- **Microsoft Teams** desktop application
- **4GB RAM** minimum (8GB recommended)
- **Audio capture capability** (built-in or VB-Cable)

### Automated Installation

1. **Download the project:**
   ```bash
   git clone https://github.com/MarinDushku/Teams-ALB-Transcripter.git
   cd Teams-ALB-Transcripter
   ```

2. **Run the automated setup:**
   ```bash
   setup-final.bat
   ```

3. **Install Tesseract OCR** (for participant detection):
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Choose `tesseract-ocr-w64-setup-v5.x.x.exe`
   - Install with default settings

4. **Install audio routing** (choose one):
   
   **Option A: VB-Cable (Recommended)**
   - Download: https://vb-audio.com/Cable/
   - Install and restart computer
   - In Teams: Settings → Devices → Speaker → Select "CABLE Input"
   
   **Option B: Windows WASAPI Loopback**
   - No installation needed
   - Works with system audio automatically

### Manual Installation

If automated setup fails:

```bash
# Install core dependencies
pip install pyaudiowpatch openai-whisper torch numpy scipy

# Install participant monitoring
pip install pygetwindow pyautogui opencv-python pillow pytesseract

# Install export capabilities
pip install python-docx

# Windows-specific
pip install pywin32
```

---

## ⚙️ Setup & Configuration

### First-Time Setup

1. **Audio Configuration:**
   - Open Teams → Settings → Devices
   - Set Speaker to "CABLE Input" (if using VB-Cable)
   - Test audio to ensure it works

2. **Teams Permissions:**
   - Ensure Teams has microphone/camera permissions
   - Keep Teams window visible during meetings

3. **Application Permissions:**
   - Allow Python through Windows Firewall
   - Grant screen capture permissions if prompted

### Configuration Options

The application automatically detects optimal settings, but you can customize:

- **Transcription Language:** Albanian (default)
- **Audio Quality:** 16kHz sample rate
- **Detection Sensitivity:** Automatic adjustment
- **Export Formats:** All formats enabled

---

## 🎯 Using the Application

### Starting a Session

1. **Launch the application:**
   ```bash
   python main.py
   ```
   or
   ```bash
   python working_transcriber.py
   ```

2. **Beautiful UI opens** with modern dark theme

3. **Join your Teams meeting** as normal

4. **Click "🎙️ Start Transcription"** in the app

### What Happens Next

✅ **Participant Monitoring Starts:**
   - App detects Teams window
   - Scans for participant names
   - Shows "🔍 Monitoring Teams participants..."

✅ **Audio Capture Begins:**
   - Captures Teams audio automatically
   - Shows "🎤 Recording started - speak now!"

✅ **Real-time Transcription:**
   - Speech converted to Albanian text
   - Speakers identified and color-coded
   - Join/leave events tracked

### Live Interface

**Main Transcript Panel:**
```
👤 John Smith joined the meeting
👤 Maria Doe joined the meeting

🎭 John Smith
[14:30:15] Hello everyone, how are you today?

🌟 Maria Doe  
[14:30:22] Mirëdita! I'm doing great, thanks for asking!

👤 Alex Johnson joined the meeting

💫 Alex Johnson
[14:30:35] Sorry I'm late! What did I miss?
```

**Statistics Panel:**
- **Words:** Live word count
- **Confidence:** AI accuracy percentage  
- **Participants:** Active speaker count
- **Duration:** Session time

### Ending a Session

1. **Click "⏹️ Stop Transcription"**
2. **Session automatically saved** to `sessions/` folder
3. **Export options available** immediately

---

## 🎨 Features

### 1. Real-time Transcription
- **OpenAI Whisper** AI engine optimized for Albanian
- **3-second processing chunks** for responsiveness
- **Confidence scoring** for quality assurance
- **Noise filtering** to avoid empty transcriptions

### 2. Participant Detection
- **OCR screen reading** to identify participant names
- **Windows API integration** for process monitoring
- **Visual speaker detection** using color analysis
- **Smart name extraction** with pattern matching

### 3. Speaker Identification
- **Voice-to-participant mapping** using audio characteristics
- **Smart assignment** based on participant list
- **Real names** instead of "Speaker A/B"
- **Consistent color coding** throughout session

### 4. Session Management
- **Automatic session creation** with timestamps
- **Participant join/leave tracking** with durations
- **Statistics calculation** (word count, participation rates)
- **Auto-save every 30 seconds** for data safety

### 5. Export Capabilities

**Text Format (.txt):**
```
🎭 Teams Meeting 2024-01-15 14:30
========================================

Start Time: 2024-01-15T14:30:00
Duration: 0:45:32
Participants: 3

TRANSCRIPT:
----------------------------------------

[14:30:15] John Smith: Hello everyone, how are you today?
  (Confidence: 95.0%)

[14:30:22] Maria Doe: Mirëdita! I'm doing great, thanks!
  (Confidence: 92.0%)
```

**JSON Format (.json):**
```json
{
  "meeting_title": "Teams Meeting 2024-01-15 14:30",
  "start_time": "2024-01-15T14:30:00",
  "participants": {
    "John Smith": {
      "joined_at": "2024-01-15T14:30:05",
      "word_count": 127,
      "participation_rate": 45.2
    }
  },
  "transcript": [
    {
      "timestamp": "2024-01-15T14:30:15",
      "speaker": "John Smith",
      "text": "Hello everyone, how are you today?",
      "confidence": 0.95
    }
  ]
}
```

**Word Document (.docx):**
- Professional formatting
- Participant summary
- Timestamped transcript
- Statistics section

### 6. User Interface

**Modern Features:**
- **Dark/Light themes** with smooth transitions
- **Color-coded speakers** with avatars
- **Real-time statistics** display
- **Beautiful animations** and visual feedback
- **Responsive design** that scales with window size

**Control Buttons:**
- **🎙️ Start/Stop:** Begin/end transcription
- **💾 Export:** Save transcript in multiple formats
- **🗑️ Clear:** Clear current transcript
- **⚙️ Settings:** Access configuration options

---

## 🔧 Troubleshooting

### Common Issues

#### ❌ "Teams not detected"
**Cause:** Teams window not found or not visible
**Solution:**
1. Ensure Teams is running and visible
2. Join a meeting (app needs active meeting)
3. Keep Teams window open, not minimized
4. Try clicking on Teams window to focus it

#### ❌ "Audio capture failed"
**Cause:** Audio routing not configured
**Solution:**
1. **For VB-Cable users:**
   - Teams Settings → Devices → Speaker → "CABLE Input"
   - Restart Teams after changing
2. **For WASAPI users:**
   - Ensure Windows audio is working
   - Check microphone permissions
   - Try running as Administrator

#### ❌ "No participants detected"
**Cause:** OCR or screen capture issues
**Solution:**
1. Install Tesseract OCR if not done
2. Ensure Teams participant panel is visible
3. Try different Teams layout (Gallery/Speaker view)
4. Check Windows screen capture permissions

#### ❌ "Whisper model failed to load"
**Cause:** AI model download/loading issues
**Solution:**
1. Check internet connection
2. Run: `pip install --upgrade openai-whisper`
3. Restart application
4. Try running as Administrator

#### ❌ "Poor transcription quality"
**Cause:** Audio quality or language issues
**Solution:**
1. Ensure clear audio input
2. Check Teams audio settings
3. Reduce background noise
4. Verify Albanian language setting

### Performance Issues

#### 🐌 "Slow transcription"
**Solutions:**
1. Close unnecessary applications
2. Ensure adequate RAM (8GB+)
3. Use wired internet connection
4. Reduce Teams video quality

#### 💾 "High memory usage"
**Solutions:**
1. Restart application every 2-3 hours
2. Clear transcript periodically
3. Close other AI applications
4. Upgrade to 16GB RAM if possible

### Advanced Troubleshooting

#### Debug Mode
Run with debug information:
```bash
python working_transcriber.py --debug
```

#### Check Dependencies
Verify all packages:
```bash
python -c "import pyaudiowpatch, whisper, cv2, pytesseract; print('All dependencies OK')"
```

#### Reset Configuration
Delete settings and restart:
```bash
del sessions\*.json
python main.py
```

---

## ❓ FAQ

### General Questions

**Q: Is this application free?**
A: Yes, completely free and open-source. No subscriptions or hidden costs.

**Q: Does it work with other meeting platforms?**
A: Currently optimized for Microsoft Teams. Other platforms may work but are not officially supported.

**Q: Is my data private?**
A: Yes, all processing is done locally on your computer. No data is sent to external servers.

**Q: Can I use it for languages other than Albanian?**
A: The AI supports many languages, but it's optimized for Albanian. You can modify the language code in the settings.

### Technical Questions

**Q: Why does it need screen capture permissions?**
A: To detect participant names from the Teams interface. This is only used for participant identification.

**Q: Can I run multiple instances?**
A: Not recommended. One instance per Teams meeting for best performance.

**Q: How accurate is the transcription?**
A: Typically 85-95% accurate for clear Albanian speech. Accuracy depends on audio quality and speaker clarity.

**Q: Does it work with Teams on the web?**
A: Best performance with Teams desktop app. Web version may have limitations.

### Usage Questions

**Q: Can I edit transcripts after the meeting?**
A: Yes, export to Word format for easy editing, or use the JSON format for programmatic processing.

**Q: How do I share transcripts with others?**
A: Export to your preferred format and share the file. All formats are standard and widely compatible.

**Q: Can I transcribe recorded meetings?**
A: Currently designed for live meetings. For recorded meetings, you'd need to play the audio while the app is running.

**Q: What if someone joins with a long/complex name?**
A: The app handles various name formats. Complex names may need manual correction in the exported transcript.

---

## 📞 Support

### Getting Help

1. **Check this user guide** for common solutions
2. **Review troubleshooting section** for technical issues
3. **Test with a simple meeting** to isolate problems
4. **Check GitHub issues** for known problems and solutions

### Reporting Issues

When reporting problems, please include:
- Windows version
- Python version (`python --version`)
- Teams version
- Error messages (full text)
- Steps to reproduce

### Community

- **GitHub Repository:** https://github.com/MarinDushku/Teams-ALB-Transcripter
- **Issues:** Report bugs and request features
- **Discussions:** Share tips and ask questions

---

## 🎉 Success Tips

### Best Practices

1. **Audio Quality:**
   - Use good microphone/headphones
   - Minimize background noise
   - Speak clearly and at moderate pace

2. **Meeting Setup:**
   - Keep Teams window visible
   - Use Gallery view for better participant detection
   - Ensure stable internet connection

3. **Application Usage:**
   - Start transcription before meeting begins
   - Keep application window open
   - Export transcripts immediately after meetings

4. **Performance:**
   - Close unnecessary applications
   - Use wired internet when possible
   - Restart app for very long meetings

### Pro Tips

- **Multiple Monitors:** Keep transcriber on secondary monitor
- **Keyboard Shortcuts:** Use Alt+Tab to quickly switch between Teams and transcriber
- **Backup:** Export transcripts in multiple formats for safety
- **Testing:** Test setup before important meetings

---

*🎭 Enjoy your enhanced Teams meetings with professional Albanian transcription!*