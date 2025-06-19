# Albanian Teams Transcriber - Quick Start Guide

## 🚀 How to Run the Application

### Option 1: Easy Installation (Recommended)
1. **Double-click** `install.py` to run the installer
2. Follow the installation wizard
3. Click "Launch Application" when installation completes
4. Desktop shortcuts will be created automatically

### Option 2: Direct Launch
1. **Double-click** `run_transcriber.py` for the GUI launcher
2. **Double-click** `Albanian_Teams_Transcriber.bat` (Windows only)
3. Or run from command line: `python main.py`

### Option 3: Command Line
```bash
# Automatic mode (starts when Teams detected)
python main.py auto

# Manual mode (user controls)
python main.py manual

# Show help
python main.py help
```

## 📋 Quick Setup Checklist

### Before First Use:
- [ ] Python 3.7+ installed
- [ ] Microsoft Teams installed
- [ ] Audio devices working
- [ ] Run `pip install -r requirements.txt`

### For Best Results:
- [ ] Install Virtual Audio Cable (Windows)
- [ ] Clone Albanian-ASR: `git clone https://github.com/florijanqosja/Albanian-ASR`
- [ ] Test your microphone and speakers
- [ ] Join a Teams meeting to test

## 🎯 How It Works

1. **Start the app** using any method above
2. **Teams Detection**: App automatically detects when you join a Teams meeting
3. **Audio Capture**: Captures system audio from Teams
4. **Live Transcription**: Shows Albanian text in real-time
5. **Speaker ID**: Different colors for different speakers
6. **Auto-Save**: Transcripts saved automatically
7. **Export**: Save as TXT, JSON, or Word document

## 🔧 Troubleshooting

### "No module named..." Error
```bash
pip install -r requirements.txt
```

### Audio Not Detected
- Check Windows audio settings
- Install Virtual Audio Cable
- Make sure Teams audio is working

### Teams Not Detected
- Make sure Teams is running
- Join an active meeting
- Check that Teams processes are visible in Task Manager

### Transcription Not Working
- Verify Albanian-ASR is set up
- Check internet connection for fallback transcription
- Ensure clear audio input

## 📁 File Overview

| File | Purpose |
|------|---------|
| `install.py` | **Easy installer with GUI** |
| `run_transcriber.py` | **GUI launcher** |
| `Albanian_Teams_Transcriber.bat` | **Windows batch launcher** |
| `main.py` | Main application |
| `requirements.txt` | Python dependencies |
| `create_desktop_shortcut.py` | Creates desktop shortcuts |

## 🎮 Usage Tips

- **Auto Mode**: Best for regular meeting transcription
- **Manual Mode**: Better for testing and control
- **Export Early**: Export important transcripts immediately
- **Check Status**: Green "Teams: Detected" means it's working
- **Speaker Colors**: Each speaker gets a different color
- **Timestamps**: All text includes timestamps

## 📞 Getting Help

1. Check this guide first
2. Look at the full `README.md`
3. Run `python main.py help` for command info
4. Check system requirements and dependencies

---

**Ready to start?** Just double-click `install.py` or `run_transcriber.py`!